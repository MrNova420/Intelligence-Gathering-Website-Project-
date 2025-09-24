"""
Enterprise Analytics Service
===========================

Advanced analytics and business intelligence service for comprehensive
platform insights, user behavior analysis, and performance optimization.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import json
import statistics
from collections import defaultdict, Counter

logger = logging.getLogger(__name__)


class AnalyticsTimeframe(Enum):
    """Analytics time frame options."""
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"


class MetricType(Enum):
    """Types of metrics tracked."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"


@dataclass
class AnalyticsEvent:
    """Individual analytics event."""
    event_id: str
    user_id: Optional[str]
    session_id: Optional[str]
    event_type: str
    event_name: str
    timestamp: datetime
    properties: Dict[str, Any]
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


@dataclass
class UserBehaviorMetrics:
    """User behavior analytics."""
    user_id: str
    total_sessions: int
    total_queries: int
    total_scans: int
    avg_session_duration: float
    favorite_scanners: List[str]
    success_rate: float
    last_activity: datetime
    subscription_plan: str
    retention_score: float


@dataclass
class PlatformMetrics:
    """Overall platform performance metrics."""
    total_users: int
    active_users_24h: int
    active_users_7d: int
    active_users_30d: int
    total_queries: int
    total_scans: int
    avg_response_time: float
    error_rate: float
    top_scanners: List[Tuple[str, int]]
    revenue_metrics: Dict[str, float]


@dataclass
class PerformanceInsight:
    """Performance analysis insight."""
    insight_type: str
    title: str
    description: str
    severity: str  # low, medium, high, critical
    impact_score: float
    recommended_actions: List[str]
    metrics: Dict[str, Any]


class EnterpriseAnalyticsService:
    """
    Enterprise analytics service providing comprehensive insights
    into platform performance, user behavior, and business metrics.
    """
    
    def __init__(self):
        self.events_storage: List[AnalyticsEvent] = []
        self.metrics_storage: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.user_sessions: Dict[str, Dict[str, Any]] = {}
        self.performance_baselines: Dict[str, float] = {}
        
        # Initialize baseline metrics
        self._initialize_baselines()
    
    def _initialize_baselines(self):
        """Initialize performance baselines for comparison."""
        self.performance_baselines = {
            "avg_response_time": 2.0,  # seconds
            "error_rate": 0.05,  # 5%
            "user_satisfaction": 0.85,  # 85%
            "query_success_rate": 0.92,  # 92%
            "scanner_availability": 0.99,  # 99%
        }
    
    async def track_event(self, event: AnalyticsEvent):
        """Track an analytics event."""
        self.events_storage.append(event)
        
        # Update user session tracking
        if event.user_id and event.session_id:
            await self._update_user_session(event)
        
        # Trigger real-time analytics if needed
        await self._process_real_time_analytics(event)
    
    async def _update_user_session(self, event: AnalyticsEvent):
        """Update user session information."""
        session_key = f"{event.user_id}:{event.session_id}"
        
        if session_key not in self.user_sessions:
            self.user_sessions[session_key] = {
                "user_id": event.user_id,
                "session_id": event.session_id,
                "start_time": event.timestamp,
                "last_activity": event.timestamp,
                "events": [],
                "page_views": 0,
                "queries": 0,
                "errors": 0
            }
        
        session = self.user_sessions[session_key]
        session["last_activity"] = event.timestamp
        session["events"].append({
            "type": event.event_type,
            "name": event.event_name,
            "timestamp": event.timestamp,
            "properties": event.properties
        })
        
        # Update session metrics based on event type
        if event.event_type == "page_view":
            session["page_views"] += 1
        elif event.event_type == "query_submitted":
            session["queries"] += 1
        elif event.event_type == "error":
            session["errors"] += 1
    
    async def _process_real_time_analytics(self, event: AnalyticsEvent):
        """Process real-time analytics for immediate insights."""
        # Check for anomalies or patterns that need immediate attention
        if event.event_type == "error":
            await self._check_error_patterns(event)
        elif event.event_type == "performance":
            await self._check_performance_degradation(event)
    
    async def _check_error_patterns(self, event: AnalyticsEvent):
        """Check for concerning error patterns."""
        # Count recent errors
        recent_errors = [
            e for e in self.events_storage[-100:]  # Last 100 events
            if e.event_type == "error" and 
            (datetime.utcnow() - e.timestamp).total_seconds() < 300  # Last 5 minutes
        ]
        
        if len(recent_errors) > 10:  # More than 10 errors in 5 minutes
            logger.warning(f"🚨 High error rate detected: {len(recent_errors)} errors in 5 minutes")
    
    async def _check_performance_degradation(self, event: AnalyticsEvent):
        """Check for performance degradation."""
        if "response_time" in event.properties:
            response_time = event.properties["response_time"]
            baseline = self.performance_baselines.get("avg_response_time", 2.0)
            
            if response_time > baseline * 2:  # Response time 2x baseline
                logger.warning(f"⚠️ Slow response detected: {response_time}s (baseline: {baseline}s)")
    
    async def get_user_behavior_analytics(self, user_id: str, 
                                        timeframe: AnalyticsTimeframe = AnalyticsTimeframe.MONTH) -> UserBehaviorMetrics:
        """Get comprehensive user behavior analytics."""
        # Filter events for user and timeframe
        cutoff_date = self._get_cutoff_date(timeframe)
        user_events = [
            e for e in self.events_storage 
            if e.user_id == user_id and e.timestamp >= cutoff_date
        ]
        
        if not user_events:
            return UserBehaviorMetrics(
                user_id=user_id,
                total_sessions=0,
                total_queries=0,
                total_scans=0,
                avg_session_duration=0.0,
                favorite_scanners=[],
                success_rate=0.0,
                last_activity=datetime.utcnow(),
                subscription_plan="unknown",
                retention_score=0.0
            )
        
        # Calculate metrics
        sessions = self._get_user_sessions(user_id, timeframe)
        queries = [e for e in user_events if e.event_type == "query_submitted"]
        scans = [e for e in user_events if e.event_type == "scan_completed"]
        
        # Calculate session duration
        session_durations = []
        for session in sessions.values():
            duration = (session["last_activity"] - session["start_time"]).total_seconds()
            session_durations.append(duration)
        
        avg_session_duration = statistics.mean(session_durations) if session_durations else 0.0
        
        # Calculate favorite scanners
        scanner_usage = Counter()
        for event in user_events:
            if event.event_type == "scan_completed" and "scanner_type" in event.properties:
                scanner_usage[event.properties["scanner_type"]] += 1
        
        favorite_scanners = [scanner for scanner, _ in scanner_usage.most_common(5)]
        
        # Calculate success rate
        successful_scans = [
            e for e in scans 
            if e.properties.get("status") == "completed"
        ]
        success_rate = len(successful_scans) / len(scans) if scans else 0.0
        
        # Calculate retention score (simplified)
        days_active = len(set(e.timestamp.date() for e in user_events))
        total_days = (datetime.utcnow().date() - cutoff_date.date()).days
        retention_score = days_active / max(total_days, 1)
        
        return UserBehaviorMetrics(
            user_id=user_id,
            total_sessions=len(sessions),
            total_queries=len(queries),
            total_scans=len(scans),
            avg_session_duration=avg_session_duration,
            favorite_scanners=favorite_scanners,
            success_rate=success_rate,
            last_activity=max(e.timestamp for e in user_events),
            subscription_plan=self._get_user_subscription_plan(user_id),
            retention_score=retention_score
        )
    
    async def get_platform_metrics(self, timeframe: AnalyticsTimeframe = AnalyticsTimeframe.DAY) -> PlatformMetrics:
        """Get comprehensive platform performance metrics."""
        cutoff_date = self._get_cutoff_date(timeframe)
        recent_events = [
            e for e in self.events_storage 
            if e.timestamp >= cutoff_date
        ]
        
        # Calculate user metrics
        unique_users = set(e.user_id for e in recent_events if e.user_id)
        active_users_24h = len(set(
            e.user_id for e in self.events_storage 
            if e.user_id and (datetime.utcnow() - e.timestamp).total_seconds() < 86400
        ))
        active_users_7d = len(set(
            e.user_id for e in self.events_storage 
            if e.user_id and (datetime.utcnow() - e.timestamp).total_seconds() < 604800
        ))
        active_users_30d = len(set(
            e.user_id for e in self.events_storage 
            if e.user_id and (datetime.utcnow() - e.timestamp).total_seconds() < 2592000
        ))
        
        # Calculate query and scan metrics
        queries = [e for e in recent_events if e.event_type == "query_submitted"]
        scans = [e for e in recent_events if e.event_type == "scan_completed"]
        
        # Calculate performance metrics
        response_times = [
            e.properties.get("response_time", 0) 
            for e in recent_events 
            if "response_time" in e.properties
        ]
        avg_response_time = statistics.mean(response_times) if response_times else 0.0
        
        # Calculate error rate
        errors = [e for e in recent_events if e.event_type == "error"]
        total_requests = len([e for e in recent_events if e.event_type in ["query_submitted", "api_request"]])
        error_rate = len(errors) / max(total_requests, 1)
        
        # Calculate top scanners
        scanner_usage = Counter()
        for event in scans:
            if "scanner_type" in event.properties:
                scanner_usage[event.properties["scanner_type"]] += 1
        
        top_scanners = scanner_usage.most_common(10)
        
        # Calculate revenue metrics (simplified)
        revenue_metrics = await self._calculate_revenue_metrics(timeframe)
        
        return PlatformMetrics(
            total_users=len(unique_users),
            active_users_24h=active_users_24h,
            active_users_7d=active_users_7d,
            active_users_30d=active_users_30d,
            total_queries=len(queries),
            total_scans=len(scans),
            avg_response_time=avg_response_time,
            error_rate=error_rate,
            top_scanners=top_scanners,
            revenue_metrics=revenue_metrics
        )
    
    async def generate_performance_insights(self, timeframe: AnalyticsTimeframe = AnalyticsTimeframe.WEEK) -> List[PerformanceInsight]:
        """Generate actionable performance insights."""
        insights = []
        platform_metrics = await self.get_platform_metrics(timeframe)
        
        # Response time insight
        if platform_metrics.avg_response_time > self.performance_baselines["avg_response_time"]:
            severity = "high" if platform_metrics.avg_response_time > 5.0 else "medium"
            insights.append(PerformanceInsight(
                insight_type="performance",
                title="Elevated Response Times",
                description=f"Average response time ({platform_metrics.avg_response_time:.2f}s) exceeds baseline ({self.performance_baselines['avg_response_time']}s)",
                severity=severity,
                impact_score=0.8,
                recommended_actions=[
                    "Review database query optimization",
                    "Check external API performance",
                    "Consider increasing concurrent processing limits",
                    "Implement additional caching layers"
                ],
                metrics={"avg_response_time": platform_metrics.avg_response_time}
            ))
        
        # Error rate insight
        if platform_metrics.error_rate > self.performance_baselines["error_rate"]:
            severity = "critical" if platform_metrics.error_rate > 0.15 else "high"
            insights.append(PerformanceInsight(
                insight_type="reliability",
                title="High Error Rate",
                description=f"Error rate ({platform_metrics.error_rate:.1%}) exceeds acceptable threshold ({self.performance_baselines['error_rate']:.1%})",
                severity=severity,
                impact_score=0.9,
                recommended_actions=[
                    "Investigate recent error patterns",
                    "Review scanner health status",
                    "Check external service availability",
                    "Implement additional error handling"
                ],
                metrics={"error_rate": platform_metrics.error_rate}
            ))
        
        # User engagement insight
        if platform_metrics.active_users_7d < platform_metrics.active_users_30d * 0.3:
            insights.append(PerformanceInsight(
                insight_type="engagement",
                title="Low Weekly User Retention",
                description="Weekly active users are below 30% of monthly active users",
                severity="medium",
                impact_score=0.6,
                recommended_actions=[
                    "Analyze user journey and identify drop-off points",
                    "Implement user re-engagement campaigns",
                    "Review onboarding process effectiveness",
                    "Gather user feedback through surveys"
                ],
                metrics={
                    "weekly_retention_rate": platform_metrics.active_users_7d / max(platform_metrics.active_users_30d, 1)
                }
            ))
        
        # Scanner performance insight
        await self._add_scanner_performance_insights(insights, timeframe)
        
        return insights
    
    async def _add_scanner_performance_insights(self, insights: List[PerformanceInsight], timeframe: AnalyticsTimeframe):
        """Add scanner-specific performance insights."""
        cutoff_date = self._get_cutoff_date(timeframe)
        scan_events = [
            e for e in self.events_storage 
            if e.event_type == "scan_completed" and e.timestamp >= cutoff_date
        ]
        
        # Analyze scanner success rates
        scanner_stats = defaultdict(lambda: {"total": 0, "successful": 0, "avg_time": []})
        
        for event in scan_events:
            scanner_type = event.properties.get("scanner_type")
            if not scanner_type:
                continue
            
            scanner_stats[scanner_type]["total"] += 1
            
            if event.properties.get("status") == "completed":
                scanner_stats[scanner_type]["successful"] += 1
            
            if "execution_time" in event.properties:
                scanner_stats[scanner_type]["avg_time"].append(event.properties["execution_time"])
        
        # Generate insights for underperforming scanners
        for scanner_type, stats in scanner_stats.items():
            if stats["total"] < 10:  # Skip scanners with low usage
                continue
            
            success_rate = stats["successful"] / stats["total"]
            if success_rate < 0.8:  # Less than 80% success rate
                insights.append(PerformanceInsight(
                    insight_type="scanner_performance",
                    title=f"Low Success Rate: {scanner_type}",
                    description=f"{scanner_type} scanner has {success_rate:.1%} success rate",
                    severity="medium" if success_rate > 0.6 else "high",
                    impact_score=0.7,
                    recommended_actions=[
                        f"Review {scanner_type} scanner implementation",
                        "Check external API dependencies",
                        "Implement additional error handling",
                        "Consider timeout adjustments"
                    ],
                    metrics={
                        "success_rate": success_rate,
                        "total_executions": stats["total"]
                    }
                ))
    
    async def get_real_time_dashboard_data(self) -> Dict[str, Any]:
        """Get real-time dashboard data for monitoring."""
        now = datetime.utcnow()
        last_hour = now - timedelta(hours=1)
        last_5_minutes = now - timedelta(minutes=5)
        
        # Recent activity
        recent_events = [e for e in self.events_storage if e.timestamp >= last_hour]
        very_recent_events = [e for e in self.events_storage if e.timestamp >= last_5_minutes]
        
        # Active sessions
        active_sessions = len([
            session for session in self.user_sessions.values()
            if (now - session["last_activity"]).total_seconds() < 1800  # 30 minutes
        ])
        
        # Current error rate
        recent_errors = [e for e in very_recent_events if e.event_type == "error"]
        recent_requests = [e for e in very_recent_events if e.event_type in ["query_submitted", "api_request"]]
        current_error_rate = len(recent_errors) / max(len(recent_requests), 1)
        
        # Response time trend
        response_times = [
            e.properties.get("response_time", 0)
            for e in very_recent_events
            if "response_time" in e.properties
        ]
        current_avg_response_time = statistics.mean(response_times) if response_times else 0.0
        
        return {
            "timestamp": now.isoformat(),
            "active_sessions": active_sessions,
            "events_last_hour": len(recent_events),
            "events_last_5_minutes": len(very_recent_events),
            "current_error_rate": current_error_rate,
            "current_avg_response_time": current_avg_response_time,
            "status": "healthy" if current_error_rate < 0.1 and current_avg_response_time < 5.0 else "warning"
        }
    
    async def _calculate_revenue_metrics(self, timeframe: AnalyticsTimeframe) -> Dict[str, float]:
        """Calculate revenue-related metrics."""
        # This would typically integrate with billing/subscription systems
        # For now, return sample metrics
        return {
            "total_revenue": 15750.00,
            "mrr": 5250.00,  # Monthly Recurring Revenue
            "arpu": 42.50,   # Average Revenue Per User
            "churn_rate": 0.05,  # 5% monthly churn
            "ltv": 850.00    # Customer Lifetime Value
        }
    
    def _get_cutoff_date(self, timeframe: AnalyticsTimeframe) -> datetime:
        """Get cutoff date for timeframe."""
        now = datetime.utcnow()
        
        if timeframe == AnalyticsTimeframe.HOUR:
            return now - timedelta(hours=1)
        elif timeframe == AnalyticsTimeframe.DAY:
            return now - timedelta(days=1)
        elif timeframe == AnalyticsTimeframe.WEEK:
            return now - timedelta(weeks=1)
        elif timeframe == AnalyticsTimeframe.MONTH:
            return now - timedelta(days=30)
        elif timeframe == AnalyticsTimeframe.QUARTER:
            return now - timedelta(days=90)
        elif timeframe == AnalyticsTimeframe.YEAR:
            return now - timedelta(days=365)
        else:
            return now - timedelta(days=7)  # Default to week
    
    def _get_user_sessions(self, user_id: str, timeframe: AnalyticsTimeframe) -> Dict[str, Dict[str, Any]]:
        """Get user sessions for timeframe."""
        cutoff_date = self._get_cutoff_date(timeframe)
        return {
            key: session for key, session in self.user_sessions.items()
            if session["user_id"] == user_id and session["start_time"] >= cutoff_date
        }
    
    def _get_user_subscription_plan(self, user_id: str) -> str:
        """Get user subscription plan (would integrate with subscription service)."""
        # Sample implementation - would integrate with actual subscription system
        return "professional"  # Default for now
    
    async def export_analytics_data(self, timeframe: AnalyticsTimeframe, 
                                  format: str = "json") -> Dict[str, Any]:
        """Export analytics data for external analysis."""
        cutoff_date = self._get_cutoff_date(timeframe)
        events = [
            e for e in self.events_storage 
            if e.timestamp >= cutoff_date
        ]
        
        # Prepare export data
        export_data = {
            "export_info": {
                "timestamp": datetime.utcnow().isoformat(),
                "timeframe": timeframe.value,
                "total_events": len(events),
                "date_range": {
                    "start": cutoff_date.isoformat(),
                    "end": datetime.utcnow().isoformat()
                }
            },
            "platform_metrics": asdict(await self.get_platform_metrics(timeframe)),
            "performance_insights": [asdict(insight) for insight in await self.generate_performance_insights(timeframe)],
            "events_summary": self._generate_events_summary(events)
        }
        
        return export_data
    
    def _generate_events_summary(self, events: List[AnalyticsEvent]) -> Dict[str, Any]:
        """Generate summary statistics for events."""
        event_types = Counter(e.event_type for e in events)
        hourly_distribution = defaultdict(int)
        
        for event in events:
            hour = event.timestamp.hour
            hourly_distribution[hour] += 1
        
        return {
            "event_types": dict(event_types),
            "hourly_distribution": dict(hourly_distribution),
            "unique_users": len(set(e.user_id for e in events if e.user_id)),
            "unique_sessions": len(set(e.session_id for e in events if e.session_id))
        }


# Analytics helper functions
async def track_user_activity(analytics_service: EnterpriseAnalyticsService,
                            user_id: str, session_id: str, activity_type: str,
                            properties: Dict[str, Any] = None):
    """Helper function to track user activity."""
    event = AnalyticsEvent(
        event_id=f"activity_{datetime.utcnow().timestamp()}",
        user_id=user_id,
        session_id=session_id,
        event_type="user_activity",
        event_name=activity_type,
        timestamp=datetime.utcnow(),
        properties=properties or {}
    )
    await analytics_service.track_event(event)


async def track_performance_metric(analytics_service: EnterpriseAnalyticsService,
                                 metric_name: str, value: float,
                                 additional_properties: Dict[str, Any] = None):
    """Helper function to track performance metrics."""
    properties = {"metric_name": metric_name, "value": value}
    if additional_properties:
        properties.update(additional_properties)
    
    event = AnalyticsEvent(
        event_id=f"perf_{datetime.utcnow().timestamp()}",
        user_id=None,
        session_id=None,
        event_type="performance",
        event_name=metric_name,
        timestamp=datetime.utcnow(),
        properties=properties
    )
    await analytics_service.track_event(event)