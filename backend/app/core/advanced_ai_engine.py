"""
Advanced AI Engine for Intelligence Correlation
==============================================

AAA-grade AI and machine learning capabilities for:
- Intelligent data correlation and pattern recognition
- Predictive analytics and threat assessment
- Natural language processing for reports
- Automated decision making and recommendations
- Advanced data mining and relationship mapping
"""

import asyncio
import logging
import json
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import math
import statistics

logger = logging.getLogger(__name__)


class AIModelType(str, Enum):
    """Types of AI models available"""
    CORRELATION = "correlation"
    CLASSIFICATION = "classification"
    CLUSTERING = "clustering"
    PREDICTION = "prediction"
    ANOMALY_DETECTION = "anomaly_detection"
    NATURAL_LANGUAGE = "natural_language"


class ThreatLevel(str, Enum):
    """Threat assessment levels"""
    MINIMAL = "minimal"
    LOW = "low" 
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AIInsight:
    """AI-generated insight from data analysis"""
    insight_id: str
    insight_type: str
    confidence_score: float
    description: str
    evidence: List[Dict[str, Any]]
    recommendations: List[str]
    threat_level: ThreatLevel
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class CorrelationResult:
    """Result of data correlation analysis"""
    correlation_id: str
    entities: List[str]
    correlation_strength: float
    correlation_type: str
    relationships: List[Dict[str, Any]]
    insights: List[AIInsight]
    confidence_score: float


class DataCorrelationEngine:
    """Advanced data correlation and pattern recognition engine"""
    
    def __init__(self):
        self.correlation_patterns = {}
        self.entity_graph = {}
        self.pattern_cache = {}
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    async def correlate_scan_results(
        self, 
        scan_results: List[Dict[str, Any]],
        correlation_threshold: float = 0.7
    ) -> List[CorrelationResult]:
        """
        Correlate scan results across different scanners to find patterns and relationships
        """
        correlations = []
        
        try:
            # Extract entities from scan results
            entities = self._extract_entities(scan_results)
            self.logger.info(f"Extracted {len(entities)} entities for correlation")
            
            # Build entity relationship graph
            relationship_graph = self._build_relationship_graph(entities, scan_results)
            
            # Find correlation patterns
            patterns = await self._find_correlation_patterns(
                relationship_graph, 
                correlation_threshold
            )
            
            # Generate correlation results
            for pattern in patterns:
                correlation = CorrelationResult(
                    correlation_id=f"corr_{hash(str(pattern))}",
                    entities=pattern["entities"],
                    correlation_strength=pattern["strength"],
                    correlation_type=pattern["type"],
                    relationships=pattern["relationships"],
                    insights=await self._generate_insights(pattern),
                    confidence_score=pattern["confidence"]
                )
                correlations.append(correlation)
            
            self.logger.info(f"Generated {len(correlations)} correlation results")
            return correlations
            
        except Exception as e:
            self.logger.error(f"Error in correlation analysis: {e}")
            return []
    
    def _extract_entities(self, scan_results: List[Dict[str, Any]]) -> Dict[str, Set[str]]:
        """Extract entities (emails, phones, domains, IPs) from scan results"""
        entities = {
            "emails": set(),
            "phones": set(),
            "domains": set(),
            "ips": set(),
            "names": set(),
            "usernames": set()
        }
        
        for result in scan_results:
            if not result.get("data"):
                continue
                
            data = result["data"]
            
            # Extract emails
            if "email" in data or "emails" in data:
                email_data = data.get("email", data.get("emails", []))
                if isinstance(email_data, str):
                    entities["emails"].add(email_data.lower())
                elif isinstance(email_data, list):
                    entities["emails"].update(email.lower() for email in email_data)
            
            # Extract phone numbers
            if "phone" in data or "phones" in data:
                phone_data = data.get("phone", data.get("phones", []))
                if isinstance(phone_data, str):
                    entities["phones"].add(self._normalize_phone(phone_data))
                elif isinstance(phone_data, list):
                    entities["phones"].update(self._normalize_phone(phone) for phone in phone_data)
            
            # Extract domains
            if "domain" in data or "domains" in data:
                domain_data = data.get("domain", data.get("domains", []))
                if isinstance(domain_data, str):
                    entities["domains"].add(domain_data.lower())
                elif isinstance(domain_data, list):
                    entities["domains"].update(domain.lower() for domain in domain_data)
            
            # Extract names from various fields
            name_fields = ["name", "display_name", "full_name", "names"]
            for field in name_fields:
                if field in data:
                    name_data = data[field]
                    if isinstance(name_data, str) and len(name_data.strip()) > 0:
                        entities["names"].add(name_data.strip().lower())
            
            # Extract usernames
            username_fields = ["username", "handle", "screen_name", "usernames"]
            for field in username_fields:
                if field in data:
                    username_data = data[field]
                    if isinstance(username_data, str) and len(username_data.strip()) > 0:
                        entities["usernames"].add(username_data.strip().lower())
        
        return entities
    
    def _normalize_phone(self, phone: str) -> str:
        """Normalize phone number for comparison"""
        cleaned = re.sub(r'[^\d+]', '', phone)
        if cleaned.startswith('1') and len(cleaned) == 11:
            return f"+{cleaned}"
        elif len(cleaned) == 10:
            return f"+1{cleaned}"
        return cleaned
    
    def _build_relationship_graph(
        self, 
        entities: Dict[str, Set[str]], 
        scan_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Build a graph of relationships between entities"""
        graph = {"nodes": [], "edges": [], "clusters": {}}
        
        # Create nodes for each entity
        node_id = 0
        entity_to_node = {}
        
        for entity_type, entity_set in entities.items():
            for entity in entity_set:
                node = {
                    "id": node_id,
                    "type": entity_type,
                    "value": entity,
                    "scan_count": 0,
                    "confidence": 0.0
                }
                graph["nodes"].append(node)
                entity_to_node[f"{entity_type}:{entity}"] = node_id
                node_id += 1
        
        # Create edges based on co-occurrence in scan results
        for result in scan_results:
            if not result.get("data"):
                continue
            
            # Find entities in this scan result
            result_entities = []
            for entity_type, entity_set in entities.items():
                for entity in entity_set:
                    if self._entity_in_result(entity, result["data"]):
                        result_entities.append(f"{entity_type}:{entity}")
                        # Update node scan count
                        if f"{entity_type}:{entity}" in entity_to_node:
                            node_idx = entity_to_node[f"{entity_type}:{entity}"]
                            graph["nodes"][node_idx]["scan_count"] += 1
            
            # Create edges between co-occurring entities
            for i, entity1 in enumerate(result_entities):
                for entity2 in result_entities[i+1:]:
                    if entity1 != entity2:
                        edge = {
                            "source": entity_to_node[entity1],
                            "target": entity_to_node[entity2],
                            "weight": 1,
                            "scanner": result.get("scanner_name", "unknown")
                        }
                        graph["edges"].append(edge)
        
        return graph
    
    def _entity_in_result(self, entity: str, result_data: Dict[str, Any]) -> bool:
        """Check if an entity appears in the scan result data"""
        result_str = json.dumps(result_data).lower()
        return entity.lower() in result_str
    
    async def _find_correlation_patterns(
        self, 
        graph: Dict[str, Any], 
        threshold: float
    ) -> List[Dict[str, Any]]:
        """Find correlation patterns in the relationship graph"""
        patterns = []
        
        # Analyze node clusters
        clusters = self._find_clusters(graph)
        
        for cluster in clusters:
            if len(cluster["nodes"]) < 2:
                continue
            
            # Calculate cluster strength
            strength = self._calculate_cluster_strength(cluster, graph)
            
            if strength >= threshold:
                pattern = {
                    "type": "entity_cluster",
                    "entities": [node["value"] for node in cluster["nodes"]],
                    "strength": strength,
                    "confidence": min(strength * 1.2, 1.0),
                    "relationships": cluster["edges"],
                    "cluster_id": cluster["id"]
                }
                patterns.append(pattern)
        
        return patterns
    
    def _find_clusters(self, graph: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find clusters of connected entities"""
        clusters = []
        visited = set()
        
        for node in graph["nodes"]:
            if node["id"] in visited:
                continue
            
            # Perform DFS to find connected component
            cluster_nodes = []
            cluster_edges = []
            stack = [node["id"]]
            
            while stack:
                current_id = stack.pop()
                if current_id in visited:
                    continue
                
                visited.add(current_id)
                current_node = next(n for n in graph["nodes"] if n["id"] == current_id)
                cluster_nodes.append(current_node)
                
                # Find connected nodes
                for edge in graph["edges"]:
                    if edge["source"] == current_id:
                        if edge["target"] not in visited:
                            stack.append(edge["target"])
                        cluster_edges.append(edge)
                    elif edge["target"] == current_id:
                        if edge["source"] not in visited:
                            stack.append(edge["source"])
                        cluster_edges.append(edge)
            
            if len(cluster_nodes) > 1:
                cluster = {
                    "id": len(clusters),
                    "nodes": cluster_nodes,
                    "edges": cluster_edges
                }
                clusters.append(cluster)
        
        return clusters
    
    def _calculate_cluster_strength(
        self, 
        cluster: Dict[str, Any], 
        graph: Dict[str, Any]
    ) -> float:
        """Calculate the strength of a cluster based on connectivity"""
        nodes = cluster["nodes"]
        edges = cluster["edges"]
        
        if len(nodes) < 2:
            return 0.0
        
        # Maximum possible edges in a complete graph
        max_edges = len(nodes) * (len(nodes) - 1) / 2
        
        # Actual edges
        actual_edges = len(edges)
        
        # Connectivity ratio
        connectivity = actual_edges / max_edges if max_edges > 0 else 0
        
        # Weight by node scan counts (higher scan count = more reliable)
        avg_scan_count = sum(node["scan_count"] for node in nodes) / len(nodes)
        scan_weight = min(avg_scan_count / 10.0, 1.0)  # Normalize to 0-1
        
        return connectivity * 0.7 + scan_weight * 0.3
    
    async def _generate_insights(self, pattern: Dict[str, Any]) -> List[AIInsight]:
        """Generate AI insights from correlation patterns"""
        insights = []
        
        # Analyze the pattern for potential insights
        entities = pattern["entities"]
        strength = pattern["strength"]
        
        # Generate entity relationship insight
        if len(entities) >= 2:
            insight = AIInsight(
                insight_id=f"insight_{hash(str(pattern))}",
                insight_type="entity_correlation",
                confidence_score=strength,
                description=f"Strong correlation detected between {len(entities)} entities",
                evidence=[{
                    "type": "correlation_pattern",
                    "entities": entities,
                    "strength": strength
                }],
                recommendations=[
                    "Investigate common connections between these entities",
                    "Verify if entities belong to the same person or organization",
                    "Cross-reference with additional data sources"
                ],
                threat_level=self._assess_threat_level(strength, entities)
            )
            insights.append(insight)
        
        return insights
    
    def _assess_threat_level(self, strength: float, entities: List[str]) -> ThreatLevel:
        """Assess threat level based on correlation strength and entity types"""
        if strength >= 0.9:
            return ThreatLevel.HIGH
        elif strength >= 0.8:
            return ThreatLevel.MEDIUM
        elif strength >= 0.6:
            return ThreatLevel.LOW
        else:
            return ThreatLevel.MINIMAL


class PredictiveAnalyticsEngine:
    """Predictive analytics for intelligence gathering operations"""
    
    def __init__(self):
        self.historical_data = []
        self.prediction_models = {}
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    async def predict_scan_success(
        self, 
        target: str, 
        scanner_names: List[str],
        historical_results: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Predict success probability for each scanner based on historical data"""
        predictions = {}
        
        try:
            # Analyze historical success rates
            scanner_stats = self._calculate_scanner_stats(historical_results)
            
            # Target-specific factors
            target_factors = self._analyze_target_factors(target)
            
            for scanner_name in scanner_names:
                base_success_rate = scanner_stats.get(scanner_name, {}).get("success_rate", 0.5)
                
                # Apply target-specific adjustments
                adjusted_rate = self._adjust_for_target_factors(
                    base_success_rate, 
                    target_factors, 
                    scanner_name
                )
                
                predictions[scanner_name] = min(max(adjusted_rate, 0.0), 1.0)
            
            self.logger.info(f"Generated predictions for {len(scanner_names)} scanners")
            return predictions
            
        except Exception as e:
            self.logger.error(f"Error in prediction: {e}")
            return {scanner: 0.5 for scanner in scanner_names}
    
    def _calculate_scanner_stats(self, historical_results: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
        """Calculate historical statistics for each scanner"""
        scanner_stats = {}
        
        for result in historical_results:
            scanner_name = result.get("scanner_name")
            if not scanner_name:
                continue
            
            if scanner_name not in scanner_stats:
                scanner_stats[scanner_name] = {
                    "total_runs": 0,
                    "successes": 0,
                    "avg_execution_time": 0.0,
                    "execution_times": []
                }
            
            stats = scanner_stats[scanner_name]
            stats["total_runs"] += 1
            
            if result.get("status") == "completed":
                stats["successes"] += 1
            
            if result.get("execution_time"):
                stats["execution_times"].append(result["execution_time"])
        
        # Calculate derived metrics
        for scanner_name, stats in scanner_stats.items():
            if stats["total_runs"] > 0:
                stats["success_rate"] = stats["successes"] / stats["total_runs"]
            else:
                stats["success_rate"] = 0.5
            
            if stats["execution_times"]:
                stats["avg_execution_time"] = statistics.mean(stats["execution_times"])
        
        return scanner_stats
    
    def _analyze_target_factors(self, target: str) -> Dict[str, Any]:
        """Analyze target characteristics that might affect scan success"""
        factors = {
            "target_type": "unknown",
            "domain_age": "unknown",
            "complexity": 0.5,
            "privacy_level": 0.5
        }
        
        # Determine target type
        if "@" in target:
            factors["target_type"] = "email"
            domain = target.split("@")[1]
            
            # Check if it's a major provider (might have better success rates)
            major_providers = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
            if domain.lower() in major_providers:
                factors["privacy_level"] = 0.3  # Less privacy protection
            else:
                factors["privacy_level"] = 0.7  # More privacy protection
        
        elif target.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "").isdigit():
            factors["target_type"] = "phone"
            # Phone numbers generally have moderate success rates
            factors["complexity"] = 0.4
        
        elif "." in target and not "@" in target:
            factors["target_type"] = "domain"
            factors["complexity"] = 0.6
        
        else:
            factors["target_type"] = "name_or_username"
            factors["complexity"] = 0.8  # Names are harder to validate
        
        return factors
    
    def _adjust_for_target_factors(
        self, 
        base_rate: float, 
        factors: Dict[str, Any], 
        scanner_name: str
    ) -> float:
        """Adjust success rate based on target factors and scanner characteristics"""
        adjusted_rate = base_rate
        
        # Scanner-specific adjustments
        if "email" in scanner_name.lower() and factors["target_type"] == "email":
            # Email scanners work better on email targets
            adjusted_rate *= 1.2
        elif "phone" in scanner_name.lower() and factors["target_type"] == "phone":
            # Phone scanners work better on phone targets
            adjusted_rate *= 1.2
        elif "domain" in scanner_name.lower() and factors["target_type"] == "domain":
            # Domain scanners work better on domain targets
            adjusted_rate *= 1.2
        else:
            # Cross-type scanning is less reliable
            adjusted_rate *= 0.8
        
        # Privacy level adjustment
        privacy_adjustment = 1.0 - (factors["privacy_level"] * 0.3)
        adjusted_rate *= privacy_adjustment
        
        # Complexity adjustment
        complexity_adjustment = 1.0 - (factors["complexity"] * 0.2)
        adjusted_rate *= complexity_adjustment
        
        return adjusted_rate
    
    async def estimate_completion_time(
        self, 
        scanner_names: List[str],
        historical_results: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Estimate completion time for each scanner"""
        estimates = {}
        
        scanner_stats = self._calculate_scanner_stats(historical_results)
        
        for scanner_name in scanner_names:
            stats = scanner_stats.get(scanner_name, {})
            avg_time = stats.get("avg_execution_time", 30.0)  # Default 30 seconds
            
            # Add some variance for uncertainty
            estimate = avg_time * 1.2  # 20% buffer
            estimates[scanner_name] = estimate
        
        return estimates


class NaturalLanguageProcessor:
    """Natural language processing for report generation and analysis"""
    
    def __init__(self):
        self.sentiment_keywords = {
            "positive": ["verified", "legitimate", "valid", "confirmed", "safe", "trusted"],
            "negative": ["suspicious", "fraud", "scam", "invalid", "risky", "threat"],
            "neutral": ["unknown", "pending", "processing", "analysis", "data"]
        }
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    async def generate_intelligence_summary(
        self, 
        scan_results: List[Dict[str, Any]],
        correlations: List[CorrelationResult]
    ) -> str:
        """Generate a natural language summary of intelligence findings"""
        
        try:
            # Analyze overall results
            total_scanners = len(scan_results)
            successful_scans = len([r for r in scan_results if r.get("status") == "completed"])
            
            # Extract key findings
            key_findings = self._extract_key_findings(scan_results)
            
            # Analyze sentiment
            overall_sentiment = self._analyze_sentiment(scan_results)
            
            # Build summary
            summary_parts = []
            
            # Opening statement
            success_rate = (successful_scans / total_scanners * 100) if total_scanners > 0 else 0
            summary_parts.append(
                f"Intelligence analysis completed with {successful_scans} of {total_scanners} "
                f"scanners successful ({success_rate:.1f}% success rate)."
            )
            
            # Key findings
            if key_findings:
                summary_parts.append("\nKey Findings:")
                for category, findings in key_findings.items():
                    if findings:
                        summary_parts.append(f"• {category.title()}: {findings}")
            
            # Correlations
            if correlations:
                summary_parts.append(f"\nCorrelation Analysis:")
                summary_parts.append(
                    f"• {len(correlations)} significant correlations identified"
                )
                
                for correlation in correlations[:3]:  # Top 3 correlations
                    entities_str = ", ".join(correlation.entities[:3])
                    if len(correlation.entities) > 3:
                        entities_str += f" and {len(correlation.entities) - 3} others"
                    
                    summary_parts.append(
                        f"• Strong relationship detected between {entities_str} "
                        f"(confidence: {correlation.confidence_score:.2f})"
                    )
            
            # Risk assessment
            risk_level = self._assess_overall_risk(scan_results, correlations)
            summary_parts.append(f"\nOverall Risk Assessment: {risk_level.value.title()}")
            
            # Recommendations
            recommendations = self._generate_recommendations(scan_results, correlations, risk_level)
            if recommendations:
                summary_parts.append("\nRecommendations:")
                for rec in recommendations:
                    summary_parts.append(f"• {rec}")
            
            return "\n".join(summary_parts)
            
        except Exception as e:
            self.logger.error(f"Error generating summary: {e}")
            return "Unable to generate intelligence summary due to processing error."
    
    def _extract_key_findings(self, scan_results: List[Dict[str, Any]]) -> Dict[str, str]:
        """Extract key findings from scan results"""
        findings = {}
        
        # Email findings
        email_results = [r for r in scan_results if "email" in r.get("scanner_name", "").lower()]
        if email_results:
            valid_emails = len([r for r in email_results if r.get("data", {}).get("valid", False)])
            findings["email_validation"] = f"{valid_emails} of {len(email_results)} emails validated"
        
        # Phone findings
        phone_results = [r for r in scan_results if "phone" in r.get("scanner_name", "").lower()]
        if phone_results:
            valid_phones = len([r for r in phone_results if r.get("data", {}).get("valid", False)])
            findings["phone_validation"] = f"{valid_phones} of {len(phone_results)} phone numbers validated"
        
        # Social media findings
        social_results = [r for r in scan_results if "social" in r.get("scanner_name", "").lower()]
        if social_results:
            profiles_found = sum(
                len(r.get("data", {}).get("profiles", [])) 
                for r in social_results 
                if r.get("data", {}).get("profiles")
            )
            findings["social_media"] = f"{profiles_found} social media profiles discovered"
        
        return findings
    
    def _analyze_sentiment(self, scan_results: List[Dict[str, Any]]) -> str:
        """Analyze overall sentiment of scan results"""
        sentiment_scores = {"positive": 0, "negative": 0, "neutral": 0}
        
        for result in scan_results:
            result_text = json.dumps(result.get("data", {})).lower()
            
            for sentiment, keywords in self.sentiment_keywords.items():
                for keyword in keywords:
                    if keyword in result_text:
                        sentiment_scores[sentiment] += 1
        
        if sentiment_scores["negative"] > sentiment_scores["positive"]:
            return "negative"
        elif sentiment_scores["positive"] > sentiment_scores["neutral"]:
            return "positive"
        else:
            return "neutral"
    
    def _assess_overall_risk(
        self, 
        scan_results: List[Dict[str, Any]], 
        correlations: List[CorrelationResult]
    ) -> ThreatLevel:
        """Assess overall risk level based on findings"""
        risk_factors = 0
        
        # Check for suspicious indicators
        for result in scan_results:
            data = result.get("data", {})
            
            if data.get("risk_score", 0) > 70:
                risk_factors += 2
            elif data.get("risk_score", 0) > 50:
                risk_factors += 1
            
            # Check for specific risk indicators
            risk_indicators = ["fraud", "scam", "suspicious", "malware", "phishing"]
            result_text = json.dumps(data).lower()
            
            for indicator in risk_indicators:
                if indicator in result_text:
                    risk_factors += 1
        
        # Factor in correlations
        high_confidence_correlations = len([
            c for c in correlations 
            if c.confidence_score > 0.8
        ])
        risk_factors += high_confidence_correlations
        
        # Determine risk level
        if risk_factors >= 5:
            return ThreatLevel.CRITICAL
        elif risk_factors >= 3:
            return ThreatLevel.HIGH
        elif risk_factors >= 1:
            return ThreatLevel.MEDIUM
        else:
            return ThreatLevel.LOW
    
    def _generate_recommendations(
        self, 
        scan_results: List[Dict[str, Any]], 
        correlations: List[CorrelationResult],
        risk_level: ThreatLevel
    ) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        
        # Risk-based recommendations
        if risk_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
            recommendations.append("Conduct immediate manual verification of findings")
            recommendations.append("Consider additional security measures")
        
        # Success rate recommendations
        success_rate = len([r for r in scan_results if r.get("status") == "completed"]) / len(scan_results)
        if success_rate < 0.5:
            recommendations.append("Consider using additional scanner types for better coverage")
        
        # Correlation recommendations
        if correlations:
            recommendations.append("Investigate identified entity relationships further")
            recommendations.append("Cross-reference findings with external databases")
        
        # Data quality recommendations
        incomplete_scans = len([r for r in scan_results if not r.get("data")])
        if incomplete_scans > 0:
            recommendations.append("Retry failed scans or use alternative scanners")
        
        return recommendations


class EnterpriseAIEngine:
    """Main enterprise AI engine coordinating all AI capabilities"""
    
    def __init__(self):
        self.correlation_engine = DataCorrelationEngine()
        self.predictive_engine = PredictiveAnalyticsEngine()
        self.nlp_processor = NaturalLanguageProcessor()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    async def analyze_intelligence_data(
        self, 
        scan_results: List[Dict[str, Any]],
        target: str,
        generate_summary: bool = True
    ) -> Dict[str, Any]:
        """
        Comprehensive AI analysis of intelligence data
        """
        try:
            self.logger.info(f"Starting AI analysis of {len(scan_results)} scan results")
            
            # Correlate data across scanners
            correlations = await self.correlation_engine.correlate_scan_results(scan_results)
            
            # Generate predictions for future scans
            scanner_names = list(set(r.get("scanner_name") for r in scan_results if r.get("scanner_name")))
            success_predictions = await self.predictive_engine.predict_scan_success(
                target, scanner_names, scan_results
            )
            
            time_estimates = await self.predictive_engine.estimate_completion_time(
                scanner_names, scan_results
            )
            
            # Generate natural language summary
            summary = ""
            if generate_summary:
                summary = await self.nlp_processor.generate_intelligence_summary(
                    scan_results, correlations
                )
            
            # Compile comprehensive analysis
            analysis = {
                "target": target,
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "scan_summary": {
                    "total_scanners": len(scan_results),
                    "successful_scans": len([r for r in scan_results if r.get("status") == "completed"]),
                    "failed_scans": len([r for r in scan_results if r.get("status") == "failed"]),
                    "success_rate": len([r for r in scan_results if r.get("status") == "completed"]) / len(scan_results) if scan_results else 0
                },
                "correlations": [
                    {
                        "correlation_id": c.correlation_id,
                        "entities": c.entities,
                        "strength": c.correlation_strength,
                        "type": c.correlation_type,
                        "confidence": c.confidence_score,
                        "insights": [
                            {
                                "type": insight.insight_type,
                                "description": insight.description,
                                "confidence": insight.confidence_score,
                                "threat_level": insight.threat_level.value,
                                "recommendations": insight.recommendations
                            }
                            for insight in c.insights
                        ]
                    }
                    for c in correlations
                ],
                "predictions": {
                    "scanner_success_rates": success_predictions,
                    "estimated_completion_times": time_estimates
                },
                "natural_language_summary": summary,
                "ai_insights": await self._generate_meta_insights(scan_results, correlations),
                "confidence_score": self._calculate_overall_confidence(scan_results, correlations)
            }
            
            self.logger.info("AI analysis completed successfully")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in AI analysis: {e}")
            return {
                "error": "AI analysis failed",
                "message": str(e),
                "analysis_timestamp": datetime.utcnow().isoformat()
            }
    
    async def _generate_meta_insights(
        self, 
        scan_results: List[Dict[str, Any]], 
        correlations: List[CorrelationResult]
    ) -> List[Dict[str, Any]]:
        """Generate high-level insights about the analysis process itself"""
        insights = []
        
        # Data quality insight
        complete_results = len([r for r in scan_results if r.get("data")])
        data_quality = complete_results / len(scan_results) if scan_results else 0
        
        insights.append({
            "type": "data_quality",
            "description": f"Data completeness: {data_quality:.2%}",
            "score": data_quality,
            "recommendation": "Consider additional scanners" if data_quality < 0.7 else "Good data coverage"
        })
        
        # Correlation strength insight
        if correlations:
            avg_correlation_strength = sum(c.correlation_strength for c in correlations) / len(correlations)
            insights.append({
                "type": "correlation_strength",
                "description": f"Average correlation strength: {avg_correlation_strength:.2f}",
                "score": avg_correlation_strength,
                "recommendation": "Strong correlations detected" if avg_correlation_strength > 0.7 else "Weak correlations - consider manual verification"
            })
        
        return insights
    
    def _calculate_overall_confidence(
        self, 
        scan_results: List[Dict[str, Any]], 
        correlations: List[CorrelationResult]
    ) -> float:
        """Calculate overall confidence in the analysis"""
        confidence_factors = []
        
        # Success rate factor
        success_rate = len([r for r in scan_results if r.get("status") == "completed"]) / len(scan_results) if scan_results else 0
        confidence_factors.append(success_rate)
        
        # Data completeness factor
        complete_results = len([r for r in scan_results if r.get("data")])
        data_completeness = complete_results / len(scan_results) if scan_results else 0
        confidence_factors.append(data_completeness)
        
        # Correlation confidence factor
        if correlations:
            avg_correlation_confidence = sum(c.confidence_score for c in correlations) / len(correlations)
            confidence_factors.append(avg_correlation_confidence)
        else:
            confidence_factors.append(0.5)  # Neutral when no correlations
        
        # Calculate weighted average
        return sum(confidence_factors) / len(confidence_factors)


# Global AI engine instance
ai_engine = EnterpriseAIEngine()


# Convenience functions
async def analyze_scan_results(
    scan_results: List[Dict[str, Any]], 
    target: str
) -> Dict[str, Any]:
    """Analyze scan results with AI capabilities"""
    return await ai_engine.analyze_intelligence_data(scan_results, target)


async def correlate_entities(scan_results: List[Dict[str, Any]]) -> List[CorrelationResult]:
    """Find correlations between entities in scan results"""
    return await ai_engine.correlation_engine.correlate_scan_results(scan_results)


async def predict_scanner_success(
    target: str, 
    scanner_names: List[str], 
    historical_data: List[Dict[str, Any]]
) -> Dict[str, float]:
    """Predict success rates for scanners"""
    return await ai_engine.predictive_engine.predict_scan_success(
        target, scanner_names, historical_data
    )