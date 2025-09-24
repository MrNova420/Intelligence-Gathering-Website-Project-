"""
Enterprise Scanner Engine
=========================

AAA-grade scanner architecture with:
- Modular and extensible design
- Async/await patterns for performance
- Comprehensive error handling
- Circuit breaker patterns
- Rate limiting and throttling
- Result caching and optimization
- Monitoring and observability
"""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Type, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
import weakref

logger = logging.getLogger(__name__)


class ScannerStatus(str, Enum):
    """Scanner execution status"""
    PENDING = "pending"
    INITIALIZING = "initializing"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"
    RATE_LIMITED = "rate_limited"


class ScannerCategory(str, Enum):
    """Scanner categories for organization"""
    EMAIL = "email"
    PHONE = "phone"
    SOCIAL_MEDIA = "social_media"
    SEARCH_ENGINE = "search_engine"
    PUBLIC_RECORDS = "public_records"
    NETWORK = "network"
    IMAGE_ANALYSIS = "image_analysis"
    AI_CORRELATION = "ai_correlation"


@dataclass
class ScannerMetrics:
    """Scanner performance metrics"""
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    average_execution_time: float = 0.0
    last_execution_time: Optional[datetime] = None
    rate_limit_hits: int = 0
    circuit_breaker_trips: int = 0
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage"""
        if self.total_executions == 0:
            return 0.0
        return (self.successful_executions / self.total_executions) * 100
    
    @property
    def reliability_score(self) -> float:
        """Calculate reliability score (0-100)"""
        success_weight = 0.6
        speed_weight = 0.3
        stability_weight = 0.1
        
        # Success rate component (0-60)
        success_component = (self.success_rate / 100) * (success_weight * 100)
        
        # Speed component (0-30) - faster is better, normalized to 30 max
        speed_component = max(0, speed_weight * 100 - (self.average_execution_time * 5))
        speed_component = min(speed_component, speed_weight * 100)
        
        # Stability component (0-10) - fewer circuit breaker trips is better
        stability_component = max(0, stability_weight * 100 - (self.circuit_breaker_trips * 2))
        
        return success_component + speed_component + stability_component


@dataclass
class ScannerConfig:
    """Scanner configuration"""
    timeout: int = 30  # seconds
    max_retries: int = 3
    retry_delay: float = 1.0
    rate_limit_requests: int = 60  # per minute
    rate_limit_window: int = 60  # seconds
    circuit_breaker_threshold: int = 5  # failures before opening
    circuit_breaker_timeout: int = 300  # seconds
    priority: int = 1  # 1-10, higher is better
    enabled: bool = True
    requires_api_key: bool = False
    cost_credits: int = 1  # credits consumed per execution


@dataclass
class ScanResult:
    """Standardized scan result"""
    scanner_name: str
    status: ScannerStatus
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_successful(self) -> bool:
        """Check if scan was successful"""
        return self.status == ScannerStatus.COMPLETED and self.data is not None


class CircuitBreaker:
    """Circuit breaker pattern implementation for scanner resilience"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 300):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func: Callable) -> Callable:
        """Decorator for circuit breaker functionality"""
        async def wrapper(*args, **kwargs):
            if self.state == "OPEN":
                if time.time() - self.last_failure_time > self.timeout:
                    self.state = "HALF_OPEN"
                else:
                    raise Exception("Circuit breaker is OPEN")
            
            try:
                result = await func(*args, **kwargs)
                if self.state == "HALF_OPEN":
                    self.state = "CLOSED"
                    self.failure_count = 0
                return result
            except Exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()
                
                if self.failure_count >= self.failure_threshold:
                    self.state = "OPEN"
                    
                raise e
        
        return wrapper


class RateLimiter:
    """Rate limiter for API calls"""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests = []
    
    async def acquire(self) -> bool:
        """Acquire rate limit permission"""
        now = time.time()
        
        # Remove old requests (older than 1 minute)
        self.requests = [req_time for req_time in self.requests if now - req_time < 60]
        
        if len(self.requests) < self.requests_per_minute:
            self.requests.append(now)
            return True
        
        return False
    
    def get_wait_time(self) -> float:
        """Get time to wait before next request"""
        if not self.requests:
            return 0
        
        oldest_request = min(self.requests)
        return max(0, 60 - (time.time() - oldest_request))


class BaseScanner(ABC):
    """Abstract base class for all scanners with enterprise features"""
    
    def __init__(self, config: Optional[ScannerConfig] = None):
        self.config = config or ScannerConfig()
        self.metrics = ScannerMetrics()
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=self.config.circuit_breaker_threshold,
            timeout=self.config.circuit_breaker_timeout
        )
        self.rate_limiter = RateLimiter(self.config.rate_limit_requests)
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Scanner name identifier"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Scanner description"""
        pass
    
    @property
    @abstractmethod
    def category(self) -> ScannerCategory:
        """Scanner category"""
        pass
    
    @abstractmethod
    async def _scan_implementation(self, target: str, **kwargs) -> Dict[str, Any]:
        """Actual scanning implementation (must be implemented by subclasses)"""
        pass
    
    async def scan(self, target: str, **kwargs) -> ScanResult:
        """Main scan method with enterprise features"""
        start_time = time.time()
        
        try:
            # Check if scanner is enabled
            if not self.config.enabled:
                return ScanResult(
                    scanner_name=self.name,
                    status=ScannerStatus.CANCELLED,
                    error="Scanner is disabled"
                )
            
            # Rate limiting
            if not await self.rate_limiter.acquire():
                self.metrics.rate_limit_hits += 1
                wait_time = self.rate_limiter.get_wait_time()
                
                self._logger.warning(f"Rate limit hit for {self.name}, waiting {wait_time:.2f}s")
                
                return ScanResult(
                    scanner_name=self.name,
                    status=ScannerStatus.RATE_LIMITED,
                    error=f"Rate limited, retry in {wait_time:.2f} seconds"
                )
            
            # Execute with circuit breaker
            scan_func = self.circuit_breaker.call(self._execute_with_timeout)
            data = await scan_func(target, **kwargs)
            
            # Record successful execution
            execution_time = time.time() - start_time
            self.metrics.successful_executions += 1
            self.metrics.total_executions += 1
            self._update_average_execution_time(execution_time)
            
            self._logger.info(f"✅ {self.name} completed successfully in {execution_time:.2f}s")
            
            return ScanResult(
                scanner_name=self.name,
                status=ScannerStatus.COMPLETED,
                data=data,
                execution_time=execution_time
            )
        
        except asyncio.TimeoutError:
            execution_time = time.time() - start_time
            self.metrics.failed_executions += 1
            self.metrics.total_executions += 1
            
            self._logger.error(f"⏰ {self.name} timed out after {execution_time:.2f}s")
            
            return ScanResult(
                scanner_name=self.name,
                status=ScannerStatus.TIMEOUT,
                error=f"Scanner timed out after {self.config.timeout} seconds",
                execution_time=execution_time
            )
        
        except Exception as e:
            execution_time = time.time() - start_time
            self.metrics.failed_executions += 1
            self.metrics.total_executions += 1
            
            self._logger.error(f"💥 {self.name} failed: {str(e)}")
            
            return ScanResult(
                scanner_name=self.name,
                status=ScannerStatus.FAILED,
                error=str(e),
                execution_time=execution_time
            )
        
        finally:
            self.metrics.last_execution_time = datetime.utcnow()
    
    async def _execute_with_timeout(self, target: str, **kwargs) -> Dict[str, Any]:
        """Execute scan with timeout"""
        return await asyncio.wait_for(
            self._scan_implementation(target, **kwargs),
            timeout=self.config.timeout
        )
    
    def _update_average_execution_time(self, execution_time: float):
        """Update average execution time"""
        if self.metrics.successful_executions == 1:
            self.metrics.average_execution_time = execution_time
        else:
            # Exponential moving average
            alpha = 0.1
            self.metrics.average_execution_time = (
                alpha * execution_time + 
                (1 - alpha) * self.metrics.average_execution_time
            )
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get scanner health status"""
        return {
            "name": self.name,
            "status": "healthy" if self.circuit_breaker.state == "CLOSED" else "unhealthy",
            "circuit_breaker_state": self.circuit_breaker.state,
            "metrics": {
                "total_executions": self.metrics.total_executions,
                "success_rate": self.metrics.success_rate,
                "reliability_score": self.metrics.reliability_score,
                "average_execution_time": self.metrics.average_execution_time,
                "last_execution": self.metrics.last_execution_time.isoformat() if self.metrics.last_execution_time else None
            }
        }


class EnterpriseScannerRegistry:
    """Registry for managing scanner instances with enterprise features"""
    
    def __init__(self):
        self._scanners: Dict[str, BaseScanner] = {}
        self._categories: Dict[ScannerCategory, List[str]] = {}
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def register(self, scanner: BaseScanner):
        """Register a scanner"""
        self._scanners[scanner.name] = scanner
        
        # Add to category index
        if scanner.category not in self._categories:
            self._categories[scanner.category] = []
        
        if scanner.name not in self._categories[scanner.category]:
            self._categories[scanner.category].append(scanner.name)
        
        self._logger.info(f"📝 Registered scanner: {scanner.name} ({scanner.category.value})")
    
    def unregister(self, scanner_name: str):
        """Unregister a scanner"""
        if scanner_name in self._scanners:
            scanner = self._scanners[scanner_name]
            del self._scanners[scanner_name]
            
            # Remove from category index
            if scanner.category in self._categories:
                if scanner_name in self._categories[scanner.category]:
                    self._categories[scanner.category].remove(scanner_name)
            
            self._logger.info(f"🗑️ Unregistered scanner: {scanner_name}")
    
    def get_scanner(self, name: str) -> Optional[BaseScanner]:
        """Get scanner by name"""
        return self._scanners.get(name)
    
    def get_scanners_by_category(self, category: ScannerCategory) -> List[BaseScanner]:
        """Get all scanners in a category"""
        scanner_names = self._categories.get(category, [])
        return [self._scanners[name] for name in scanner_names if name in self._scanners]
    
    def get_all_scanners(self) -> List[BaseScanner]:
        """Get all registered scanners"""
        return list(self._scanners.values())
    
    def get_enabled_scanners(self) -> List[BaseScanner]:
        """Get all enabled scanners"""
        return [scanner for scanner in self._scanners.values() if scanner.config.enabled]
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """Get registry statistics"""
        enabled_count = len(self.get_enabled_scanners())
        
        return {
            "total_scanners": len(self._scanners),
            "enabled_scanners": enabled_count,
            "disabled_scanners": len(self._scanners) - enabled_count,
            "categories": {cat.value: len(scanners) for cat, scanners in self._categories.items()},
            "scanner_list": list(self._scanners.keys())
        }
    
    def get_health_report(self) -> Dict[str, Any]:
        """Get comprehensive health report for all scanners"""
        health_data = {}
        
        for scanner in self._scanners.values():
            health_data[scanner.name] = scanner.get_health_status()
        
        # Calculate overall health metrics
        total_scanners = len(self._scanners)
        healthy_scanners = sum(1 for data in health_data.values() if data["status"] == "healthy")
        
        overall_health = {
            "status": "healthy" if healthy_scanners == total_scanners else "degraded",
            "healthy_scanners": healthy_scanners,
            "unhealthy_scanners": total_scanners - healthy_scanners,
            "health_percentage": (healthy_scanners / total_scanners * 100) if total_scanners > 0 else 0
        }
        
        return {
            "overall": overall_health,
            "scanners": health_data,
            "timestamp": datetime.utcnow().isoformat()
        }


class EnterpriseScannerOrchestrator:
    """Enterprise scanner orchestrator with advanced execution patterns"""
    
    def __init__(self, registry: EnterpriseScannerRegistry, max_concurrent: int = 10):
        self.registry = registry
        self.max_concurrent = max_concurrent
        self.executor = ThreadPoolExecutor(max_workers=max_concurrent)
        self._active_scans: Dict[str, asyncio.Task] = {}
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    async def execute_scan_batch(
        self, 
        target: str, 
        scanner_names: Optional[List[str]] = None,
        categories: Optional[List[ScannerCategory]] = None,
        priority_threshold: int = 1
    ) -> Dict[str, ScanResult]:
        """Execute multiple scanners concurrently with advanced orchestration"""
        
        # Determine scanners to execute
        scanners = self._select_scanners(scanner_names, categories, priority_threshold)
        
        if not scanners:
            self._logger.warning("No scanners selected for execution")
            return {}
        
        self._logger.info(f"🚀 Starting batch scan with {len(scanners)} scanners for target: {target}")
        
        # Create tasks for concurrent execution
        tasks = {}
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        for scanner in scanners:
            task = asyncio.create_task(
                self._execute_scanner_with_semaphore(semaphore, scanner, target)
            )
            tasks[scanner.name] = task
            self._active_scans[f"{scanner.name}_{target}"] = task
        
        # Wait for all tasks to complete
        try:
            results = await asyncio.gather(*tasks.values(), return_exceptions=True)
            
            # Process results
            scan_results = {}
            for i, (scanner_name, task) in enumerate(tasks.items()):
                result = results[i]
                
                if isinstance(result, Exception):
                    self._logger.error(f"💥 Task error for {scanner_name}: {result}")
                    scan_results[scanner_name] = ScanResult(
                        scanner_name=scanner_name,
                        status=ScannerStatus.FAILED,
                        error=str(result)
                    )
                else:
                    scan_results[scanner_name] = result
                
                # Clean up active scans
                scan_key = f"{scanner_name}_{target}"
                if scan_key in self._active_scans:
                    del self._active_scans[scan_key]
            
            self._logger.info(f"✅ Batch scan completed: {len(scan_results)} results")
            return scan_results
            
        except Exception as e:
            self._logger.exception(f"💥 Batch scan failed: {e}")
            raise
    
    async def _execute_scanner_with_semaphore(
        self, 
        semaphore: asyncio.Semaphore, 
        scanner: BaseScanner, 
        target: str
    ) -> ScanResult:
        """Execute scanner with semaphore for concurrency control"""
        async with semaphore:
            return await scanner.scan(target)
    
    def _select_scanners(
        self, 
        scanner_names: Optional[List[str]], 
        categories: Optional[List[ScannerCategory]], 
        priority_threshold: int
    ) -> List[BaseScanner]:
        """Select scanners based on criteria"""
        scanners = []
        
        if scanner_names:
            # Specific scanners requested
            for name in scanner_names:
                scanner = self.registry.get_scanner(name)
                if scanner and scanner.config.enabled:
                    scanners.append(scanner)
        elif categories:
            # Scanners by category
            for category in categories:
                category_scanners = self.registry.get_scanners_by_category(category)
                scanners.extend([s for s in category_scanners if s.config.enabled])
        else:
            # All enabled scanners
            scanners = self.registry.get_enabled_scanners()
        
        # Filter by priority threshold
        scanners = [s for s in scanners if s.config.priority >= priority_threshold]
        
        # Sort by priority (highest first) and reliability
        scanners.sort(key=lambda s: (s.config.priority, s.metrics.reliability_score), reverse=True)
        
        return scanners
    
    def get_active_scans(self) -> Dict[str, Any]:
        """Get information about currently active scans"""
        return {
            "active_count": len(self._active_scans),
            "scans": list(self._active_scans.keys()),
            "max_concurrent": self.max_concurrent
        }
    
    async def cancel_scan(self, scan_key: str) -> bool:
        """Cancel an active scan"""
        if scan_key in self._active_scans:
            task = self._active_scans[scan_key]
            task.cancel()
            del self._active_scans[scan_key]
            self._logger.info(f"🛑 Cancelled scan: {scan_key}")
            return True
        return False


# Global registry instance
scanner_registry = EnterpriseScannerRegistry()

# Convenience function to get orchestrator
def get_orchestrator(max_concurrent: int = 10) -> EnterpriseScannerOrchestrator:
    """Get scanner orchestrator instance"""
    return EnterpriseScannerOrchestrator(scanner_registry, max_concurrent)