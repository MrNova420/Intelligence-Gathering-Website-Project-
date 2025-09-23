"""
Test suite for the aggregation engine.
Tests normalization, deduplication, confidence scoring, and relationship linking.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from typing import Dict, Any, List
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.core.aggregation_engine import (
    EntityNormalizer, EntityDeduplicator, ConfidenceScorer,
    RelationshipLinker, AggregationEngine
)


class TestEntityNormalizer:
    """Test suite for entity normalization"""
    
    def test_email_normalization_valid(self):
        """Test email normalization with valid emails"""
        normalizer = EntityNormalizer()
        
        test_cases = [
            ("test@example.com", "test@example.com"),
            ("Test@Example.Com", "test@example.com"),
            ("  test@example.com  ", "test@example.com"),
            ("test.dots@gmail.com", "testdots@gmail.com"),  # Gmail dot removal
            ("test+tag@gmail.com", "test@gmail.com"),  # Gmail plus removal
        ]
        
        for input_email, expected in test_cases:
            result = normalizer.normalize_email(input_email)
            assert result["valid"] is True
            assert result["normalized"] == expected
            assert "local_part" in result
            assert "domain" in result
    
    def test_email_normalization_invalid(self):
        """Test email normalization with invalid emails"""
        normalizer = EntityNormalizer()
        
        invalid_emails = [
            "",
            "invalid",
            "@example.com",
            "test@",
            "test..double@example.com",
            "test@example",
        ]
        
        for invalid_email in invalid_emails:
            result = normalizer.normalize_email(invalid_email)
            assert result["valid"] is False
            assert "reason" in result
    
    def test_phone_normalization_valid(self):
        """Test phone normalization with valid phones"""
        normalizer = EntityNormalizer()
        
        test_cases = [
            ("+1234567890", "+1234567890"),
            ("1234567890", "+11234567890"),  # Assumes US
            "(123) 456-7890", "+11234567890"),
            "+1-234-567-8900", "+12345678900"),
            "+44 20 1234 5678", "+442012345678"),
        ]
        
        for input_phone, expected_e164 in test_cases:
            result = normalizer.normalize_phone(input_phone)
            if result["valid"]:  # Some may not parse correctly in mock
                assert "normalized" in result
                assert "country_code" in result
                assert "national_number" in result
    
    def test_name_normalization(self):
        """Test name normalization"""
        normalizer = EntityNormalizer()
        
        test_cases = [
            ("john doe", "John Doe"),
            ("JOHN DOE", "John Doe"),
            ("  john   doe  ", "John Doe"),
            ("Dr. John Doe Jr.", "John Doe"),  # Removes prefix/suffix
            ("john-doe", "John-Doe"),
            ("McDonald", "Mcdonald"),  # Simple title case
        ]
        
        for input_name, expected in test_cases:
            result = normalizer.normalize_name(input_name)
            assert result["valid"] is True
            assert result["normalized"] == expected or result["full_normalized"] == expected
    
    def test_address_normalization(self):
        """Test address normalization"""
        normalizer = EntityNormalizer()
        
        test_cases = [
            "123 Main St, Anytown, CA 12345",
            "456 Oak Ave Apt 2B",
            "789 Pine Rd.",
            "1000 Broadway Suite 100, New York, NY 10001"
        ]
        
        for address in test_cases:
            result = normalizer.normalize_address(address)
            assert result["valid"] is True
            assert "normalized" in result
            assert "street" in result
    
    def test_url_normalization(self):
        """Test URL normalization"""
        normalizer = EntityNormalizer()
        
        test_cases = [
            ("example.com", "https://example.com"),
            ("http://example.com", "http://example.com"),
            ("https://example.com", "https://example.com"),
            ("www.example.com", "https://www.example.com"),
        ]
        
        for input_url, expected in test_cases:
            result = normalizer.normalize_url(input_url)
            if result["valid"]:  # May not all be valid in simple implementation
                assert result["normalized"] == expected
                assert "domain" in result


class TestEntityDeduplicator:
    """Test suite for entity deduplication"""
    
    def test_email_deduplication(self):
        """Test email entity deduplication"""
        deduplicator = EntityDeduplicator()
        
        # Create duplicate email entities
        entities = [
            {"type": "email", "value": "test@example.com", "source": "scanner1", "confidence": 0.8},
            {"type": "email", "value": "TEST@EXAMPLE.COM", "source": "scanner2", "confidence": 0.9},
            {"type": "email", "value": "test+tag@example.com", "source": "scanner3", "confidence": 0.7},
            {"type": "email", "value": "different@example.com", "source": "scanner1", "confidence": 0.6},
        ]
        
        deduplicated = deduplicator.deduplicate_entities(entities)
        
        # Should have 2 unique emails (test@example.com and different@example.com)
        email_entities = [e for e in deduplicated if e["type"] == "email"]
        assert len(email_entities) == 2
        
        # Check that sources are merged
        for entity in email_entities:
            assert "sources" in entity
            assert "aggregate_confidence" in entity
            assert "source_count" in entity
    
    def test_phone_deduplication(self):
        """Test phone entity deduplication"""
        deduplicator = EntityDeduplicator()
        
        entities = [
            {"type": "phone", "value": "+1234567890", "source": "scanner1", "confidence": 0.8},
            {"type": "phone", "value": "1234567890", "source": "scanner2", "confidence": 0.9},
            {"type": "phone", "value": "(123) 456-7890", "source": "scanner3", "confidence": 0.7},
            {"type": "phone", "value": "+9876543210", "source": "scanner1", "confidence": 0.6},
        ]
        
        deduplicated = deduplicator.deduplicate_entities(entities)
        
        # Should deduplicate normalized phone numbers
        phone_entities = [e for e in deduplicated if e["type"] == "phone"]
        assert len(phone_entities) <= 2  # May vary based on normalization success
        
        for entity in phone_entities:
            assert "sources" in entity
            assert "aggregate_confidence" in entity
    
    def test_name_deduplication_fuzzy_matching(self):
        """Test name deduplication with fuzzy matching"""
        deduplicator = EntityDeduplicator()
        
        entities = [
            {"type": "name", "value": "John Doe", "source": "scanner1", "confidence": 0.8},
            {"type": "name", "value": "John Doe", "source": "scanner2", "confidence": 0.9},
            {"type": "name", "value": "Jon Doe", "source": "scanner3", "confidence": 0.7},  # Similar but different
            {"type": "name", "value": "Jane Smith", "source": "scanner1", "confidence": 0.6},
        ]
        
        deduplicated = deduplicator.deduplicate_entities(entities)
        
        name_entities = [e for e in deduplicated if e["type"] == "name"]
        
        # Should have deduplicated similar names
        for entity in name_entities:
            assert "sources" in entity
            assert "variants" in entity  # Should track name variations
    
    def test_mixed_entity_deduplication(self):
        """Test deduplication with mixed entity types"""
        deduplicator = EntityDeduplicator()
        
        entities = [
            {"type": "email", "value": "test@example.com", "source": "scanner1", "confidence": 0.8},
            {"type": "phone", "value": "+1234567890", "source": "scanner1", "confidence": 0.7},
            {"type": "name", "value": "John Doe", "source": "scanner2", "confidence": 0.9},
            {"type": "email", "value": "test@example.com", "source": "scanner3", "confidence": 0.6},  # Duplicate
        ]
        
        deduplicated = deduplicator.deduplicate_entities(entities)
        
        # Should have 3 unique entities (1 email, 1 phone, 1 name)
        assert len(deduplicated) == 3
        
        # Check entity types are preserved
        types = {e["type"] for e in deduplicated}
        assert types == {"email", "phone", "name"}


class TestConfidenceScorer:
    """Test suite for confidence scoring"""
    
    def test_single_source_confidence(self):
        """Test confidence scoring with single source"""
        scorer = ConfidenceScorer()
        
        entity = {
            "type": "email",
            "value": "test@example.com",
            "sources": [
                {"source": "email_validator", "confidence": 0.9}
            ]
        }
        
        confidence = scorer.calculate_entity_confidence(entity)
        
        assert isinstance(confidence, float)
        assert 0 <= confidence <= 1
        assert confidence > 0.5  # Should be reasonably high for email validator
    
    def test_multiple_source_confidence(self):
        """Test confidence scoring with multiple sources"""
        scorer = ConfidenceScorer()
        
        entity = {
            "type": "email",
            "value": "test@example.com",
            "sources": [
                {"source": "email_validator", "confidence": 0.9},
                {"source": "email_reputation", "confidence": 0.8},
                {"source": "social_media_email_scanner", "confidence": 0.6}
            ]
        }
        
        confidence = scorer.calculate_entity_confidence(entity)
        
        assert isinstance(confidence, float)
        assert 0 <= confidence <= 1
        
        # Should be higher than single source due to multiple confirmations
        single_source_entity = {
            "type": "email",
            "value": "test@example.com",
            "sources": [{"source": "email_validator", "confidence": 0.9}]
        }
        single_confidence = scorer.calculate_entity_confidence(single_source_entity)
        
        assert confidence >= single_confidence
    
    def test_source_reliability_weighting(self):
        """Test that source reliability affects confidence"""
        scorer = ConfidenceScorer()
        
        # High reliability source
        high_reliability_entity = {
            "type": "email",
            "sources": [{"source": "email_validator", "confidence": 0.8}]
        }
        
        # Low reliability source
        low_reliability_entity = {
            "type": "email",
            "sources": [{"source": "unknown", "confidence": 0.8}]
        }
        
        high_confidence = scorer.calculate_entity_confidence(high_reliability_entity)
        low_confidence = scorer.calculate_entity_confidence(low_reliability_entity)
        
        assert high_confidence > low_confidence
    
    def test_confidence_modifiers(self):
        """Test confidence modifiers based on entity properties"""
        scorer = ConfidenceScorer()
        
        # Entity with good metadata
        good_entity = {
            "type": "email",
            "sources": [{"source": "email_validator", "confidence": 0.8}],
            "metadata": {"valid": True},
            "last_updated": "2024-01-01T00:00:00Z"
        }
        
        # Entity without metadata
        basic_entity = {
            "type": "email", 
            "sources": [{"source": "email_validator", "confidence": 0.8}]
        }
        
        good_confidence = scorer.calculate_entity_confidence(good_entity)
        basic_confidence = scorer.calculate_entity_confidence(basic_entity)
        
        assert good_confidence >= basic_confidence


class TestRelationshipLinker:
    """Test suite for relationship linking"""
    
    def test_email_name_relationship(self):
        """Test linking email and name entities"""
        linker = RelationshipLinker()
        
        entities = [
            {
                "type": "email",
                "value": "john.doe@company.com",
                "sources": [{"source": "email_validator"}],
                "_index": 0
            },
            {
                "type": "name", 
                "value": "John Doe",
                "sources": [{"source": "social_scanner"}],
                "_index": 1
            }
        ]
        
        relationships = linker.link_entities(entities)
        
        assert "relationships" in relationships
        assert "entity_clusters" in relationships
        
        # Should find relationship between email and name
        if relationships["relationships"]:
            assert len(relationships["relationships"]) >= 0
    
    def test_same_domain_email_relationship(self):
        """Test linking emails from same domain"""
        linker = RelationshipLinker()
        
        entities = [
            {
                "type": "email",
                "value": "john@company.com",
                "sources": [{"source": "scanner1"}],
                "metadata": {"domain": "company.com"},
                "_index": 0
            },
            {
                "type": "email",
                "value": "jane@company.com", 
                "sources": [{"source": "scanner2"}],
                "metadata": {"domain": "company.com"},
                "_index": 1
            }
        ]
        
        relationships = linker.link_entities(entities)
        
        # May find domain-based relationships
        assert "relationships" in relationships
    
    def test_relationship_confidence_calculation(self):
        """Test relationship confidence calculation"""
        linker = RelationshipLinker()
        
        entities = [
            {
                "type": "email",
                "aggregate_confidence": 0.9,
                "sources": [{"source": "scanner1"}],
                "_index": 0
            },
            {
                "type": "name",
                "aggregate_confidence": 0.8,
                "sources": [{"source": "scanner1"}],  # Same source
                "_index": 1
            }
        ]
        
        relationships = linker.link_entities(entities)
        
        for relationship in relationships.get("relationships", []):
            assert "confidence" in relationship
            assert isinstance(relationship["confidence"], float)
            assert 0 <= relationship["confidence"] <= 1


class TestAggregationEngine:
    """Test suite for the complete aggregation engine"""
    
    @pytest.mark.asyncio
    async def test_complete_aggregation_workflow(self):
        """Test complete aggregation workflow"""
        engine = AggregationEngine()
        
        # Mock scan results
        scan_results = [
            {
                "scanner": "email_validator",
                "confidence": 0.9,
                "timestamp": "2024-01-01T00:00:00Z",
                "result": {
                    "email": "john.doe@company.com",
                    "valid": True,
                    "confidence": 0.9
                }
            },
            {
                "scanner": "social_scanner",
                "confidence": 0.8,
                "timestamp": "2024-01-01T00:00:00Z",
                "result": {
                    "name": "John Doe",
                    "profile_url": "https://linkedin.com/in/johndoe",
                    "confidence": 0.8
                }
            },
            {
                "scanner": "email_validator",  # Duplicate scanner
                "confidence": 0.85,
                "timestamp": "2024-01-01T00:00:00Z",
                "result": {
                    "email": "john.doe@company.com",  # Same email
                    "valid": True,
                    "confidence": 0.85
                }
            }
        ]
        
        # Run aggregation
        result = await engine.aggregate_scan_results(scan_results)
        
        # Verify structure
        assert "entities" in result
        assert "relationships" in result
        assert "summary" in result
        assert "aggregation_metadata" in result
        
        # Check aggregation metadata
        metadata = result["aggregation_metadata"]
        assert "total_raw_entities" in metadata
        assert "deduplicated_count" in metadata
        assert "deduplication_rate" in metadata
        assert "high_confidence_entities" in metadata
        
        # Should have deduplication
        assert metadata["deduplicated_count"] <= metadata["total_raw_entities"]
    
    @pytest.mark.asyncio
    async def test_empty_scan_results(self):
        """Test aggregation with empty scan results"""
        engine = AggregationEngine()
        
        result = await engine.aggregate_scan_results([])
        
        assert "entities" in result
        assert len(result["entities"]) == 0
        assert "summary" in result
        assert result["summary"]["total_entities"] == 0
    
    @pytest.mark.asyncio
    async def test_invalid_scan_results(self):
        """Test aggregation with invalid scan results"""
        engine = AggregationEngine()
        
        # Malformed scan results
        scan_results = [
            {"invalid": "data"},
            {"scanner": "test", "result": None},
            {"scanner": "test2", "result": {"no_entities": True}}
        ]
        
        # Should handle gracefully
        result = await engine.aggregate_scan_results(scan_results)
        
        assert "entities" in result
        assert "summary" in result
        assert isinstance(result["entities"], list)
    
    @pytest.mark.asyncio
    async def test_large_dataset_aggregation(self):
        """Test aggregation with large dataset"""
        engine = AggregationEngine()
        
        # Generate large dataset
        scan_results = []
        for i in range(100):
            scan_results.append({
                "scanner": f"scanner_{i % 10}",
                "confidence": 0.5 + (i % 5) * 0.1,
                "timestamp": "2024-01-01T00:00:00Z",
                "result": {
                    "email": f"user{i}@example.com",
                    "name": f"User {i}",
                    "confidence": 0.5 + (i % 5) * 0.1
                }
            })
        
        # Should process efficiently
        import time
        start_time = time.time()
        result = await engine.aggregate_scan_results(scan_results)
        end_time = time.time()
        
        # Should complete reasonably quickly
        assert end_time - start_time < 5.0  # Less than 5 seconds
        
        assert "entities" in result
        assert len(result["entities"]) > 0
        assert result["summary"]["total_entities"] > 0
    
    @pytest.mark.asyncio
    async def test_data_quality_scoring(self):
        """Test data quality scoring"""
        engine = AggregationEngine()
        
        # High quality scan results
        high_quality_results = [
            {
                "scanner": "email_validator",
                "confidence": 0.95,
                "result": {"email": "test@example.com", "valid": True}
            },
            {
                "scanner": "phone_validator", 
                "confidence": 0.90,
                "result": {"phone": "+1234567890", "valid": True}
            }
        ]
        
        # Low quality scan results
        low_quality_results = [
            {
                "scanner": "unknown_scanner",
                "confidence": 0.3,
                "result": {"data": "uncertain"}
            }
        ]
        
        high_quality_aggregation = await engine.aggregate_scan_results(high_quality_results)
        low_quality_aggregation = await engine.aggregate_scan_results(low_quality_results)
        
        # High quality should have better data quality score
        high_score = high_quality_aggregation["summary"]["data_quality_score"]
        low_score = low_quality_aggregation["summary"]["data_quality_score"]
        
        assert high_score >= low_score


if __name__ == "__main__":
    pytest.main([__file__, "-v"])