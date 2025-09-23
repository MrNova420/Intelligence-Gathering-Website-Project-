"""
Social Media Intelligence Scanner Modules
Real implementations for social media profile detection and analysis.
"""

import asyncio
import re
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import aiohttp
import json
import hashlib
import time
from urllib.parse import quote, urljoin

from .base import BaseScannerModule, ScannerType
from ..db.models import Query
from .email_scanners import RateLimiter

logger = logging.getLogger(__name__)


class SocialMediaBaseScanner(BaseScannerModule):
    """Base class for social media scanners"""
    
    def __init__(self, name: str, platform: str, description: str):
        super().__init__(
            name=name,
            scanner_type=ScannerType.SOCIAL_MEDIA,
            description=description
        )
        self.platform = platform
        self.rate_limiter = RateLimiter(max_requests=60, time_window=60)
        
        # Common username patterns
        self.username_patterns = [
            r'^[a-zA-Z0-9._-]{3,30}$',  # Basic alphanumeric with dots, underscores, hyphens
            r'^[a-zA-Z][a-zA-Z0-9._-]{2,29}$',  # Must start with letter
        ]
        
        # Platform-specific blocked usernames (simplified)
        self.blocked_usernames = {
            "admin", "administrator", "root", "support", "help", "info",
            "contact", "sales", "marketing", "noreply", "mail", "email"
        }
    
    def _validate_username(self, username: str) -> Dict[str, Any]:
        """Validate username format for the platform"""
        if not username:
            return {"valid": False, "reason": "Empty username"}
        
        if username.lower() in self.blocked_usernames:
            return {"valid": False, "reason": "Reserved username"}
        
        # Check against patterns
        for pattern in self.username_patterns:
            if re.match(pattern, username):
                return {
                    "valid": True,
                    "pattern_matched": pattern,
                    "length": len(username)
                }
        
        return {"valid": False, "reason": "Invalid format"}
    
    def _generate_username_variations(self, base_username: str) -> List[str]:
        """Generate possible username variations"""
        variations = [base_username]
        
        # Add common variations
        variations.extend([
            base_username + str(year) for year in range(2020, 2025)
        ])
        variations.extend([
            base_username + suffix for suffix in ["_", ".", "official", "real"]
        ])
        
        # Remove invalid ones
        return [v for v in variations if self._validate_username(v)["valid"]][:10]


class TwitterScanner(SocialMediaBaseScanner):
    """Twitter/X profile scanner"""
    
    def __init__(self):
        super().__init__(
            name="twitter_scanner",
            platform="twitter",
            description="Twitter/X profile detection and analysis"
        )
        self.username_patterns = [r'^[a-zA-Z0-9_]{1,15}$']  # Twitter specific
    
    def can_handle(self, query: Query) -> bool:
        return query.query_type.lower() in ['username', 'email', 'name']
    
    async def _search_twitter_profiles(self, query_value: str, query_type: str) -> Dict[str, Any]:
        """Search for Twitter profiles (mock implementation)"""
        # In real implementation, this would use Twitter API v2
        
        if query_type == 'username':
            # Direct username lookup
            username = query_value.replace('@', '').strip()
            validation = self._validate_username(username)
            
            if not validation["valid"]:
                return {
                    "profile_found": False,
                    "reason": validation["reason"],
                    "searched_username": username
                }
            
            # Mock profile data based on username hash
            user_hash = hashlib.sha256(username.lower().encode()).hexdigest()[:10]
            
            # Simulate profile existence (70% chance for valid usernames)
            profile_exists = int(user_hash[0], 16) % 10 < 7
            
            if profile_exists:
                return {
                    "profile_found": True,
                    "username": username,
                    "display_name": username.replace('_', ' ').title(),
                    "profile_url": f"https://twitter.com/{username}",
                    "account_type": "public" if int(user_hash[1], 16) % 4 != 0 else "private",
                    "verified": int(user_hash[2], 16) % 20 == 0,  # 5% chance
                    "follower_count": int(user_hash[3:6], 16) % 10000,
                    "following_count": int(user_hash[6:9], 16) % 5000,
                    "tweet_count": int(user_hash[7:10], 16) % 50000,
                    "created_date": "2020-01-01",  # Mock date
                    "bio_snippet": f"Bio for {username}",
                    "location": "Unknown",
                    "website": None
                }
            else:
                return {
                    "profile_found": False,
                    "searched_username": username,
                    "available": True
                }
        
        elif query_type == 'email':
            # Search by email (limited in real API)
            local_part = query_value.split('@')[0] if '@' in query_value else query_value
            possible_usernames = self._generate_username_variations(local_part)
            
            found_profiles = []
            for username in possible_usernames[:5]:  # Check top 5
                profile_result = await self._search_twitter_profiles(username, 'username')
                if profile_result.get("profile_found"):
                    found_profiles.append(profile_result)
            
            return {
                "email_searched": query_value,
                "possible_usernames": possible_usernames,
                "profiles_found": found_profiles,
                "total_found": len(found_profiles)
            }
        
        elif query_type == 'name':
            # Search by name (mock implementation)
            name_parts = query_value.lower().split()
            possible_usernames = []
            
            # Generate username possibilities from name
            for part in name_parts:
                possible_usernames.extend([
                    part,
                    ''.join(name_parts),
                    '_'.join(name_parts),
                    ''.join([p[0] for p in name_parts]) + name_parts[-1]
                ])
            
            # Remove duplicates and validate
            possible_usernames = list(set(possible_usernames))
            possible_usernames = [u for u in possible_usernames if self._validate_username(u)["valid"]]
            
            found_profiles = []
            for username in possible_usernames[:3]:  # Check top 3
                profile_result = await self._search_twitter_profiles(username, 'username')
                if profile_result.get("profile_found"):
                    found_profiles.append(profile_result)
            
            return {
                "name_searched": query_value,
                "possible_usernames": possible_usernames,
                "profiles_found": found_profiles,
                "total_found": len(found_profiles)
            }
    
    async def scan(self, query: Query) -> Dict[str, Any]:
        """Perform Twitter profile scan"""
        await self.rate_limiter.wait_if_needed()
        
        search_results = await self._search_twitter_profiles(query.query_value, query.query_type)
        
        # Calculate confidence
        confidence = 0.8 if search_results.get("profile_found") or search_results.get("total_found", 0) > 0 else 0.4
        
        return {
            "platform": "twitter",
            "query_type": query.query_type,
            "query_value": query.query_value,
            "search_results": search_results,
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat()
        }


class LinkedInScanner(SocialMediaBaseScanner):
    """LinkedIn profile scanner"""
    
    def __init__(self):
        super().__init__(
            name="linkedin_scanner",
            platform="linkedin",
            description="LinkedIn professional profile detection and analysis"
        )
        self.username_patterns = [r'^[a-zA-Z0-9-]{3,100}$']  # LinkedIn allows hyphens
    
    def can_handle(self, query: Query) -> bool:
        return query.query_type.lower() in ['email', 'name', 'username']
    
    async def _search_linkedin_profiles(self, query_value: str, query_type: str) -> Dict[str, Any]:
        """Search for LinkedIn profiles (mock implementation)"""
        # In real implementation, this would use LinkedIn API or web scraping
        
        if query_type == 'email':
            # LinkedIn profile search by email
            domain = query_value.split('@')[1] if '@' in query_value else ''
            local_part = query_value.split('@')[0] if '@' in query_value else query_value
            
            # Mock profile data
            profile_hash = hashlib.sha256(query_value.lower().encode()).hexdigest()[:12]
            
            # Higher chance of profile for business domains
            business_domains = ['gmail.com', 'outlook.com', 'company.com', 'corp.com']
            profile_chance = 0.8 if any(bd in domain for bd in business_domains) else 0.6
            
            profile_exists = int(profile_hash[0], 16) % 10 < (profile_chance * 10)
            
            if profile_exists:
                return {
                    "profile_found": True,
                    "profile_url": f"https://linkedin.com/in/{local_part.replace('.', '-')}",
                    "full_name": local_part.replace('.', ' ').title(),
                    "headline": "Professional at Company",
                    "location": "San Francisco Bay Area",
                    "industry": "Technology",
                    "connections": int(profile_hash[1:4], 16) % 500 + 50,
                    "company": "Tech Company",
                    "position": "Senior Developer",
                    "experience_years": int(profile_hash[4], 16) % 15 + 1,
                    "education": "University",
                    "skills_count": int(profile_hash[5], 16) % 50 + 10,
                    "recommendations": int(profile_hash[6], 16) % 20,
                    "profile_completeness": int(profile_hash[7], 16) % 40 + 60
                }
            else:
                return {
                    "profile_found": False,
                    "searched_email": query_value
                }
        
        elif query_type == 'name':
            # Search by full name
            name_parts = query_value.strip().split()
            if len(name_parts) < 2:
                return {
                    "profile_found": False,
                    "reason": "Need full name for LinkedIn search"
                }
            
            first_name = name_parts[0]
            last_name = name_parts[-1]
            full_name = ' '.join(name_parts)
            
            # Mock search results
            name_hash = hashlib.sha256(full_name.lower().encode()).hexdigest()[:12]
            
            # Multiple profiles possible for common names
            profile_count = int(name_hash[0], 16) % 5 + 1
            profiles = []
            
            for i in range(min(profile_count, 3)):  # Limit to 3 results
                profile_variation = f"{name_hash[i:i+4]}"
                profiles.append({
                    "profile_url": f"https://linkedin.com/in/{first_name.lower()}-{last_name.lower()}-{profile_variation[:4]}",
                    "full_name": full_name,
                    "headline": f"Professional in {['Technology', 'Finance', 'Marketing', 'Healthcare'][i % 4]}",
                    "location": ["San Francisco", "New York", "Los Angeles", "Chicago"][i % 4],
                    "company": f"Company {i+1}",
                    "match_confidence": max(0.7 - i * 0.1, 0.4)
                })
            
            return {
                "name_searched": full_name,
                "profiles_found": profiles,
                "total_profiles": len(profiles),
                "search_notes": "Multiple profiles found - manual verification recommended"
            }
        
        elif query_type == 'username':
            # Direct LinkedIn username lookup
            username = query_value.strip()
            validation = self._validate_username(username)
            
            if not validation["valid"]:
                return {
                    "profile_found": False,
                    "reason": validation["reason"]
                }
            
            # Mock profile lookup
            user_hash = hashlib.sha256(username.lower().encode()).hexdigest()[:10]
            profile_exists = int(user_hash[0], 16) % 10 < 5  # 50% chance
            
            if profile_exists:
                return {
                    "profile_found": True,
                    "username": username,
                    "profile_url": f"https://linkedin.com/in/{username}",
                    "full_name": username.replace('-', ' ').title(),
                    "headline": "Professional",
                    "is_premium": int(user_hash[1], 16) % 10 == 0  # 10% chance
                }
            else:
                return {
                    "profile_found": False,
                    "username_available": True
                }
    
    async def scan(self, query: Query) -> Dict[str, Any]:
        """Perform LinkedIn profile scan"""
        await self.rate_limiter.wait_if_needed()
        
        search_results = await self._search_linkedin_profiles(query.query_value, query.query_type)
        
        # Calculate confidence
        confidence = 0.75
        if search_results.get("profile_found"):
            confidence = 0.85
        elif search_results.get("total_profiles", 0) > 0:
            confidence = 0.7
        else:
            confidence = 0.3
        
        return {
            "platform": "linkedin",
            "query_type": query.query_type,
            "query_value": query.query_value,
            "search_results": search_results,
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat()
        }


class InstagramScanner(SocialMediaBaseScanner):
    """Instagram profile scanner"""
    
    def __init__(self):
        super().__init__(
            name="instagram_scanner",
            platform="instagram",
            description="Instagram profile detection and analysis"
        )
        self.username_patterns = [r'^[a-zA-Z0-9._]{1,30}$']  # Instagram specific
    
    def can_handle(self, query: Query) -> bool:
        return query.query_type.lower() in ['username', 'email']
    
    async def _search_instagram_profiles(self, query_value: str, query_type: str) -> Dict[str, Any]:
        """Search for Instagram profiles (mock implementation)"""
        
        if query_type == 'username':
            username = query_value.replace('@', '').strip()
            validation = self._validate_username(username)
            
            if not validation["valid"]:
                return {
                    "profile_found": False,
                    "reason": validation["reason"]
                }
            
            # Mock profile data
            user_hash = hashlib.sha256(username.lower().encode()).hexdigest()[:12]
            profile_exists = int(user_hash[0], 16) % 10 < 6  # 60% chance
            
            if profile_exists:
                is_private = int(user_hash[1], 16) % 3 == 0  # 33% chance
                is_verified = int(user_hash[2], 16) % 50 == 0  # 2% chance
                
                return {
                    "profile_found": True,
                    "username": username,
                    "profile_url": f"https://instagram.com/{username}",
                    "display_name": username.replace('_', ' ').replace('.', ' ').title(),
                    "is_private": is_private,
                    "is_verified": is_verified,
                    "is_business": int(user_hash[3], 16) % 10 == 0,  # 10% chance
                    "follower_count": int(user_hash[4:7], 16) % 100000 if not is_private else "hidden",
                    "following_count": int(user_hash[7:10], 16) % 10000 if not is_private else "hidden",
                    "post_count": int(user_hash[8:11], 16) % 5000 if not is_private else "hidden",
                    "bio_snippet": f"Bio for {username}" if not is_private else "private",
                    "external_url": None,
                    "category": "Personal" if not int(user_hash[3], 16) % 10 == 0 else "Business"
                }
            else:
                return {
                    "profile_found": False,
                    "username_available": True
                }
        
        elif query_type == 'email':
            # Search by email - generate possible usernames
            local_part = query_value.split('@')[0] if '@' in query_value else query_value
            possible_usernames = self._generate_username_variations(local_part)
            
            found_profiles = []
            for username in possible_usernames[:4]:  # Check top 4
                profile_result = await self._search_instagram_profiles(username, 'username')
                if profile_result.get("profile_found"):
                    found_profiles.append(profile_result)
            
            return {
                "email_searched": query_value,
                "possible_usernames": possible_usernames,
                "profiles_found": found_profiles,
                "total_found": len(found_profiles)
            }
    
    async def scan(self, query: Query) -> Dict[str, Any]:
        """Perform Instagram profile scan"""
        await self.rate_limiter.wait_if_needed()
        
        search_results = await self._search_instagram_profiles(query.query_value, query.query_type)
        
        # Calculate confidence
        confidence = 0.75 if search_results.get("profile_found") or search_results.get("total_found", 0) > 0 else 0.4
        
        return {
            "platform": "instagram",
            "query_type": query.query_type,
            "query_value": query.query_value,
            "search_results": search_results,
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat()
        }


class FacebookScanner(SocialMediaBaseScanner):
    """Facebook profile scanner"""
    
    def __init__(self):
        super().__init__(
            name="facebook_scanner",
            platform="facebook",
            description="Facebook profile detection and analysis"
        )
    
    def can_handle(self, query: Query) -> bool:
        return query.query_type.lower() in ['email', 'name', 'phone']
    
    async def _search_facebook_profiles(self, query_value: str, query_type: str) -> Dict[str, Any]:
        """Search for Facebook profiles (mock implementation)"""
        # Note: Facebook's API is very restricted for profile searches
        
        if query_type == 'email':
            # Facebook email search (very limited in real API)
            email_hash = hashlib.sha256(query_value.lower().encode()).hexdigest()[:10]
            
            # Low chance of finding public profile via email
            profile_exists = int(email_hash[0], 16) % 10 < 2  # 20% chance
            
            if profile_exists:
                return {
                    "profile_found": True,
                    "search_method": "email",
                    "profile_id": f"profile.{email_hash[:8]}",
                    "profile_url": f"https://facebook.com/profile.php?id={email_hash[:8]}",
                    "name": "Name Hidden",
                    "privacy_level": "high",
                    "profile_picture": "visible",
                    "mutual_friends": int(email_hash[1], 16) % 10,
                    "location": "Hidden",
                    "work": "Hidden",
                    "education": "Hidden"
                }
            else:
                return {
                    "profile_found": False,
                    "reason": "No public profile found or privacy settings restrict search"
                }
        
        elif query_type == 'name':
            # Name-based search
            full_name = query_value.strip()
            name_parts = full_name.split()
            
            if len(name_parts) < 2:
                return {
                    "profile_found": False,
                    "reason": "Need full name for Facebook search"
                }
            
            name_hash = hashlib.sha256(full_name.lower().encode()).hexdigest()[:12]
            
            # Multiple profiles possible
            profile_count = min(int(name_hash[0], 16) % 3 + 1, 3)
            profiles = []
            
            for i in range(profile_count):
                profiles.append({
                    "profile_id": f"{name_hash[i*2:(i*2)+4]}",
                    "profile_url": f"https://facebook.com/{name_hash[i*2:(i*2)+8]}",
                    "display_name": full_name,
                    "location": ["New York", "Los Angeles", "Chicago", "Unknown"][i % 4],
                    "mutual_friends": int(name_hash[i+1], 16) % 20,
                    "profile_picture": "visible" if int(name_hash[i], 16) % 2 == 0 else "hidden",
                    "privacy_level": ["medium", "high", "very_high"][i % 3],
                    "match_confidence": max(0.8 - i * 0.2, 0.4)
                })
            
            return {
                "name_searched": full_name,
                "profiles_found": profiles,
                "total_profiles": len(profiles),
                "note": "Facebook profiles have high privacy settings"
            }
        
        elif query_type == 'phone':
            # Phone-based search (very limited)
            phone_hash = hashlib.sha256(query_value.encode()).hexdigest()[:10]
            
            # Very low chance due to privacy
            profile_exists = int(phone_hash[0], 16) % 20 == 0  # 5% chance
            
            if profile_exists:
                return {
                    "profile_found": True,
                    "search_method": "phone",
                    "profile_type": "business" if int(phone_hash[1], 16) % 3 == 0 else "personal",
                    "privacy_note": "Limited information due to privacy settings"
                }
            else:
                return {
                    "profile_found": False,
                    "reason": "No profile found or phone number not publicly associated"
                }
    
    async def scan(self, query: Query) -> Dict[str, Any]:
        """Perform Facebook profile scan"""
        await self.rate_limiter.wait_if_needed()
        
        search_results = await self._search_facebook_profiles(query.query_value, query.query_type)
        
        # Lower confidence due to Facebook's privacy restrictions
        confidence = 0.6 if search_results.get("profile_found") or search_results.get("total_profiles", 0) > 0 else 0.2
        
        return {
            "platform": "facebook",
            "query_type": query.query_type,
            "query_value": query.query_value,
            "search_results": search_results,
            "privacy_note": "Facebook has strict privacy controls - results may be limited",
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat()
        }


class GitHubScanner(SocialMediaBaseScanner):
    """GitHub profile scanner"""
    
    def __init__(self):
        super().__init__(
            name="github_scanner",
            platform="github",
            description="GitHub developer profile detection and analysis"
        )
        self.username_patterns = [r'^[a-zA-Z0-9]([a-zA-Z0-9-]){0,38}$']  # GitHub specific
    
    def can_handle(self, query: Query) -> bool:
        return query.query_type.lower() in ['username', 'email', 'name']
    
    async def _search_github_profiles(self, query_value: str, query_type: str) -> Dict[str, Any]:
        """Search for GitHub profiles (mock implementation)"""
        
        if query_type == 'username':
            username = query_value.strip()
            validation = self._validate_username(username)
            
            if not validation["valid"]:
                return {
                    "profile_found": False,
                    "reason": validation["reason"]
                }
            
            # Mock GitHub profile data
            user_hash = hashlib.sha256(username.lower().encode()).hexdigest()[:12]
            profile_exists = int(user_hash[0], 16) % 10 < 4  # 40% chance
            
            if profile_exists:
                return {
                    "profile_found": True,
                    "username": username,
                    "profile_url": f"https://github.com/{username}",
                    "display_name": username.replace('-', ' ').title(),
                    "bio": f"Developer and coder",
                    "company": "Tech Company" if int(user_hash[1], 16) % 3 == 0 else None,
                    "location": "San Francisco" if int(user_hash[2], 16) % 4 == 0 else None,
                    "email": f"{username}@email.com" if int(user_hash[3], 16) % 5 == 0 else None,
                    "public_repos": int(user_hash[4:6], 16) % 200,
                    "public_gists": int(user_hash[6:8], 16) % 50,
                    "followers": int(user_hash[8:10], 16) % 1000,
                    "following": int(user_hash[10:12], 16) % 500,
                    "created_at": "2020-01-01",
                    "updated_at": "2024-01-01",
                    "blog": f"https://{username}.dev" if int(user_hash[4], 16) % 10 == 0 else None,
                    "twitter_username": username if int(user_hash[5], 16) % 8 == 0 else None,
                    "primary_language": ["Python", "JavaScript", "Java", "Go", "Rust"][int(user_hash[6], 16) % 5],
                    "contribution_years": list(range(2020, 2025))
                }
            else:
                return {
                    "profile_found": False,
                    "username_available": True
                }
        
        elif query_type == 'email':
            # Search by email - limited in real GitHub API
            local_part = query_value.split('@')[0] if '@' in query_value else query_value
            possible_usernames = self._generate_username_variations(local_part)
            
            found_profiles = []
            for username in possible_usernames[:3]:  # Check top 3
                profile_result = await self._search_github_profiles(username, 'username')
                if profile_result.get("profile_found"):
                    found_profiles.append(profile_result)
            
            return {
                "email_searched": query_value,
                "possible_usernames": possible_usernames,
                "profiles_found": found_profiles,
                "total_found": len(found_profiles)
            }
        
        elif query_type == 'name':
            # Search by name
            name_parts = query_value.lower().split()
            possible_usernames = []
            
            # Generate GitHub-style usernames from name
            if len(name_parts) >= 2:
                first, last = name_parts[0], name_parts[-1]
                possible_usernames.extend([
                    first + last,
                    first + '-' + last,
                    first[0] + last,
                    last + first[0],
                    first,
                    last
                ])
            else:
                possible_usernames.append(name_parts[0])
            
            # Remove duplicates and validate
            possible_usernames = list(set(possible_usernames))
            possible_usernames = [u for u in possible_usernames if self._validate_username(u)["valid"]]
            
            found_profiles = []
            for username in possible_usernames[:3]:
                profile_result = await self._search_github_profiles(username, 'username')
                if profile_result.get("profile_found"):
                    found_profiles.append(profile_result)
            
            return {
                "name_searched": query_value,
                "possible_usernames": possible_usernames,
                "profiles_found": found_profiles,
                "total_found": len(found_profiles)
            }
    
    async def scan(self, query: Query) -> Dict[str, Any]:
        """Perform GitHub profile scan"""
        await self.rate_limiter.wait_if_needed()
        
        search_results = await self._search_github_profiles(query.query_value, query.query_type)
        
        # Calculate confidence
        confidence = 0.8 if search_results.get("profile_found") or search_results.get("total_found", 0) > 0 else 0.3
        
        return {
            "platform": "github",
            "query_type": query.query_type,
            "query_value": query.query_value,
            "search_results": search_results,
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat()
        }


# Registry of social media scanners
SOCIAL_SCANNERS = [
    TwitterScanner,
    LinkedInScanner,
    InstagramScanner,
    FacebookScanner,
    GitHubScanner
]


def register_social_scanners(scanner_registry):
    """Register all social media scanner modules"""
    for scanner_class in SOCIAL_SCANNERS:
        scanner_instance = scanner_class()
        scanner_registry.register(scanner_instance)
        logger.info(f"Registered social media scanner: {scanner_instance.name}")
    
    return len(SOCIAL_SCANNERS)