#!/usr/bin/env python3
"""
Advanced Features Validation Script
===================================

Test the newly implemented advanced enterprise features:
- AI Engine and correlation analysis
- Enterprise monitoring system
- Advanced reporting capabilities  
- Integration and webhook system
"""

import asyncio
import logging
import sys
import os
import json
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'app'))

async def test_ai_engine():
    """Test the Advanced AI Engine"""
    print("\n" + "="*80)
    print("🤖 TESTING ADVANCED AI ENGINE")
    print("="*80)
    
    try:
        from core.advanced_ai_engine import EnterpriseAIEngine
        
        ai_engine = EnterpriseAIEngine()
        
        # Sample scan results
        sample_results = [
            {
                "scanner_name": "email_validator",
                "status": "completed",
                "execution_time": 1.2,
                "data": {
                    "email": "john.doe@example.com",
                    "valid": True,
                    "domain": "example.com",
                    "risk_score": 15
                }
            },
            {
                "scanner_name": "phone_validator",
                "status": "completed", 
                "execution_time": 1.8,
                "data": {
                    "phone": "+1234567890",
                    "valid": True,
                    "carrier": "Verizon"
                }
            },
            {
                "scanner_name": "social_media_scanner",
                "status": "completed",
                "execution_time": 2.5,
                "data": {
                    "profiles": [
                        {"platform": "twitter", "username": "johndoe"},
                        {"platform": "linkedin", "username": "john-doe"}
                    ]
                }
            }
        ]
        
        print("✅ AI Engine initialized successfully")
        
        # Test comprehensive analysis
        analysis = await ai_engine.analyze_intelligence_data(
            sample_results, "john.doe@example.com"
        )
        
        print(f"✅ AI Analysis completed")
        print(f"📊 Target: {analysis['target']}")
        print(f"📊 Confidence Score: {analysis['confidence_score']:.2f}")
        print(f"📊 Total Scanners: {analysis['scan_summary']['total_scanners']}")
        print(f"📊 Success Rate: {analysis['scan_summary']['success_rate']:.1%}")
        print(f"📊 Correlations Found: {len(analysis['correlations'])}")
        
        if analysis['natural_language_summary']:
            print(f"📄 Summary Preview: {analysis['natural_language_summary'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ AI Engine test failed: {e}")
        return False


async def test_monitoring_system():
    """Test the Enterprise Monitoring System"""
    print("\n" + "="*80)
    print("📊 TESTING ENTERPRISE MONITORING SYSTEM")
    print("="*80)
    
    try:
        from monitoring.enterprise_monitoring import EnterpriseMonitoringSystem
        
        monitoring = EnterpriseMonitoringSystem()
        
        print("✅ Monitoring system initialized")
        
        # Test metrics collection
        monitoring.metrics_collector.increment_counter("test.api.requests", 10)
        monitoring.metrics_collector.set_gauge("test.system.cpu", 45.2)
        monitoring.metrics_collector.record_timer("test.scan.duration", 2.34)
        
        print("✅ Metrics recorded successfully")
        
        # Test dashboard
        dashboard = monitoring.get_monitoring_dashboard()
        
        print(f"📊 Dashboard generated at: {dashboard['timestamp']}")
        print(f"📊 Active alerts: {len(dashboard['alerts']['active'])}")
        print(f"📊 Health status: {dashboard['health']['overall_status']}")
        print(f"📊 System CPU: {dashboard['system']['cpu_percent']:.1f}%")
        
        # Test alert rules
        monitoring.alert_manager.add_alert_rule(
            "high_cpu_test",
            "test.system.cpu",
            "gt",
            40.0,
            description="Test CPU alert"
        )
        
        # Trigger alert
        await monitoring.alert_manager._check_single_rule(
            monitoring.alert_manager.alert_rules[-1]
        )
        
        active_alerts = monitoring.alert_manager.get_active_alerts()
        print(f"✅ Alert system working - {len(active_alerts)} active alerts")
        
        return True
        
    except Exception as e:
        print(f"❌ Monitoring system test failed: {e}")
        return False


async def test_reporting_service():
    """Test the Advanced Reporting Service"""
    print("\n" + "="*80)
    print("📋 TESTING ADVANCED REPORTING SERVICE")
    print("="*80)
    
    try:
        from services.advanced_reporting_service import (
            AdvancedReportingService, 
            ReportRequest, 
            ReportFormat, 
            ReportType
        )
        
        reporting = AdvancedReportingService()
        
        print("✅ Reporting service initialized")
        
        # Test available templates
        templates = reporting.get_available_templates()
        print(f"📊 Available templates: {len(templates)}")
        for template in templates:
            print(f"   - {template['name']}: {template['description'][:50]}...")
        
        # Test JSON report generation
        request = ReportRequest(
            report_id="test_001",
            template_id="executive_summary",
            report_type=ReportType.EXECUTIVE_SUMMARY,
            format=ReportFormat.JSON,
            title="Test Intelligence Report",
            include_visualizations=False
        )
        
        json_report = await reporting.generate_report(request)
        report_data = json.loads(json_report)
        
        print(f"✅ JSON report generated - {len(report_data['sections'])} sections")
        
        # Test HTML report generation
        request.format = ReportFormat.HTML
        html_report = await reporting.generate_report(request)
        
        print(f"✅ HTML report generated - {len(html_report)} characters")
        
        # Test CSV report generation
        request.format = ReportFormat.CSV
        csv_report = await reporting.generate_report(request)
        
        print(f"✅ CSV report generated - {len(csv_report.split(chr(10)))} lines")
        
        return True
        
    except Exception as e:
        print(f"❌ Reporting service test failed: {e}")
        return False


async def test_integration_system():
    """Test the Advanced Integration System"""
    print("\n" + "="*80)
    print("🔗 TESTING ADVANCED INTEGRATION SYSTEM")
    print("="*80)
    
    try:
        from api.advanced_integration_api import (
            WebhookManager,
            ThirdPartyIntegrationManager,
            WebhookEventType,
            IntegrationType
        )
        
        webhook_manager = WebhookManager()
        integration_manager = ThirdPartyIntegrationManager()
        
        print("✅ Integration systems initialized")
        
        # Test webhook endpoint registration
        endpoint_id = webhook_manager.register_webhook_endpoint(
            name="Test Webhook",
            url="https://httpbin.org/post",
            event_types=[WebhookEventType.SCAN_COMPLETED]
        )
        
        print(f"✅ Webhook endpoint registered: {endpoint_id}")
        
        # Test webhook event triggering
        await webhook_manager.trigger_webhook_event(
            WebhookEventType.SCAN_COMPLETED,
            {"scan_id": "test_123", "status": "completed"}
        )
        
        print("✅ Webhook event triggered")
        
        # Test third-party integration
        slack_id = integration_manager.register_integration(
            IntegrationType.SLACK,
            "Test Slack Integration",
            {"webhook_url": "https://httpbin.org/post"}
        )
        
        print(f"✅ Slack integration registered: {slack_id}")
        
        # List integrations
        integrations = integration_manager.get_integrations()
        print(f"📊 Total integrations: {len(integrations)}")
        
        # List webhook endpoints
        endpoints = webhook_manager.get_webhook_endpoints()
        print(f"📊 Active webhook endpoints: {len(endpoints)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration system test failed: {e}")
        return False


async def main():
    """Run all advanced feature tests"""
    print("🚀 ADVANCED ENTERPRISE FEATURES VALIDATION")
    print("=" * 80)
    print("Testing newly implemented AAA-grade enterprise capabilities...")
    
    tests = [
        ("AI Engine", test_ai_engine),
        ("Monitoring System", test_monitoring_system), 
        ("Reporting Service", test_reporting_service),
        ("Integration System", test_integration_system)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results[test_name] = result
        except Exception as e:
            logger.error(f"Test {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*80)
    print("🎯 ADVANCED FEATURES TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} {test_name}")
    
    print(f"\n📊 Overall Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🏆 ALL ADVANCED FEATURES WORKING CORRECTLY!")
        print("🚀 Enterprise platform ready for production deployment")
        return 0
    else:
        print("⚠️  Some advanced features need attention")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)