"""
Optimized Scanner Implementation
===============================

High-performance scanners with async operations, proper error handling, and optimization.
"""

import asyncio
import aiohttp
import time
import logging
from typing import Dict, Any, Optional, List
from concurrent.futures import ThreadPoolExecutor
import json

logger = logging.getLogger(__name__)

class OptimizedScannerBase:
    """Base class for optimized scanners with enhanced performance"""
    
    def __init__(self, name: str, scanner_type: str, description: str = ""):
        self.name = name
        self.scanner_type = scanner_type
        self.description = description
        self.enabled = True
        self.timeout = 30
        self.retry_count = 3
        self.rate_limit = 1.0  # seconds between requests
        self._last_request = 0
        self.session = None
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            connector=aiohttp.TCPConnector(limit=10, limit_per_host=5)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
        self.executor.shutdown(wait=True)
    
    async def scan(self, query) -> Dict[str, Any]:
        """Enhanced scan with comprehensive error handling and optimization."""
        start_time = time.time()
        
        # Rate limiting
        await self._apply_rate_limit()
        
        for attempt in range(self.retry_count):
            try:
                result = await asyncio.wait_for(
                    self._perform_scan(query),
                    timeout=self.timeout
                )
                
                processing_time = time.time() - start_time
                
                return {
                    "scanner": self.name,
                    "type": self.scanner_type,
                    "query": self._extract_query_value(query),
                    "result": result,
                    "confidence": self._calculate_confidence(result),
                    "timestamp": time.time(),
                    "processing_time": processing_time,
                    "attempt": attempt + 1,
                    "status": "success"
                }
                
            except asyncio.TimeoutError:
                logger.warning(f"Scanner {self.name} timeout on attempt {attempt + 1}")
                if attempt == self.retry_count - 1:
                    return self._error_result(query, "timeout", time.time() - start_time)
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                
            except Exception as e:
                logger.error(f"Scanner {self.name} error on attempt {attempt + 1}: {e}")
                if attempt == self.retry_count - 1:
                    return self._error_result(query, str(e), time.time() - start_time)
                await asyncio.sleep(1 * attempt)  # Linear backoff for other errors
        
        return self._error_result(query, "max_retries_exceeded", time.time() - start_time)
    
    async def _apply_rate_limit(self):
        """Apply rate limiting between requests"""
        current_time = time.time()
        time_since_last = current_time - self._last_request
        if time_since_last < self.rate_limit:
            await asyncio.sleep(self.rate_limit - time_since_last)
        self._last_request = time.time()
    
    def _extract_query_value(self, query) -> str:
        """Extract query value from query object"""
        if hasattr(query, 'query_value'):
            return query.query_value
        elif hasattr(query, 'value'):
            return query.value
        elif isinstance(query, dict):
            return query.get('query', str(query))
        else:
            return str(query)
    
    async def _perform_scan(self, query) -> Dict[str, Any]:
        """Override this method in child classes"""
        return {"data": "mock_scan_result"}
    
    def _calculate_confidence(self, result: Dict[str, Any]) -> float:
        """Calculate confidence score for the result"""
        if not result or not isinstance(result, dict):
            return 0.0
        
        # Basic confidence calculation
        confidence = 0.5  # Base confidence
        
        if result.get('verified', False):
            confidence += 0.3
        
        if result.get('multiple_sources', False):
            confidence += 0.2
        
        if result.get('recent_data', False):
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _error_result(self, query, error: str, processing_time: float) -> Dict[str, Any]:
        """Generate error result structure"""
        return {
            "scanner": self.name,
            "type": self.scanner_type,
            "query": self._extract_query_value(query),
            "result": {"error": error},
            "confidence": 0.0,
            "timestamp": time.time(),
            "processing_time": processing_time,
            "status": "error"
        }

class EmailScanner(OptimizedScannerBase):
    """Optimized email scanner"""
    
    def __init__(self):
        super().__init__("email_scanner", "email", "Advanced email intelligence scanner")
    
    async def _perform_scan(self, query) -> Dict[str, Any]:
        """Perform email scan with multiple techniques"""
        email = self._extract_query_value(query)
        
        results = {
            "email": email,
            "domain": email.split('@')[1] if '@' in email else None,
            "valid_format": '@' in email and '.' in email,
            "reputation": await self._check_email_reputation(email),
            "breach_check": await self._check_data_breaches(email),
            "social_presence": await self._check_social_presence(email)
        }
        
        return results
    
    async def _check_email_reputation(self, email: str) -> Dict[str, Any]:
        """Check email reputation (mock implementation)"""
        return {
            "score": 0.8,
            "status": "good",
            "risk_factors": []
        }
    
    async def _check_data_breaches(self, email: str) -> Dict[str, Any]:
        """Check for data breach involvement (mock implementation)"""
        return {
            "breaches_found": 0,
            "last_breach": None,
            "severity": "low"
        }
    
    async def _check_social_presence(self, email: str) -> Dict[str, Any]:
        """Check social media presence (mock implementation)"""
        return {
            "platforms": [],
            "verified_accounts": 0,
            "last_activity": None
        }

class PhoneScanner(OptimizedScannerBase):
    """Optimized phone number scanner"""
    
    def __init__(self):
        super().__init__("phone_scanner", "phone", "Advanced phone number intelligence scanner")
    
    async def _perform_scan(self, query) -> Dict[str, Any]:
        """Perform phone number scan"""
        phone = self._extract_query_value(query)
        
        results = {
            "phone": phone,
            "formatted": self._format_phone(phone),
            "carrier": await self._get_carrier_info(phone),
            "location": await self._get_location_info(phone),
            "reputation": await self._check_phone_reputation(phone),
            "social_presence": await self._check_phone_social_presence(phone)
        }
        
        return results
    
    def _format_phone(self, phone: str) -> str:
        """Format phone number"""
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        return phone
    
    async def _get_carrier_info(self, phone: str) -> Dict[str, Any]:
        """Get carrier information (mock implementation)"""
        return {
            "carrier": "Unknown",
            "type": "mobile",
            "country": "US"
        }
    
    async def _get_location_info(self, phone: str) -> Dict[str, Any]:
        """Get location information (mock implementation)"""
        return {
            "area_code": phone[-10:-7] if len(phone) >= 10 else None,
            "region": "Unknown",
            "timezone": "UTC"
        }
    
    async def _check_phone_reputation(self, phone: str) -> Dict[str, Any]:
        """Check phone reputation (mock implementation)"""
        return {
            "spam_score": 0.1,
            "reports": 0,
            "status": "clean"
        }
    
    async def _check_phone_social_presence(self, phone: str) -> Dict[str, Any]:
        """Check social media presence (mock implementation)"""
        return {
            "linked_accounts": [],
            "verification_status": "unverified"
        }

class ScannerOrchestrator:
    """Orchestrates multiple scanners for comprehensive results"""
    
    def __init__(self):
        self.scanners = {
            "email": EmailScanner(),
            "phone": PhoneScanner()
        }
    
    async def run_comprehensive_scan(self, query, scanner_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run comprehensive scan across multiple scanners"""
        start_time = time.time()
        
        if scanner_types is None:
            scanner_types = list(self.scanners.keys())
        
        results = {}
        tasks = []
        
        for scanner_type in scanner_types:
            if scanner_type in self.scanners:
                scanner = self.scanners[scanner_type]
                async with scanner as s:
                    task = asyncio.create_task(s.scan(query))
                    tasks.append((scanner_type, task))
        
        # Wait for all tasks to complete
        for scanner_type, task in tasks:
            try:
                result = await task
                results[scanner_type] = result
            except Exception as e:
                logger.error(f"Scanner {scanner_type} failed: {e}")
                results[scanner_type] = {
                    "scanner": scanner_type,
                    "status": "error",
                    "error": str(e)
                }
        
        total_time = time.time() - start_time
        
        return {
            "query": str(query),
            "scanners_used": len(scanner_types),
            "results": results,
            "summary": self._generate_summary(results),
            "total_processing_time": total_time,
            "timestamp": time.time()
        }
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of scan results"""
        successful_scans = sum(1 for r in results.values() if r.get('status') == 'success')
        total_scans = len(results)
        avg_confidence = sum(r.get('confidence', 0) for r in results.values()) / total_scans if total_scans > 0 else 0
        
        return {
            "success_rate": successful_scans / total_scans if total_scans > 0 else 0,
            "average_confidence": avg_confidence,
            "total_scanners": total_scans,
            "successful_scanners": successful_scans
        }

# Global orchestrator instance
scanner_orchestrator = ScannerOrchestrator()
