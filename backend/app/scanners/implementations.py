# Mock implementation to avoid import issues
async def mock_scan(query):
    """Mock scan function."""
    import asyncio
    await asyncio.sleep(1)
    return {"source": "mock", "query": query.query_value, "status": "found"}


# Simplified scanner for testing
class MockBaseScannerModule:
    def __init__(self, name: str, scanner_type: str, description: str = ""):
        self.name = name
        self.scanner_type = scanner_type
        self.description = description
        self.enabled = True
        self.scan = mock_scan
        self.can_handle = lambda q: True


class MockScannerRegistry:
    def __init__(self):
        self._scanners = []
    
    def register(self, scanner):
        self._scanners.append(scanner)
    
    def get_all_scanners(self):
        return self._scanners


scanner_registry = MockScannerRegistry()


def register_scanners():
    """Register all 100+ scanner modules."""
    import logging
    
    logger = logging.getLogger(__name__)
    
    # Register 100+ mock scanners
    scanner_types = [
        "api", "social_media", "public_records", "email_verification", 
        "phone_lookup", "image_media", "forum_community", "deep_web"
    ]
    
    scanner_names = [
        # Email scanners (15)
        "clearbit", "hunter_email", "emailrep", "email_validator", "email_breach_check",
        "email_social_finder", "verify_email", "email_deliverability", "email_reputation",
        "email_domain_check", "email_mx_lookup", "email_syntax_check", "email_blacklist",
        "email_disposable_check", "email_role_detection",
        
        # Social Media scanners (20)
        "twitter_profile", "linkedin_profile", "instagram_profile", "facebook_profile",
        "tiktok_scanner", "youtube_scanner", "reddit_scanner", "pinterest_scanner",
        "snapchat_scanner", "telegram_scanner", "discord_scanner", "whatsapp_lookup",
        "skype_search", "vk_profile", "weibo_search", "line_search", "viber_lookup",
        "signal_search", "clubhouse_profile", "social_cross_search",
        
        # Phone scanners (10)
        "truecaller", "whitepages", "carrier_lookup", "phone_location", "spam_checker",
        "phone_validator", "number_portability", "sms_verification", "call_history",
        "phone_reputation",
        
        # Public Records scanners (25)
        "public_records", "court_records", "bankruptcy_records", "criminal_records",
        "marriage_records", "divorce_records", "death_records", "voter_records",
        "professional_licenses", "business_registry", "property_records", "tax_records",
        "trademark_search", "patent_search", "sec_filings", "fcc_search",
        "customs_records", "aviation_records", "vessel_records", "federal_contractors",
        "charity_search", "lobbying_records", "campaign_finance", "sanctions_check",
        "watch_lists",
        
        # Search Engine scanners (15)
        "google_search", "bing_search", "duckduckgo_search", "yandex_search",
        "baidu_search", "google_images", "bing_images", "reverse_image",
        "google_news", "specialized_search", "academic_search", "patent_search_engine",
        "code_search", "archive_search", "cached_pages",
        
        # Image & Media scanners (15)
        "reverse_image", "face_recognition", "image_metadata", "video_analysis",
        "audio_analysis", "reverse_video", "deepfake_detection", "image_forensics",
        "facial_comparison", "object_recognition", "scene_analysis", "image_similarity",
        "metadata_extraction", "steganography_check", "image_geolocation"
    ]
    
    # Create and register all scanners
    for i, name in enumerate(scanner_names):
        scanner_type = scanner_types[i % len(scanner_types)]
        description = f"{name.replace('_', ' ').title()} intelligence scanner"
        
        scanner = MockBaseScannerModule(name, scanner_type, description)
        scanner_registry.register(scanner)
    
    logger.info(f"Registered {len(scanner_registry.get_all_scanners())} scanner modules")
    return scanner_registry