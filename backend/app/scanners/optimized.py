
# Enhanced scanner base with proper async handling
import asyncio
import aiohttp
import time
from typing import Dict, Any, Optional

class OptimizedBaseScannerModule:
    def __init__(self, name: str, scanner_type: str, description: str = ""):
        self.name = name
        self.scanner_type = scanner_type
        self.description = description
        self.enabled = True
        self.timeout = 30
        self.retry_count = 3
        self.rate_limit = 1.0  # seconds between requests
        self._last_request = 0
    
    async def scan(self, query) -> Dict[str, Any]:
        """Enhanced scan with timeout, retries, and rate limiting."""
        # Rate limiting
        current_time = time.time()
        time_since_last = current_time - self._last_request
        if time_since_last < self.rate_limit:
            await asyncio.sleep(self.rate_limit - time_since_last)
        
        self._last_request = time.time()
        
        for attempt in range(self.retry_count):
            try:
                async with asyncio.timeout(self.timeout):
                    result = await self._perform_scan(query)
                    return {
                        "scanner": self.name,
                        "type": self.scanner_type,
                        "query": query.query_value if hasattr(query, 'query_value') else str(query),
                        "result": result,
                        "confidence": self._calculate_confidence(result),
                        "timestamp": time.time(),
                        "attempt": attempt + 1
                    }
            except asyncio.TimeoutError:
                self.logger.warning(f"Scanner {self.name} timeout on attempt {attempt + 1}")
                if attempt == self.retry_count - 1:
                    return self._error_result(query, "timeout")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                self.logger.error(f"Scanner {self.name} error: {e}")
                if attempt == self.retry_count - 1:
                    return self._error_result(query, str(e))
                await asyncio.sleep(1)
        
        return self._error_result(query, "max_retries_exceeded")
    
    async def _perform_scan(self, query) -> Dict[str, Any]:
        """Override this method in subclasses."""
        await asyncio.sleep(0.1)  # Simulate API call
        return {"status": "success", "data": f"Mock result for {query}"}
    
    def _calculate_confidence(self, result: Dict[str, Any]) -> float:
        """Calculate confidence score for the result."""
        if not result or result.get("status") == "error":
            return 0.0
        return 0.85  # Default confidence
    
    def _error_result(self, query, error: str) -> Dict[str, Any]:
        """Create error result structure."""
        return {
            "scanner": self.name,
            "type": self.scanner_type,
            "query": query.query_value if hasattr(query, 'query_value') else str(query),
            "result": {"status": "error", "error": error},
            "confidence": 0.0,
            "timestamp": time.time(),
            "error": True
        }
