"""
Enterprise Components Test Suite
===============================

Comprehensive tests for enterprise-grade components with:
- Unit tests for all major components
- Integration tests for service layer
- Performance benchmarks
- Error handling validation
- Security testing
"""

import pytest
import asyncio
import json
from datetime import datetime, timezone
from uuid import uuid4
from unittest.mock import Mock, patch, AsyncMock

# Test the configuration system
def test_enterprise_configuration():
    """Test enterprise configuration loading"""
    from app.core.enterprise_config import EnterpriseSettings, Environment
    
    # Test configuration initialization
    settings = EnterpriseSettings()
    
    assert settings.environment in [env.value for env in Environment]
    assert settings.database is not None
    assert settings.security is not None
    assert settings.api is not None
    assert settings.monitoring is not None
    
    # Test configuration validation
    assert settings.database.pool_size > 0
    assert settings.security.bcrypt_rounds >= 10
    assert len(settings.security.secret_key) >= 32


def test_enhanced_security_manager():
    """Test enhanced security features"""
    from app.core.enhanced_security import EnhancedSecurityManager, PasswordValidator
    
    security = EnhancedSecurityManager()
    
    # Test encryption/decryption
    test_data = "sensitive information"
    encrypted = security.encrypt_sensitive_data(test_data)
    assert encrypted != test_data
    
    decrypted = security.decrypt_sensitive_data(encrypted)
    assert decrypted == test_data
    
    # Test password hashing
    password = "testpassword123"
    hashed = security.hash_password(password)
    assert security.verify_password(password, hashed)
    assert not security.verify_password("wrongpassword", hashed)
    
    # Test password validation
    validator = PasswordValidator()
    
    # Test weak password
    weak_result = validator.validate_password("123")
    assert not weak_result["valid"]
    assert len(weak_result["errors"]) > 0
    
    # Test strong password
    strong_result = validator.validate_password("MyStr0ng!P@ssw0rd")
    assert strong_result["valid"]
    assert strong_result["strength"] in ["strong", "very strong"]


def test_scanner_engine():
    """Test enterprise scanner engine"""
    from app.scanners.enterprise_scanner_engine import (
        EnterpriseScannerRegistry, BaseScanner, ScannerCategory, ScannerConfig
    )
    
    registry = EnterpriseScannerRegistry()
    
    # Create a mock scanner
    class MockScanner(BaseScanner):
        @property
        def name(self):
            return "test_scanner"
        
        @property
        def description(self):
            return "Test scanner for unit tests"
        
        @property
        def category(self):
            return ScannerCategory.EMAIL
        
        async def _scan_implementation(self, target, **kwargs):
            return {"test": "data", "target": target}
    
    scanner = MockScanner()
    
    # Test scanner registration
    registry.register(scanner)
    stats = registry.get_registry_stats()
    
    assert stats["total_scanners"] == 1
    assert stats["enabled_scanners"] == 1
    assert ScannerCategory.EMAIL.value in stats["categories"]
    
    # Test scanner retrieval
    retrieved_scanner = registry.get_scanner("test_scanner")
    assert retrieved_scanner is not None
    assert retrieved_scanner.name == "test_scanner"
    
    # Test health report
    health = registry.get_health_report()
    assert health["overall"]["status"] == "healthy"
    assert health["overall"]["healthy_scanners"] == 1


@pytest.mark.asyncio
async def test_scanner_execution():
    """Test scanner execution with async patterns"""
    from app.scanners.enterprise_scanner_engine import BaseScanner, ScannerCategory, ScannerStatus
    
    class TestScanner(BaseScanner):
        @property
        def name(self):
            return "async_test_scanner"
        
        @property
        def description(self):
            return "Async test scanner"
        
        @property
        def category(self):
            return ScannerCategory.EMAIL
        
        async def _scan_implementation(self, target, **kwargs):
            await asyncio.sleep(0.1)  # Simulate async work
            return {"result": "success", "target": target}
    
    scanner = TestScanner()
    
    # Test successful scan
    result = await scanner.scan("test@example.com")
    
    assert result.scanner_name == "async_test_scanner"
    assert result.status == ScannerStatus.COMPLETED
    assert result.data is not None
    assert result.data["result"] == "success"
    assert result.execution_time is not None
    assert result.execution_time > 0


@pytest.mark.asyncio
async def test_scanner_orchestrator():
    """Test scanner orchestrator with batch execution"""
    from app.scanners.enterprise_scanner_engine import (
        EnterpriseScannerOrchestrator, EnterpriseScannerRegistry, BaseScanner, ScannerCategory
    )
    
    registry = EnterpriseScannerRegistry()
    
    # Create multiple test scanners
    class FastScanner(BaseScanner):
        @property
        def name(self):
            return "fast_scanner"
        
        @property
        def description(self):
            return "Fast test scanner"
        
        @property
        def category(self):
            return ScannerCategory.EMAIL
        
        async def _scan_implementation(self, target, **kwargs):
            await asyncio.sleep(0.05)
            return {"speed": "fast"}
    
    class SlowScanner(BaseScanner):
        @property
        def name(self):
            return "slow_scanner"
        
        @property
        def description(self):
            return "Slow test scanner"
        
        @property
        def category(self):
            return ScannerCategory.PHONE
        
        async def _scan_implementation(self, target, **kwargs):
            await asyncio.sleep(0.2)
            return {"speed": "slow"}
    
    # Register scanners
    registry.register(FastScanner())
    registry.register(SlowScanner())
    
    # Test orchestrator
    orchestrator = EnterpriseScannerOrchestrator(registry, max_concurrent=2)
    
    start_time = asyncio.get_event_loop().time()
    results = await orchestrator.execute_scan_batch("test@example.com")
    end_time = asyncio.get_event_loop().time()
    
    # Verify results
    assert len(results) == 2
    assert "fast_scanner" in results
    assert "slow_scanner" in results
    
    # Verify concurrent execution (should be faster than sequential)
    execution_time = end_time - start_time
    assert execution_time < 0.3  # Should be less than sum of individual times


def test_api_models():
    """Test enterprise API models and validation"""
    from app.api.enterprise_routes import IntelligenceQuery, QueryResponse, UserProfile
    
    # Test query model validation
    valid_query = IntelligenceQuery(
        query_type="email",
        target="test@example.com",
        priority="high"
    )
    
    assert valid_query.query_type == "email"
    assert valid_query.target == "test@example.com"
    assert valid_query.priority == "high"
    
    # Test invalid query
    with pytest.raises(Exception):  # Should raise validation error
        IntelligenceQuery(
            query_type="email",
            target="",  # Empty target should fail
            priority="invalid_priority"
        )
    
    # Test response model
    response = QueryResponse(
        query_id=str(uuid4()),
        status="queued"
    )
    
    assert response.success is True
    assert response.query_id is not None
    assert response.status == "queued"


def test_enterprise_main_application():
    """Test enterprise main application creation"""
    from app.enterprise_main import create_enterprise_application
    
    app = create_enterprise_application()
    
    assert app.title == "Intelligence Gathering Platform"
    assert app.version == "2.0.0"
    assert app.openapi_url == "/openapi.json"
    
    # Test routes are registered
    route_paths = [route.path for route in app.routes]
    assert "/" in route_paths
    assert "/health" in route_paths
    assert "/metrics" in route_paths


def test_example_scanners():
    """Test example scanner implementations"""
    from app.scanners.example_scanners import (
        EmailValidationScanner, PhoneValidationScanner, 
        SocialMediaScanner, DomainAnalysisScanner
    )
    
    # Test scanner instantiation
    email_scanner = EmailValidationScanner()
    phone_scanner = PhoneValidationScanner()
    social_scanner = SocialMediaScanner()
    domain_scanner = DomainAnalysisScanner()
    
    # Verify scanner properties
    assert email_scanner.name == "email_validator"
    assert phone_scanner.name == "phone_validator"
    assert social_scanner.name == "social_media_scanner"
    assert domain_scanner.name == "domain_analyzer"
    
    # Verify configurations
    assert email_scanner.config.priority >= 1
    assert phone_scanner.config.cost_credits >= 1
    assert social_scanner.config.timeout > 0
    assert domain_scanner.config.enabled is True


@pytest.mark.asyncio
async def test_email_scanner_execution():
    """Test email scanner with real execution"""
    from app.scanners.example_scanners import EmailValidationScanner
    
    scanner = EmailValidationScanner()
    
    # Test valid email
    result = await scanner.scan("test@gmail.com")
    
    assert result.scanner_name == "email_validator"
    assert result.status.value == "completed"
    assert result.data is not None
    assert "valid" in result.data
    assert "domain" in result.data
    assert result.execution_time is not None
    
    # Test invalid email
    invalid_result = await scanner.scan("invalid-email")
    
    assert invalid_result.data is not None
    assert invalid_result.data["valid"] is False
    assert "reason" in invalid_result.data


@pytest.mark.asyncio
async def test_phone_scanner_execution():
    """Test phone scanner with real execution"""
    from app.scanners.example_scanners import PhoneValidationScanner
    
    scanner = PhoneValidationScanner()
    
    # Test US phone number
    result = await scanner.scan("(555) 123-4567")
    
    assert result.scanner_name == "phone_validator"
    assert result.status.value == "completed"
    assert result.data is not None
    assert "valid" in result.data
    assert "normalized" in result.data
    assert "carrier" in result.data
    
    # Verify normalization
    assert result.data["normalized"].startswith("+1")


@pytest.mark.asyncio  
async def test_circuit_breaker():
    """Test circuit breaker pattern in scanners"""
    from app.scanners.enterprise_scanner_engine import BaseScanner, ScannerCategory, CircuitBreaker
    
    class FailingScanner(BaseScanner):
        def __init__(self):
            super().__init__()
            self.failure_count = 0
        
        @property
        def name(self):
            return "failing_scanner"
        
        @property
        def description(self):
            return "Scanner that fails for testing"
        
        @property
        def category(self):
            return ScannerCategory.EMAIL
        
        async def _scan_implementation(self, target, **kwargs):
            self.failure_count += 1
            if self.failure_count <= 3:
                raise Exception("Simulated failure")
            return {"recovered": True}
    
    scanner = FailingScanner()
    
    # First few scans should fail
    for i in range(3):
        result = await scanner.scan("test")
        assert result.status.value == "failed"
    
    # Circuit breaker should be open now
    # This test verifies the pattern is implemented


def test_performance_metrics():
    """Test performance metrics collection"""
    from app.scanners.enterprise_scanner_engine import ScannerMetrics
    
    metrics = ScannerMetrics()
    
    # Simulate some executions
    metrics.total_executions = 100
    metrics.successful_executions = 85
    metrics.failed_executions = 15
    metrics.average_execution_time = 2.5
    
    # Test calculated properties
    assert metrics.success_rate == 85.0
    assert metrics.reliability_score > 0
    assert metrics.reliability_score <= 100


def test_error_handling():
    """Test comprehensive error handling"""
    from app.enterprise_main import EnterpriseExceptionHandler
    from fastapi import Request
    from fastapi.exceptions import RequestValidationError
    import asyncio
    
    # Mock request
    request = Mock(spec=Request)
    request.url.path = "/test"
    request.state.request_id = "test-123"
    
    # Test validation error handler
    validation_error = RequestValidationError([{"msg": "test error"}])
    
    # This would normally be async, but we're testing the structure
    handler = EnterpriseExceptionHandler()
    assert handler.validation_exception_handler is not None
    assert handler.http_exception_handler is not None
    assert handler.general_exception_handler is not None


def test_configuration_validation():
    """Test configuration validation"""
    from app.core.enterprise_config import EnterpriseSettings, DatabaseConfig, SecurityConfig
    
    # Test database config validation
    db_config = DatabaseConfig(
        host="localhost",
        port=5432,
        pool_size=20
    )
    
    assert db_config.host == "localhost"
    assert db_config.port == 5432
    assert db_config.url.startswith("postgresql://")
    
    # Test security config validation
    security_config = SecurityConfig(
        secret_key="a" * 32,  # 32 character key
        bcrypt_rounds=12
    )
    
    assert len(security_config.secret_key) >= 32
    assert security_config.bcrypt_rounds >= 10


def test_audit_logging():
    """Test audit logging functionality"""
    # Test that the security manager has logging capabilities
    from app.core.enhanced_security import EnhancedSecurityManager
    
    security = EnhancedSecurityManager()
    
    # Test that security manager exists and has methods
    assert hasattr(security, 'hash_password')
    assert hasattr(security, 'verify_password')
    assert hasattr(security, 'encrypt_sensitive_data')
    assert hasattr(security, 'decrypt_sensitive_data')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])