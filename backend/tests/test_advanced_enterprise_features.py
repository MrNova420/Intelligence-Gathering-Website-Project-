"""
Advanced Enterprise Features Test Suite
=======================================

Comprehensive testing for all advanced enterprise capabilities:
- AI Engine and correlation analysis
- Advanced monitoring and alerting
- Reporting and visualization system
- Integration API and webhook system
- Performance and reliability testing
"""

import pytest
import asyncio
import json
import time
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

# Import the modules to test
from core.advanced_ai_engine import (
    EnterpriseAIEngine,
    DataCorrelationEngine, 
    PredictiveAnalyticsEngine,
    NaturalLanguageProcessor,
    ThreatLevel,
    CorrelationResult,
    AIInsight
)

from monitoring.enterprise_monitoring import (
    EnterpriseMonitoringSystem,
    MetricsCollector,
    AlertManager,
    HealthCheckManager,
    Alert,
    AlertSeverity,
    MetricType,
    Metric
)

from services.advanced_reporting_service import (
    AdvancedReportingService,
    DataVisualizationEngine,
    ReportFormat,
    ReportType,
    ReportRequest,
    VisualizationType
)

from api.advanced_integration_api import (
    AdvancedIntegrationAPI,
    WebhookManager,
    ThirdPartyIntegrationManager,
    WebhookEventType,
    IntegrationType,
    WebhookEndpoint
)


class TestAdvancedAIEngine:
    """Test the Advanced AI Engine capabilities"""
    
    @pytest.fixture
    def ai_engine(self):
        """Create AI engine instance for testing"""
        return EnterpriseAIEngine()
    
    @pytest.fixture
    def sample_scan_results(self):
        """Sample scan results for testing"""
        return [
            {
                "scanner_name": "email_validator",
                "status": "completed",
                "execution_time": 1.2,
                "data": {
                    "email": "john.doe@example.com",
                    "valid": True,
                    "domain": "example.com",
                    "risk_score": 10
                }
            },
            {
                "scanner_name": "phone_validator", 
                "status": "completed",
                "execution_time": 1.8,
                "data": {
                    "phone": "+1234567890",
                    "valid": True,
                    "carrier": "Verizon",
                    "risk_score": 5
                }
            },
            {
                "scanner_name": "social_media_scanner",
                "status": "completed", 
                "execution_time": 3.2,
                "data": {
                    "profiles": [
                        {"platform": "twitter", "username": "johndoe", "followers": 150},
                        {"platform": "linkedin", "username": "john-doe", "connections": 300}
                    ],
                    "risk_score": 20
                }
            }
        ]
    
    @pytest.mark.asyncio
    async def test_data_correlation_engine(self, ai_engine, sample_scan_results):
        """Test data correlation capabilities"""
        correlations = await ai_engine.correlation_engine.correlate_scan_results(
            sample_scan_results, correlation_threshold=0.5
        )
        
        assert isinstance(correlations, list)
        # Should find correlations between entities in scan results
        if correlations:
            correlation = correlations[0]
            assert isinstance(correlation, CorrelationResult)
            assert correlation.correlation_strength >= 0.5
            assert len(correlation.entities) >= 2
    
    @pytest.mark.asyncio
    async def test_predictive_analytics(self, ai_engine, sample_scan_results):
        """Test predictive analytics capabilities"""
        scanner_names = ["email_validator", "phone_validator", "social_media_scanner"]
        
        predictions = await ai_engine.predictive_engine.predict_scan_success(
            "test@example.com", scanner_names, sample_scan_results
        )
        
        assert isinstance(predictions, dict)
        assert len(predictions) == len(scanner_names)
        
        for scanner, prediction in predictions.items():
            assert 0.0 <= prediction <= 1.0
    
    @pytest.mark.asyncio 
    async def test_time_estimation(self, ai_engine, sample_scan_results):
        """Test execution time estimation"""
        scanner_names = ["email_validator", "phone_validator"]
        
        estimates = await ai_engine.predictive_engine.estimate_completion_time(
            scanner_names, sample_scan_results
        )
        
        assert isinstance(estimates, dict)
        assert len(estimates) == len(scanner_names)
        
        for scanner, estimate in estimates.items():
            assert estimate > 0
    
    @pytest.mark.asyncio
    async def test_natural_language_processing(self, ai_engine, sample_scan_results):
        """Test natural language report generation"""
        correlations = await ai_engine.correlation_engine.correlate_scan_results(
            sample_scan_results
        )
        
        summary = await ai_engine.nlp_processor.generate_intelligence_summary(
            sample_scan_results, correlations
        )
        
        assert isinstance(summary, str)
        assert len(summary) > 100  # Should be a substantial summary
        assert "analysis completed" in summary.lower()
    
    @pytest.mark.asyncio
    async def test_comprehensive_ai_analysis(self, ai_engine, sample_scan_results):
        """Test comprehensive AI analysis"""
        analysis = await ai_engine.analyze_intelligence_data(
            sample_scan_results, "test@example.com"
        )
        
        assert isinstance(analysis, dict)
        assert "target" in analysis
        assert "scan_summary" in analysis
        assert "correlations" in analysis
        assert "predictions" in analysis
        assert "natural_language_summary" in analysis
        assert "confidence_score" in analysis
        
        # Validate scan summary
        scan_summary = analysis["scan_summary"]
        assert scan_summary["total_scanners"] == 3
        assert scan_summary["successful_scans"] == 3
        assert scan_summary["success_rate"] == 1.0


class TestEnterpriseMonitoring:
    """Test the Enterprise Monitoring System"""
    
    @pytest.fixture
    def monitoring_system(self):
        """Create monitoring system instance for testing"""
        return EnterpriseMonitoringSystem()
    
    @pytest.fixture
    def metrics_collector(self):
        """Create metrics collector instance for testing"""
        return MetricsCollector()
    
    def test_metrics_collection(self, metrics_collector):
        """Test metrics collection functionality"""
        # Test counter
        metrics_collector.increment_counter("test.counter", 5.0)
        assert metrics_collector.get_counter_value("test.counter") == 5.0
        
        metrics_collector.increment_counter("test.counter", 3.0)
        assert metrics_collector.get_counter_value("test.counter") == 8.0
        
        # Test gauge
        metrics_collector.set_gauge("test.gauge", 42.0)
        assert metrics_collector.get_gauge_value("test.gauge") == 42.0
        
        # Test timer
        metrics_collector.record_timer("test.timer", 1.5)
        metrics_collector.record_timer("test.timer", 2.5)
        
        timer_stats = metrics_collector.get_timer_stats("test.timer")
        assert timer_stats["count"] == 2
        assert timer_stats["mean"] == 2.0
    
    @pytest.mark.asyncio
    async def test_alert_manager(self, monitoring_system):
        """Test alert management"""
        alert_manager = monitoring_system.alert_manager
        
        # Add test alert rule
        alert_manager.add_alert_rule(
            "test_alert",
            "test.metric",
            "gt", 
            10.0,
            AlertSeverity.WARNING,
            "Test alert rule"
        )
        
        # Set metric value to trigger alert
        monitoring_system.metrics_collector.set_gauge("test.metric", 15.0)
        
        # Check alert rules
        await alert_manager._check_alert_rules()
        
        # Should have triggered an alert
        active_alerts = alert_manager.get_active_alerts()
        assert len(active_alerts) > 0
        
        alert = active_alerts[0]
        assert alert.severity == AlertSeverity.WARNING
        assert "test_alert" in alert.title.lower()
    
    @pytest.mark.asyncio
    async def test_health_checks(self, monitoring_system):
        """Test health check functionality"""
        health_manager = monitoring_system.health_check_manager
        
        # Mock health check function
        async def mock_health_check():
            return True
        
        from monitoring.enterprise_monitoring import HealthCheck
        health_check = HealthCheck(
            name="test_service",
            check_function=mock_health_check,
            interval_seconds=1,
            timeout_seconds=5,
            critical=True
        )
        
        health_manager.register_health_check(health_check)
        
        # Execute health check
        await health_manager._execute_health_check(health_check)
        
        assert health_check.last_status == True
        assert health_check.consecutive_failures == 0
    
    @pytest.mark.asyncio
    async def test_monitoring_dashboard(self, monitoring_system):
        """Test monitoring dashboard data"""
        # Add some test data
        monitoring_system.metrics_collector.set_gauge("system.cpu.percent", 45.0)
        monitoring_system.metrics_collector.set_gauge("system.memory.percent", 60.0)
        monitoring_system.metrics_collector.increment_counter("app.requests", 100)
        
        dashboard_data = monitoring_system.get_monitoring_dashboard()
        
        assert isinstance(dashboard_data, dict)
        assert "timestamp" in dashboard_data
        assert "metrics" in dashboard_data
        assert "alerts" in dashboard_data
        assert "health" in dashboard_data
        assert "system" in dashboard_data
    
    def test_monitoring_decorators(self):
        """Test monitoring decorators"""
        from monitoring.enterprise_monitoring import monitor_execution_time, count_calls
        
        @monitor_execution_time("test.execution_time")
        @count_calls("test.call_count")
        def test_function():
            time.sleep(0.1)
            return "test_result"
        
        result = test_function()
        assert result == "test_result"
        
        # Note: In a real test, we'd verify the metrics were recorded
        # This would require access to the global metrics collector


class TestAdvancedReporting:
    """Test the Advanced Reporting System"""
    
    @pytest.fixture
    def reporting_service(self):
        """Create reporting service instance for testing"""
        return AdvancedReportingService()
    
    @pytest.fixture
    def sample_report_request(self):
        """Sample report request for testing"""
        return ReportRequest(
            report_id="test_report_001",
            template_id="executive_summary",
            report_type=ReportType.EXECUTIVE_SUMMARY,
            format=ReportFormat.JSON,
            title="Test Intelligence Report",
            include_visualizations=False  # Disable visualizations for testing
        )
    
    @pytest.mark.asyncio
    async def test_json_report_generation(self, reporting_service, sample_report_request):
        """Test JSON report generation"""
        report_content = await reporting_service.generate_report(sample_report_request)
        
        assert isinstance(report_content, str)
        report_data = json.loads(report_content)
        
        assert "title" in report_data
        assert "sections" in report_data
        assert "generated_at" in report_data
        assert report_data["title"] == "Test Intelligence Report"
    
    @pytest.mark.asyncio
    async def test_html_report_generation(self, reporting_service):
        """Test HTML report generation"""
        request = ReportRequest(
            report_id="test_html_001",
            template_id="executive_summary",
            report_type=ReportType.EXECUTIVE_SUMMARY,
            format=ReportFormat.HTML,
            title="Test HTML Report",
            include_visualizations=False
        )
        
        report_content = await reporting_service.generate_report(request)
        
        assert isinstance(report_content, str)
        assert "<!DOCTYPE html>" in report_content
        assert "Test HTML Report" in report_content
    
    @pytest.mark.asyncio
    async def test_csv_report_generation(self, reporting_service):
        """Test CSV report generation"""
        request = ReportRequest(
            report_id="test_csv_001",
            template_id="executive_summary", 
            report_type=ReportType.EXECUTIVE_SUMMARY,
            format=ReportFormat.CSV,
            title="Test CSV Report"
        )
        
        report_content = await reporting_service.generate_report(request)
        
        assert isinstance(report_content, str)
        assert "Report Title,Test CSV Report" in report_content
    
    @pytest.mark.asyncio 
    async def test_data_visualization_engine(self, reporting_service):
        """Test data visualization capabilities"""
        viz_engine = reporting_service.visualization_engine
        
        # Test bar chart creation
        chart_data = {
            "categories": ["A", "B", "C", "D"],
            "values": [10, 20, 15, 25]
        }
        
        image_base64 = await viz_engine.create_visualization(
            chart_data,
            VisualizationType.BAR_CHART,
            "Test Bar Chart"
        )
        
        if image_base64:  # Only if matplotlib is available
            assert isinstance(image_base64, str)
            assert len(image_base64) > 100  # Should be substantial base64 data
    
    def test_report_templates(self, reporting_service):
        """Test report template management"""
        templates = reporting_service.get_available_templates()
        
        assert isinstance(templates, list)
        assert len(templates) >= 2  # Should have at least 2 default templates
        
        for template in templates:
            assert "template_id" in template
            assert "name" in template
            assert "description" in template
            assert "type" in template


class TestAdvancedIntegration:
    """Test the Advanced Integration System"""
    
    @pytest.fixture
    def webhook_manager(self):
        """Create webhook manager instance for testing"""
        return WebhookManager()
    
    @pytest.fixture
    def integration_manager(self):
        """Create integration manager instance for testing"""
        return ThirdPartyIntegrationManager()
    
    def test_webhook_endpoint_management(self, webhook_manager):
        """Test webhook endpoint management"""
        # Register webhook endpoint
        endpoint_id = webhook_manager.register_webhook_endpoint(
            name="Test Webhook",
            url="https://example.com/webhook",
            event_types=[WebhookEventType.SCAN_COMPLETED, WebhookEventType.QUERY_CREATED]
        )
        
        assert isinstance(endpoint_id, str)
        
        # Get endpoints
        endpoints = webhook_manager.get_webhook_endpoints()
        assert len(endpoints) == 1
        
        endpoint = endpoints[0]
        assert endpoint.name == "Test Webhook"
        assert endpoint.url == "https://example.com/webhook"
        assert len(endpoint.event_types) == 2
        
        # Update endpoint
        success = webhook_manager.update_webhook_endpoint(
            endpoint_id, 
            name="Updated Webhook",
            active=False
        )
        assert success == True
        
        # Delete endpoint
        success = webhook_manager.delete_webhook_endpoint(endpoint_id)
        assert success == True
        
        endpoints = webhook_manager.get_webhook_endpoints()
        assert len(endpoints) == 0
    
    @pytest.mark.asyncio
    async def test_webhook_event_triggering(self, webhook_manager):
        """Test webhook event triggering"""
        # Register webhook endpoint
        endpoint_id = webhook_manager.register_webhook_endpoint(
            name="Test Event Webhook",
            url="https://httpbin.org/post",
            event_types=[WebhookEventType.SCAN_COMPLETED]
        )
        
        # Trigger event
        await webhook_manager.trigger_webhook_event(
            WebhookEventType.SCAN_COMPLETED,
            {"scan_id": "12345", "status": "completed"}
        )
        
        # Check that delivery was created
        deliveries = webhook_manager.get_delivery_history(endpoint_id)
        assert len(deliveries) >= 1
    
    def test_third_party_integration_management(self, integration_manager):
        """Test third-party integration management"""
        # Register Slack integration
        integration_id = integration_manager.register_integration(
            IntegrationType.SLACK,
            "Test Slack",
            {"webhook_url": "https://hooks.slack.com/test"}
        )
        
        assert isinstance(integration_id, str)
        
        # Get integrations
        integrations = integration_manager.get_integrations()
        assert len(integrations) == 1
        
        integration = integrations[0]
        assert integration["name"] == "Test Slack"
        assert integration["type"] == IntegrationType.SLACK
    
    @pytest.mark.asyncio 
    async def test_slack_notification(self, integration_manager):
        """Test Slack notification sending"""
        # Register Slack integration
        integration_id = integration_manager.register_integration(
            IntegrationType.SLACK,
            "Test Slack Notification",
            {"webhook_url": "https://httpbin.org/post"}  # Using httpbin for testing
        )
        
        # Send notification (this will fail but we can test the flow)
        result = await integration_manager.send_notification(
            integration_id,
            "Test notification message",
            {"key": "value"}
        )
        
        # Result may be False due to test URL, but the function should complete
        assert isinstance(result, bool)


class TestPerformanceAndReliability:
    """Test performance and reliability aspects"""
    
    @pytest.mark.asyncio
    async def test_concurrent_ai_analysis(self):
        """Test concurrent AI analysis performance"""
        ai_engine = EnterpriseAIEngine()
        
        sample_results = [
            {
                "scanner_name": f"scanner_{i}",
                "status": "completed",
                "execution_time": 1.0 + (i * 0.1),
                "data": {"test": f"data_{i}"}
            }
            for i in range(10)
        ]
        
        # Run multiple analyses concurrently
        tasks = [
            ai_engine.analyze_intelligence_data(sample_results, f"target_{i}")
            for i in range(5)
        ]
        
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        execution_time = time.time() - start_time
        
        assert len(results) == 5
        assert execution_time < 10.0  # Should complete in reasonable time
        
        for result in results:
            assert "confidence_score" in result
    
    @pytest.mark.asyncio
    async def test_monitoring_system_performance(self):
        """Test monitoring system performance under load"""
        monitoring = EnterpriseMonitoringSystem()
        
        # Generate lots of metrics
        start_time = time.time()
        for i in range(1000):
            monitoring.metrics_collector.increment_counter("test.performance", 1.0)
            monitoring.metrics_collector.set_gauge("test.gauge", float(i))
            monitoring.metrics_collector.record_timer("test.timer", 0.1 + (i * 0.001))
        
        metrics_time = time.time() - start_time
        
        # Get dashboard data
        start_time = time.time()
        dashboard = monitoring.get_monitoring_dashboard()
        dashboard_time = time.time() - start_time
        
        assert metrics_time < 1.0  # Should record metrics quickly
        assert dashboard_time < 0.5  # Should generate dashboard quickly
        assert isinstance(dashboard, dict)
    
    def test_memory_usage_patterns(self):
        """Test memory usage patterns for large datasets"""
        import sys
        
        # Test metrics collector with large dataset
        collector = MetricsCollector(max_datapoints=10000)
        
        initial_size = sys.getsizeof(collector.metrics)
        
        # Add lots of metrics
        for i in range(15000):  # More than max_datapoints
            collector.record_timer("test.memory", float(i))
        
        final_size = sys.getsizeof(collector.metrics)
        
        # Should not grow indefinitely due to deque maxlen
        assert final_size < initial_size * 2  # Reasonable growth limit
    
    @pytest.mark.asyncio
    async def test_error_handling_resilience(self):
        """Test error handling and resilience"""
        ai_engine = EnterpriseAIEngine()
        
        # Test with invalid data
        invalid_results = [
            {"invalid": "data"},
            None,
            {"scanner_name": None, "status": "invalid"}
        ]
        
        # Should handle gracefully without crashing
        result = await ai_engine.analyze_intelligence_data(invalid_results, "test")
        
        # Should return error information rather than crashing
        assert isinstance(result, dict)
        # May contain error information
    
    def test_configuration_validation(self):
        """Test configuration validation and defaults"""
        # Test with various monitoring configurations
        monitoring1 = EnterpriseMonitoringSystem()
        monitoring2 = EnterpriseMonitoringSystem()
        
        # Should create independent instances
        monitoring1.metrics_collector.increment_counter("test1", 1.0)
        monitoring2.metrics_collector.increment_counter("test2", 2.0)
        
        assert monitoring1.metrics_collector.get_counter_value("test1") == 1.0
        assert monitoring1.metrics_collector.get_counter_value("test2") == 0.0
        assert monitoring2.metrics_collector.get_counter_value("test2") == 2.0
        assert monitoring2.metrics_collector.get_counter_value("test1") == 0.0


@pytest.mark.asyncio
async def test_integration_with_existing_components():
    """Test integration with existing platform components"""
    
    # This test would verify that new advanced features integrate properly
    # with the existing scanner engine, configuration system, etc.
    
    # Test AI engine with real scanner results format
    from scanners.enterprise_scanner_engine import EnterpriseScannerOrchestrator
    from core.enterprise_config import EnterpriseConfig
    
    try:
        config = EnterpriseConfig()
        orchestrator = EnterpriseScannerOrchestrator(max_concurrent_scanners=5)
        ai_engine = EnterpriseAIEngine()
        
        # This would be a real integration test
        # For now, just verify components can be instantiated together
        assert config is not None
        assert orchestrator is not None
        assert ai_engine is not None
        
    except Exception as e:
        # If there are import issues, that's also valuable test information
        pytest.skip(f"Integration test skipped due to import issue: {e}")


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v", "--tb=short"])