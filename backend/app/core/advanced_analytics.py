"""
Advanced Analytics and Intelligence Engine
=============================================

This module provides advanced analytics capabilities including:
- ML-based confidence scoring
- Behavioral pattern analysis  
- Risk assessment algorithms
- Data quality metrics
- Predictive analytics
"""

import asyncio
import logging
import json
import statistics
from typing import Dict, Any, List, Optional, Tuple, Set
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import hashlib
import re
import math

logger = logging.getLogger(__name__)


class DataQualityAnalyzer:
    """Analyzes data quality and completeness across sources"""
    
    def __init__(self):
        self.quality_metrics = {
            'completeness': 0.0,
            'consistency': 0.0,
            'accuracy': 0.0,
            'timeliness': 0.0,
            'uniqueness': 0.0,
            'validity': 0.0
        }
        
    def analyze_data_quality(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Comprehensive data quality analysis"""
        
        # Completeness - how much data is present vs expected
        completeness = self._calculate_completeness(data)
        
        # Consistency - data follows expected patterns/formats
        consistency = self._calculate_consistency(data)
        
        # Accuracy - data appears to be correct
        accuracy = self._calculate_accuracy(data)
        
        # Timeliness - how recent is the data
        timeliness = self._calculate_timeliness(data)
        
        # Uniqueness - absence of duplicates
        uniqueness = self._calculate_uniqueness(data)
        
        # Validity - data conforms to business rules
        validity = self._calculate_validity(data)
        
        return {
            'completeness': completeness,
            'consistency': consistency,
            'accuracy': accuracy,
            'timeliness': timeliness,
            'uniqueness': uniqueness,
            'validity': validity,
            'overall_score': statistics.mean([
                completeness, consistency, accuracy, 
                timeliness, uniqueness, validity
            ])
        }
    
    def _calculate_completeness(self, data: Dict[str, Any]) -> float:
        """Calculate data completeness score"""
        if not data:
            return 0.0
        
        expected_fields = {
            'basic_info', 'contact_details', 'social_profiles',
            'professional_info', 'location_data', 'verification_status'
        }
        
        present_fields = set()
        for field in expected_fields:
            if field in data and data[field] and data[field] != "unknown":
                present_fields.add(field)
        
        return len(present_fields) / len(expected_fields)
    
    def _calculate_consistency(self, data: Dict[str, Any]) -> float:
        """Calculate data consistency score"""
        consistency_checks = []
        
        # Email format consistency
        if 'emails' in data:
            emails = data['emails'] if isinstance(data['emails'], list) else [data['emails']]
            email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            valid_emails = sum(1 for email in emails if email_pattern.match(str(email)))
            consistency_checks.append(valid_emails / len(emails) if emails else 0.0)
        
        # Phone format consistency
        if 'phones' in data:
            phones = data['phones'] if isinstance(data['phones'], list) else [data['phones']]
            phone_pattern = re.compile(r'[\+]?[1-9]?[\d\s\-\(\)\.]{7,15}')
            valid_phones = sum(1 for phone in phones if phone_pattern.match(str(phone)))
            consistency_checks.append(valid_phones / len(phones) if phones else 0.0)
        
        return statistics.mean(consistency_checks) if consistency_checks else 0.5
    
    def _calculate_accuracy(self, data: Dict[str, Any]) -> float:
        """Calculate data accuracy score based on verification status"""
        accuracy_indicators = []
        
        # Verification status indicators
        if 'verification_status' in data:
            verification = data['verification_status']
            if isinstance(verification, dict):
                verified_count = sum(1 for v in verification.values() if v == 'verified')
                total_count = len(verification)
                accuracy_indicators.append(verified_count / total_count if total_count > 0 else 0.0)
        
        # Cross-source validation
        if 'source_count' in data and data['source_count'] > 1:
            # Higher source count typically indicates higher accuracy
            source_accuracy = min(data['source_count'] / 5.0, 1.0)  # Cap at 5 sources
            accuracy_indicators.append(source_accuracy)
        
        return statistics.mean(accuracy_indicators) if accuracy_indicators else 0.5
    
    def _calculate_timeliness(self, data: Dict[str, Any]) -> float:
        """Calculate data timeliness score"""
        current_time = datetime.utcnow()
        timeliness_scores = []
        
        if 'last_updated' in data:
            try:
                last_updated = datetime.fromisoformat(data['last_updated'].replace('Z', '+00:00'))
                age_days = (current_time - last_updated).days
                # Score decreases with age, 0 days = 1.0, 365 days = 0.0
                timeliness_score = max(0.0, 1.0 - (age_days / 365.0))
                timeliness_scores.append(timeliness_score)
            except (ValueError, TypeError):
                timeliness_scores.append(0.5)
        
        return statistics.mean(timeliness_scores) if timeliness_scores else 0.5
    
    def _calculate_uniqueness(self, data: Dict[str, Any]) -> float:
        """Calculate data uniqueness score"""
        # Check for duplicate entries within the dataset
        all_values = []
        
        def collect_values(obj):
            if isinstance(obj, dict):
                for v in obj.values():
                    collect_values(v)
            elif isinstance(obj, list):
                for item in obj:
                    collect_values(item)
            else:
                if obj and str(obj).strip():
                    all_values.append(str(obj).lower().strip())
        
        collect_values(data)
        
        if not all_values:
            return 1.0
        
        unique_values = len(set(all_values))
        total_values = len(all_values)
        
        return unique_values / total_values
    
    def _calculate_validity(self, data: Dict[str, Any]) -> float:
        """Calculate data validity score based on business rules"""
        validity_checks = []
        
        # Business rule: if location is provided, it should be valid
        if 'location' in data and data['location']:
            location = str(data['location'])
            # Simple validation - should contain letters and possibly comma/spaces
            if re.match(r'^[a-zA-Z\s,.-]+$', location):
                validity_checks.append(1.0)
            else:
                validity_checks.append(0.0)
        
        # Business rule: social profiles should have valid usernames
        if 'social_profiles' in data:
            profiles = data['social_profiles']
            if isinstance(profiles, dict):
                valid_profiles = 0
                total_profiles = 0
                for platform, username in profiles.items():
                    total_profiles += 1
                    # Basic username validation
                    if isinstance(username, str) and re.match(r'^[a-zA-Z0-9._-]{1,30}$', username):
                        valid_profiles += 1
                
                if total_profiles > 0:
                    validity_checks.append(valid_profiles / total_profiles)
        
        return statistics.mean(validity_checks) if validity_checks else 0.7


class BehavioralPatternAnalyzer:
    """Analyzes behavioral patterns and anomalies in data"""
    
    def __init__(self):
        self.pattern_cache = {}
        self.anomaly_threshold = 2.0  # Standard deviations
        
    def analyze_patterns(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze behavioral patterns in historical data"""
        
        patterns = {
            'temporal_patterns': self._analyze_temporal_patterns(historical_data),
            'activity_patterns': self._analyze_activity_patterns(historical_data), 
            'anomalies': self._detect_anomalies(historical_data),
            'trends': self._identify_trends(historical_data)
        }
        
        return patterns
    
    def _analyze_temporal_patterns(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze temporal activity patterns"""
        timestamps = []
        
        for record in data:
            if 'timestamp' in record:
                try:
                    ts = datetime.fromisoformat(record['timestamp'].replace('Z', '+00:00'))
                    timestamps.append(ts)
                except (ValueError, TypeError):
                    continue
        
        if not timestamps:
            return {'error': 'No valid timestamps found'}
        
        # Analyze patterns by hour, day of week, etc.
        hours = [ts.hour for ts in timestamps]
        days = [ts.weekday() for ts in timestamps]
        
        return {
            'most_active_hour': Counter(hours).most_common(1)[0][0] if hours else None,
            'most_active_day': Counter(days).most_common(1)[0][0] if days else None,
            'activity_distribution': {
                'hourly': dict(Counter(hours)),
                'daily': dict(Counter(days))
            },
            'total_records': len(timestamps)
        }
    
    def _analyze_activity_patterns(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze activity and engagement patterns"""
        activity_metrics = {
            'query_frequency': len(data),
            'unique_query_types': len(set(record.get('query_type', '') for record in data)),
            'average_confidence': 0.0,
            'source_diversity': 0.0
        }
        
        # Calculate average confidence
        confidences = [record.get('confidence_score', 0.0) for record in data if 'confidence_score' in record]
        if confidences:
            activity_metrics['average_confidence'] = statistics.mean(confidences)
        
        # Calculate source diversity
        sources = set()
        for record in data:
            if 'sources' in record:
                if isinstance(record['sources'], list):
                    sources.update(record['sources'])
                else:
                    sources.add(record['sources'])
        
        activity_metrics['source_diversity'] = len(sources)
        
        return activity_metrics
    
    def _detect_anomalies(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect anomalies in the data patterns"""
        anomalies = []
        
        # Anomaly detection based on confidence scores
        confidences = [record.get('confidence_score', 0.0) for record in data if 'confidence_score' in record]
        
        if len(confidences) > 3:
            mean_confidence = statistics.mean(confidences)
            std_confidence = statistics.stdev(confidences)
            
            for i, record in enumerate(data):
                confidence = record.get('confidence_score', 0.0)
                z_score = abs(confidence - mean_confidence) / std_confidence if std_confidence > 0 else 0
                
                if z_score > self.anomaly_threshold:
                    anomalies.append({
                        'record_index': i,
                        'anomaly_type': 'confidence_outlier',
                        'z_score': z_score,
                        'value': confidence,
                        'severity': 'high' if z_score > 3.0 else 'medium'
                    })
        
        return anomalies
    
    def _identify_trends(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Identify trends in the data"""
        trends = {
            'confidence_trend': 'stable',
            'activity_trend': 'stable',
            'quality_trend': 'stable'
        }
        
        # Analyze confidence trend over time
        time_confidence_pairs = []
        for record in data:
            if 'timestamp' in record and 'confidence_score' in record:
                try:
                    ts = datetime.fromisoformat(record['timestamp'].replace('Z', '+00:00'))
                    confidence = record['confidence_score']
                    time_confidence_pairs.append((ts, confidence))
                except (ValueError, TypeError):
                    continue
        
        if len(time_confidence_pairs) > 2:
            # Sort by timestamp
            time_confidence_pairs.sort(key=lambda x: x[0])
            
            # Simple trend analysis - compare first half vs second half
            mid_point = len(time_confidence_pairs) // 2
            first_half_avg = statistics.mean([conf for _, conf in time_confidence_pairs[:mid_point]])
            second_half_avg = statistics.mean([conf for _, conf in time_confidence_pairs[mid_point:]])
            
            if second_half_avg > first_half_avg * 1.1:
                trends['confidence_trend'] = 'improving'
            elif second_half_avg < first_half_avg * 0.9:
                trends['confidence_trend'] = 'declining'
        
        return trends


class RiskAssessmentEngine:
    """Advanced risk assessment for intelligence data"""
    
    def __init__(self):
        self.risk_factors = {
            'data_age': 0.2,
            'source_reliability': 0.3,
            'verification_status': 0.25,
            'consistency_score': 0.15,
            'completeness_score': 0.1
        }
        
    def assess_risk(self, data: Dict[str, Any], metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Comprehensive risk assessment"""
        metadata = metadata or {}
        
        risk_scores = {}
        
        # Assess individual risk factors
        risk_scores['data_age_risk'] = self._assess_data_age_risk(data)
        risk_scores['source_reliability_risk'] = self._assess_source_reliability_risk(data, metadata)
        risk_scores['verification_risk'] = self._assess_verification_risk(data)
        risk_scores['consistency_risk'] = self._assess_consistency_risk(data)
        risk_scores['completeness_risk'] = self._assess_completeness_risk(data)
        
        # Calculate overall risk score
        overall_risk = sum(
            risk_scores[risk_type] * weight
            for risk_type, weight in {
                'data_age_risk': self.risk_factors['data_age'],
                'source_reliability_risk': self.risk_factors['source_reliability'],
                'verification_risk': self.risk_factors['verification_status'],
                'consistency_risk': self.risk_factors['consistency_score'],
                'completeness_risk': self.risk_factors['completeness_score']
            }.items()
        )
        
        # Classify risk level
        risk_level = 'low'
        if overall_risk > 0.7:
            risk_level = 'high'
        elif overall_risk > 0.4:
            risk_level = 'medium'
        
        # Generate recommendations
        recommendations = self._generate_risk_recommendations(risk_scores)
        
        return {
            'overall_risk_score': overall_risk,
            'risk_level': risk_level,
            'individual_risks': risk_scores,
            'risk_factors': self.risk_factors,
            'recommendations': recommendations,
            'assessment_timestamp': datetime.utcnow().isoformat()
        }
    
    def _assess_data_age_risk(self, data: Dict[str, Any]) -> float:
        """Assess risk based on data age"""
        if 'last_updated' not in data:
            return 0.8  # High risk if no timestamp
        
        try:
            last_updated = datetime.fromisoformat(data['last_updated'].replace('Z', '+00:00'))
            age_days = (datetime.utcnow() - last_updated).days
            
            # Risk increases with age
            if age_days <= 30:
                return 0.1
            elif age_days <= 90:
                return 0.3
            elif age_days <= 365:
                return 0.6
            else:
                return 0.9
        except (ValueError, TypeError):
            return 0.8
    
    def _assess_source_reliability_risk(self, data: Dict[str, Any], metadata: Dict[str, Any]) -> float:
        """Assess risk based on source reliability"""
        source_count = data.get('source_count', 1)
        
        # More sources typically mean lower risk
        if source_count >= 5:
            return 0.1
        elif source_count >= 3:
            return 0.3
        elif source_count >= 2:
            return 0.6
        else:
            return 0.8
    
    def _assess_verification_risk(self, data: Dict[str, Any]) -> float:
        """Assess risk based on verification status"""
        verification_status = data.get('verification_status', {})
        
        if not verification_status:
            return 0.7
        
        if isinstance(verification_status, dict):
            verified_count = sum(1 for status in verification_status.values() if status == 'verified')
            total_count = len(verification_status)
            
            if total_count == 0:
                return 0.7
            
            verification_ratio = verified_count / total_count
            return 1.0 - verification_ratio
        
        return 0.5
    
    def _assess_consistency_risk(self, data: Dict[str, Any]) -> float:
        """Assess risk based on data consistency"""
        # Use the data quality analyzer
        analyzer = DataQualityAnalyzer()
        consistency_score = analyzer._calculate_consistency(data)
        
        return 1.0 - consistency_score
    
    def _assess_completeness_risk(self, data: Dict[str, Any]) -> float:
        """Assess risk based on data completeness"""
        analyzer = DataQualityAnalyzer()
        completeness_score = analyzer._calculate_completeness(data)
        
        return 1.0 - completeness_score
    
    def _generate_risk_recommendations(self, risk_scores: Dict[str, float]) -> List[str]:
        """Generate actionable risk mitigation recommendations"""
        recommendations = []
        
        if risk_scores.get('data_age_risk', 0) > 0.5:
            recommendations.append("Consider refreshing data from original sources")
        
        if risk_scores.get('source_reliability_risk', 0) > 0.5:
            recommendations.append("Seek additional data sources for cross-validation")
        
        if risk_scores.get('verification_risk', 0) > 0.5:
            recommendations.append("Implement additional verification steps")
        
        if risk_scores.get('consistency_risk', 0) > 0.5:
            recommendations.append("Review and normalize inconsistent data fields")
        
        if risk_scores.get('completeness_risk', 0) > 0.5:
            recommendations.append("Gather additional data to fill information gaps")
        
        return recommendations


class PredictiveAnalytics:
    """Predictive analytics for intelligence data"""
    
    def __init__(self):
        self.models = {}
        
    def predict_data_quality_evolution(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Predict how data quality will evolve over time"""
        
        if len(historical_data) < 3:
            return {'error': 'Insufficient historical data for prediction'}
        
        # Extract quality metrics over time
        quality_timeline = []
        analyzer = DataQualityAnalyzer()
        
        for record in historical_data:
            if 'timestamp' in record:
                try:
                    ts = datetime.fromisoformat(record['timestamp'].replace('Z', '+00:00'))
                    quality_metrics = analyzer.analyze_data_quality(record)
                    quality_timeline.append((ts, quality_metrics['overall_score']))
                except (ValueError, TypeError):
                    continue
        
        if len(quality_timeline) < 3:
            return {'error': 'Insufficient valid timestamps for prediction'}
        
        # Sort by timestamp
        quality_timeline.sort(key=lambda x: x[0])
        
        # Simple linear trend prediction
        quality_scores = [score for _, score in quality_timeline]
        
        # Calculate trend
        if len(quality_scores) >= 2:
            recent_avg = statistics.mean(quality_scores[-3:])  # Last 3 data points
            early_avg = statistics.mean(quality_scores[:3])   # First 3 data points
            
            trend_direction = 'improving' if recent_avg > early_avg else 'declining'
            trend_magnitude = abs(recent_avg - early_avg)
            
            # Predict future quality score (simple linear extrapolation)
            if len(quality_scores) >= 2:
                slope = (quality_scores[-1] - quality_scores[0]) / (len(quality_scores) - 1)
                predicted_score = max(0.0, min(1.0, quality_scores[-1] + slope * 3))  # 3 periods ahead
            else:
                predicted_score = recent_avg
            
            return {
                'current_quality': quality_scores[-1],
                'predicted_quality': predicted_score,
                'trend_direction': trend_direction,
                'trend_magnitude': trend_magnitude,
                'confidence': min(0.8, len(quality_timeline) / 10.0),  # Higher confidence with more data
                'recommendation': self._generate_quality_prediction_recommendation(
                    trend_direction, predicted_score
                )
            }
        
        return {'error': 'Unable to calculate trend'}
    
    def _generate_quality_prediction_recommendation(self, trend: str, predicted_score: float) -> str:
        """Generate recommendations based on quality predictions"""
        
        if trend == 'declining' and predicted_score < 0.5:
            return "Urgent: Data quality is declining rapidly. Implement immediate quality improvement measures."
        elif trend == 'declining':
            return "Warning: Data quality trend is declining. Consider proactive quality maintenance."
        elif predicted_score > 0.8:
            return "Good: Data quality is stable and high. Continue current practices."
        else:
            return "Monitor: Data quality is stable but could be improved with targeted efforts."


# Global instances
data_quality_analyzer = DataQualityAnalyzer()
behavioral_analyzer = BehavioralPatternAnalyzer()
risk_engine = RiskAssessmentEngine()
predictive_analytics = PredictiveAnalytics()