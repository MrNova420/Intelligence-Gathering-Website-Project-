"""
Advanced Data Visualization Engine
As promised in PR #2 for interactive charts, network graphs, and geographic mapping
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
from enum import Enum
import statistics
import math

logger = logging.getLogger(__name__)


class ChartType(Enum):
    """Supported chart types for visualization"""
    LINE = "line"
    BAR = "bar"
    PIE = "pie"
    SCATTER = "scatter"
    AREA = "area"
    DONUT = "donut"
    HEATMAP = "heatmap"
    RADAR = "radar"
    TREEMAP = "treemap"
    NETWORK = "network"
    GEOGRAPHIC = "geographic"
    TIMELINE = "timeline"


@dataclass
class ChartData:
    """Chart data structure"""
    chart_type: ChartType
    title: str
    data: List[Dict[str, Any]]
    labels: List[str]
    colors: Optional[List[str]] = None
    options: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class NetworkNode:
    """Network graph node"""
    id: str
    label: str
    size: float
    color: str
    group: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class NetworkEdge:
    """Network graph edge"""
    source: str
    target: str
    weight: float
    label: Optional[str] = None
    color: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class GeographicPoint:
    """Geographic data point"""
    latitude: float
    longitude: float
    value: float
    label: str
    color: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class IntelligenceVisualizationEngine:
    """Advanced visualization engine for intelligence data"""
    
    def __init__(self):
        self.color_palettes = self._initialize_color_palettes()
        self.chart_templates = self._initialize_chart_templates()
        
    def _initialize_color_palettes(self) -> Dict[str, List[str]]:
        """Initialize color palettes for different visualization themes"""
        return {
            "intelligence": [
                "#1a365d", "#2c5aa0", "#3182ce", "#4299e1", "#63b3ed",
                "#90cdf4", "#bee3f8", "#e6f3ff", "#2d3748", "#4a5568"
            ],
            "security": [
                "#742a2a", "#c53030", "#e53e3e", "#f56565", "#fc8181",
                "#feb2b2", "#fed7d7", "#fff5f5", "#1a202c", "#2d3748"
            ],
            "performance": [
                "#1a202c", "#2d3748", "#4a5568", "#718096", "#a0aec0",
                "#cbd5e0", "#e2e8f0", "#f7fafc", "#38a169", "#68d391"
            ],
            "business": [
                "#744210", "#b7791f", "#d69e2e", "#ecc94b", "#f6e05e",
                "#faf089", "#fefcbf", "#fffff0", "#2b6cb0", "#4299e1"
            ],
            "rainbow": [
                "#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4", "#feca57",
                "#ff9ff3", "#54a0ff", "#5f27cd", "#00d2d3", "#ff9f43"
            ]
        }
    
    def _initialize_chart_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize chart templates with default configurations"""
        return {
            "performance_dashboard": {
                "charts": [
                    {"type": ChartType.LINE, "title": "Performance Trends"},
                    {"type": ChartType.BAR, "title": "Scanner Success Rates"},
                    {"type": ChartType.PIE, "title": "Query Type Distribution"},
                    {"type": ChartType.HEATMAP, "title": "Activity Heatmap"}
                ],
                "layout": "grid",
                "theme": "intelligence"
            },
            "security_overview": {
                "charts": [
                    {"type": ChartType.TIMELINE, "title": "Security Events Timeline"},
                    {"type": ChartType.NETWORK, "title": "Threat Actor Network"},
                    {"type": ChartType.GEOGRAPHIC, "title": "Threat Origins Map"},
                    {"type": ChartType.RADAR, "title": "Security Posture"}
                ],
                "layout": "dashboard",
                "theme": "security"
            },
            "business_intelligence": {
                "charts": [
                    {"type": ChartType.AREA, "title": "Revenue Trends"},
                    {"type": ChartType.DONUT, "title": "Subscription Breakdown"},
                    {"type": ChartType.BAR, "title": "User Engagement"},
                    {"type": ChartType.SCATTER, "title": "User Value Analysis"}
                ],
                "layout": "executive",
                "theme": "business"
            }
        }
    
    async def create_scanner_performance_chart(self, scanner_data: Dict[str, Any]) -> ChartData:
        """Create scanner performance visualization"""
        scanner_names = []
        success_rates = []
        response_times = []
        colors = self.color_palettes["performance"]
        
        for scanner_name, data in scanner_data.items():
            if not data.get("error"):
                scanner_names.append(scanner_name.replace("_", " ").title())
                
                # Calculate success rate
                success_rate = data.get("confidence", 0.0) * 100
                success_rates.append(success_rate)
                
                # Get response time (simulate if not present)
                response_time = data.get("response_time", 
                                       len(scanner_name) * 0.1 + 0.5)  # Simulate based on name length
                response_times.append(response_time)
        
        chart_data = [
            {"scanner": name, "success_rate": rate, "response_time": time}
            for name, rate, time in zip(scanner_names, success_rates, response_times)
        ]
        
        return ChartData(
            chart_type=ChartType.BAR,
            title="Scanner Performance Analysis",
            data=chart_data,
            labels=scanner_names,
            colors=colors[:len(scanner_names)],
            options={
                "responsive": True,
                "scales": {
                    "y": {
                        "beginAtZero": True,
                        "max": 100,
                        "title": {"display": True, "text": "Success Rate (%)"}
                    },
                    "x": {
                        "title": {"display": True, "text": "Scanner Modules"}
                    }
                },
                "plugins": {
                    "legend": {"display": True, "position": "top"},
                    "tooltip": {
                        "callbacks": {
                            "afterLabel": "function(context) { return 'Response Time: ' + context.raw.response_time + 's'; }"
                        }
                    }
                }
            },
            metadata={
                "total_scanners": len(scanner_names),
                "avg_success_rate": statistics.mean(success_rates) if success_rates else 0,
                "avg_response_time": statistics.mean(response_times) if response_times else 0
            }
        )
    
    async def create_confidence_distribution_chart(self, scan_results: Dict[str, Any]) -> ChartData:
        """Create confidence score distribution visualization"""
        confidence_ranges = {
            "Very High (90-100%)": 0,
            "High (80-89%)": 0,
            "Good (70-79%)": 0,
            "Medium (60-69%)": 0,
            "Low (50-59%)": 0,
            "Very Low (<50%)": 0
        }
        
        for result in scan_results.values():
            if not result.get("error"):
                confidence = result.get("confidence", 0.0) * 100
                
                if confidence >= 90:
                    confidence_ranges["Very High (90-100%)"] += 1
                elif confidence >= 80:
                    confidence_ranges["High (80-89%)"] += 1
                elif confidence >= 70:
                    confidence_ranges["Good (70-79%)"] += 1
                elif confidence >= 60:
                    confidence_ranges["Medium (60-69%)"] += 1
                elif confidence >= 50:
                    confidence_ranges["Low (50-59%)"] += 1
                else:
                    confidence_ranges["Very Low (<50%)"] += 1
        
        data = [
            {"range": range_name, "count": count}
            for range_name, count in confidence_ranges.items()
            if count > 0
        ]
        
        return ChartData(
            chart_type=ChartType.PIE,
            title="Confidence Score Distribution",
            data=data,
            labels=list(confidence_ranges.keys()),
            colors=self.color_palettes["intelligence"][:len(data)],
            options={
                "responsive": True,
                "plugins": {
                    "legend": {"display": True, "position": "right"},
                    "tooltip": {
                        "callbacks": {
                            "label": "function(context) { return context.label + ': ' + context.parsed + ' scanners'; }"
                        }
                    }
                }
            }
        )
    
    async def create_intelligence_network_graph(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create network graph showing entity relationships"""
        nodes = []
        edges = []
        node_colors = self.color_palettes["intelligence"]
        
        # Extract entities and relationships
        entities = entity_data.get("entities", [])
        relationships = entity_data.get("relationships", [])
        
        # Create nodes for entities
        entity_types = defaultdict(int)
        for i, entity in enumerate(entities):
            entity_type = entity.get("type", "unknown")
            entity_types[entity_type] += 1
            
            # Assign color based on entity type
            type_colors = {
                "email": node_colors[0],
                "phone": node_colors[1],
                "name": node_colors[2],
                "address": node_colors[3],
                "username": node_colors[4],
                "profile": node_colors[5]
            }
            
            node = NetworkNode(
                id=f"entity_{i}",
                label=entity.get("value", "Unknown"),
                size=entity.get("confidence", 0.5) * 50 + 10,  # Size based on confidence
                color=type_colors.get(entity_type, node_colors[6]),
                group=entity_type,
                metadata={
                    "type": entity_type,
                    "confidence": entity.get("confidence", 0.0),
                    "sources": entity.get("sources", [])
                }
            )
            nodes.append(node)
        
        # Create edges for relationships
        for relationship in relationships:
            source_idx = relationship.get("source_index", 0)
            target_idx = relationship.get("target_index", 0)
            
            if source_idx < len(nodes) and target_idx < len(nodes):
                edge = NetworkEdge(
                    source=f"entity_{source_idx}",
                    target=f"entity_{target_idx}",
                    weight=relationship.get("strength", 0.5) * 5,
                    label=relationship.get("type", "related"),
                    color="#718096",
                    metadata={
                        "relationship_type": relationship.get("type", "unknown"),
                        "confidence": relationship.get("confidence", 0.0)
                    }
                )
                edges.append(edge)
        
        return {
            "chart_type": "network",
            "title": "Intelligence Entity Network",
            "nodes": [asdict(node) for node in nodes],
            "edges": [asdict(edge) for edge in edges],
            "options": {
                "physics": {
                    "enabled": True,
                    "solver": "forceAtlas2Based",
                    "forceAtlas2Based": {
                        "gravitationalConstant": -50,
                        "centralGravity": 0.01,
                        "springLength": 100,
                        "springConstant": 0.08
                    }
                },
                "interaction": {
                    "hover": True,
                    "tooltipDelay": 200
                },
                "groups": {
                    entity_type: {"color": color, "shape": "circle"}
                    for entity_type, color in zip(entity_types.keys(), node_colors)
                }
            },
            "metadata": {
                "total_entities": len(entities),
                "total_relationships": len(relationships),
                "entity_types": dict(entity_types)
            }
        }
    
    async def create_geographic_intelligence_map(self, location_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create geographic visualization of intelligence data"""
        geographic_points = []
        
        for location in location_data:
            if "latitude" in location and "longitude" in location:
                point = GeographicPoint(
                    latitude=location["latitude"],
                    longitude=location["longitude"],
                    value=location.get("confidence", 0.5),
                    label=location.get("label", "Unknown Location"),
                    color=self._get_confidence_color(location.get("confidence", 0.5)),
                    metadata={
                        "country": location.get("country", "Unknown"),
                        "region": location.get("region", "Unknown"),
                        "sources": location.get("sources", []),
                        "threat_level": location.get("threat_level", "low")
                    }
                )
                geographic_points.append(point)
        
        return {
            "chart_type": "geographic",
            "title": "Geographic Intelligence Distribution",
            "data": [asdict(point) for point in geographic_points],
            "options": {
                "center": {"lat": 39.8283, "lng": -98.5795},  # Center of US
                "zoom": 4,
                "mapType": "roadmap",
                "markers": {
                    "clustering": True,
                    "maxZoom": 15
                },
                "heatmap": {
                    "enabled": True,
                    "radius": 20,
                    "maxIntensity": 1.0
                }
            },
            "metadata": {
                "total_points": len(geographic_points),
                "countries": len(set(p.metadata.get("country", "Unknown") for p in geographic_points)),
                "avg_confidence": statistics.mean([p.value for p in geographic_points]) if geographic_points else 0
            }
        }
    
    async def create_timeline_visualization(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create timeline visualization for intelligence events"""
        timeline_data = []
        
        for event in events:
            timeline_data.append({
                "x": event.get("timestamp", datetime.utcnow().isoformat()),
                "y": event.get("severity", 1),
                "label": event.get("title", "Unknown Event"),
                "description": event.get("description", ""),
                "category": event.get("category", "general"),
                "color": self._get_category_color(event.get("category", "general"))
            })
        
        # Sort by timestamp
        timeline_data.sort(key=lambda x: x["x"])
        
        return {
            "chart_type": "timeline",
            "title": "Intelligence Events Timeline",
            "data": timeline_data,
            "options": {
                "responsive": True,
                "scales": {
                    "x": {
                        "type": "time",
                        "time": {
                            "unit": "hour",
                            "displayFormats": {
                                "hour": "MMM DD, HH:mm"
                            }
                        },
                        "title": {"display": True, "text": "Time"}
                    },
                    "y": {
                        "title": {"display": True, "text": "Severity Level"},
                        "min": 0,
                        "max": 5
                    }
                },
                "plugins": {
                    "legend": {"display": True},
                    "zoom": {
                        "pan": {"enabled": True, "mode": "x"},
                        "zoom": {"enabled": True, "mode": "x"}
                    }
                }
            },
            "metadata": {
                "total_events": len(events),
                "time_span": self._calculate_time_span(timeline_data),
                "categories": list(set(event.get("category", "general") for event in events))
            }
        }
    
    async def create_threat_heatmap(self, threat_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create heatmap visualization for threat intelligence"""
        # Create matrix data for heatmap
        threat_types = ["malware", "phishing", "spam", "fraud", "bot", "suspicious"]
        time_periods = ["00-04", "04-08", "08-12", "12-16", "16-20", "20-24"]
        
        matrix_data = []
        for i, time_period in enumerate(time_periods):
            row = []
            for j, threat_type in enumerate(threat_types):
                # Simulate threat intensity (replace with actual data)
                intensity = threat_data.get(f"{threat_type}_{time_period}", 
                                         (i + j) * 0.1 + 0.1)
                row.append({
                    "x": j,
                    "y": i,
                    "value": intensity,
                    "threat_type": threat_type,
                    "time_period": time_period
                })
            matrix_data.extend(row)
        
        return {
            "chart_type": "heatmap",
            "title": "Threat Activity Heatmap",
            "data": matrix_data,
            "labels": {
                "x": threat_types,
                "y": time_periods
            },
            "options": {
                "responsive": True,
                "scales": {
                    "x": {"title": {"display": True, "text": "Threat Types"}},
                    "y": {"title": {"display": True, "text": "Time Periods (Hours)"}}
                },
                "plugins": {
                    "tooltip": {
                        "callbacks": {
                            "title": "function(context) { return context[0].parsed.threat_type + ' - ' + context[0].parsed.time_period; }",
                            "label": "function(context) { return 'Intensity: ' + context.parsed.value.toFixed(2); }"
                        }
                    }
                },
                "colorScale": {
                    "min": 0,
                    "max": 1,
                    "colors": ["#e6f3ff", "#3182ce", "#1a365d"]
                }
            },
            "metadata": {
                "max_intensity": max(point["value"] for point in matrix_data),
                "avg_intensity": statistics.mean(point["value"] for point in matrix_data),
                "peak_threat_type": max(threat_types, key=lambda t: sum(
                    point["value"] for point in matrix_data if point["threat_type"] == t
                ))
            }
        }
    
    async def create_executive_dashboard_layout(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive executive dashboard layout"""
        dashboard_components = []
        
        # Key Performance Indicators
        kpi_data = business_data.get("kpis", {})
        kpi_chart = await self._create_kpi_summary_chart(kpi_data)
        dashboard_components.append(kpi_chart)
        
        # Revenue trends
        revenue_data = business_data.get("revenue", [])
        revenue_chart = await self._create_revenue_trend_chart(revenue_data)
        dashboard_components.append(revenue_chart)
        
        # User engagement
        engagement_data = business_data.get("engagement", {})
        engagement_chart = await self._create_user_engagement_chart(engagement_data)
        dashboard_components.append(engagement_chart)
        
        # Platform health
        health_data = business_data.get("health", {})
        health_chart = await self._create_platform_health_chart(health_data)
        dashboard_components.append(health_chart)
        
        return {
            "dashboard_type": "executive",
            "title": "Executive Intelligence Dashboard",
            "layout": "grid",
            "components": dashboard_components,
            "refresh_interval": 300,  # 5 minutes
            "metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "total_components": len(dashboard_components),
                "data_sources": ["business_metrics", "platform_health", "user_analytics"]
            }
        }
    
    async def _create_kpi_summary_chart(self, kpi_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create KPI summary visualization"""
        kpis = []
        for name, data in kpi_data.items():
            kpis.append({
                "name": name.replace("_", " ").title(),
                "current": data.get("current", 0),
                "target": data.get("target", 0),
                "trend": data.get("trend", "stable")
            })
        
        return {
            "chart_type": "kpi_summary",
            "title": "Key Performance Indicators",
            "data": kpis,
            "options": {"layout": "cards", "showTrends": True}
        }
    
    async def _create_revenue_trend_chart(self, revenue_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create revenue trend visualization"""
        return {
            "chart_type": "area",
            "title": "Revenue Trends",
            "data": revenue_data,
            "options": {
                "fill": True,
                "gradient": True,
                "colors": self.color_palettes["business"][:2]
            }
        }
    
    async def _create_user_engagement_chart(self, engagement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create user engagement visualization"""
        return {
            "chart_type": "donut",
            "title": "User Engagement Breakdown",
            "data": [
                {"category": k.replace("_", " ").title(), "value": v}
                for k, v in engagement_data.items()
            ],
            "options": {"innerRadius": 0.6}
        }
    
    async def _create_platform_health_chart(self, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create platform health radar chart"""
        return {
            "chart_type": "radar",
            "title": "Platform Health Overview",
            "data": [
                {"metric": k.replace("_", " ").title(), "score": v}
                for k, v in health_data.items()
            ],
            "options": {"scale": {"min": 0, "max": 100}}
        }
    
    def _get_confidence_color(self, confidence: float) -> str:
        """Get color based on confidence level"""
        if confidence >= 0.9:
            return "#38a169"  # Green
        elif confidence >= 0.7:
            return "#d69e2e"  # Yellow
        elif confidence >= 0.5:
            return "#dd6b20"  # Orange
        else:
            return "#e53e3e"  # Red
    
    def _get_category_color(self, category: str) -> str:
        """Get color based on event category"""
        category_colors = {
            "security": "#e53e3e",
            "performance": "#3182ce",
            "business": "#d69e2e",
            "system": "#38a169",
            "user": "#805ad5"
        }
        return category_colors.get(category, "#718096")
    
    def _calculate_time_span(self, timeline_data: List[Dict[str, Any]]) -> str:
        """Calculate time span of timeline data"""
        if not timeline_data:
            return "No data"
        
        timestamps = [datetime.fromisoformat(item["x"].replace("Z", "+00:00")) 
                     for item in timeline_data]
        time_span = max(timestamps) - min(timestamps)
        
        if time_span.days > 0:
            return f"{time_span.days} days"
        elif time_span.seconds > 3600:
            return f"{time_span.seconds // 3600} hours"
        else:
            return f"{time_span.seconds // 60} minutes"


# Global visualization engine instance
visualization_engine = IntelligenceVisualizationEngine()