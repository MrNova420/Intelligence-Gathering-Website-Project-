"""
Enterprise Business Intelligence Dashboard Module
As promised in PR #2 for comprehensive enterprise analytics and reporting
"""

import asyncio
import logging
import json
import statistics
from typing import Dict, Any, List, Optional, Tuple, Set, Union
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import uuid

logger = logging.getLogger(__name__)


class AlertLevel(Enum):
    """Business intelligence alert levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class MetricType(Enum):
    """Types of business metrics"""
    PERFORMANCE = "performance"
    USAGE = "usage"
    QUALITY = "quality"
    SECURITY = "security"
    BUSINESS = "business"


@dataclass
class BusinessMetric:
    """Business intelligence metric"""
    name: str
    value: float
    metric_type: MetricType
    timestamp: datetime
    target: Optional[float] = None
    threshold_low: Optional[float] = None
    threshold_high: Optional[float] = None
    unit: str = ""
    description: str = ""


@dataclass
class BusinessAlert:
    """Business intelligence alert"""
    id: str
    title: str
    description: str
    level: AlertLevel
    metric_name: str
    current_value: float
    threshold_value: float
    created_at: datetime
    resolved_at: Optional[datetime] = None
    acknowledged: bool = False


class BusinessIntelligenceDashboard:
    """Comprehensive business intelligence and analytics dashboard"""
    
    def __init__(self):
        self.metrics_cache = {}
        self.historical_data = defaultdict(list)
        self.active_alerts = {}
        self.kpi_definitions = self._initialize_kpis()
        self.executive_reports = {}
        
    def _initialize_kpis(self) -> Dict[str, Dict[str, Any]]:
        """Initialize key performance indicators for the intelligence platform"""
        return {
            # Platform Performance KPIs
            "scan_success_rate": {
                "name": "Scan Success Rate",
                "description": "Percentage of successful intelligence scans",
                "target": 95.0,
                "threshold_low": 85.0,
                "unit": "%",
                "metric_type": MetricType.PERFORMANCE
            },
            "average_scan_time": {
                "name": "Average Scan Duration",
                "description": "Average time to complete intelligence scans",
                "target": 30.0,
                "threshold_high": 60.0,
                "unit": "seconds",
                "metric_type": MetricType.PERFORMANCE
            },
            "scanner_availability": {
                "name": "Scanner Module Availability",
                "description": "Percentage of scanner modules operational",
                "target": 98.0,
                "threshold_low": 90.0,
                "unit": "%",
                "metric_type": MetricType.PERFORMANCE
            },
            
            # Usage and Adoption KPIs
            "daily_active_users": {
                "name": "Daily Active Users",
                "description": "Number of unique users per day",
                "target": 100.0,
                "threshold_low": 50.0,
                "unit": "users",
                "metric_type": MetricType.USAGE
            },
            "scans_per_day": {
                "name": "Daily Scan Volume",
                "description": "Total number of scans performed daily",
                "target": 1000.0,
                "threshold_low": 500.0,
                "unit": "scans",
                "metric_type": MetricType.USAGE
            },
            "api_requests_per_minute": {
                "name": "API Request Rate",
                "description": "API requests per minute",
                "target": 100.0,
                "threshold_high": 500.0,
                "unit": "requests/min",
                "metric_type": MetricType.USAGE
            },
            
            # Data Quality KPIs
            "data_confidence_score": {
                "name": "Average Data Confidence",
                "description": "Average confidence score across all scans",
                "target": 85.0,
                "threshold_low": 70.0,
                "unit": "%",
                "metric_type": MetricType.QUALITY
            },
            "source_reliability": {
                "name": "Source Reliability Index",
                "description": "Reliability index of intelligence sources",
                "target": 90.0,
                "threshold_low": 80.0,
                "unit": "%",
                "metric_type": MetricType.QUALITY
            },
            
            # Security KPIs
            "security_incidents": {
                "name": "Security Incidents",
                "description": "Number of security incidents detected",
                "target": 0.0,
                "threshold_high": 1.0,
                "unit": "incidents",
                "metric_type": MetricType.SECURITY
            },
            "authentication_failures": {
                "name": "Authentication Failures",
                "description": "Failed authentication attempts per hour",
                "target": 0.0,
                "threshold_high": 10.0,
                "unit": "failures/hour",
                "metric_type": MetricType.SECURITY
            },
            
            # Business KPIs
            "subscription_conversion_rate": {
                "name": "Subscription Conversion Rate",
                "description": "Percentage of users converting to paid plans",
                "target": 10.0,
                "threshold_low": 5.0,
                "unit": "%",
                "metric_type": MetricType.BUSINESS
            },
            "revenue_per_user": {
                "name": "Average Revenue Per User",
                "description": "Monthly revenue per active user",
                "target": 25.0,
                "threshold_low": 15.0,
                "unit": "$",
                "metric_type": MetricType.BUSINESS
            },
            "customer_satisfaction": {
                "name": "Customer Satisfaction Score",
                "description": "Average customer satisfaction rating",
                "target": 4.5,
                "threshold_low": 4.0,
                "unit": "/5",
                "metric_type": MetricType.BUSINESS
            }
        }
    
    async def collect_platform_metrics(self) -> Dict[str, BusinessMetric]:
        """Collect current platform metrics for business intelligence"""
        current_time = datetime.utcnow()
        metrics = {}
        
        # Simulate metric collection (replace with actual data sources)
        platform_data = await self._gather_platform_data()
        
        for kpi_id, kpi_config in self.kpi_definitions.items():
            value = await self._calculate_metric_value(kpi_id, platform_data)
            
            metric = BusinessMetric(
                name=kpi_config["name"],
                value=value,
                metric_type=kpi_config["metric_type"],
                timestamp=current_time,
                target=kpi_config.get("target"),
                threshold_low=kpi_config.get("threshold_low"),
                threshold_high=kpi_config.get("threshold_high"),
                unit=kpi_config.get("unit", ""),
                description=kpi_config.get("description", "")
            )
            
            metrics[kpi_id] = metric
            
            # Store historical data
            self.historical_data[kpi_id].append({
                "timestamp": current_time.isoformat(),
                "value": value
            })
            
            # Check for alerts
            await self._check_metric_thresholds(kpi_id, metric)
        
        self.metrics_cache = metrics
        return metrics
    
    async def _gather_platform_data(self) -> Dict[str, Any]:
        """Gather platform operational data for metrics calculation"""
        # Simulate gathering data from various platform components
        # In real implementation, this would query actual databases and services
        
        return {
            "total_scans_today": 847,
            "successful_scans_today": 803,
            "failed_scans_today": 44,
            "active_users_today": 127,
            "total_api_requests": 15420,
            "scanner_modules_up": 96,
            "total_scanner_modules": 98,
            "average_scan_duration": 28.5,
            "confidence_scores": [85.2, 90.1, 78.9, 88.7, 92.3, 81.4, 89.0],
            "subscription_conversions": 13,
            "total_trials": 145,
            "security_events": 0,
            "auth_failures": 3,
            "customer_ratings": [4.8, 4.2, 4.7, 4.9, 4.3, 4.6, 4.8, 4.5],
            "revenue_data": 3247.50
        }
    
    async def _calculate_metric_value(self, metric_id: str, platform_data: Dict[str, Any]) -> float:
        """Calculate specific metric values from platform data"""
        
        if metric_id == "scan_success_rate":
            total = platform_data["successful_scans_today"] + platform_data["failed_scans_today"]
            return (platform_data["successful_scans_today"] / total * 100) if total > 0 else 0.0
        
        elif metric_id == "average_scan_time":
            return platform_data["average_scan_duration"]
        
        elif metric_id == "scanner_availability":
            return (platform_data["scanner_modules_up"] / platform_data["total_scanner_modules"]) * 100
        
        elif metric_id == "daily_active_users":
            return float(platform_data["active_users_today"])
        
        elif metric_id == "scans_per_day":
            return float(platform_data["total_scans_today"])
        
        elif metric_id == "api_requests_per_minute":
            return platform_data["total_api_requests"] / (24 * 60)  # Rough estimate
        
        elif metric_id == "data_confidence_score":
            return statistics.mean(platform_data["confidence_scores"])
        
        elif metric_id == "source_reliability":
            return 89.5  # Simulated source reliability index
        
        elif metric_id == "security_incidents":
            return float(platform_data["security_events"])
        
        elif metric_id == "authentication_failures":
            return float(platform_data["auth_failures"])
        
        elif metric_id == "subscription_conversion_rate":
            return (platform_data["subscription_conversions"] / platform_data["total_trials"]) * 100
        
        elif metric_id == "revenue_per_user":
            return platform_data["revenue_data"] / platform_data["active_users_today"]
        
        elif metric_id == "customer_satisfaction":
            return statistics.mean(platform_data["customer_ratings"])
        
        else:
            return 0.0
    
    async def _check_metric_thresholds(self, metric_id: str, metric: BusinessMetric):
        """Check metric against thresholds and generate alerts if needed"""
        kpi_config = self.kpi_definitions[metric_id]
        alert_needed = False
        alert_level = AlertLevel.INFO
        alert_description = ""
        
        # Check low threshold
        if metric.threshold_low and metric.value < metric.threshold_low:
            alert_needed = True
            alert_level = AlertLevel.HIGH if metric.value < (metric.threshold_low * 0.8) else AlertLevel.MEDIUM
            alert_description = f"{metric.name} is below threshold: {metric.value:.2f}{metric.unit} < {metric.threshold_low:.2f}{metric.unit}"
        
        # Check high threshold
        elif metric.threshold_high and metric.value > metric.threshold_high:
            alert_needed = True
            alert_level = AlertLevel.CRITICAL if metric.value > (metric.threshold_high * 1.2) else AlertLevel.HIGH
            alert_description = f"{metric.name} exceeds threshold: {metric.value:.2f}{metric.unit} > {metric.threshold_high:.2f}{metric.unit}"
        
        if alert_needed:
            alert_id = f"{metric_id}_{int(metric.timestamp.timestamp())}"
            
            alert = BusinessAlert(
                id=alert_id,
                title=f"{metric.name} Alert",
                description=alert_description,
                level=alert_level,
                metric_name=metric.name,
                current_value=metric.value,
                threshold_value=metric.threshold_low or metric.threshold_high,
                created_at=metric.timestamp
            )
            
            self.active_alerts[alert_id] = alert
            logger.warning(f"Business Intelligence Alert: {alert_description}")
    
    async def generate_executive_dashboard(self) -> Dict[str, Any]:
        """Generate executive-level dashboard with key insights"""
        metrics = await self.collect_platform_metrics()
        
        # Categorize metrics for executive view
        performance_metrics = {k: v for k, v in metrics.items() 
                             if v.metric_type == MetricType.PERFORMANCE}
        business_metrics = {k: v for k, v in metrics.items() 
                          if v.metric_type == MetricType.BUSINESS}
        security_metrics = {k: v for k, v in metrics.items() 
                          if v.metric_type == MetricType.SECURITY}
        
        # Calculate trends (simplified - would use more historical data in production)
        trends = await self._calculate_trends(metrics)
        
        # Generate insights
        insights = await self._generate_executive_insights(metrics, trends)
        
        # Active alerts summary
        critical_alerts = [alert for alert in self.active_alerts.values() 
                          if alert.level == AlertLevel.CRITICAL and not alert.acknowledged]
        
        dashboard = {
            "generated_at": datetime.utcnow().isoformat(),
            "summary": {
                "platform_health": self._calculate_overall_health(metrics),
                "total_metrics": len(metrics),
                "active_alerts": len(self.active_alerts),
                "critical_alerts": len(critical_alerts)
            },
            "key_performance_indicators": {
                "performance": {k: asdict(v) for k, v in performance_metrics.items()},
                "business": {k: asdict(v) for k, v in business_metrics.items()},
                "security": {k: asdict(v) for k, v in security_metrics.items()}
            },
            "trends": trends,
            "insights": insights,
            "alerts": {
                "critical": [asdict(alert) for alert in critical_alerts],
                "total_active": len(self.active_alerts)
            },
            "recommendations": await self._generate_recommendations(metrics, trends)
        }
        
        # Cache the executive report
        report_id = f"executive_{int(datetime.utcnow().timestamp())}"
        self.executive_reports[report_id] = dashboard
        
        return dashboard
    
    async def _calculate_trends(self, current_metrics: Dict[str, BusinessMetric]) -> Dict[str, Dict[str, Any]]:
        """Calculate metric trends over time"""
        trends = {}
        
        for metric_id, metric in current_metrics.items():
            historical = self.historical_data.get(metric_id, [])
            
            if len(historical) >= 2:
                # Calculate simple trend (would use more sophisticated analysis in production)
                recent_values = [point["value"] for point in historical[-7:]]  # Last 7 data points
                trend_direction = "stable"
                trend_percentage = 0.0
                
                if len(recent_values) >= 2:
                    if recent_values[-1] > recent_values[0]:
                        trend_direction = "increasing"
                        trend_percentage = ((recent_values[-1] - recent_values[0]) / recent_values[0]) * 100
                    elif recent_values[-1] < recent_values[0]:
                        trend_direction = "decreasing"
                        trend_percentage = ((recent_values[0] - recent_values[-1]) / recent_values[0]) * 100
                
                trends[metric_id] = {
                    "direction": trend_direction,
                    "percentage": round(trend_percentage, 2),
                    "volatility": round(statistics.stdev(recent_values) if len(recent_values) > 1 else 0, 2),
                    "data_points": len(recent_values)
                }
            else:
                trends[metric_id] = {
                    "direction": "insufficient_data",
                    "percentage": 0.0,
                    "volatility": 0.0,
                    "data_points": len(historical)
                }
        
        return trends
    
    async def _generate_executive_insights(self, metrics: Dict[str, BusinessMetric], 
                                         trends: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate executive-level insights from metrics and trends"""
        insights = []
        
        # Platform performance insight
        scan_success_rate = metrics.get("scan_success_rate")
        if scan_success_rate and scan_success_rate.value >= 95:
            insights.append({
                "type": "positive",
                "title": "Excellent Platform Reliability",
                "description": f"Scan success rate of {scan_success_rate.value:.1f}% exceeds target performance",
                "impact": "high",
                "category": "performance"
            })
        
        # Business growth insight
        conversion_rate = metrics.get("subscription_conversion_rate")
        if conversion_rate and trends.get("subscription_conversion_rate", {}).get("direction") == "increasing":
            insights.append({
                "type": "positive",
                "title": "Growing Subscription Conversions",
                "description": f"Conversion rate trending upward at {conversion_rate.value:.1f}%",
                "impact": "high",
                "category": "business"
            })
        
        # Security insight
        security_incidents = metrics.get("security_incidents")
        if security_incidents and security_incidents.value == 0:
            insights.append({
                "type": "positive",
                "title": "Strong Security Posture",
                "description": "Zero security incidents detected in current period",
                "impact": "medium",
                "category": "security"
            })
        
        # Usage insight
        active_users = metrics.get("daily_active_users")
        user_trend = trends.get("daily_active_users", {})
        if active_users and user_trend.get("direction") == "increasing":
            insights.append({
                "type": "positive",
                "title": "User Engagement Growing",
                "description": f"Daily active users increasing by {user_trend.get('percentage', 0):.1f}%",
                "impact": "high",
                "category": "usage"
            })
        
        return insights
    
    async def _generate_recommendations(self, metrics: Dict[str, BusinessMetric], 
                                      trends: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate actionable recommendations based on metrics analysis"""
        recommendations = []
        
        # Performance recommendations
        avg_scan_time = metrics.get("average_scan_time")
        if avg_scan_time and avg_scan_time.value > 45:
            recommendations.append({
                "priority": "high",
                "category": "performance",
                "title": "Optimize Scan Performance",
                "description": f"Average scan time of {avg_scan_time.value:.1f}s exceeds optimal range",
                "action_items": [
                    "Review scanner module efficiency",
                    "Implement additional caching layers",
                    "Consider parallel processing optimization"
                ],
                "expected_impact": "Reduce scan time by 20-30%"
            })
        
        # Business recommendations
        conversion_rate = metrics.get("subscription_conversion_rate")
        if conversion_rate and conversion_rate.value < 8:
            recommendations.append({
                "priority": "medium",
                "category": "business",
                "title": "Improve Conversion Strategy",
                "description": f"Conversion rate of {conversion_rate.value:.1f}% is below industry average",
                "action_items": [
                    "A/B test pricing strategies",
                    "Enhance free tier value proposition",
                    "Implement targeted upgrade campaigns"
                ],
                "expected_impact": "Increase conversion rate by 2-4%"
            })
        
        # Security recommendations
        auth_failures = metrics.get("authentication_failures")
        if auth_failures and auth_failures.value > 5:
            recommendations.append({
                "priority": "high",
                "category": "security",
                "title": "Strengthen Authentication Security",
                "description": f"{auth_failures.value:.0f} authentication failures detected",
                "action_items": [
                    "Implement additional rate limiting",
                    "Review suspicious IP patterns",
                    "Consider implementing CAPTCHA for repeated failures"
                ],
                "expected_impact": "Reduce authentication attacks by 80%"
            })
        
        return recommendations
    
    def _calculate_overall_health(self, metrics: Dict[str, BusinessMetric]) -> str:
        """Calculate overall platform health score"""
        health_scores = []
        
        for metric in metrics.values():
            if metric.target:
                # Calculate health as percentage of target achievement
                score = min(100, (metric.value / metric.target) * 100)
                health_scores.append(score)
        
        if not health_scores:
            return "unknown"
        
        avg_health = statistics.mean(health_scores)
        
        if avg_health >= 95:
            return "excellent"
        elif avg_health >= 85:
            return "good"
        elif avg_health >= 70:
            return "fair"
        else:
            return "needs_attention"
    
    async def get_real_time_dashboard(self) -> Dict[str, Any]:
        """Get real-time dashboard data for live monitoring"""
        current_metrics = await self.collect_platform_metrics()
        
        # Real-time system status
        system_status = {
            "timestamp": datetime.utcnow().isoformat(),
            "status": "operational",
            "uptime": "99.9%",  # Would calculate from actual uptime data
            "response_time": "250ms",  # Would measure actual response times
            "active_connections": 127,  # Would get from connection pool
            "queue_depth": 3  # Would get from task queue
        }
        
        # Live performance metrics
        live_metrics = {
            "scans_per_minute": 12.5,
            "success_rate_last_hour": 96.8,
            "avg_confidence_last_hour": 87.2,
            "api_requests_per_second": 15.7
        }
        
        # Recent alerts (last 24 hours)
        recent_alerts = [
            alert for alert in self.active_alerts.values()
            if (datetime.utcnow() - alert.created_at).total_seconds() < 86400
        ]
        
        return {
            "system_status": system_status,
            "live_metrics": live_metrics,
            "current_kpis": {k: asdict(v) for k, v in current_metrics.items()},
            "recent_alerts": [asdict(alert) for alert in recent_alerts[-5:]],  # Last 5 alerts
            "health_score": self._calculate_overall_health(current_metrics)
        }


# Global business intelligence dashboard instance
business_intelligence = BusinessIntelligenceDashboard()