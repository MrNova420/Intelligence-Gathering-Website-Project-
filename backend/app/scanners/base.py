from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import asyncio
import logging
from datetime import datetime

# Conditional imports with fallbacks
try:
    from sqlalchemy.ext.asyncio import AsyncSession
    from app.db.models import Query, ScanResult, ScannerType, QueryStatus
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False
    # Mock classes
    class MockAsyncSession:
        async def commit(self):
            pass
        async def refresh(self, obj):
            pass
    
    AsyncSession = MockAsyncSession
    
    # Mock enums and models
    class MockScannerType:
        EMAIL_INTELLIGENCE = "email_intelligence"
        EMAIL_VERIFICATION = "email_verification"
        PHONE_LOOKUP = "phone_lookup"
        SOCIAL_MEDIA = "social_media"
        PUBLIC_RECORDS = "public_records"
        IMAGE_ANALYSIS = "image_analysis"
        API = "api"
        FORUM_COMMUNITY = "forum_community"
        DEEP_WEB = "deep_web"
        NETWORK = "network"
        BLOCKCHAIN = "blockchain"
        CYBERSECURITY = "cybersecurity"
        GEOSPATIAL = "geospatial"
    
    class MockQueryStatus:
        PENDING = "pending"
        RUNNING = "running" 
        COMPLETED = "completed"
        FAILED = "failed"
    
    class MockQuery:
        def __init__(self):
            self.id = 1
            self.query_value = ""
            self.query_type = ""
    
    class MockScanResult:
        def __init__(self):
            self.id = 1
            self.status = MockQueryStatus.PENDING
            self.data = {}
            self.processed_data = {}
            self.entities_found = []
            self.confidence_score = 0.0
            self.relevance_score = 0.0
            self.completed_at = None
    
    Query = MockQuery
    ScanResult = MockScanResult
    ScannerType = MockScannerType
    QueryStatus = MockQueryStatus

logger = logging.getLogger(__name__)


class BaseScannerModule(ABC):
    """Base class for all scanner modules."""
    
    def __init__(self, name: str, scanner_type: ScannerType, description: str = ""):
        self.name = name
        self.scanner_type = scanner_type
        self.description = description
        self.enabled = True
        self.rate_limit = 100  # requests per hour
        self.priority = 1  # lower number = higher priority
        self.cost_credits = 1  # credits per scan
        self.timeout = 30  # seconds
    
    @abstractmethod
    async def scan(self, query: Query) -> Dict[str, Any]:
        """
        Perform the actual scanning operation.
        
        Args:
            query: The query object containing the search parameters
            
        Returns:
            Dict containing the scan results
        """
        pass
    
    @abstractmethod
    def can_handle(self, query: Query) -> bool:
        """
        Check if this scanner can handle the given query type.
        
        Args:
            query: The query object to check
            
        Returns:
            True if this scanner can handle the query, False otherwise
        """
        pass
    
    async def preprocess_query(self, query: Query) -> Dict[str, Any]:
        """
        Preprocess the query before scanning.
        Can be overridden by specific scanners.
        
        Args:
            query: The query object
            
        Returns:
            Preprocessed query data
        """
        return {
            "query_type": query.query_type,
            "query_value": query.query_value,
            "metadata": query.metadata or {}
        }
    
    async def postprocess_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Postprocess the scan results.
        Can be overridden by specific scanners for normalization.
        
        Args:
            results: Raw scan results
            
        Returns:
            Processed scan results
        """
        return results
    
    def calculate_confidence_score(self, results: Dict[str, Any]) -> float:
        """
        Calculate confidence score for the results.
        Should be overridden by specific scanners.
        
        Args:
            results: Scan results
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        return 0.5  # Default neutral confidence
    
    def extract_entities(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract entities from scan results.
        Should be overridden by specific scanners.
        
        Args:
            results: Scan results
            
        Returns:
            List of extracted entities
        """
        return []
    
    async def execute_scan(self, query: Query, db: AsyncSession) -> Optional[ScanResult]:
        """
        Execute the complete scanning workflow.
        
        Args:
            query: The query to scan
            db: Database session
            
        Returns:
            ScanResult object or None if scan failed
        """
        if not self.can_handle(query):
            logger.info(f"Scanner {self.name} cannot handle query type {query.query_type}")
            return None
        
        # Create scan result record
        scan_result = ScanResult(
            query_id=query.id,
            scanner_type=self.scanner_type,
            scanner_name=self.name,
            status=QueryStatus.PROCESSING,
            started_at=datetime.utcnow(),
            cost_credits=self.cost_credits
        )
        
        db.add(scan_result)
        await db.commit()
        await db.refresh(scan_result)
        
        try:
            logger.info(f"Starting scan with {self.name} for query {query.id}")
            
            # Preprocess query
            preprocessed_data = await self.preprocess_query(query)
            
            # Perform scan with timeout
            raw_results = await asyncio.wait_for(
                self.scan(query), 
                timeout=self.timeout
            )
            
            # Postprocess results
            processed_results = await self.postprocess_results(raw_results)
            
            # Calculate confidence score
            confidence_score = self.calculate_confidence_score(processed_results)
            
            # Extract entities
            entities = self.extract_entities(processed_results)
            
            # Update scan result
            scan_result.status = QueryStatus.COMPLETED
            scan_result.data = raw_results
            scan_result.processed_data = processed_results
            scan_result.entities_found = entities
            scan_result.confidence_score = confidence_score
            scan_result.relevance_score = confidence_score  # Simple relevance calculation
            scan_result.completed_at = datetime.utcnow()
            
            await db.commit()
            await db.refresh(scan_result)
            
            logger.info(f"Completed scan with {self.name} for query {query.id}")
            return scan_result
            
        except asyncio.TimeoutError:
            logger.error(f"Timeout in scanner {self.name} for query {query.id}")
            scan_result.status = QueryStatus.FAILED
            scan_result.error_message = "Scanner timeout"
            scan_result.completed_at = datetime.utcnow()
            await db.commit()
            return scan_result
            
        except Exception as e:
            logger.error(f"Error in scanner {self.name} for query {query.id}: {str(e)}")
            
            # Update scan result with error
            scan_result.status = QueryStatus.FAILED
            scan_result.error_message = str(e)
            scan_result.completed_at = datetime.utcnow()
            
            await db.commit()
            await db.refresh(scan_result)
            
            return scan_result


class ScannerRegistry:
    """Registry for all available scanner modules."""
    
    def __init__(self):
        self._scanners: List[BaseScannerModule] = []
    
    def register(self, scanner: BaseScannerModule):
        """Register a scanner module."""
        self._scanners.append(scanner)
        logger.info(f"Registered scanner: {scanner.name} ({scanner.description})")
    
    def get_scanners_for_query(self, query: Query) -> List[BaseScannerModule]:
        """Get all scanners that can handle a specific query."""
        applicable_scanners = [
            scanner for scanner in self._scanners
            if scanner.enabled and scanner.can_handle(query)
        ]
        
        # Sort by priority (lower number = higher priority)
        applicable_scanners.sort(key=lambda x: x.priority)
        
        return applicable_scanners
    
    def get_all_scanners(self) -> List[BaseScannerModule]:
        """Get all registered scanners."""
        return self._scanners.copy()
    
    def get_scanner_by_name(self, name: str) -> Optional[BaseScannerModule]:
        """Get a scanner by name."""
        for scanner in self._scanners:
            if scanner.name == name:
                return scanner
        return None
    
    def get_scanners_by_type(self, scanner_type: ScannerType) -> List[BaseScannerModule]:
        """Get all scanners of a specific type."""
        return [s for s in self._scanners if s.scanner_type == scanner_type]
    
    def enable_scanner(self, name: str):
        """Enable a scanner."""
        scanner = self.get_scanner_by_name(name)
        if scanner:
            scanner.enabled = True
            logger.info(f"Enabled scanner: {name}")
    
    def disable_scanner(self, name: str):
        """Disable a scanner."""
        scanner = self.get_scanner_by_name(name)
        if scanner:
            scanner.enabled = False
            logger.info(f"Disabled scanner: {name}")
    
    def get_scanner_stats(self) -> Dict[str, Any]:
        """Get statistics about registered scanners."""
        total_scanners = len(self._scanners)
        enabled_scanners = len([s for s in self._scanners if s.enabled])
        
        by_type = {}
        for scanner in self._scanners:
            scanner_type = scanner.scanner_type.value
            if scanner_type not in by_type:
                by_type[scanner_type] = {"total": 0, "enabled": 0}
            by_type[scanner_type]["total"] += 1
            if scanner.enabled:
                by_type[scanner_type]["enabled"] += 1
        
        return {
            "total_scanners": total_scanners,
            "enabled_scanners": enabled_scanners,
            "disabled_scanners": total_scanners - enabled_scanners,
            "by_type": by_type
        }


# Global scanner registry
scanner_registry = ScannerRegistry()

# Backward compatibility alias
BaseScanner = BaseScannerModule
