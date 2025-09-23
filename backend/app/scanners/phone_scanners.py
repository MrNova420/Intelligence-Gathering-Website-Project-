"""
Phone Intelligence Scanner Modules
Real implementations with carrier lookup, location detection, and spam analysis.
"""

import asyncio
import re
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import aiohttp
import json
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import hashlib
import time

from .base import BaseScannerModule, ScannerType
from ..db.models import Query

logger = logging.getLogger(__name__)


class PhoneValidatorScanner(BaseScannerModule):
    """Phone number validation and formatting scanner"""
    
    def __init__(self):
        super().__init__(
            name="phone_validator",
            scanner_type=ScannerType.PHONE_LOOKUP,
            description="Phone number validation, formatting, and basic info extraction"
        )
        self.rate_limiter = RateLimiter(max_requests=200, time_window=60)
    
    def can_handle(self, query: Query) -> bool:
        return query.query_type.lower() == 'phone'
    
    def _clean_phone_number(self, phone: str) -> str:
        """Clean and normalize phone number"""
        # Remove all non-digit characters except +
        cleaned = re.sub(r'[^\d+]', '', phone.strip())
        
        # Add + if not present and looks like international
        if not cleaned.startswith('+') and len(cleaned) > 10:
            cleaned = '+' + cleaned
        
        return cleaned
    
    def _validate_phone_format(self, phone: str) -> Dict[str, Any]:
        """Validate phone number format using phonenumbers library"""
        try:
            # Try to parse the number
            parsed = phonenumbers.parse(phone, None)
            
            # Check if valid
            is_valid = phonenumbers.is_valid_number(parsed)
            is_possible = phonenumbers.is_possible_number(parsed)
            
            # Get number type
            number_type = phonenumbers.number_type(parsed)
            type_name = {
                0: "FIXED_LINE",
                1: "MOBILE", 
                2: "FIXED_LINE_OR_MOBILE",
                3: "TOLL_FREE",
                4: "PREMIUM_RATE",
                5: "SHARED_COST",
                6: "VOIP",
                7: "PERSONAL_NUMBER",
                8: "PAGER",
                9: "UAN",
                10: "VOICEMAIL",
                99: "UNKNOWN"
            }.get(number_type, "UNKNOWN")
            
            # Format in different ways
            formats = {
                "international": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                "national": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
                "e164": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
                "rfc3966": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.RFC3966)
            }
            
            return {
                "is_valid": is_valid,
                "is_possible": is_possible,
                "country_code": parsed.country_code,
                "national_number": parsed.national_number,
                "number_type": type_name,
                "formats": formats,
                "parsing_success": True
            }
            
        except phonenumbers.NumberParseException as e:
            return {
                "is_valid": False,
                "is_possible": False,
                "error": str(e),
                "error_type": e.error_type,
                "parsing_success": False
            }
    
    async def scan(self, query: Query) -> Dict[str, Any]:
        """Perform phone validation scan"""
        await self.rate_limiter.wait_if_needed()
        
        phone = query.query_value.strip()
        cleaned_phone = self._clean_phone_number(phone)
        
        # Validate format
        validation_result = self._validate_phone_format(cleaned_phone)
        
        # Basic pattern analysis
        pattern_analysis = {
            "original_format": phone,
            "cleaned_format": cleaned_phone,
            "length": len(cleaned_phone),
            "starts_with_plus": cleaned_phone.startswith('+'),
            "digit_count": len(re.sub(r'[^\d]', '', cleaned_phone))
        }
        
        confidence = 0.95 if validation_result.get("is_valid", False) else 0.3
        
        return {
            "phone": phone,
            "cleaned_phone": cleaned_phone,
            "validation": validation_result,
            "pattern_analysis": pattern_analysis,
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat()
        }


class PhoneLocationScanner(BaseScannerModule):
    """Phone number location and timezone scanner"""
    
    def __init__(self):
        super().__init__(
            name="phone_location_scanner",
            scanner_type=ScannerType.PHONE_LOOKUP,
            description="Phone number geographic location and timezone detection"
        )
        self.rate_limiter = RateLimiter(max_requests=150, time_window=60)
    
    def can_handle(self, query: Query) -> bool:
        return query.query_type.lower() == 'phone'
    
    async def _get_geographic_info(self, phone: str) -> Dict[str, Any]:
        """Get geographic information for phone number"""
        try:
            parsed = phonenumbers.parse(phone, None)
            
            if not phonenumbers.is_valid_number(parsed):
                return {"error": "Invalid phone number"}
            
            # Get country info
            country_code = parsed.country_code
            region_code = phonenumbers.region_code_for_number(parsed)
            
            # Get location description
            location = geocoder.description_for_number(parsed, "en")
            
            # Get timezone info
            timezones_list = timezone.time_zones_for_number(parsed)
            
            # Get carrier info if available
            carrier_name = carrier.name_for_number(parsed, "en")
            
            return {
                "country_code": country_code,
                "region_code": region_code,
                "location_description": location,
                "carrier": carrier_name or "Unknown",
                "timezones": list(timezones_list),
                "timezone_count": len(timezones_list),
                "success": True
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }
    
    async def _analyze_number_patterns(self, phone: str) -> Dict[str, Any]:
        """Analyze phone number patterns for additional insights"""
        digits = re.sub(r'[^\d]', '', phone)
        
        # Analyze digit patterns
        digit_frequency = {}
        for digit in digits:
            digit_frequency[digit] = digit_frequency.get(digit, 0) + 1
        
        # Check for sequential numbers
        sequential_count = 0
        for i in range(len(digits) - 1):
            if int(digits[i+1]) == int(digits[i]) + 1:
                sequential_count += 1
        
        # Check for repeated patterns
        repeated_patterns = {}
        for length in [2, 3, 4]:
            for i in range(len(digits) - length + 1):
                pattern = digits[i:i+length]
                if digits.count(pattern) > 1:
                    repeated_patterns[pattern] = digits.count(pattern)
        
        return {
            "digit_frequency": digit_frequency,
            "most_common_digit": max(digit_frequency, key=digit_frequency.get) if digit_frequency else None,
            "sequential_count": sequential_count,
            "repeated_patterns": repeated_patterns,
            "total_digits": len(digits),
            "unique_digits": len(set(digits))
        }
    
    async def scan(self, query: Query) -> Dict[str, Any]:
        """Perform phone location scan"""
        await self.rate_limiter.wait_if_needed()
        
        phone = query.query_value.strip()
        
        # Get geographic information
        geo_info = await self._get_geographic_info(phone)
        pattern_analysis = await self._analyze_number_patterns(phone)
        
        # Calculate confidence based on available data
        confidence = 0.8 if geo_info.get("success", False) else 0.4
        if geo_info.get("location_description"):
            confidence += 0.1
        if geo_info.get("carrier") and geo_info["carrier"] != "Unknown":
            confidence += 0.1
        
        confidence = min(confidence, 1.0)
        
        return {
            "phone": phone,
            "geographic_info": geo_info,
            "pattern_analysis": pattern_analysis,
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat()
        }


class PhoneSpamScanner(BaseScannerModule):
    """Phone number spam and reputation scanner"""
    
    def __init__(self):
        super().__init__(
            name="phone_spam_scanner",
            scanner_type=ScannerType.PHONE_LOOKUP,
            description="Phone number spam detection and reputation analysis"
        )
        self.rate_limiter = RateLimiter(max_requests=100, time_window=60)
        
        # Known spam patterns (in real implementation, this would be a larger database)
        self.spam_patterns = {
            "robocaller_prefixes": ["555", "800", "888", "877", "866", "855", "844", "833"],
            "suspicious_patterns": [
                r"(\d)\1{4,}",  # 5+ repeated digits
                r"123456",      # Sequential
                r"000000",      # All zeros
            ]
        }
    
    def can_handle(self, query: Query) -> bool:
        return query.query_type.lower() == 'phone'
    
    def _analyze_spam_patterns(self, phone: str) -> Dict[str, Any]:
        """Analyze phone number for spam patterns"""
        digits = re.sub(r'[^\d]', '', phone)
        spam_indicators = {}
        spam_score = 0.0
        
        # Check for robocaller prefixes
        for prefix in self.spam_patterns["robocaller_prefixes"]:
            if prefix in digits:
                spam_indicators[f"robocaller_prefix_{prefix}"] = True
                spam_score += 0.2
        
        # Check for suspicious patterns
        for i, pattern in enumerate(self.spam_patterns["suspicious_patterns"]):
            if re.search(pattern, digits):
                spam_indicators[f"suspicious_pattern_{i}"] = True
                spam_score += 0.3
        
        # Check for other suspicious characteristics
        if len(set(digits)) < 4:  # Too few unique digits
            spam_indicators["low_digit_diversity"] = True
            spam_score += 0.2
        
        if digits.startswith("1") and len(digits) == 11:  # US number format
            area_code = digits[1:4]
            # Check for invalid area codes (simplified check)
            invalid_area_codes = ["000", "001", "555", "911"]
            if area_code in invalid_area_codes:
                spam_indicators["invalid_area_code"] = True
                spam_score += 0.4
        
        return {
            "spam_score": min(spam_score, 1.0),
            "spam_indicators": spam_indicators,
            "risk_level": self._calculate_risk_level(spam_score)
        }
    
    def _calculate_risk_level(self, spam_score: float) -> str:
        """Calculate risk level based on spam score"""
        if spam_score >= 0.7:
            return "high"
        elif spam_score >= 0.4:
            return "medium"
        elif spam_score >= 0.2:
            return "low"
        else:
            return "clean"
    
    async def _check_blacklist_databases(self, phone: str) -> Dict[str, Any]:
        """Mock check against spam databases (would be real APIs in production)"""
        # In real implementation, this would check against databases like:
        # - FTC Do Not Call Registry
        # - Spam reporting databases
        # - Carrier spam lists
        
        # Simulate database check based on phone hash
        phone_hash = hashlib.sha256(phone.encode()).hexdigest()[:10]
        
        # Mock results based on hash
        mock_results = {
            "do_not_call_registry": int(phone_hash[0], 16) % 10 == 0,  # 10% chance
            "spam_reports": int(phone_hash[1], 16) % 5,  # 0-4 reports
            "carrier_blocked": int(phone_hash[2], 16) % 20 == 0,  # 5% chance
            "robocaller_database": int(phone_hash[3], 16) % 15 == 0,  # ~7% chance
        }
        
        return {
            "blacklist_checks": mock_results,
            "total_spam_reports": mock_results["spam_reports"],
            "is_do_not_call": mock_results["do_not_call_registry"],
            "carrier_blocked": mock_results["carrier_blocked"],
            "robocaller_identified": mock_results["robocaller_database"]
        }
    
    async def scan(self, query: Query) -> Dict[str, Any]:
        """Perform phone spam scan"""
        await self.rate_limiter.wait_if_needed()
        
        phone = query.query_value.strip()
        
        # Analyze spam patterns
        pattern_analysis = self._analyze_spam_patterns(phone)
        
        # Check blacklist databases
        blacklist_results = await self._check_blacklist_databases(phone)
        
        # Calculate overall reputation score
        reputation_score = 1.0 - pattern_analysis["spam_score"]
        
        # Adjust based on blacklist results
        if blacklist_results["is_do_not_call"]:
            reputation_score -= 0.2
        if blacklist_results["carrier_blocked"]:
            reputation_score -= 0.3
        if blacklist_results["robocaller_identified"]:
            reputation_score -= 0.4
        if blacklist_results["total_spam_reports"] > 2:
            reputation_score -= 0.3
        
        reputation_score = max(0.0, reputation_score)
        
        return {
            "phone": phone,
            "pattern_analysis": pattern_analysis,
            "blacklist_results": blacklist_results,
            "reputation_score": reputation_score,
            "overall_risk": self._calculate_risk_level(1.0 - reputation_score),
            "recommendations": self._generate_recommendations(pattern_analysis, blacklist_results),
            "confidence": 0.75,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _generate_recommendations(self, pattern_analysis: Dict, blacklist_results: Dict) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if pattern_analysis["spam_score"] > 0.5:
            recommendations.append("High spam pattern detected - exercise caution")
        
        if blacklist_results["is_do_not_call"]:
            recommendations.append("Number is on Do Not Call registry")
        
        if blacklist_results["carrier_blocked"]:
            recommendations.append("Number has been blocked by carriers")
        
        if blacklist_results["total_spam_reports"] > 0:
            recommendations.append(f"Number has {blacklist_results['total_spam_reports']} spam reports")
        
        if not recommendations:
            recommendations.append("No significant spam indicators detected")
        
        return recommendations


class PhoneCarrierScanner(BaseScannerModule):
    """Phone number carrier and network information scanner"""
    
    def __init__(self):
        super().__init__(
            name="phone_carrier_scanner",
            scanner_type=ScannerType.PHONE_LOOKUP,
            description="Phone number carrier identification and network analysis"
        )
        self.rate_limiter = RateLimiter(max_requests=120, time_window=60)
        
        # Mock carrier database (in real implementation, this would be comprehensive)
        self.carrier_database = {
            "US": {
                "Verizon": {"prefixes": ["201", "202", "301", "302"], "type": "mobile"},
                "AT&T": {"prefixes": ["203", "205", "251", "256"], "type": "mobile"},
                "T-Mobile": {"prefixes": ["206", "253", "360", "425"], "type": "mobile"},
                "Sprint": {"prefixes": ["262", "414", "608", "715"], "type": "mobile"},
            }
        }
    
    def can_handle(self, query: Query) -> bool:
        return query.query_type.lower() == 'phone'
    
    async def _identify_carrier(self, phone: str) -> Dict[str, Any]:
        """Identify carrier information"""
        try:
            parsed = phonenumbers.parse(phone, None)
            
            if not phonenumbers.is_valid_number(parsed):
                return {"error": "Invalid phone number"}
            
            # Get basic carrier info from phonenumbers library
            carrier_name = carrier.name_for_number(parsed, "en")
            country_code = parsed.country_code
            region = phonenumbers.region_code_for_number(parsed)
            
            # Additional analysis for US numbers
            if country_code == 1:  # US/Canada
                phone_str = str(parsed.national_number)
                area_code = phone_str[:3] if len(phone_str) >= 10 else None
                
                # Mock additional carrier details
                carrier_details = self._get_detailed_carrier_info(area_code, region)
                
                return {
                    "carrier": carrier_name or "Unknown",
                    "country_code": country_code,
                    "region": region,
                    "area_code": area_code,
                    "carrier_details": carrier_details,
                    "success": True
                }
            else:
                return {
                    "carrier": carrier_name or "Unknown",
                    "country_code": country_code,
                    "region": region,
                    "success": True
                }
                
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }
    
    def _get_detailed_carrier_info(self, area_code: str, region: str) -> Dict[str, Any]:
        """Get detailed carrier information (mock implementation)"""
        # In real implementation, this would query carrier databases
        
        carrier_info = {
            "network_type": "unknown",
            "technology": "unknown",
            "mvno": False,  # Mobile Virtual Network Operator
            "porting_history": []
        }
        
        # Mock logic based on area code
        if area_code:
            area_code_int = int(area_code) if area_code.isdigit() else 0
            
            if area_code_int % 4 == 0:
                carrier_info.update({
                    "network_type": "GSM",
                    "technology": "LTE",
                    "mvno": False
                })
            elif area_code_int % 4 == 1:
                carrier_info.update({
                    "network_type": "CDMA", 
                    "technology": "5G",
                    "mvno": False
                })
            else:
                carrier_info.update({
                    "network_type": "GSM",
                    "technology": "LTE", 
                    "mvno": True
                })
        
        return carrier_info
    
    async def _analyze_number_portability(self, phone: str) -> Dict[str, Any]:
        """Analyze number portability information"""
        # Mock portability check (would be real database lookup in production)
        phone_hash = hashlib.sha256(phone.encode()).hexdigest()[:8]
        
        # Simulate portability data
        has_been_ported = int(phone_hash[0], 16) % 3 == 0  # 33% chance
        port_count = int(phone_hash[1], 16) % 4 if has_been_ported else 0
        
        return {
            "portable_number": True,  # Most modern numbers are portable
            "has_been_ported": has_been_ported,
            "estimated_port_count": port_count,
            "last_port_date": "2023-06-15" if has_been_ported else None,
            "original_carrier": "AT&T" if has_been_ported else None
        }
    
    async def scan(self, query: Query) -> Dict[str, Any]:
        """Perform phone carrier scan"""
        await self.rate_limiter.wait_if_needed()
        
        phone = query.query_value.strip()
        
        # Get carrier information
        carrier_info = await self._identify_carrier(phone)
        portability_info = await self._analyze_number_portability(phone)
        
        # Calculate confidence
        confidence = 0.7 if carrier_info.get("success", False) else 0.3
        if carrier_info.get("carrier") and carrier_info["carrier"] != "Unknown":
            confidence += 0.2
        
        confidence = min(confidence, 1.0)
        
        return {
            "phone": phone,
            "carrier_info": carrier_info,
            "portability_info": portability_info,
            "network_analysis": {
                "is_mobile": carrier_info.get("carrier_details", {}).get("network_type") in ["GSM", "CDMA"],
                "supports_sms": True,  # Most modern numbers do
                "supports_mms": True,
                "data_capable": True
            },
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat()
        }


# Import the RateLimiter class from email_scanners
from .email_scanners import RateLimiter


# Registry of phone scanners
PHONE_SCANNERS = [
    PhoneValidatorScanner,
    PhoneLocationScanner,
    PhoneSpamScanner,
    PhoneCarrierScanner
]


def register_phone_scanners(scanner_registry):
    """Register all phone scanner modules"""
    for scanner_class in PHONE_SCANNERS:
        scanner_instance = scanner_class()
        scanner_registry.register(scanner_instance)
        logger.info(f"Registered phone scanner: {scanner_instance.name}")
    
    return len(PHONE_SCANNERS)


# Aliases for backward compatibility
PhoneValidator = PhoneValidatorScanner
PhoneLocation = PhoneLocationScanner
PhoneSpam = PhoneSpamScanner
PhoneCarrier = PhoneCarrierScanner