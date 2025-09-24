"""
Enterprise Query Service
========================

AAA-grade service layer for intelligence query management with:
- Advanced async operations
- Transaction management
- Caching strategies
- Performance optimization
- Comprehensive error handling
"""

import asyncio
import hashlib
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
from uuid import UUID, uuid4

try:
    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
    from sqlalchemy.orm import sessionmaker, selectinload
    from sqlalchemy import select, update, delete, func, and_, or_
    from sqlalchemy.exc import IntegrityError, SQLAlchemyError
    ASYNC_SQLALCHEMY_AVAILABLE = True
except ImportError:
    ASYNC_SQLALCHEMY_AVAILABLE = False
    AsyncSession = object

from ..db.enterprise_models import (
    User, IntelligenceQuery, ScanResult, Report, AuditLog,
    QueryStatus, ScannerStatus, UserPlanType
)
from ..scanners.enterprise_scanner_engine import (
    scanner_registry, get_orchestrator, ScannerCategory
)

logger = logging.getLogger(__name__)


class QueryServiceError(Exception):
    """Base exception for query service errors"""
    pass


class InsufficientCreditsError(QueryServiceError):
    """Raised when user has insufficient credits"""
    pass


class QuotaExceededError(QueryServiceError):
    """Raised when user has exceeded their quota"""
    pass


class EnterpriseQueryService:
    """Enterprise-grade query management service"""
    
    def __init__(self, db_session: AsyncSession, cache_client=None):
        self.db = db_session
        self.cache = cache_client
        self.orchestrator = get_orchestrator()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    async def submit_query(
        self,
        user_id: UUID,
        query_type: str,
        target: str,
        scanner_names: Optional[List[str]] = None,
        categories: Optional[List[ScannerCategory]] = None,
        priority: str = "normal",
        metadata: Optional[Dict[str, Any]] = None
    ) -> IntelligenceQuery:
        """Submit a new intelligence query with comprehensive validation"""
        
        try:
            # Get user and validate permissions
            user = await self._get_user_by_id(user_id)
            if not user:
                raise QueryServiceError(f"User {user_id} not found")
            
            # Calculate estimated cost
            estimated_cost = await self._calculate_query_cost(
                query_type, scanner_names, categories
            )
            
            # Check user quotas and credits
            if not user.can_perform_query(estimated_cost):
                if user.api_quota_used >= user.api_quota_limit:
                    raise QuotaExceededError("API quota exceeded")
                else:
                    raise InsufficientCreditsError("Insufficient credits")
            
            # Create target hash for deduplication
            target_hash = self._create_target_hash(target, query_type)
            
            # Check for recent duplicate query
            duplicate_query = await self._check_duplicate_query(
                user_id, target_hash, query_type
            )
            if duplicate_query:
                self.logger.info(f"Returning existing query {duplicate_query.id} for duplicate request")
                return duplicate_query
            
            # Create new query
            query = IntelligenceQuery(
                user_id=user_id,
                query_type=query_type,
                target=target,
                target_hash=target_hash,
                priority=priority,
                estimated_cost=estimated_cost,
                scanner_selection=scanner_names,
                scan_categories=[cat.value for cat in categories] if categories else None,
                metadata=metadata or {},
                scheduled_at=datetime.now(timezone.utc)
            )
            
            # Save to database
            self.db.add(query)
            await self.db.commit()
            await self.db.refresh(query)
            
            # Consume user quota and credits
            user.consume_quota(1, estimated_cost)
            await self.db.commit()
            
            # Log audit event
            await self._log_audit_event(
                user_id=user_id,
                event_type="query_submitted",
                event_category="query_management",
                event_description=f"Intelligence query submitted: {query_type}",
                resource_type="query",
                resource_id=query.id,
                metadata={"query_type": query_type, "estimated_cost": estimated_cost}
            )
            
            # Start async processing
            asyncio.create_task(self._process_query_async(query.id))
            
            self.logger.info(f"✅ Query {query.id} submitted successfully for user {user_id}")
            return query
            
        except (InsufficientCreditsError, QuotaExceededError):
            raise
        except Exception as e:
            self.logger.exception(f"💥 Error submitting query: {e}")
            await self.db.rollback()
            raise QueryServiceError(f"Failed to submit query: {str(e)}")
    
    async def get_query(self, query_id: UUID, user_id: Optional[UUID] = None) -> Optional[IntelligenceQuery]:
        """Get query by ID with optional user validation"""
        try:
            query_filter = [IntelligenceQuery.id == query_id, ~IntelligenceQuery.is_deleted]
            if user_id:
                query_filter.append(IntelligenceQuery.user_id == user_id)
            
            result = await self.db.execute(
                select(IntelligenceQuery)
                .options(selectinload(IntelligenceQuery.scan_results))
                .where(and_(*query_filter))
            )
            
            return result.scalar_one_or_none()
            
        except Exception as e:
            self.logger.exception(f"💥 Error retrieving query {query_id}: {e}")
            return None
    
    async def list_user_queries(
        self,
        user_id: UUID,
        status_filter: Optional[str] = None,
        query_type_filter: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
        order_by: str = "created_at",
        order_desc: bool = True
    ) -> Tuple[List[IntelligenceQuery], int]:
        """List user queries with filtering and pagination"""
        
        try:
            # Base query
            base_query = select(IntelligenceQuery).where(
                and_(
                    IntelligenceQuery.user_id == user_id,
                    ~IntelligenceQuery.is_deleted
                )
            )
            
            # Apply filters
            if status_filter:
                base_query = base_query.where(IntelligenceQuery.status == status_filter)
            
            if query_type_filter:
                base_query = base_query.where(IntelligenceQuery.query_type == query_type_filter)
            
            # Count total results
            count_query = select(func.count()).select_from(base_query.subquery())
            total_count = (await self.db.execute(count_query)).scalar()
            
            # Apply ordering and pagination
            order_column = getattr(IntelligenceQuery, order_by, IntelligenceQuery.created_at)
            if order_desc:
                order_column = order_column.desc()
            
            queries_query = (base_query
                           .order_by(order_column)
                           .limit(limit)
                           .offset(offset))
            
            result = await self.db.execute(queries_query)
            queries = result.scalars().all()
            
            return list(queries), total_count
            
        except Exception as e:
            self.logger.exception(f"💥 Error listing queries for user {user_id}: {e}")
            return [], 0
    
    async def cancel_query(self, query_id: UUID, user_id: UUID) -> bool:
        """Cancel a query if it's still running"""
        try:
            # Get query
            query = await self.get_query(query_id, user_id)
            if not query:
                return False
            
            # Check if query can be cancelled
            if query.is_completed:
                return False
            
            # Update query status
            query.status = QueryStatus.CANCELLED.value
            query.completed_at = datetime.now(timezone.utc)
            
            # Cancel any running scanners
            await self.orchestrator.cancel_scan(f"query_{query_id}")
            
            await self.db.commit()
            
            # Log audit event
            await self._log_audit_event(
                user_id=user_id,
                event_type="query_cancelled",
                event_category="query_management",
                event_description=f"Query cancelled: {query_id}",
                resource_type="query",
                resource_id=query_id
            )
            
            self.logger.info(f"🛑 Query {query_id} cancelled by user {user_id}")
            return True
            
        except Exception as e:
            self.logger.exception(f"💥 Error cancelling query {query_id}: {e}")
            return False
    
    async def get_query_progress(self, query_id: UUID, user_id: Optional[UUID] = None) -> Dict[str, Any]:
        """Get real-time query progress"""
        try:
            query = await self.get_query(query_id, user_id)
            if not query:
                return {"error": "Query not found"}
            
            # Get scan results
            result = await self.db.execute(
                select(ScanResult)
                .where(ScanResult.query_id == query_id)
                .order_by(ScanResult.created_at)
            )
            scan_results = result.scalars().all()
            
            # Calculate progress
            total_scanners = len(scan_results)
            completed_scanners = len([r for r in scan_results if r.status == ScannerStatus.COMPLETED.value])
            failed_scanners = len([r for r in scan_results if r.status == ScannerStatus.FAILED.value])
            running_scanners = len([r for r in scan_results if r.status == ScannerStatus.RUNNING.value])
            
            progress_percentage = 0
            if total_scanners > 0:
                progress_percentage = ((completed_scanners + failed_scanners) / total_scanners) * 100
            
            # Estimate completion time
            estimated_completion = None
            if query.started_at and running_scanners > 0:
                # Simple estimation based on average completion time
                avg_time = 30  # seconds
                estimated_completion = datetime.now(timezone.utc) + timedelta(seconds=avg_time * running_scanners)
            
            return {
                "query_id": str(query_id),
                "status": query.status,
                "progress_percentage": round(progress_percentage, 2),
                "total_scanners": total_scanners,
                "completed_scanners": completed_scanners,
                "failed_scanners": failed_scanners,
                "running_scanners": running_scanners,
                "started_at": query.started_at.isoformat() if query.started_at else None,
                "estimated_completion": estimated_completion.isoformat() if estimated_completion else None,
                "execution_time_seconds": query.execution_time_seconds,
                "scanner_details": [
                    {
                        "name": r.scanner_name,
                        "category": r.scanner_category,
                        "status": r.status,
                        "execution_time": r.execution_time_seconds,
                        "confidence_score": r.confidence_score
                    }
                    for r in scan_results
                ]
            }
            
        except Exception as e:
            self.logger.exception(f"💥 Error getting query progress {query_id}: {e}")
            return {"error": "Failed to get progress"}
    
    async def _process_query_async(self, query_id: UUID):
        """Process query asynchronously"""
        try:
            # Get query
            query = await self.get_query(query_id)
            if not query:
                self.logger.error(f"Query {query_id} not found for processing")
                return
            
            # Mark as started
            query.mark_started()
            await self.db.commit()
            
            self.logger.info(f"🚀 Processing query {query_id}: {query.query_type} - {query.target}")
            
            # Determine scanners to use
            scanner_names = query.scanner_selection
            categories = None
            if query.scan_categories:
                categories = [ScannerCategory(cat) for cat in query.scan_categories]
            
            # Execute scanners
            scan_results = await self.orchestrator.execute_scan_batch(
                target=query.target,
                scanner_names=scanner_names,
                categories=categories
            )
            
            # Save scan results
            total_scanners = len(scan_results)
            completed_scanners = 0
            failed_scanners = 0
            
            for scanner_name, result in scan_results.items():
                scan_result = ScanResult(
                    query_id=query_id,
                    scanner_name=scanner_name,
                    scanner_category=result.metadata.get('category', 'unknown'),
                    status=result.status.value,
                    data=result.data,
                    error_message=result.error,
                    execution_time_seconds=result.execution_time,
                    confidence_score=result.metadata.get('confidence_score'),
                    started_at=result.timestamp,
                    completed_at=result.timestamp
                )
                
                self.db.add(scan_result)
                
                if result.is_successful():
                    completed_scanners += 1
                else:
                    failed_scanners += 1
            
            # Update query with results
            query.total_scanners = total_scanners
            query.completed_scanners = completed_scanners
            query.failed_scanners = failed_scanners
            query.success_rate = (completed_scanners / total_scanners * 100) if total_scanners > 0 else 0
            query.mark_completed(success=completed_scanners > 0)
            
            await self.db.commit()
            
            # Cache results if needed
            if self.cache:
                cache_key = f"query_results:{query_id}"
                await self._cache_query_results(cache_key, query_id)
            
            self.logger.info(f"✅ Query {query_id} completed: {completed_scanners}/{total_scanners} scanners successful")
            
        except Exception as e:
            self.logger.exception(f"💥 Error processing query {query_id}: {e}")
            
            # Mark query as failed
            try:
                query = await self.get_query(query_id)
                if query:
                    query.status = QueryStatus.FAILED.value
                    query.error_message = str(e)
                    query.completed_at = datetime.now(timezone.utc)
                    await self.db.commit()
            except Exception as commit_error:
                self.logger.exception(f"💥 Error updating failed query status: {commit_error}")
    
    async def _get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID"""
        result = await self.db.execute(
            select(User).where(and_(User.id == user_id, ~User.is_deleted))
        )
        return result.scalar_one_or_none()
    
    async def _calculate_query_cost(
        self,
        query_type: str,
        scanner_names: Optional[List[str]],
        categories: Optional[List[ScannerCategory]]
    ) -> int:
        """Calculate estimated query cost in credits"""
        
        # Base cost per query type
        base_costs = {
            "email": 2,
            "phone": 3,
            "name": 5,
            "username": 4,
            "domain": 2,
            "ip": 1
        }
        
        base_cost = base_costs.get(query_type, 3)
        
        # If specific scanners are requested, calculate based on their costs
        if scanner_names:
            total_cost = 0
            for scanner_name in scanner_names:
                scanner = scanner_registry.get_scanner(scanner_name)
                if scanner:
                    total_cost += scanner.config.cost_credits
            return max(total_cost, base_cost)
        
        # If categories are specified, estimate based on category
        if categories:
            category_multipliers = {
                ScannerCategory.EMAIL: 1.0,
                ScannerCategory.PHONE: 1.2,
                ScannerCategory.SOCIAL_MEDIA: 1.5,
                ScannerCategory.PUBLIC_RECORDS: 2.0,
                ScannerCategory.NETWORK: 0.8,
                ScannerCategory.IMAGE_ANALYSIS: 2.5,
                ScannerCategory.AI_CORRELATION: 3.0
            }
            
            multiplier = max([category_multipliers.get(cat, 1.0) for cat in categories])
            return int(base_cost * multiplier)
        
        return base_cost
    
    def _create_target_hash(self, target: str, query_type: str) -> str:
        """Create hash for target deduplication"""
        normalized_target = target.lower().strip()
        hash_input = f"{query_type}:{normalized_target}"
        return hashlib.sha256(hash_input.encode()).hexdigest()
    
    async def _check_duplicate_query(
        self,
        user_id: UUID,
        target_hash: str,
        query_type: str,
        hours_threshold: int = 24
    ) -> Optional[IntelligenceQuery]:
        """Check for recent duplicate queries"""
        
        threshold_time = datetime.now(timezone.utc) - timedelta(hours=hours_threshold)
        
        result = await self.db.execute(
            select(IntelligenceQuery).where(
                and_(
                    IntelligenceQuery.user_id == user_id,
                    IntelligenceQuery.target_hash == target_hash,
                    IntelligenceQuery.query_type == query_type,
                    IntelligenceQuery.created_at > threshold_time,
                    ~IntelligenceQuery.is_deleted
                )
            ).limit(1)
        )
        
        return result.scalar_one_or_none()
    
    async def _log_audit_event(
        self,
        user_id: UUID,
        event_type: str,
        event_category: str,
        event_description: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[UUID] = None,
        metadata: Optional[Dict[str, Any]] = None,
        severity: str = "info"
    ):
        """Log audit event"""
        
        audit_log = AuditLog(
            user_id=user_id,
            event_type=event_type,
            event_category=event_category,
            event_description=event_description,
            resource_type=resource_type,
            resource_id=resource_id,
            metadata=metadata,
            severity=severity
        )
        
        self.db.add(audit_log)
        # Note: Commit is handled by the calling method
    
    async def _cache_query_results(self, cache_key: str, query_id: UUID):
        """Cache query results for faster retrieval"""
        if not self.cache:
            return
        
        try:
            # Get query with results
            query = await self.get_query(query_id)
            if query:
                cache_data = {
                    "query_id": str(query_id),
                    "status": query.status,
                    "results_count": query.completed_scanners,
                    "cached_at": datetime.now(timezone.utc).isoformat()
                }
                
                # Cache for 1 hour
                await self.cache.setex(cache_key, 3600, cache_data)
                
        except Exception as e:
            self.logger.warning(f"Failed to cache query results: {e}")


# Service factory
def create_query_service(db_session: AsyncSession, cache_client=None) -> EnterpriseQueryService:
    """Create query service instance"""
    return EnterpriseQueryService(db_session, cache_client)