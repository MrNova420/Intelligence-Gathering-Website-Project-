"""
Comprehensive test suite for scanner modules.
Tests all email, phone, and social media scanners with edge cases.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.scanners.email_scanners import (
    EmailValidatorScanner, EmailReputationScanner, 
    EmailBreachScanner, SocialMediaEmailScanner
)
from app.scanners.phone_scanners import (
    PhoneValidatorScanner, PhoneLocationScanner,
    PhoneSpamScanner, PhoneCarrierScanner
)
from app.scanners.social_scanners import (
    TwitterScanner, LinkedInScanner, InstagramScanner,
    FacebookScanner, GitHubScanner
)


class MockQuery:
    """Mock query object for testing"""
    def __init__(self, query_type: str, query_value: str):
        self.query_type = query_type
        self.query_value = query_value


@pytest.fixture
def mock_query_email():
    return MockQuery("email", "test@example.com")


@pytest.fixture  
def mock_query_phone():
    return MockQuery("phone", "+1234567890")


@pytest.fixture
def mock_query_username():
    return MockQuery("username", "testuser")


class TestEmailScanners:
    """Test suite for email scanner modules"""
    
    @pytest.mark.asyncio
    async def test_email_validator_scanner_valid_email(self, mock_query_email):
        """Test email validator with valid email"""
        scanner = EmailValidatorScanner()
        result = await scanner.scan(mock_query_email)
        
        assert result is not None
        assert "email" in result
        assert "valid" in result
        assert "syntax" in result
        assert "domain_check" in result
        assert "mx_check" in result
        assert "confidence" in result
        assert isinstance(result["confidence"], float)
        assert 0 <= result["confidence"] <= 1
    
    @pytest.mark.asyncio
    async def test_email_validator_scanner_invalid_email(self):
        """Test email validator with invalid email"""
        scanner = EmailValidatorScanner()
        invalid_query = MockQuery("email", "invalid-email")
        result = await scanner.scan(invalid_query)
        
        assert result is not None
        assert result["valid"] is False
        assert "reason" in result
        assert result["confidence"] < 0.5
    
    @pytest.mark.asyncio
    async def test_email_reputation_scanner(self, mock_query_email):
        """Test email reputation scanner"""
        scanner = EmailReputationScanner()
        result = await scanner.scan(mock_query_email)
        
        assert result is not None
        assert "email" in result
        assert "reputation_score" in result
        assert "disposable_check" in result
        assert "role_account_check" in result
        assert "structure_analysis" in result
        assert "risk_level" in result
        assert isinstance(result["reputation_score"], float)
        assert 0 <= result["reputation_score"] <= 1
    
    @pytest.mark.asyncio
    async def test_email_breach_scanner(self, mock_query_email):
        """Test email breach scanner"""
        scanner = EmailBreachScanner()
        result = await scanner.scan(mock_query_email)
        
        assert result is not None
        assert "email" in result
        assert "breach_analysis" in result
        assert "paste_analysis" in result
        assert "risk_score" in result
        assert "risk_level" in result
        assert "recommendations" in result
        assert isinstance(result["recommendations"], list)
    
    @pytest.mark.asyncio
    async def test_social_media_email_scanner(self, mock_query_email):
        """Test social media email scanner"""
        scanner = SocialMediaEmailScanner()
        result = await scanner.scan(mock_query_email)
        
        assert result is not None
        assert "email" in result
        assert "platform_analysis" in result
        assert "profile_predictions" in result
        assert "top_likely_platforms" in result
        assert "search_suggestions" in result
    
    @pytest.mark.asyncio
    async def test_email_scanner_edge_cases(self):
        """Test email scanners with edge cases"""
        scanners = [
            EmailValidatorScanner(),
            EmailReputationScanner(),
            EmailBreachScanner(),
            SocialMediaEmailScanner()
        ]
        
        edge_cases = [
            MockQuery("email", ""),  # Empty email
            MockQuery("email", " "),  # Whitespace only
            MockQuery("email", "a@b.c"),  # Very short email
            MockQuery("email", "very.long.email.address.with.many.dots@very.long.domain.name.example.com"),  # Long email
            MockQuery("email", "test+tag@example.com"),  # Email with plus tag
            MockQuery("email", "test.email+tag@gmail.com"),  # Gmail with dots and tag
        ]
        
        for scanner in scanners:
            for edge_case in edge_cases:
                try:
                    result = await scanner.scan(edge_case)
                    assert result is not None
                    assert "email" in result or "error" in result
                except Exception as e:
                    pytest.fail(f"{scanner.__class__.__name__} failed with edge case '{edge_case.query_value}': {str(e)}")


class TestPhoneScanners:
    """Test suite for phone scanner modules"""
    
    @pytest.mark.asyncio
    async def test_phone_validator_scanner_valid_phone(self, mock_query_phone):
        """Test phone validator with valid phone"""
        scanner = PhoneValidatorScanner()
        result = await scanner.scan(mock_query_phone)
        
        assert result is not None
        assert "phone" in result
        assert "cleaned_phone" in result
        assert "validation" in result
        assert "pattern_analysis" in result
        assert "confidence" in result
        assert isinstance(result["confidence"], float)
    
    @pytest.mark.asyncio
    async def test_phone_location_scanner(self, mock_query_phone):
        """Test phone location scanner"""
        scanner = PhoneLocationScanner()
        result = await scanner.scan(mock_query_phone)
        
        assert result is not None
        assert "phone" in result
        assert "geographic_info" in result
        assert "pattern_analysis" in result
        assert "confidence" in result
    
    @pytest.mark.asyncio
    async def test_phone_spam_scanner(self, mock_query_phone):
        """Test phone spam scanner"""
        scanner = PhoneSpamScanner()
        result = await scanner.scan(mock_query_phone)
        
        assert result is not None
        assert "phone" in result
        assert "pattern_analysis" in result
        assert "blacklist_results" in result
        assert "reputation_score" in result
        assert "overall_risk" in result
        assert "recommendations" in result
        assert isinstance(result["recommendations"], list)
    
    @pytest.mark.asyncio
    async def test_phone_carrier_scanner(self, mock_query_phone):
        """Test phone carrier scanner"""
        scanner = PhoneCarrierScanner()
        result = await scanner.scan(mock_query_phone)
        
        assert result is not None
        assert "phone" in result
        assert "carrier_info" in result
        assert "portability_info" in result
        assert "network_analysis" in result
        assert "confidence" in result
    
    @pytest.mark.asyncio
    async def test_phone_scanner_edge_cases(self):
        """Test phone scanners with edge cases"""
        scanners = [
            PhoneValidatorScanner(),
            PhoneLocationScanner(),
            PhoneSpamScanner(),
            PhoneCarrierScanner()
        ]
        
        edge_cases = [
            MockQuery("phone", ""),  # Empty phone
            MockQuery("phone", "123"),  # Too short
            MockQuery("phone", "1234567890"),  # No country code
            MockQuery("phone", "+1-234-567-8900"),  # Formatted with dashes
            MockQuery("phone", "(234) 567-8900"),  # Formatted with parentheses
            MockQuery("phone", "+1 234 567 8900"),  # Formatted with spaces
            MockQuery("phone", "01234567890123456789"),  # Too long
            MockQuery("phone", "+999999999999999"),  # Invalid country code
        ]
        
        for scanner in scanners:
            for edge_case in edge_cases:
                try:
                    result = await scanner.scan(edge_case)
                    assert result is not None
                    # Should handle edge cases gracefully
                except Exception as e:
                    pytest.fail(f"{scanner.__class__.__name__} failed with edge case '{edge_case.query_value}': {str(e)}")


class TestSocialScanners:
    """Test suite for social media scanner modules"""
    
    @pytest.mark.asyncio
    async def test_twitter_scanner_username(self, mock_query_username):
        """Test Twitter scanner with username"""
        scanner = TwitterScanner()
        result = await scanner.scan(mock_query_username)
        
        assert result is not None
        assert "platform" in result
        assert result["platform"] == "twitter"
        assert "query_type" in result
        assert "search_results" in result
        assert "confidence" in result
    
    @pytest.mark.asyncio
    async def test_linkedin_scanner_email(self, mock_query_email):
        """Test LinkedIn scanner with email"""
        scanner = LinkedInScanner()
        result = await scanner.scan(mock_query_email)
        
        assert result is not None
        assert "platform" in result
        assert result["platform"] == "linkedin"
        assert "search_results" in result
        assert "confidence" in result
    
    @pytest.mark.asyncio
    async def test_instagram_scanner(self, mock_query_username):
        """Test Instagram scanner"""
        scanner = InstagramScanner()
        result = await scanner.scan(mock_query_username)
        
        assert result is not None
        assert "platform" in result
        assert result["platform"] == "instagram"
        assert "search_results" in result
    
    @pytest.mark.asyncio
    async def test_facebook_scanner(self, mock_query_email):
        """Test Facebook scanner"""
        scanner = FacebookScanner()
        result = await scanner.scan(mock_query_email)
        
        assert result is not None
        assert "platform" in result
        assert result["platform"] == "facebook"
        assert "privacy_note" in result  # Facebook has privacy restrictions
    
    @pytest.mark.asyncio
    async def test_github_scanner(self, mock_query_username):
        """Test GitHub scanner"""
        scanner = GitHubScanner()
        result = await scanner.scan(mock_query_username)
        
        assert result is not None
        assert "platform" in result
        assert result["platform"] == "github"
        assert "search_results" in result
    
    @pytest.mark.asyncio
    async def test_social_scanner_name_query(self):
        """Test social scanners with name query"""
        name_query = MockQuery("name", "John Doe")
        scanners = [TwitterScanner(), LinkedInScanner(), GitHubScanner()]
        
        for scanner in scanners:
            if scanner.can_handle(name_query):
                result = await scanner.scan(name_query)
                assert result is not None
                assert "platform" in result
    
    @pytest.mark.asyncio
    async def test_social_scanner_edge_cases(self):
        """Test social scanners with edge cases"""
        scanners = [
            TwitterScanner(),
            LinkedInScanner(), 
            InstagramScanner(),
            FacebookScanner(),
            GitHubScanner()
        ]
        
        edge_cases = [
            MockQuery("username", ""),  # Empty username
            MockQuery("username", "a"),  # Very short username
            MockQuery("username", "a" * 50),  # Very long username
            MockQuery("username", "user-with-hyphens"),  # Hyphens
            MockQuery("username", "user_with_underscores"),  # Underscores
            MockQuery("username", "user.with.dots"),  # Dots
            MockQuery("username", "123numeric"),  # Starting with numbers
            MockQuery("username", "admin"),  # Reserved username
        ]
        
        for scanner in scanners:
            for edge_case in edge_cases:
                if scanner.can_handle(edge_case):
                    try:
                        result = await scanner.scan(edge_case)
                        assert result is not None
                    except Exception as e:
                        pytest.fail(f"{scanner.__class__.__name__} failed with edge case '{edge_case.query_value}': {str(e)}")


class TestScannerPerformance:
    """Test scanner performance and rate limiting"""
    
    @pytest.mark.asyncio
    async def test_scanner_rate_limiting(self):
        """Test that scanners respect rate limits"""
        scanner = EmailValidatorScanner()
        query = MockQuery("email", "test@example.com")
        
        # Measure time for multiple rapid requests
        start_time = asyncio.get_event_loop().time()
        
        tasks = []
        for _ in range(5):  # Make 5 rapid requests
            tasks.append(scanner.scan(query))
        
        results = await asyncio.gather(*tasks)
        end_time = asyncio.get_event_loop().time()
        
        # Should take some time due to rate limiting
        total_time = end_time - start_time
        assert total_time > 0.1  # Should take at least 100ms
        
        # All requests should succeed
        assert len(results) == 5
        for result in results:
            assert result is not None
    
    @pytest.mark.asyncio
    async def test_scanner_timeout_handling(self):
        """Test scanner timeout handling"""
        scanner = EmailValidatorScanner()
        
        # Mock a slow operation
        original_scan = scanner._validate_email_syntax
        
        def slow_validation(email):
            import time
            time.sleep(0.1)  # Simulate slow operation
            return original_scan(email)
        
        scanner._validate_email_syntax = slow_validation
        
        query = MockQuery("email", "test@example.com")
        
        # Should complete despite slow operation
        result = await scanner.scan(query)
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_concurrent_scanner_execution(self):
        """Test concurrent execution of multiple scanners"""
        scanners = [
            EmailValidatorScanner(),
            EmailReputationScanner(),
            PhoneValidatorScanner(),
            TwitterScanner()
        ]
        
        queries = [
            MockQuery("email", "test@example.com"),
            MockQuery("email", "another@example.com"),
            MockQuery("phone", "+1234567890"),
            MockQuery("username", "testuser")
        ]
        
        # Execute scanners concurrently
        tasks = []
        for scanner, query in zip(scanners, queries):
            if scanner.can_handle(query):
                tasks.append(scanner.scan(query))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Check that all completed
        assert len(results) == len(tasks)
        
        # Check that no exceptions occurred
        for result in results:
            assert not isinstance(result, Exception), f"Scanner failed with exception: {result}"
            assert result is not None


class TestScannerIntegration:
    """Integration tests for scanner modules"""
    
    @pytest.mark.asyncio
    async def test_scanner_registry_integration(self):
        """Test scanner registry integration"""
        # This would test integration with the scanner registry
        # For now, we'll test that scanners can be instantiated
        
        email_scanners = [
            EmailValidatorScanner(),
            EmailReputationScanner(),
            EmailBreachScanner(),
            SocialMediaEmailScanner()
        ]
        
        phone_scanners = [
            PhoneValidatorScanner(),
            PhoneLocationScanner(),
            PhoneSpamScanner(),
            PhoneCarrierScanner()
        ]
        
        social_scanners = [
            TwitterScanner(),
            LinkedInScanner(),
            InstagramScanner(),
            FacebookScanner(),
            GitHubScanner()
        ]
        
        all_scanners = email_scanners + phone_scanners + social_scanners
        
        # Test that all scanners have required attributes
        for scanner in all_scanners:
            assert hasattr(scanner, 'name')
            assert hasattr(scanner, 'scanner_type')
            assert hasattr(scanner, 'description')
            assert hasattr(scanner, 'can_handle')
            assert hasattr(scanner, 'scan')
            assert scanner.name is not None
            assert len(scanner.name) > 0
    
    @pytest.mark.asyncio
    async def test_end_to_end_scan_workflow(self):
        """Test complete scan workflow"""
        # Test a realistic workflow
        email_query = MockQuery("email", "john.doe@company.com")
        
        # Use multiple scanners
        scanners = [
            EmailValidatorScanner(),
            EmailReputationScanner(),
            SocialMediaEmailScanner()
        ]
        
        all_results = []
        
        for scanner in scanners:
            if scanner.can_handle(email_query):
                result = await scanner.scan(email_query)
                all_results.append({
                    "scanner": scanner.name,
                    "result": result
                })
        
        # Verify results
        assert len(all_results) > 0
        
        for scan_result in all_results:
            assert "scanner" in scan_result
            assert "result" in scan_result
            assert scan_result["result"] is not None
            
            # Each result should have confidence score
            result = scan_result["result"]
            assert "confidence" in result
            assert isinstance(result["confidence"], (int, float))
            assert 0 <= result["confidence"] <= 1


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])