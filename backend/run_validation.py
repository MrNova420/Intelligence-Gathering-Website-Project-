#!/usr/bin/env python3
"""
Intelligence Gathering Platform - Validation Suite
Validates that all major components are properly implemented
"""

import sys
import traceback
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def validate_scanner_modules():
    """Validate scanner module implementations"""
    print("🔍 Validating Scanner Modules...")
    
    try:
        # Test email scanners
        from app.scanners.email_scanners import EmailValidator, EmailReputation, EmailBreach, SocialMediaEmail
        
        # Test phone scanners  
        from app.scanners.phone_scanners import PhoneValidator, PhoneLocation, PhoneSpam, PhoneCarrier
        
        # Test social scanners
        from app.scanners.social_scanners import TwitterScanner, LinkedInScanner, InstagramScanner, FacebookScanner, GitHubScanner
        
        # Test basic functionality
        email_scanner = EmailValidator()
        phone_scanner = PhoneValidator()
        social_scanner = TwitterScanner()
        
        print("  ✅ All scanner modules imported successfully")
        print(f"  ✅ Email scanner: {email_scanner.name}")
        print(f"  ✅ Phone scanner: {phone_scanner.name}")
        print(f"  ✅ Social scanner: {social_scanner.name}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Scanner validation failed: {e}")
        traceback.print_exc()
        return False

def validate_aggregation_engine():
    """Validate aggregation engine implementation"""
    print("\n🧠 Validating Aggregation Engine...")
    
    try:
        from app.core.aggregation_engine import DataAggregationEngine
        
        engine = DataAggregationEngine()
        
        # Test normalization
        test_email = "test.user+tag@gmail.com"
        normalized = engine.normalize_email(test_email)
        print(f"  ✅ Email normalization: {test_email} -> {normalized}")
        
        # Test phone normalization
        test_phone = "(555) 123-4567"
        normalized_phone = engine.normalize_phone(test_phone)
        print(f"  ✅ Phone normalization: {test_phone} -> {normalized_phone}")
        
        # Test deduplication
        test_data = [
            {"email": "test@example.com", "name": "John Doe"},
            {"email": "test@example.com", "name": "J. Doe"}
        ]
        deduplicated = engine.deduplicate_entities(test_data)
        print(f"  ✅ Deduplication: {len(test_data)} -> {len(deduplicated)} records")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Aggregation engine validation failed: {e}")
        traceback.print_exc()
        return False

def validate_report_generator():
    """Validate report generator implementation"""
    print("\n📄 Validating Report Generator...")
    
    try:
        from app.core.report_generator import ReportGenerator
        
        generator = ReportGenerator()
        
        # Test subscription logic
        subscription_tiers = generator.get_subscription_features()
        print(f"  ✅ Subscription tiers: {list(subscription_tiers.keys())}")
        
        # Test report filtering
        test_data = {
            "email": "test@example.com",
            "phone": "+1234567890",
            "social_profiles": ["twitter.com/test"],
            "breach_data": "sensitive info"
        }
        
        filtered_free = generator.filter_data_by_subscription(test_data, "free")
        filtered_professional = generator.filter_data_by_subscription(test_data, "professional")
        
        print(f"  ✅ Free tier filtering: {len(filtered_free)} fields")
        print(f"  ✅ Professional tier filtering: {len(filtered_professional)} fields")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Report generator validation failed: {e}")
        traceback.print_exc()
        return False

def validate_security_system():
    """Validate security system implementation"""
    print("\n🛡️ Validating Security System...")
    
    try:
        from app.core.enhanced_security import SecurityManager, MFAManager, RBACManager
        
        # Test security manager
        security_manager = SecurityManager()
        
        # Test password validation
        weak_password = "123456"
        strong_password = "MyStr0ng!P@ssw0rd#2024"
        
        weak_score = security_manager.calculate_password_strength(weak_password)
        strong_score = security_manager.calculate_password_strength(strong_password)
        
        print(f"  ✅ Password strength scoring: weak={weak_score}, strong={strong_score}")
        
        # Test MFA manager
        mfa_manager = MFAManager()
        secret_data = mfa_manager.generate_secret("test@example.com")
        
        print(f"  ✅ MFA secret generation: {len(secret_data['secret'])} chars")
        print(f"  ✅ QR code generation: {len(secret_data['qr_code'])} chars")
        
        # Test RBAC manager
        rbac_manager = RBACManager()
        permissions = rbac_manager.get_role_permissions("premium")
        
        print(f"  ✅ RBAC permissions for premium: {len(permissions)} permissions")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Security system validation failed: {e}")
        traceback.print_exc()
        return False

def validate_performance_optimizer():
    """Validate performance optimization implementation"""
    print("\n⚡ Validating Performance Optimizer...")
    
    try:
        from app.core.performance_optimizer import RedisCache, PerformanceMonitor, AsyncScannerOrchestrator, CacheManager
        
        # Test Redis cache (mock mode)
        cache = RedisCache()
        cache_key = cache.generate_cache_key("email", "test@example.com")
        print(f"  ✅ Cache key generation: {cache_key}")
        
        # Test performance monitor
        monitor = PerformanceMonitor()
        metrics = monitor.get_system_metrics()
        print(f"  ✅ System metrics: {len(metrics)} metrics collected")
        
        # Test async orchestrator
        cache_manager = CacheManager()
        orchestrator = AsyncScannerOrchestrator(cache_manager)
        print(f"  ✅ Async orchestrator initialized with cache manager")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Performance optimizer validation failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run comprehensive validation"""
    print("🚀 Intelligence Gathering Platform - Validation Suite")
    print("=" * 60)
    
    results = []
    
    # Run all validations
    results.append(("Scanner Modules", validate_scanner_modules()))
    results.append(("Aggregation Engine", validate_aggregation_engine()))
    results.append(("Report Generator", validate_report_generator()))
    results.append(("Security System", validate_security_system()))
    results.append(("Performance Optimizer", validate_performance_optimizer()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 VALIDATION RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for component, success in results:
        if success:
            print(f"✅ {component}: PASSED")
            passed += 1
        else:
            print(f"❌ {component}: FAILED")
            failed += 1
    
    print(f"\n📈 Overall Score: {passed}/{len(results)} components validated")
    
    if failed == 0:
        print("🎉 ALL VALIDATIONS PASSED - PLATFORM READY!")
        return 0
    else:
        print(f"⚠️  {failed} VALIDATIONS FAILED - REVIEW REQUIRED")
        return 1

if __name__ == "__main__":
    sys.exit(main())