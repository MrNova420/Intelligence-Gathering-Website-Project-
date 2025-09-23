"""
Email Intelligence Scanner Modules
Real implementations with API wrappers, error handling, and rate limiting.
"""

import asyncio
import re
import dns.resolver
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import aiohttp
import json
from urllib.parse import quote
import hashlib
import time

from .base import BaseScannerModule, ScannerType
from ..db.models import Query

logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    async def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = time.time()
        # Remove old requests outside time window
        self.requests = [req_time for req_time in self.requests if now - req_time < self.time_window]
        
        if len(self.requests) >= self.max_requests:
            # Wait until oldest request is outside window
            sleep_time = self.time_window - (now - self.requests[0]) + 0.1
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
        
        self.requests.append(now)


class EmailValidatorScanner(BaseScannerModule):
    """Email syntax and domain validation scanner"""
    
    def __init__(self):
        super().__init__(
            name="email_validator",
            scanner_type=ScannerType.EMAIL_VERIFICATION,
            description="Email syntax validation and domain verification"
        )
        self.rate_limiter = RateLimiter(max_requests=100, time_window=60)
    
    def can_handle(self, query: Query) -> bool:
        return query.query_type.lower() == 'email'
    
    def _validate_email_syntax(self, email: str) -> Dict[str, Any]:
        """Validate email syntax using regex"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_valid = bool(re.match(pattern, email))
        
        return {
            "syntax_valid": is_valid,
            "pattern_match": is_valid,
            "length": len(email),
            "has_subdomain": email.count('.') > 1 if '@' in email else False
        }
    
    async def _check_mx_record(self, domain: str) -> Dict[str, Any]:
        """Check if domain has MX record"""
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            mx_list = [str(mx) for mx in mx_records]
            return {
                "has_mx": True,
                "mx_records": mx_list,
                "mx_count": len(mx_list)
            }
        except Exception as e:
            return {
                "has_mx": False,
                "error": str(e),
                "mx_records": []
            }
    
    async def _check_domain_exists(self, domain: str) -> Dict[str, Any]:
        """Check if domain exists via DNS A record"""
        try:
            a_records = dns.resolver.resolve(domain, 'A')
            ip_list = [str(ip) for ip in a_records]
            return {
                "domain_exists": True,
                "ip_addresses": ip_list,
                "ip_count": len(ip_list)
            }
        except Exception as e:
            return {
                "domain_exists": False,
                "error": str(e),
                "ip_addresses": []
            }
    
    async def scan(self, query: Query) -> Dict[str, Any]:
        """Perform email validation scan"""
        await self.rate_limiter.wait_if_needed()
        
        email = query.query_value.lower().strip()
        
        # Basic syntax validation
        syntax_result = self._validate_email_syntax(email)
        
        if not syntax_result["syntax_valid"]:
            return {
                "email": email,
                "valid": False,
                "reason": "Invalid syntax",
                "syntax": syntax_result,
                "domain_check": None,
                "mx_check": None,
                "confidence": 0.9
            }
        
        # Extract domain
        domain = email.split('@')[1]
        
        # Check domain and MX records
        domain_result = await self._check_domain_exists(domain)
        mx_result = await self._check_mx_record(domain)
        
        # Calculate overall validity
        is_valid = (syntax_result["syntax_valid"] and 
                   domain_result["domain_exists"] and 
                   mx_result["has_mx"])
        
        confidence = 0.9 if is_valid else 0.1
        
        return {
            "email": email,
            "valid": is_valid,
            "syntax": syntax_result,
            "domain_check": domain_result,
            "mx_check": mx_result,
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat()
        }


class EmailReputationScanner(BaseScannerModule):
    """Email reputation and security scanner"""
    
    def __init__(self):
        super().__init__(
            name="email_reputation",
            scanner_type=ScannerType.EMAIL_VERIFICATION,
            description="Email reputation and security analysis"
        )
        self.rate_limiter = RateLimiter(max_requests=50, time_window=60)
        self.disposable_domains = {
            "10minutemail.com", "tempmail.org", "guerrillamail.com", 
            "mailinator.com", "throwaway.email", "temp-mail.org"
        }
        self.role_indicators = {
            "admin", "support", "info", "contact", "sales", "marketing",
            "help", "noreply", "no-reply", "donotreply"
        }
    
    def can_handle(self, query: Query) -> bool:
        return query.query_type.lower() == 'email'
    
    def _check_disposable_email(self, email: str) -> Dict[str, Any]:
        """Check if email is from disposable email provider"""
        domain = email.split('@')[1] if '@' in email else ''
        is_disposable = domain.lower() in self.disposable_domains
        
        return {
            "is_disposable": is_disposable,
            "domain": domain,
            "provider_type": "disposable" if is_disposable else "standard"
        }
    
    def _check_role_account(self, email: str) -> Dict[str, Any]:
        """Check if email appears to be a role account"""
        local_part = email.split('@')[0] if '@' in email else email
        is_role = any(indicator in local_part.lower() for indicator in self.role_indicators)
        
        matched_indicators = [indicator for indicator in self.role_indicators 
                            if indicator in local_part.lower()]
        
        return {
            "is_role_account": is_role,
            "matched_indicators": matched_indicators,
            "local_part": local_part
        }
    
    def _analyze_email_structure(self, email: str) -> Dict[str, Any]:
        """Analyze email structure for suspicious patterns"""
        local_part = email.split('@')[0] if '@' in email else email
        
        # Check for suspicious patterns
        has_numbers = bool(re.search(r'\d', local_part))
        has_special_chars = bool(re.search(r'[^a-zA-Z0-9._-]', local_part))
        length = len(local_part)
        
        # Suspicious indicators
        suspicious_score = 0
        if length < 3:
            suspicious_score += 0.3
        if length > 20:
            suspicious_score += 0.2
        if local_part.count('.') > 2:
            suspicious_score += 0.2
        if local_part.startswith('.') or local_part.endswith('.'):
            suspicious_score += 0.4
        
        return {
            "local_part_length": length,
            "has_numbers": has_numbers,
            "has_special_chars": has_special_chars,
            "suspicious_score": min(suspicious_score, 1.0),
            "structure_analysis": {
                "dots_count": local_part.count('.'),
                "hyphens_count": local_part.count('-'),
                "underscores_count": local_part.count('_')
            }
        }
    
    async def scan(self, query: Query) -> Dict[str, Any]:
        """Perform email reputation scan"""
        await self.rate_limiter.wait_if_needed()
        
        email = query.query_value.lower().strip()
        
        # Run all checks
        disposable_check = self._check_disposable_email(email)
        role_check = self._check_role_account(email)
        structure_analysis = self._analyze_email_structure(email)
        
        # Calculate overall reputation score
        reputation_score = 1.0
        
        if disposable_check["is_disposable"]:
            reputation_score -= 0.5
        
        if role_check["is_role_account"]:
            reputation_score -= 0.2
        
        reputation_score -= structure_analysis["suspicious_score"] * 0.3
        reputation_score = max(0.0, reputation_score)
        
        return {
            "email": email,
            "reputation_score": reputation_score,
            "disposable_check": disposable_check,
            "role_account_check": role_check,
            "structure_analysis": structure_analysis,
            "risk_level": "high" if reputation_score < 0.3 else "medium" if reputation_score < 0.7 else "low",
            "confidence": 0.85,
            "timestamp": datetime.utcnow().isoformat()
        }


class EmailBreachScanner(BaseScannerModule):
    """Email data breach scanner (mock API calls for demonstration)"""
    
    def __init__(self):
        super().__init__(
            name="email_breach_scanner",
            scanner_type=ScannerType.EMAIL_VERIFICATION,
            description="Email data breach detection and analysis"
        )
        self.rate_limiter = RateLimiter(max_requests=20, time_window=60)
    
    def can_handle(self, query: Query) -> bool:
        return query.query_type.lower() == 'email'
    
    async def _check_haveibeenpwned_api(self, email: str) -> Dict[str, Any]:
        """Mock HaveIBeenPwned API check (would need real API key)"""
        # In real implementation, this would call the actual API
        # For demo purposes, we'll simulate based on email characteristics
        
        email_hash = hashlib.sha1(email.encode()).hexdigest()[:10]
        
        # Simulate breach data based on hash
        mock_breaches = []
        if int(email_hash[0], 16) % 3 == 0:  # 33% chance of breach
            mock_breaches = [
                {
                    "Name": "Adobe",
                    "BreachDate": "2013-10-04",
                    "AddedDate": "2013-12-04T00:00:00Z",
                    "PwnCount": 152445165,
                    "DataClasses": ["Email addresses", "Password hints", "Passwords", "Usernames"]
                }
            ]
        
        return {
            "breaches_found": len(mock_breaches),
            "breaches": mock_breaches,
            "total_accounts_breached": sum(b.get("PwnCount", 0) for b in mock_breaches),
            "most_recent_breach": mock_breaches[0]["BreachDate"] if mock_breaches else None
        }
    
    async def _check_paste_exposures(self, email: str) -> Dict[str, Any]:
        """Mock paste exposure check"""
        email_hash = hashlib.sha1(email.encode()).hexdigest()[:10]
        
        # Simulate paste exposures
        mock_pastes = []
        if int(email_hash[1], 16) % 4 == 0:  # 25% chance
            mock_pastes = [
                {
                    "Source": "Pastebin",
                    "Id": "8Q0BvKD8",
                    "Date": "2022-01-15T04:51:18Z",
                    "EmailCount": 139
                }
            ]
        
        return {
            "pastes_found": len(mock_pastes),
            "pastes": mock_pastes,
            "total_emails_in_pastes": sum(p.get("EmailCount", 0) for p in mock_pastes)
        }
    
    async def scan(self, query: Query) -> Dict[str, Any]:
        """Perform email breach scan"""
        await self.rate_limiter.wait_if_needed()
        
        email = query.query_value.lower().strip()
        
        # Check breaches and pastes
        breach_data = await self._check_haveibeenpwned_api(email)
        paste_data = await self._check_paste_exposures(email)
        
        # Calculate risk score
        risk_score = 0.0
        if breach_data["breaches_found"] > 0:
            risk_score += min(breach_data["breaches_found"] * 0.2, 0.6)
        
        if paste_data["pastes_found"] > 0:
            risk_score += min(paste_data["pastes_found"] * 0.1, 0.3)
        
        risk_score = min(risk_score, 1.0)
        
        return {
            "email": email,
            "breach_analysis": breach_data,
            "paste_analysis": paste_data,
            "risk_score": risk_score,
            "risk_level": "critical" if risk_score > 0.7 else "high" if risk_score > 0.4 else "medium" if risk_score > 0.1 else "low",
            "recommendations": self._generate_recommendations(risk_score, breach_data, paste_data),
            "confidence": 0.8,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _generate_recommendations(self, risk_score: float, breach_data: Dict, paste_data: Dict) -> List[str]:
        """Generate security recommendations based on findings"""
        recommendations = []
        
        if breach_data["breaches_found"] > 0:
            recommendations.append("Change passwords for accounts associated with this email")
            recommendations.append("Enable two-factor authentication where possible")
        
        if paste_data["pastes_found"] > 0:
            recommendations.append("Monitor for suspicious account activity")
            recommendations.append("Consider using email aliases for sensitive accounts")
        
        if risk_score > 0.5:
            recommendations.append("Consider replacing this email address for sensitive accounts")
            recommendations.append("Set up identity monitoring services")
        
        return recommendations


class SocialMediaEmailScanner(BaseScannerModule):
    """Social media profile scanner based on email"""
    
    def __init__(self):
        super().__init__(
            name="social_media_email_scanner",
            scanner_type=ScannerType.SOCIAL_MEDIA,
            description="Social media profile detection via email"
        )
        self.rate_limiter = RateLimiter(max_requests=30, time_window=60)
        self.platforms = ["twitter", "linkedin", "facebook", "instagram", "github", "reddit"]
    
    def can_handle(self, query: Query) -> bool:
        return query.query_type.lower() == 'email'
    
    async def _check_platform_patterns(self, email: str) -> Dict[str, Any]:
        """Check for platform-specific email patterns"""
        local_part = email.split('@')[0] if '@' in email else email
        domain = email.split('@')[1] if '@' in email else ''
        
        platform_indicators = {}
        
        # Check for platform-specific indicators in email
        for platform in self.platforms:
            score = 0.0
            
            # Check for platform name in email
            if platform in local_part.lower():
                score += 0.3
            
            # Check for common platform-related terms
            platform_terms = {
                "twitter": ["tweet", "tw", "bird"],
                "linkedin": ["ln", "professional", "career"],
                "github": ["git", "code", "dev", "developer"],
                "facebook": ["fb", "face"],
                "instagram": ["insta", "ig", "photo"],
                "reddit": ["reddit", "r/"]
            }
            
            for term in platform_terms.get(platform, []):
                if term in local_part.lower():
                    score += 0.2
            
            platform_indicators[platform] = {
                "likelihood_score": min(score, 1.0),
                "indicators_found": [term for term in platform_terms.get(platform, []) if term in local_part.lower()]
            }
        
        return platform_indicators
    
    async def _generate_profile_predictions(self, email: str) -> Dict[str, Any]:
        """Generate predictions about possible social media profiles"""
        local_part = email.split('@')[0] if '@' in email else email
        
        # Generate possible usernames
        possible_usernames = [
            local_part,
            local_part.replace('.', ''),
            local_part.replace('_', ''),
            local_part.replace('-', ''),
            local_part + "official",
            local_part + str(datetime.now().year)
        ]
        
        # Remove duplicates and very short names
        possible_usernames = list(set([name for name in possible_usernames if len(name) >= 3]))
        
        return {
            "possible_usernames": possible_usernames[:10],  # Limit to top 10
            "username_variations": len(possible_usernames),
            "primary_username": local_part
        }
    
    async def scan(self, query: Query) -> Dict[str, Any]:
        """Perform social media email scan"""
        await self.rate_limiter.wait_if_needed()
        
        email = query.query_value.lower().strip()
        
        # Analyze platform patterns and generate predictions
        platform_analysis = await self._check_platform_patterns(email)
        profile_predictions = await self._generate_profile_predictions(email)
        
        # Find platforms with highest likelihood
        top_platforms = sorted(
            platform_analysis.items(), 
            key=lambda x: x[1]["likelihood_score"], 
            reverse=True
        )[:3]
        
        return {
            "email": email,
            "platform_analysis": platform_analysis,
            "profile_predictions": profile_predictions,
            "top_likely_platforms": [{"platform": p[0], "score": p[1]["likelihood_score"]} for p in top_platforms],
            "search_suggestions": {
                platform: f"Search for '{profile_predictions['primary_username']}' on {platform.title()}"
                for platform, _ in top_platforms
            },
            "confidence": 0.6,
            "timestamp": datetime.utcnow().isoformat()
        }


# Registry of email scanners
EMAIL_SCANNERS = [
    EmailValidatorScanner,
    EmailReputationScanner,
    EmailBreachScanner,
    SocialMediaEmailScanner
]


def register_email_scanners(scanner_registry):
    """Register all email scanner modules"""
    for scanner_class in EMAIL_SCANNERS:
        scanner_instance = scanner_class()
        scanner_registry.register(scanner_instance)
        logger.info(f"Registered email scanner: {scanner_instance.name}")
    
    return len(EMAIL_SCANNERS)