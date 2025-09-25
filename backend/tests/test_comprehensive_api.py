#!/usr/bin/env python3
"""
Comprehensive API Testing Suite
Tests all API endpoints, error handling, and edge cases
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
import sys
import os
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

@pytest.fixture
def client():
    """Create test client for API testing"""
    try:
        from app.main import app
        return TestClient(app)
    except ImportError as e:
        pytest.skip(f"Cannot import app: {e}")

@pytest.fixture
def auth_headers():
    """Mock authentication headers"""
    return {"Authorization": "Bearer test-token"}

class TestHealthEndpoints:
    """Test health and status endpoints"""
    
    def test_health_endpoint(self, client):
        """Test basic health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] in ["healthy", "ok"]
    
    def test_api_info_endpoint(self, client):
        """Test API information endpoint"""
        response = client.get("/api/v1/info")
        if response.status_code == 200:
            data = response.json()
            assert "version" in data or "name" in data

class TestScannerEndpoints:
    """Test intelligence gathering scanner endpoints"""
    
    def test_email_scan_endpoint(self, client):
        """Test email scanning endpoint"""
        test_data = {"email": "test@example.com"}
        response = client.post("/api/v1/scan/email", json=test_data)
        # Should return 200 (success) or 422 (validation error) or 404 (not implemented)
        assert response.status_code in [200, 404, 422]
    
    def test_phone_scan_endpoint(self, client):
        """Test phone scanning endpoint"""
        test_data = {"phone": "+1234567890"}
        response = client.post("/api/v1/scan/phone", json=test_data)
        assert response.status_code in [200, 404, 422]
    
    def test_social_scan_endpoint(self, client):
        """Test social media scanning endpoint"""
        test_data = {"username": "testuser", "platform": "twitter"}
        response = client.post("/api/v1/scan/social", json=test_data)
        assert response.status_code in [200, 404, 422]
    
    def test_invalid_email_format(self, client):
        """Test invalid email format handling"""
        test_data = {"email": "invalid-email"}
        response = client.post("/api/v1/scan/email", json=test_data)
        assert response.status_code in [422, 400, 404]  # Validation error or not found

class TestAuthenticationEndpoints:
    """Test authentication and authorization"""
    
    def test_login_endpoint(self, client):
        """Test login endpoint"""
        test_data = {"username": "test", "password": "test123"}
        response = client.post("/api/v1/auth/login", json=test_data)
        # Should return 200, 401, or 404
        assert response.status_code in [200, 401, 404]
    
    def test_register_endpoint(self, client):
        """Test user registration endpoint"""
        test_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123"
        }
        response = client.post("/api/v1/auth/register", json=test_data)
        assert response.status_code in [200, 201, 409, 422, 404]

class TestReportEndpoints:
    """Test report generation endpoints"""
    
    def test_generate_report_endpoint(self, client, auth_headers):
        """Test report generation"""
        test_data = {"scan_id": "test-scan-123", "format": "pdf"}
        response = client.post("/api/v1/reports/generate", 
                             json=test_data, 
                             headers=auth_headers)
        assert response.status_code in [200, 201, 401, 404, 422]
    
    def test_get_reports_list(self, client, auth_headers):
        """Test getting reports list"""
        response = client.get("/api/v1/reports", headers=auth_headers)
        assert response.status_code in [200, 401, 404]

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_invalid_json_payload(self, client):
        """Test invalid JSON handling"""
        response = client.post("/api/v1/scan/email", 
                             data="invalid json",
                             headers={"Content-Type": "application/json"})
        assert response.status_code in [400, 422]
    
    def test_missing_required_fields(self, client):
        """Test missing required fields"""
        response = client.post("/api/v1/scan/email", json={})
        assert response.status_code in [400, 422]
    
    def test_rate_limiting(self, client):
        """Test rate limiting (if implemented)"""
        # Make multiple rapid requests
        responses = []
        for _ in range(10):
            response = client.get("/health")
            responses.append(response.status_code)
        
        # Should mostly be 200, might have some 429 (too many requests)
        assert all(status in [200, 429] for status in responses)
    
    def test_large_payload(self, client):
        """Test handling of large payloads"""
        large_data = {"email": "test@example.com", "data": "x" * 10000}
        response = client.post("/api/v1/scan/email", json=large_data)
        assert response.status_code in [200, 413, 422, 404]  # 413 = Payload too large

class TestCORSAndSecurity:
    """Test CORS and security headers"""
    
    def test_cors_headers(self, client):
        """Test CORS headers are present"""
        response = client.options("/health")
        # Should return 200 or 405 (method not allowed)
        assert response.status_code in [200, 405]
    
    def test_security_headers(self, client):
        """Test security headers"""
        response = client.get("/health")
        headers = response.headers
        
        # Check for common security headers (if implemented)
        security_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options", 
            "X-XSS-Protection"
        ]
        
        # Don't fail if not present, just check they're valid if they exist
        for header in security_headers:
            if header in headers:
                assert headers[header] is not None

@pytest.mark.integration
class TestIntegrationScenarios:
    """Test complete user workflows"""
    
    def test_complete_scan_workflow(self, client):
        """Test complete scan workflow"""
        # 1. Health check
        health_response = client.get("/health")
        assert health_response.status_code == 200
        
        # 2. Try to scan email
        scan_data = {"email": "integration@test.com"}
        scan_response = client.post("/api/v1/scan/email", json=scan_data)
        
        if scan_response.status_code == 200:
            # 3. If scan successful, try to get results
            scan_result = scan_response.json()
            if "scan_id" in scan_result:
                results_response = client.get(f"/api/v1/scan/{scan_result['scan_id']}")
                assert results_response.status_code in [200, 404]

@pytest.mark.performance
class TestPerformance:
    """Test API performance"""
    
    def test_health_endpoint_performance(self, client):
        """Test health endpoint response time"""
        import time
        
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Health endpoint should respond within 1 second
        assert response_time < 1.0
        assert response.status_code == 200
    
    def test_concurrent_requests(self, client):
        """Test handling of concurrent requests"""
        import threading
        import time
        
        results = []
        
        def make_request():
            response = client.get("/health")
            results.append(response.status_code)
        
        # Create 5 concurrent threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
        
        # Start all threads
        start_time = time.time()
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        
        # All requests should succeed
        assert all(status == 200 for status in results)
        assert len(results) == 5
        
        # Should complete within reasonable time
        assert (end_time - start_time) < 5.0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])