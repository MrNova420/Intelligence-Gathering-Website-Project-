"""
Advanced Business Intelligence API
==================================

Enterprise-grade business intelligence and analytics endpoints providing:
- Real-time platform metrics and KPIs
- Advanced data visualization endpoints
- Custom dashboard creation
- Automated reporting and insights
- Predictive analytics and forecasting
- Cross-platform integration analytics
"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import statistics
from collections import defaultdict, Counter

logger = logging.getLogger(__name__)

# Mock FastAPI imports for development
try:
    from fastapi import APIRouter, HTTPException, Depends, Query, Path, Body
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel, Field, validator
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    # Mock classes for development
    class APIRouter:
        def __init__(self, **kwargs): pass
        def get(self, path): return lambda func: func
        def post(self, path): return lambda func: func
    
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
    
    HTTPException = Exception
    Depends = Query = Path = Body = Field = lambda *args, **kwargs: None


# Enums for API consistency
class MetricType(str, Enum):
    SCANS = "scans"
    USERS = "users"
    PERFORMANCE = "performance"
    REVENUE = "revenue"
    SECURITY = "security"
    SYSTEM = "system"

class TimeRange(str, Enum):
    HOUR = "1h"
    DAY = "24h"
    WEEK = "7d"
    MONTH = "30d"
    QUARTER = "90d"
    YEAR = "365d"

class VisualizationType(str, Enum):
    LINE_CHART = "line"
    BAR_CHART = "bar"
    PIE_CHART = "pie"
    AREA_CHART = "area"
    HEATMAP = "heatmap"
    GAUGE = "gauge"


# Pydantic Models
class MetricQuery(BaseModel):
    metric_type: MetricType
    time_range: TimeRange = TimeRange.DAY
    granularity: str = Field(default="hour", description="hour, day, week, month")
    filters: Optional[Dict[str, Any]] = Field(default_factory=dict)
    include_predictions: bool = Field(default=False)

class DashboardWidget(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    metric_type: MetricType
    visualization: VisualizationType
    time_range: TimeRange
    position: Dict[str, int] = Field(description="x, y, width, height")
    filters: Optional[Dict[str, Any]] = Field(default_factory=dict)
    refresh_interval: int = Field(default=30, description="Refresh interval in seconds")

class CustomDashboard(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    widgets: List[DashboardWidget]
    created_by: str
    shared_with: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ReportTemplate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    metrics: List[MetricType]
    time_range: TimeRange
    schedule: Optional[str] = Field(None, description="Cron expression for automated reports")
    recipients: List[str] = Field(default_factory=list)
    format: str = Field(default="pdf", description="pdf, html, json, csv")


# Data Classes for Internal Use
@dataclass
class MetricPoint:
    timestamp: datetime
    value: float
    metadata: Dict[str, Any] = None

@dataclass
class PlatformMetric:
    name: str
    description: str
    current_value: float
    previous_value: float
    change_percentage: float
    trend: str  # "up", "down", "stable"
    unit: str
    category: MetricType


class BusinessIntelligenceService:
    """Core business intelligence service providing analytics and insights"""
    
    def __init__(self):
        self.metrics_cache = {}
        self.dashboards = {}
        self.report_templates = {}
        self._initialize_mock_data()
    
    def _initialize_mock_data(self):
        """Initialize with mock data for demonstration"""
        # Mock historical data for the last 30 days
        base_time = datetime.utcnow() - timedelta(days=30)
        
        self.mock_data = {
            MetricType.SCANS: self._generate_time_series(base_time, 30, base_value=100, trend=0.05),
            MetricType.USERS: self._generate_time_series(base_time, 30, base_value=50, trend=0.03),
            MetricType.PERFORMANCE: self._generate_time_series(base_time, 30, base_value=2.5, trend=-0.01, noise=0.3),
            MetricType.REVENUE: self._generate_time_series(base_time, 30, base_value=5000, trend=0.08),
            MetricType.SECURITY: self._generate_time_series(base_time, 30, base_value=95, trend=0.001, noise=0.1),
            MetricType.SYSTEM: self._generate_time_series(base_time, 30, base_value=99.5, trend=0.0005, noise=0.05)
        }
    
    def _generate_time_series(self, start_time: datetime, days: int, base_value: float, 
                            trend: float = 0, noise: float = 0.1) -> List[MetricPoint]:
        """Generate realistic time series data"""
        points = []
        current_value = base_value
        
        for day in range(days):
            for hour in range(24):
                timestamp = start_time + timedelta(days=day, hours=hour)
                
                # Add trend
                current_value *= (1 + trend / 24)
                
                # Add noise and daily patterns
                daily_factor = 1 + 0.1 * abs(12 - hour) / 12  # Peak during day
                noise_factor = 1 + noise * (2 * (hash(str(timestamp)) % 1000) / 1000 - 1)
                
                value = current_value * daily_factor * noise_factor
                
                points.append(MetricPoint(
                    timestamp=timestamp,
                    value=max(0, value),
                    metadata={"day_of_week": timestamp.weekday(), "hour": hour}
                ))
        
        return points
    
    async def get_platform_metrics(self, time_range: TimeRange = TimeRange.DAY) -> Dict[str, PlatformMetric]:
        """Get comprehensive platform metrics"""
        metrics = {}
        
        for metric_type in MetricType:
            data = self.mock_data[metric_type]
            current_data = self._filter_by_time_range(data, time_range)
            
            if not current_data:
                continue
            
            current_value = current_data[-1].value
            previous_value = current_data[0].value if len(current_data) > 1 else current_value
            
            change = ((current_value - previous_value) / previous_value) * 100 if previous_value > 0 else 0
            trend = "up" if change > 1 else "down" if change < -1 else "stable"
            
            metrics[metric_type.value] = PlatformMetric(
                name=metric_type.value.replace("_", " ").title(),
                description=self._get_metric_description(metric_type),
                current_value=round(current_value, 2),
                previous_value=round(previous_value, 2),
                change_percentage=round(change, 2),
                trend=trend,
                unit=self._get_metric_unit(metric_type),
                category=metric_type
            )
        
        return metrics
    
    async def get_time_series_data(self, query: MetricQuery) -> Dict[str, Any]:
        """Get time series data for visualization"""
        if query.metric_type not in self.mock_data:
            raise HTTPException(status_code=404, detail=f"Metric {query.metric_type} not found")
        
        data = self.mock_data[query.metric_type]
        filtered_data = self._filter_by_time_range(data, query.time_range)
        
        # Apply granularity aggregation
        aggregated_data = self._aggregate_by_granularity(filtered_data, query.granularity)
        
        result = {
            "metric_type": query.metric_type,
            "time_range": query.time_range,
            "granularity": query.granularity,
            "data": [
                {
                    "timestamp": point.timestamp.isoformat(),
                    "value": point.value,
                    "metadata": point.metadata
                }
                for point in aggregated_data
            ],
            "statistics": self._calculate_statistics(aggregated_data),
            "total_points": len(aggregated_data)
        }
        
        # Add predictions if requested
        if query.include_predictions:
            result["predictions"] = await self._generate_predictions(aggregated_data)
        
        return result
    
    async def create_custom_dashboard(self, dashboard: CustomDashboard) -> Dict[str, Any]:
        """Create a custom analytics dashboard"""
        dashboard_id = dashboard.id
        
        # Validate widgets
        for widget in dashboard.widgets:
            if widget.metric_type not in MetricType:
                raise HTTPException(status_code=400, detail=f"Invalid metric type: {widget.metric_type}")
        
        # Store dashboard
        self.dashboards[dashboard_id] = dashboard
        
        # Generate initial data for all widgets
        widget_data = {}
        for widget in dashboard.widgets:
            query = MetricQuery(
                metric_type=widget.metric_type,
                time_range=widget.time_range,
                filters=widget.filters or {}
            )
            widget_data[widget.id] = await self.get_time_series_data(query)
        
        return {
            "dashboard_id": dashboard_id,
            "name": dashboard.name,
            "created_at": dashboard.created_at.isoformat(),
            "widgets": len(dashboard.widgets),
            "widget_data": widget_data
        }
    
    async def get_dashboard_data(self, dashboard_id: str) -> Dict[str, Any]:
        """Get real-time data for a dashboard"""
        if dashboard_id not in self.dashboards:
            raise HTTPException(status_code=404, detail="Dashboard not found")
        
        dashboard = self.dashboards[dashboard_id]
        
        widget_data = {}
        for widget in dashboard.widgets:
            query = MetricQuery(
                metric_type=widget.metric_type,
                time_range=widget.time_range,
                filters=widget.filters or {}
            )
            widget_data[widget.id] = await self.get_time_series_data(query)
        
        return {
            "dashboard": asdict(dashboard),
            "widget_data": widget_data,
            "last_updated": datetime.utcnow().isoformat()
        }
    
    async def generate_insights_report(self, time_range: TimeRange = TimeRange.WEEK) -> Dict[str, Any]:
        """Generate automated insights and recommendations"""
        metrics = await self.get_platform_metrics(time_range)
        
        insights = []
        recommendations = []
        
        # Analyze trends and generate insights
        for metric_name, metric in metrics.items():
            if metric.trend == "up" and metric.change_percentage > 10:
                insights.append({
                    "type": "positive_trend",
                    "metric": metric_name,
                    "description": f"{metric.name} has increased by {metric.change_percentage:.1f}% in the last {time_range.value}",
                    "impact": "high" if metric.change_percentage > 25 else "medium"
                })
            elif metric.trend == "down" and metric.change_percentage < -10:
                insights.append({
                    "type": "negative_trend",
                    "metric": metric_name,
                    "description": f"{metric.name} has decreased by {abs(metric.change_percentage):.1f}% in the last {time_range.value}",
                    "impact": "high" if abs(metric.change_percentage) > 25 else "medium"
                })
        
        # Generate recommendations
        scan_metric = metrics.get("scans")
        if scan_metric and scan_metric.trend == "down":
            recommendations.append({
                "category": "user_engagement",
                "priority": "high",
                "title": "Boost Scan Activity",
                "description": "Consider implementing user engagement campaigns or introducing new scan types to increase platform usage.",
                "actions": [
                    "Launch email campaign highlighting new features",
                    "Implement gamification elements",
                    "Add social sharing capabilities"
                ]
            })
        
        performance_metric = metrics.get("performance")
        if performance_metric and performance_metric.current_value > 3.0:
            recommendations.append({
                "category": "system_optimization",
                "priority": "medium",
                "title": "Optimize System Performance",
                "description": "Response times are above optimal thresholds. Consider infrastructure improvements.",
                "actions": [
                    "Implement caching strategies",
                    "Optimize database queries",
                    "Consider load balancing"
                ]
            })
        
        return {
            "generated_at": datetime.utcnow().isoformat(),
            "time_range": time_range,
            "summary": {
                "total_insights": len(insights),
                "total_recommendations": len(recommendations),
                "high_priority_items": len([r for r in recommendations if r["priority"] == "high"])
            },
            "insights": insights,
            "recommendations": recommendations,
            "metrics_summary": {k: asdict(v) for k, v in metrics.items()}
        }
    
    def _filter_by_time_range(self, data: List[MetricPoint], time_range: TimeRange) -> List[MetricPoint]:
        """Filter data by time range"""
        cutoff_time = datetime.utcnow() - self._time_range_to_timedelta(time_range)
        return [point for point in data if point.timestamp >= cutoff_time]
    
    def _time_range_to_timedelta(self, time_range: TimeRange) -> timedelta:
        """Convert time range to timedelta"""
        mapping = {
            TimeRange.HOUR: timedelta(hours=1),
            TimeRange.DAY: timedelta(days=1),
            TimeRange.WEEK: timedelta(days=7),
            TimeRange.MONTH: timedelta(days=30),
            TimeRange.QUARTER: timedelta(days=90),
            TimeRange.YEAR: timedelta(days=365)
        }
        return mapping[time_range]
    
    def _aggregate_by_granularity(self, data: List[MetricPoint], granularity: str) -> List[MetricPoint]:
        """Aggregate data by specified granularity"""
        if granularity == "hour" or len(data) <= 24:
            return data
        
        # Group by granularity
        grouped = defaultdict(list)
        
        for point in data:
            if granularity == "day":
                key = point.timestamp.date()
            elif granularity == "week":
                key = point.timestamp.isocalendar()[:2]  # year, week
            elif granularity == "month":
                key = (point.timestamp.year, point.timestamp.month)
            else:
                key = point.timestamp.date()
            
            grouped[key].append(point)
        
        # Aggregate each group
        aggregated = []
        for key, points in grouped.items():
            avg_value = statistics.mean([p.value for p in points])
            timestamp = points[0].timestamp.replace(minute=0, second=0, microsecond=0)
            
            aggregated.append(MetricPoint(
                timestamp=timestamp,
                value=avg_value,
                metadata={"aggregated": True, "point_count": len(points)}
            ))
        
        return sorted(aggregated, key=lambda x: x.timestamp)
    
    def _calculate_statistics(self, data: List[MetricPoint]) -> Dict[str, float]:
        """Calculate statistical measures"""
        if not data:
            return {}
        
        values = [point.value for point in data]
        
        return {
            "min": min(values),
            "max": max(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "std_dev": statistics.stdev(values) if len(values) > 1 else 0,
            "total": sum(values),
            "count": len(values)
        }
    
    async def _generate_predictions(self, historical_data: List[MetricPoint]) -> Dict[str, Any]:
        """Generate simple trend-based predictions"""
        if len(historical_data) < 2:
            return {"error": "Insufficient data for predictions"}
        
        # Simple linear trend prediction
        values = [point.value for point in historical_data[-10:]]  # Use last 10 points
        
        if len(values) < 2:
            return {"error": "Insufficient recent data"}
        
        # Calculate simple moving average trend
        trend = (values[-1] - values[0]) / len(values)
        
        # Generate next 5 predictions
        predictions = []
        last_timestamp = historical_data[-1].timestamp
        last_value = historical_data[-1].value
        
        for i in range(1, 6):
            predicted_time = last_timestamp + timedelta(hours=i)
            predicted_value = max(0, last_value + (trend * i))
            
            predictions.append({
                "timestamp": predicted_time.isoformat(),
                "predicted_value": round(predicted_value, 2),
                "confidence": max(0.3, 0.9 - (i * 0.1))  # Decreasing confidence
            })
        
        return {
            "method": "linear_trend",
            "trend_value": round(trend, 4),
            "predictions": predictions
        }
    
    def _get_metric_description(self, metric_type: MetricType) -> str:
        """Get description for metric type"""
        descriptions = {
            MetricType.SCANS: "Total number of intelligence scans performed",
            MetricType.USERS: "Active user count and engagement metrics",
            MetricType.PERFORMANCE: "Average system response time in seconds",
            MetricType.REVENUE: "Platform revenue and monetization metrics",
            MetricType.SECURITY: "Security score and threat detection rate",
            MetricType.SYSTEM: "System uptime and availability percentage"
        }
        return descriptions.get(metric_type, "Platform metric")
    
    def _get_metric_unit(self, metric_type: MetricType) -> str:
        """Get unit for metric type"""
        units = {
            MetricType.SCANS: "count",
            MetricType.USERS: "users",
            MetricType.PERFORMANCE: "seconds",
            MetricType.REVENUE: "USD",
            MetricType.SECURITY: "percentage",
            MetricType.SYSTEM: "percentage"
        }
        return units.get(metric_type, "units")


class BusinessIntelligenceAPI:
    """FastAPI router for business intelligence endpoints"""
    
    def __init__(self):
        self.router = APIRouter(prefix="/api/v1/business-intelligence", tags=["Business Intelligence"])
        self.service = BusinessIntelligenceService()
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup API routes"""
        
        @self.router.get("/metrics", summary="Get Platform Metrics")
        async def get_platform_metrics(
            time_range: TimeRange = Query(TimeRange.DAY, description="Time range for metrics")
        ):
            """Get comprehensive platform metrics and KPIs"""
            try:
                metrics = await self.service.get_platform_metrics(time_range)
                
                return {
                    "success": True,
                    "time_range": time_range,
                    "generated_at": datetime.utcnow().isoformat(),
                    "metrics": {k: asdict(v) for k, v in metrics.items()}
                }
            except Exception as e:
                logger.error(f"Error getting platform metrics: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.post("/metrics/time-series", summary="Get Time Series Data")
        async def get_time_series_data(query: MetricQuery):
            """Get detailed time series data for visualization"""
            try:
                data = await self.service.get_time_series_data(query)
                
                return {
                    "success": True,
                    "query": asdict(query) if hasattr(query, '__dict__') else query.dict(),
                    "data": data
                }
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Error getting time series data: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.post("/dashboards", summary="Create Custom Dashboard")
        async def create_dashboard(dashboard: CustomDashboard):
            """Create a custom analytics dashboard"""
            try:
                result = await self.service.create_custom_dashboard(dashboard)
                
                return {
                    "success": True,
                    "message": "Dashboard created successfully",
                    "dashboard": result
                }
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Error creating dashboard: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/dashboards/{dashboard_id}", summary="Get Dashboard Data")
        async def get_dashboard_data(dashboard_id: str = Path(..., description="Dashboard ID")):
            """Get real-time data for a specific dashboard"""
            try:
                data = await self.service.get_dashboard_data(dashboard_id)
                
                return {
                    "success": True,
                    "dashboard_id": dashboard_id,
                    "data": data
                }
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Error getting dashboard data: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/insights", summary="Generate Insights Report")
        async def generate_insights(
            time_range: TimeRange = Query(TimeRange.WEEK, description="Analysis time range")
        ):
            """Generate automated insights and recommendations"""
            try:
                report = await self.service.generate_insights_report(time_range)
                
                return {
                    "success": True,
                    "report": report
                }
            except Exception as e:
                logger.error(f"Error generating insights: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/health", summary="Business Intelligence Health Check")
        async def health_check():
            """Health check for business intelligence services"""
            return {
                "success": True,
                "service": "Business Intelligence API",
                "status": "operational",
                "version": "1.0.0",
                "features": [
                    "Platform Metrics",
                    "Time Series Analytics",
                    "Custom Dashboards",
                    "Automated Insights",
                    "Predictive Analytics"
                ]
            }


# Global instances
business_intelligence_service = BusinessIntelligenceService()
business_intelligence_api = BusinessIntelligenceAPI()

# Convenience functions
async def get_platform_kpis(time_range: TimeRange = TimeRange.DAY) -> Dict[str, Any]:
    """Get key platform KPIs"""
    return await business_intelligence_service.get_platform_metrics(time_range)

async def create_metric_visualization(metric_type: MetricType, time_range: TimeRange = TimeRange.DAY) -> Dict[str, Any]:
    """Create visualization data for a specific metric"""
    query = MetricQuery(metric_type=metric_type, time_range=time_range)
    return await business_intelligence_service.get_time_series_data(query)

async def generate_executive_summary(time_range: TimeRange = TimeRange.MONTH) -> Dict[str, Any]:
    """Generate executive summary report"""
    return await business_intelligence_service.generate_insights_report(time_range)