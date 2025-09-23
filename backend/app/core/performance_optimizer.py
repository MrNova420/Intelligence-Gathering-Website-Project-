"""
Performance Optimization Module
Implements Redis caching, database indexes, query optimization, and async orchestration.
"""

import asyncio
import logging
import time
import hashlib
import json
from typing import Dict, Any, List, Optional, Union, Callable
from datetime import datetime, timedelta
from collections import defaultdict
import functools
from concurrent.futures import ThreadPoolExecutor, as_completed
import weakref

# Mock Redis implementation for demonstration
class MockRedis:
    """Mock Redis implementation for caching"""
    
    def __init__(self):
        self._cache = {}
        self._ttl = {}
    
    async def get(self, key: str) -> Optional[str]:
        """Get value from cache"""
        if key in self._cache:
            # Check TTL
            if key in self._ttl and datetime.utcnow() > self._ttl[key]:
                del self._cache[key]
                del self._ttl[key]
                return None
            return self._cache[key]
        return None
    
    async def set(self, key: str, value: str, ttl: int = None):
        """Set value in cache with optional TTL"""
        self._cache[key] = value
        if ttl:
            self._ttl[key] = datetime.utcnow() + timedelta(seconds=ttl)
    
    async def delete(self, key: str):
        """Delete key from cache"""
        self._cache.pop(key, None)
        self._ttl.pop(key, None)
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        return key in self._cache
    
    async def keys(self, pattern: str) -> List[str]:
        """Get keys matching pattern"""
        if pattern.endswith('*'):
            prefix = pattern[:-1]
            return [k for k in self._cache.keys() if k.startswith(prefix)]
        return [k for k in self._cache.keys() if k == pattern]

logger = logging.getLogger(__name__)


class RedisCache:
    """Redis caching implementation"""
    
    def __init__(self, redis_client=None):
        self.redis = redis_client or MockRedis()
        self.hit_count = 0
        self.miss_count = 0
    
    async def get(self, key: str) -> Optional[str]:
        """Get value from Redis cache"""
        try:
            result = await self.redis.get(key)
            if result:
                self.hit_count += 1
            else:
                self.miss_count += 1
            return result
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            self.miss_count += 1
            return None
    
    async def set(self, key: str, value: str, ttl: int = 3600):
        """Set value in Redis cache"""
        try:
            await self.redis.set(key, value, ttl)
        except Exception as e:
            logger.error(f"Redis set error: {e}")
    
    async def delete(self, key: str):
        """Delete key from Redis cache"""
        try:
            await self.redis.delete(key)
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
    
    def generate_cache_key(self, prefix: str, *args) -> str:
        """Generate consistent cache key"""
        key_parts = [str(arg) for arg in args]
        key_string = ':'.join([prefix] + key_parts)
        
        # Hash long keys to keep them manageable
        if len(key_string) > 250:
            key_hash = hashlib.sha256(key_string.encode()).hexdigest()[:16]
            return f"{prefix}:hashed:{key_hash}"
        
        return key_string
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total_requests) if total_requests > 0 else 0
        return {
            "hits": self.hit_count,
            "misses": self.miss_count,
            "hit_rate": hit_rate,
            "total_requests": total_requests
        }


class CacheManager:
    """Manages Redis caching for performance optimization"""
    
    def __init__(self, redis_client=None):
        # In production, would use real Redis client
        self.redis = redis_client or MockRedis()
        self.default_ttl = 3600  # 1 hour
        self.hit_count = 0
        self.miss_count = 0
    
    def generate_cache_key(self, prefix: str, *args) -> str:
        """Generate consistent cache key"""
        key_parts = [str(arg) for arg in args]
        key_string = ':'.join([prefix] + key_parts)
        
        # Hash long keys to keep them manageable
        if len(key_string) > 250:
            key_hash = hashlib.sha256(key_string.encode()).hexdigest()[:16]
            return f"{prefix}:hashed:{key_hash}"
        
        return key_string
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache and deserialize"""
        try:
            cached_value = await self.redis.get(key)
            if cached_value:
                self.hit_count += 1
                return json.loads(cached_value)
            else:
                self.miss_count += 1
                return None
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {str(e)}")
            self.miss_count += 1
            return None
    
    async def set(self, key: str, value: Any, ttl: int = None):
        """Serialize and store value in cache"""
        try:
            if ttl is None:
                ttl = self.default_ttl
            
            serialized_value = json.dumps(value, default=str)
            await self.redis.set(key, serialized_value, ttl)
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {str(e)}")
    
    async def delete(self, key: str):
        """Delete key from cache"""
        try:
            await self.redis.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {str(e)}")
    
    async def clear_pattern(self, pattern: str):
        """Clear all keys matching pattern"""
        try:
            keys = await self.redis.keys(pattern)
            for key in keys:
                await self.redis.delete(key)
        except Exception as e:
            logger.error(f"Cache clear pattern error for {pattern}: {str(e)}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "total_requests": total_requests,
            "hit_rate_percent": round(hit_rate, 2)
        }


class QueryCache:
    """Specialized caching for query results"""
    
    def __init__(self, cache_manager: CacheManager):
        self.cache = cache_manager
        self.query_ttl = 1800  # 30 minutes for query results
        self.report_ttl = 3600  # 1 hour for reports
    
    async def get_query_result(self, query_type: str, query_value: str, user_plan: str) -> Optional[Dict[str, Any]]:
        """Get cached query result"""
        key = self.cache.generate_cache_key("query", query_type, query_value, user_plan)
        return await self.cache.get(key)
    
    async def cache_query_result(self, query_type: str, query_value: str, user_plan: str, result: Dict[str, Any]):
        """Cache query result"""
        key = self.cache.generate_cache_key("query", query_type, query_value, user_plan)
        await self.cache.set(key, result, self.query_ttl)
    
    async def get_report(self, report_id: str) -> Optional[Dict[str, Any]]:
        """Get cached report"""
        key = self.cache.generate_cache_key("report", report_id)
        return await self.cache.get(key)
    
    async def cache_report(self, report_id: str, report: Dict[str, Any]):
        """Cache report"""
        key = self.cache.generate_cache_key("report", report_id)
        await self.cache.set(key, report, self.report_ttl)
    
    async def invalidate_user_cache(self, user_id: str):
        """Invalidate all cache entries for a user"""
        pattern = f"*:user:{user_id}:*"
        await self.cache.clear_pattern(pattern)


def cache_result(ttl: int = 3600, key_prefix: str = "default"):
    """Decorator for caching function results"""
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Get cache manager from first argument if it's available
            cache_manager = None
            if args and hasattr(args[0], 'cache_manager'):
                cache_manager = args[0].cache_manager
            
            if not cache_manager:
                # No cache available, execute function normally
                return await func(*args, **kwargs)
            
            # Generate cache key
            key_parts = [str(arg) for arg in args] + [f"{k}:{v}" for k, v in sorted(kwargs.items())]
            cache_key = cache_manager.generate_cache_key(f"{key_prefix}:{func.__name__}", *key_parts)
            
            # Try to get from cache
            cached_result = await cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            if result is not None:
                await cache_manager.set(cache_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator


class AsyncScannerOrchestrator:
    """Optimized async orchestrator for scanner modules"""
    
    def __init__(self, cache_manager: CacheManager, max_concurrent_scanners: int = 20):
        self.cache_manager = cache_manager
        self.query_cache = QueryCache(cache_manager)
        self.max_concurrent_scanners = max_concurrent_scanners
        self.executor = ThreadPoolExecutor(max_workers=10)
        
        # Performance tracking
        self.scanner_performance = defaultdict(list)
        self.active_scans = weakref.WeakValueDictionary()
    
    async def execute_scan_optimized(
        self,
        query: Dict[str, Any],
        scanners: List[Any],
        user_plan: str,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """Execute scan with performance optimizations"""
        
        scan_id = f"scan_{int(time.time())}_{hash(str(query))}"
        query_type = query.get("query_type", "unknown")
        query_value = query.get("query_value", "")
        
        # Check cache first
        if use_cache:
            cached_result = await self.query_cache.get_query_result(query_type, query_value, user_plan)
            if cached_result:
                logger.info(f"Cache hit for query: {query_type}:{query_value}")
                return cached_result
        
        # Track scan start
        scan_start_time = time.time()
        self.active_scans[scan_id] = {"start_time": scan_start_time, "status": "running"}
        
        # Filter scanners based on user plan and performance
        optimized_scanners = self._select_optimal_scanners(scanners, user_plan)
        
        # Execute scanners with batching and rate limiting
        scanner_results = await self._execute_scanners_batched(optimized_scanners, query)
        
        # Aggregate results
        aggregated_results = await self._aggregate_results_optimized(scanner_results)
        
        # Cache results
        if use_cache and aggregated_results:
            await self.query_cache.cache_query_result(query_type, query_value, user_plan, aggregated_results)
        
        # Update performance metrics
        total_time = time.time() - scan_start_time
        self._update_performance_metrics(scan_id, optimized_scanners, total_time)
        
        # Clean up
        self.active_scans.pop(scan_id, None)
        
        return aggregated_results
    
    async def _execute_scanners_batched(self, scanners: List[Any], query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute scanners in optimized batches"""
        results = []
        
        # Create semaphore to limit concurrent scanners
        semaphore = asyncio.Semaphore(self.max_concurrent_scanners)
        
        async def execute_scanner_with_semaphore(scanner):
            async with semaphore:
                return await self._execute_single_scanner_optimized(scanner, query)
        
        # Execute scanners in batches
        batch_size = 5
        for i in range(0, len(scanners), batch_size):
            batch = scanners[i:i + batch_size]
            
            # Execute batch concurrently
            batch_tasks = [execute_scanner_with_semaphore(scanner) for scanner in batch]
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            
            # Process results
            for result in batch_results:
                if isinstance(result, Exception):
                    logger.error(f"Scanner error: {str(result)}")
                    continue
                if result:
                    results.append(result)
            
            # Small delay between batches to prevent overwhelming external APIs
            await asyncio.sleep(0.1)
        
        return results
    
    async def _execute_single_scanner_optimized(self, scanner: Any, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute single scanner with performance optimizations"""
        scanner_name = getattr(scanner, 'name', 'unknown')
        start_time = time.time()
        
        try:
            # Check if scanner can handle query
            if hasattr(scanner, 'can_handle') and not scanner.can_handle(query):
                return None
            
            # Execute scanner with timeout
            result = await asyncio.wait_for(
                scanner.scan(query),
                timeout=30  # 30 second timeout per scanner
            )
            
            execution_time = time.time() - start_time
            
            # Track performance
            self.scanner_performance[scanner_name].append({
                "execution_time": execution_time,
                "timestamp": datetime.utcnow(),
                "success": True
            })
            
            return {
                "scanner": scanner_name,
                "result": result,
                "execution_time": execution_time,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "success"
            }
            
        except asyncio.TimeoutError:
            execution_time = time.time() - start_time
            logger.warning(f"Scanner {scanner_name} timed out after {execution_time:.2f}s")
            
            self.scanner_performance[scanner_name].append({
                "execution_time": execution_time,
                "timestamp": datetime.utcnow(),
                "success": False,
                "error": "timeout"
            })
            
            return {
                "scanner": scanner_name,
                "result": {"error": "Scanner timed out"},
                "execution_time": execution_time,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "timeout"
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Scanner {scanner_name} error: {str(e)}")
            
            self.scanner_performance[scanner_name].append({
                "execution_time": execution_time,
                "timestamp": datetime.utcnow(),
                "success": False,
                "error": str(e)
            })
            
            return {
                "scanner": scanner_name,
                "result": {"error": str(e)},
                "execution_time": execution_time,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "error"
            }
    
    def _select_optimal_scanners(self, scanners: List[Any], user_plan: str) -> List[Any]:
        """Select optimal scanners based on performance and user plan"""
        
        # Plan-based scanner limits
        plan_limits = {
            "free": 10,
            "professional": 50,
            "enterprise": 100
        }
        
        max_scanners = plan_limits.get(user_plan, 10)
        
        # Sort scanners by performance (success rate and speed)
        scanner_scores = {}
        for scanner in scanners:
            scanner_name = getattr(scanner, 'name', 'unknown')
            performance_data = self.scanner_performance.get(scanner_name, [])
            
            if performance_data:
                # Calculate performance score
                recent_data = performance_data[-10:]  # Last 10 executions
                success_rate = sum(1 for p in recent_data if p["success"]) / len(recent_data)
                avg_time = sum(p["execution_time"] for p in recent_data) / len(recent_data)
                
                # Score: higher success rate and lower time = better score
                score = success_rate * 100 - avg_time
            else:
                # Default score for new scanners
                score = 50
            
            scanner_scores[scanner] = score
        
        # Sort by score and take top performers
        optimal_scanners = sorted(scanners, key=lambda s: scanner_scores.get(s, 0), reverse=True)
        return optimal_scanners[:max_scanners]
    
    async def _aggregate_results_optimized(self, scanner_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Optimized result aggregation"""
        
        successful_results = [r for r in scanner_results if r.get("status") == "success"]
        
        # Extract entities from results
        all_entities = []
        for result in successful_results:
            result_data = result.get("result", {})
            
            # Extract entities based on result structure
            if isinstance(result_data, dict):
                entities = self._extract_entities_from_result(result_data, result.get("scanner"))
                all_entities.extend(entities)
        
        # Basic deduplication (more sophisticated logic would be in aggregation engine)
        unique_entities = self._deduplicate_entities_simple(all_entities)
        
        return {
            "query_id": f"query_{int(time.time())}",
            "total_scanners": len(scanner_results),
            "successful_scanners": len(successful_results),
            "entities": unique_entities,
            "scanner_results": successful_results,
            "performance": {
                "total_time": sum(r.get("execution_time", 0) for r in scanner_results),
                "success_rate": len(successful_results) / len(scanner_results) if scanner_results else 0
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _extract_entities_from_result(self, result_data: Dict[str, Any], scanner_name: str) -> List[Dict[str, Any]]:
        """Extract entities from scanner result"""
        entities = []
        
        # Look for common entity fields
        entity_fields = {
            "email": ["email", "email_address", "contact_email"],
            "phone": ["phone", "phone_number", "mobile", "telephone"],
            "name": ["name", "full_name", "display_name", "username"],
            "url": ["url", "website", "profile_url", "homepage"]
        }
        
        for entity_type, field_names in entity_fields.items():
            for field_name in field_names:
                if field_name in result_data and result_data[field_name]:
                    entities.append({
                        "type": entity_type,
                        "value": result_data[field_name],
                        "source": scanner_name,
                        "confidence": result_data.get("confidence", 0.5)
                    })
        
        return entities
    
    def _deduplicate_entities_simple(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Simple entity deduplication"""
        seen = set()
        unique_entities = []
        
        for entity in entities:
            entity_key = f"{entity['type']}:{entity['value'].lower()}"
            if entity_key not in seen:
                seen.add(entity_key)
                unique_entities.append(entity)
        
        return unique_entities
    
    def _update_performance_metrics(self, scan_id: str, scanners: List[Any], total_time: float):
        """Update performance metrics"""
        logger.info(f"Scan {scan_id} completed in {total_time:.2f}s with {len(scanners)} scanners")
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        stats = {}
        
        for scanner_name, performance_data in self.scanner_performance.items():
            if not performance_data:
                continue
            
            recent_data = performance_data[-50:]  # Last 50 executions
            successful = [p for p in recent_data if p["success"]]
            
            stats[scanner_name] = {
                "total_executions": len(recent_data),
                "successful_executions": len(successful),
                "success_rate": len(successful) / len(recent_data) if recent_data else 0,
                "avg_execution_time": sum(p["execution_time"] for p in recent_data) / len(recent_data) if recent_data else 0,
                "avg_successful_time": sum(p["execution_time"] for p in successful) / len(successful) if successful else 0
            }
        
        return stats


class DatabaseOptimizer:
    """Database query optimization and connection management"""
    
    def __init__(self):
        self.query_cache = {}
        self.slow_query_threshold = 2.0  # seconds
    
    def optimize_query(self, query: str, params: Dict[str, Any] = None) -> str:
        """Optimize database query"""
        
        # Add common optimizations
        optimized_query = query
        
        # Add LIMIT if not present for SELECT queries
        if "SELECT" in query.upper() and "LIMIT" not in query.upper():
            optimized_query += " LIMIT 1000"
        
        # Add index hints for common patterns
        if "WHERE email =" in query:
            optimized_query = optimized_query.replace("WHERE email =", "WHERE email = /* USE INDEX (idx_email) */")
        
        if "WHERE user_id =" in query:
            optimized_query = optimized_query.replace("WHERE user_id =", "WHERE user_id = /* USE INDEX (idx_user_id) */")
        
        return optimized_query
    
    def get_recommended_indexes(self) -> List[Dict[str, Any]]:
        """Get recommended database indexes"""
        return [
            {
                "table": "users",
                "columns": ["email"],
                "type": "UNIQUE",
                "name": "idx_users_email"
            },
            {
                "table": "queries", 
                "columns": ["user_id", "created_at"],
                "type": "INDEX",
                "name": "idx_queries_user_created"
            },
            {
                "table": "scan_results",
                "columns": ["query_id", "scanner_type"],
                "type": "INDEX", 
                "name": "idx_scan_results_query_scanner"
            },
            {
                "table": "reports",
                "columns": ["user_id", "report_type", "created_at"],
                "type": "INDEX",
                "name": "idx_reports_user_type_created"
            },
            {
                "table": "audit_logs",
                "columns": ["user_id", "event_type", "timestamp"],
                "type": "INDEX",
                "name": "idx_audit_user_event_time"
            }
        ]


class PerformanceMonitor:
    """Monitor and track system performance"""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.start_time = time.time()
    
    def record_metric(self, metric_name: str, value: float, tags: Dict[str, str] = None):
        """Record performance metric"""
        metric_entry = {
            "timestamp": datetime.utcnow(),
            "value": value,
            "tags": tags or {}
        }
        
        self.metrics[metric_name].append(metric_entry)
        
        # Keep only recent metrics (last 1000 entries)
        if len(self.metrics[metric_name]) > 1000:
            self.metrics[metric_name] = self.metrics[metric_name][-1000:]
    
    def get_metric_stats(self, metric_name: str, time_window_minutes: int = 60) -> Dict[str, Any]:
        """Get statistics for a metric"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=time_window_minutes)
        
        recent_metrics = [
            m for m in self.metrics.get(metric_name, [])
            if m["timestamp"] > cutoff_time
        ]
        
        if not recent_metrics:
            return {"count": 0}
        
        values = [m["value"] for m in recent_metrics]
        
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
            "latest": values[-1] if values else None
        }
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health score"""
        
        # Get cache performance
        cache_stats = self.cache_manager.get_stats() if hasattr(self.cache_manager, 'get_stats') else {"hit_rate": 0.5}
        
        # Calculate health score based on various metrics
        cache_health = min(cache_stats.get("hit_rate", 0.5) * 2, 1.0)  # Good cache hit rate
        
        # Check if we have any active scans
        active_scan_count = len(getattr(self, 'active_scans', {}))
        load_health = 1.0 if active_scan_count < 10 else max(0.1, 1.0 - (active_scan_count - 10) * 0.1)
        
        overall_health = (cache_health + load_health) / 2
        
        return {
            "overall_score": overall_health,
            "cache_health": cache_health,
            "load_health": load_health,
            "active_scans": active_scan_count,
            "status": "healthy" if overall_health > 0.7 else "degraded" if overall_health > 0.4 else "unhealthy",
            "timestamp": datetime.utcnow().isoformat()
        }


class PerformanceMonitor:
    """Monitors system performance and provides metrics"""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.start_time = datetime.utcnow()
        self.request_count = 0
        self.error_count = 0
    
    def record_metric(self, metric_name: str, value: float, tags: Dict[str, str] = None):
        """Record a performance metric"""
        metric_data = {
            "value": value,
            "timestamp": datetime.utcnow(),
            "tags": tags or {}
        }
        self.metrics[metric_name].append(metric_data)
        
        # Keep only last 1000 metrics per type
        if len(self.metrics[metric_name]) > 1000:
            self.metrics[metric_name] = self.metrics[metric_name][-1000:]
    
    def record_request(self, duration: float, success: bool = True):
        """Record request metrics"""
        self.request_count += 1
        if not success:
            self.error_count += 1
        
        self.record_metric("request_duration", duration)
        self.record_metric("request_count", 1)
        if not success:
            self.record_metric("error_count", 1)
    
    def get_metrics_summary(self, metric_name: str, minutes: int = 60) -> Dict[str, Any]:
        """Get summary of metrics for the last N minutes"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
        
        if metric_name not in self.metrics:
            return {"count": 0, "avg": 0, "min": 0, "max": 0}
        
        recent_metrics = [
            m for m in self.metrics[metric_name] 
            if m["timestamp"] > cutoff_time
        ]
        
        if not recent_metrics:
            return {"count": 0, "avg": 0, "min": 0, "max": 0}
        
        values = [m["value"] for m in recent_metrics]
        return {
            "count": len(values),
            "avg": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "latest": values[-1] if values else 0
        }
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get overall system statistics"""
        uptime = datetime.utcnow() - self.start_time
        error_rate = (self.error_count / self.request_count) if self.request_count > 0 else 0
        
        return {
            "uptime_seconds": uptime.total_seconds(),
            "uptime_formatted": self._format_duration(uptime.total_seconds()),
            "total_requests": self.request_count,
            "total_errors": self.error_count,
            "error_rate": error_rate,
            "avg_response_time": self.get_metrics_summary("request_duration", 60)["avg"],
            "health_status": "healthy" if error_rate < 0.05 else "degraded"
        }
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Alias for get_system_stats for backward compatibility"""
        return self.get_system_stats()
    
    def _format_duration(self, seconds: int) -> str:
        """Format duration in human readable format"""
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
        """Get overall system health metrics"""
        uptime_seconds = time.time() - self.start_time
        
        health_status = {
            "uptime_seconds": uptime_seconds,
            "uptime_human": self._format_uptime(uptime_seconds),
            "metrics_collected": len(self.metrics),
            "cache_stats": {},  # Would be populated by cache manager
            "active_scans": 0,  # Would be populated by orchestrator
            "status": "healthy"
        }
        
        # Check for any concerning metrics
        query_time_stats = self.get_metric_stats("query_execution_time", 15)
        if query_time_stats.get("avg", 0) > 5.0:  # Average query time > 5 seconds
            health_status["status"] = "degraded"
            health_status["alerts"] = ["High average query execution time"]
        
        return health_status
    
    def _format_uptime(self, seconds: float) -> str:
        """Format uptime in human readable format"""
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"


# Factory functions
def create_performance_optimizer() -> Dict[str, Any]:
    """Create and return performance optimization components"""
    cache_manager = CacheManager()
    orchestrator = AsyncScannerOrchestrator(cache_manager)
    db_optimizer = DatabaseOptimizer()
    performance_monitor = PerformanceMonitor()
    
    return {
        "cache_manager": cache_manager,
        "orchestrator": orchestrator,
        "db_optimizer": db_optimizer,
        "performance_monitor": performance_monitor
    }