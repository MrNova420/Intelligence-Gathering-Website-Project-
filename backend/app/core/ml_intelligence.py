"""
Machine Learning Intelligence Module
====================================

Advanced ML-powered features for the intelligence platform:
- Intelligent source prioritization
- Automated pattern recognition
- Confidence prediction models
- Anomaly detection algorithms
- Natural language processing for data extraction
"""

import asyncio
import logging
import json
import re
import math
from typing import Dict, Any, List, Optional, Tuple, Set
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import hashlib
import statistics

logger = logging.getLogger(__name__)


class SourcePrioritizationEngine:
    """ML-powered source prioritization and reliability scoring"""
    
    def __init__(self):
        self.source_reliability_scores = {}
        self.historical_accuracy = defaultdict(list)
        self.source_response_times = defaultdict(list)
        self.source_coverage = defaultdict(set)
        
    def evaluate_source_reliability(self, source_name: str, historical_results: List[Dict[str, Any]]) -> float:
        """Evaluate and score source reliability based on historical performance"""
        
        if not historical_results:
            return 0.5  # Default neutral score
        
        reliability_factors = {
            'accuracy': self._calculate_source_accuracy(source_name, historical_results),
            'consistency': self._calculate_source_consistency(source_name, historical_results),
            'coverage': self._calculate_source_coverage(source_name, historical_results),
            'response_time': self._calculate_source_speed(source_name, historical_results),
            'freshness': self._calculate_source_freshness(source_name, historical_results)
        }
        
        # Weighted average of reliability factors
        weights = {
            'accuracy': 0.35,
            'consistency': 0.25,
            'coverage': 0.15,
            'response_time': 0.15,
            'freshness': 0.1
        }
        
        reliability_score = sum(
            reliability_factors[factor] * weight
            for factor, weight in weights.items()
        )
        
        self.source_reliability_scores[source_name] = reliability_score
        
        return reliability_score
    
    def _calculate_source_accuracy(self, source_name: str, results: List[Dict[str, Any]]) -> float:
        """Calculate accuracy based on verification success rate"""
        verified_results = 0
        total_verifiable = 0
        
        for result in results:
            if 'verification_status' in result:
                total_verifiable += 1
                if result['verification_status'] == 'verified':
                    verified_results += 1
        
        return verified_results / total_verifiable if total_verifiable > 0 else 0.5
    
    def _calculate_source_consistency(self, source_name: str, results: List[Dict[str, Any]]) -> float:
        """Calculate consistency of data format and structure"""
        if not results:
            return 0.5
        
        # Check consistency of data structure
        expected_fields = set()
        if results:
            expected_fields = set(results[0].keys())
        
        consistency_scores = []
        for result in results:
            current_fields = set(result.keys())
            field_overlap = len(expected_fields.intersection(current_fields))
            total_fields = len(expected_fields.union(current_fields))
            consistency_scores.append(field_overlap / total_fields if total_fields > 0 else 0)
        
        return statistics.mean(consistency_scores)
    
    def _calculate_source_coverage(self, source_name: str, results: List[Dict[str, Any]]) -> float:
        """Calculate coverage breadth of the source"""
        unique_data_types = set()
        
        for result in results:
            if 'data_type' in result:
                unique_data_types.add(result['data_type'])
            
            # Infer data types from structure
            if 'email' in result or 'emails' in result:
                unique_data_types.add('email')
            if 'phone' in result or 'phones' in result:
                unique_data_types.add('phone')
            if 'social' in result or 'social_profiles' in result:
                unique_data_types.add('social')
        
        # Score based on coverage breadth (max 5 types)
        return min(len(unique_data_types) / 5.0, 1.0)
    
    def _calculate_source_speed(self, source_name: str, results: List[Dict[str, Any]]) -> float:
        """Calculate source response speed score"""
        response_times = []
        
        for result in results:
            if 'processing_time' in result:
                response_times.append(result['processing_time'])
        
        if not response_times:
            return 0.5
        
        avg_response_time = statistics.mean(response_times)
        
        # Score inversely to response time (faster = better)
        # Assume 5 seconds is excellent, 30 seconds is poor
        speed_score = max(0.0, 1.0 - (avg_response_time / 30.0))
        return min(speed_score, 1.0)
    
    def _calculate_source_freshness(self, source_name: str, results: List[Dict[str, Any]]) -> float:
        """Calculate data freshness score"""
        timestamps = []
        current_time = datetime.utcnow()
        
        for result in results:
            if 'timestamp' in result:
                try:
                    ts = datetime.fromisoformat(result['timestamp'].replace('Z', '+00:00'))
                    age_hours = (current_time - ts).total_seconds() / 3600
                    timestamps.append(age_hours)
                except (ValueError, TypeError):
                    continue
        
        if not timestamps:
            return 0.5
        
        avg_age_hours = statistics.mean(timestamps)
        
        # Score based on freshness (24 hours = excellent, 168 hours = poor)
        freshness_score = max(0.0, 1.0 - (avg_age_hours / 168.0))
        return min(freshness_score, 1.0)
    
    def prioritize_sources(self, available_sources: List[str], query_context: Dict[str, Any]) -> List[Tuple[str, float]]:
        """Prioritize sources based on reliability and query context"""
        
        prioritized_sources = []
        
        for source in available_sources:
            base_score = self.source_reliability_scores.get(source, 0.5)
            
            # Apply context-based adjustments
            context_boost = self._calculate_context_boost(source, query_context)
            final_score = min(1.0, base_score + context_boost)
            
            prioritized_sources.append((source, final_score))
        
        # Sort by score (highest first)
        prioritized_sources.sort(key=lambda x: x[1], reverse=True)
        
        return prioritized_sources
    
    def _calculate_context_boost(self, source: str, context: Dict[str, Any]) -> float:
        """Calculate context-based score boost for source"""
        boost = 0.0
        
        query_type = context.get('query_type', '')
        
        # Source-specific boosts based on query type
        if 'email' in query_type.lower() and 'email' in source.lower():
            boost += 0.1
        if 'phone' in query_type.lower() and 'phone' in source.lower():
            boost += 0.1
        if 'social' in query_type.lower() and 'social' in source.lower():
            boost += 0.1
        
        # Geographic context
        if 'location' in context:
            location = context['location'].lower()
            if any(geo in source.lower() for geo in ['us', 'eu', 'global']) and any(geo in location for geo in ['united states', 'europe', 'international']):
                boost += 0.05
        
        return boost


class PatternRecognitionEngine:
    """Advanced pattern recognition for intelligence data"""
    
    def __init__(self):
        self.known_patterns = {}
        self.pattern_confidence_thresholds = {
            'email_patterns': 0.8,
            'phone_patterns': 0.85,
            'name_patterns': 0.75,
            'location_patterns': 0.7
        }
    
    def recognize_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Recognize patterns in the provided data"""
        
        patterns = {
            'email_patterns': self._recognize_email_patterns(data),
            'phone_patterns': self._recognize_phone_patterns(data),
            'name_patterns': self._recognize_name_patterns(data),
            'location_patterns': self._recognize_location_patterns(data),
            'social_patterns': self._recognize_social_patterns(data),
            'temporal_patterns': self._recognize_temporal_patterns(data)
        }
        
        # Calculate overall pattern confidence
        confidences = [p.get('confidence', 0.0) for p in patterns.values() if isinstance(p, dict)]
        overall_confidence = statistics.mean(confidences) if confidences else 0.0
        
        return {
            'patterns': patterns,
            'overall_confidence': overall_confidence,
            'high_confidence_patterns': [
                pattern_type for pattern_type, pattern_data in patterns.items()
                if isinstance(pattern_data, dict) and 
                pattern_data.get('confidence', 0.0) > self.pattern_confidence_thresholds.get(pattern_type, 0.8)
            ]
        }
    
    def _recognize_email_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Recognize email-related patterns"""
        email_data = []
        
        # Extract email information
        if 'emails' in data:
            emails = data['emails'] if isinstance(data['emails'], list) else [data['emails']]
            email_data.extend(emails)
        
        if 'email' in data:
            email_data.append(data['email'])
        
        if not email_data:
            return {'confidence': 0.0, 'patterns': []}
        
        patterns = []
        
        # Domain patterns
        domains = [email.split('@')[1] for email in email_data if '@' in str(email)]
        domain_counts = Counter(domains)
        
        if domain_counts:
            most_common_domain = domain_counts.most_common(1)[0]
            patterns.append({
                'type': 'primary_domain',
                'value': most_common_domain[0],
                'frequency': most_common_domain[1] / len(domains),
                'confidence': min(most_common_domain[1] / len(domains) * 2, 1.0)
            })
        
        # Business vs personal email patterns
        business_indicators = ['corp', 'company', 'inc', 'ltd', 'llc', 'org']
        personal_indicators = ['gmail', 'yahoo', 'hotmail', 'outlook', 'icloud']
        
        business_count = sum(1 for domain in domains if any(ind in domain.lower() for ind in business_indicators))
        personal_count = sum(1 for domain in domains if any(ind in domain.lower() for ind in personal_indicators))
        
        if business_count > personal_count:
            patterns.append({
                'type': 'professional_context',
                'confidence': business_count / len(domains) if domains else 0,
                'indication': 'business'
            })
        elif personal_count > 0:
            patterns.append({
                'type': 'professional_context',
                'confidence': personal_count / len(domains) if domains else 0,
                'indication': 'personal'
            })
        
        overall_confidence = statistics.mean([p.get('confidence', 0.0) for p in patterns]) if patterns else 0.0
        
        return {
            'confidence': overall_confidence,
            'patterns': patterns,
            'total_emails': len(email_data)
        }
    
    def _recognize_phone_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Recognize phone number patterns"""
        phone_data = []
        
        # Extract phone information
        if 'phones' in data:
            phones = data['phones'] if isinstance(data['phones'], list) else [data['phones']]
            phone_data.extend(phones)
        
        if 'phone' in data:
            phone_data.append(data['phone'])
        
        if not phone_data:
            return {'confidence': 0.0, 'patterns': []}
        
        patterns = []
        
        # Country code patterns
        country_codes = []
        for phone in phone_data:
            phone_str = str(phone)
            if phone_str.startswith('+'):
                # Extract country code (1-3 digits after +)
                match = re.match(r'\+(\d{1,3})', phone_str)
                if match:
                    country_codes.append(match.group(1))
        
        if country_codes:
            code_counts = Counter(country_codes)
            most_common_code = code_counts.most_common(1)[0]
            patterns.append({
                'type': 'primary_country_code',
                'value': most_common_code[0],
                'frequency': most_common_code[1] / len(country_codes),
                'confidence': min(most_common_code[1] / len(country_codes) * 2, 1.0)
            })
        
        # Format consistency patterns
        format_patterns = []
        for phone in phone_data:
            phone_str = str(phone)
            if re.match(r'\+\d{1,3}\s\d{3}\s\d{3}\s\d{4}', phone_str):
                format_patterns.append('international_spaced')
            elif re.match(r'\(\d{3}\)\s\d{3}-\d{4}', phone_str):
                format_patterns.append('us_parentheses')
            elif re.match(r'\d{3}-\d{3}-\d{4}', phone_str):
                format_patterns.append('us_dashed')
            else:
                format_patterns.append('other')
        
        if format_patterns:
            format_counts = Counter(format_patterns)
            most_common_format = format_counts.most_common(1)[0]
            patterns.append({
                'type': 'format_consistency',
                'value': most_common_format[0],
                'frequency': most_common_format[1] / len(format_patterns),
                'confidence': most_common_format[1] / len(format_patterns)
            })
        
        overall_confidence = statistics.mean([p.get('confidence', 0.0) for p in patterns]) if patterns else 0.0
        
        return {
            'confidence': overall_confidence,
            'patterns': patterns,
            'total_phones': len(phone_data)
        }
    
    def _recognize_name_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Recognize name patterns and variations"""
        name_data = []
        
        # Extract name information
        for field in ['name', 'full_name', 'first_name', 'last_name', 'names']:
            if field in data:
                names = data[field] if isinstance(data[field], list) else [data[field]]
                name_data.extend(names)
        
        if not name_data:
            return {'confidence': 0.0, 'patterns': []}
        
        patterns = []
        
        # Name format patterns
        format_patterns = []
        for name in name_data:
            name_str = str(name).strip()
            parts = name_str.split()
            
            if len(parts) == 2:
                format_patterns.append('first_last')
            elif len(parts) == 3:
                format_patterns.append('first_middle_last')
            elif len(parts) == 1:
                format_patterns.append('single_name')
            else:
                format_patterns.append('complex')
        
        if format_patterns:
            format_counts = Counter(format_patterns)
            most_common_format = format_counts.most_common(1)[0]
            patterns.append({
                'type': 'name_format',
                'value': most_common_format[0],
                'frequency': most_common_format[1] / len(format_patterns),
                'confidence': most_common_format[1] / len(format_patterns)
            })
        
        # Cultural/ethnic patterns (basic analysis)
        # This is a simplified example - real implementation would use more sophisticated NLP
        cultural_indicators = {
            'western': ['smith', 'johnson', 'williams', 'brown', 'jones', 'garcia', 'miller'],
            'asian': ['wong', 'lee', 'kim', 'chen', 'zhang', 'liu', 'wang'],
            'arabic': ['mohammad', 'ahmed', 'hassan', 'ali', 'ibrahim', 'omar'],
            'hispanic': ['rodriguez', 'martinez', 'hernandez', 'lopez', 'gonzalez']
        }
        
        cultural_scores = {culture: 0 for culture in cultural_indicators}
        
        for name in name_data:
            name_lower = str(name).lower()
            for culture, indicators in cultural_indicators.items():
                if any(indicator in name_lower for indicator in indicators):
                    cultural_scores[culture] += 1
        
        if any(score > 0 for score in cultural_scores.values()):
            dominant_culture = max(cultural_scores, key=cultural_scores.get)
            confidence = cultural_scores[dominant_culture] / len(name_data)
            
            if confidence > 0.3:  # Only report if confidence is reasonable
                patterns.append({
                    'type': 'cultural_pattern',
                    'value': dominant_culture,
                    'confidence': confidence
                })
        
        overall_confidence = statistics.mean([p.get('confidence', 0.0) for p in patterns]) if patterns else 0.0
        
        return {
            'confidence': overall_confidence,
            'patterns': patterns,
            'total_names': len(name_data)
        }
    
    def _recognize_location_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Recognize location and geographic patterns"""
        location_data = []
        
        # Extract location information
        for field in ['location', 'address', 'city', 'country', 'locations']:
            if field in data:
                locations = data[field] if isinstance(data[field], list) else [data[field]]
                location_data.extend(locations)
        
        if not location_data:
            return {'confidence': 0.0, 'patterns': []}
        
        patterns = []
        
        # Country patterns
        country_indicators = {
            'US': ['usa', 'united states', 'america', ' us ', 'california', 'texas', 'florida', 'new york'],
            'UK': ['united kingdom', 'england', 'scotland', 'wales', 'london', 'manchester'],
            'Canada': ['canada', 'toronto', 'vancouver', 'montreal', 'ottawa'],
            'Australia': ['australia', 'sydney', 'melbourne', 'brisbane', 'perth'],
            'Germany': ['germany', 'berlin', 'munich', 'hamburg', 'frankfurt'],
            'France': ['france', 'paris', 'lyon', 'marseille', 'toulouse']
        }
        
        country_scores = {country: 0 for country in country_indicators}
        
        for location in location_data:
            location_lower = str(location).lower()
            for country, indicators in country_indicators.items():
                if any(indicator in location_lower for indicator in indicators):
                    country_scores[country] += 1
        
        if any(score > 0 for score in country_scores.values()):
            dominant_country = max(country_scores, key=country_scores.get)
            confidence = country_scores[dominant_country] / len(location_data)
            
            patterns.append({
                'type': 'primary_country',
                'value': dominant_country,
                'confidence': confidence,
                'frequency': country_scores[dominant_country]
            })
        
        # Urban vs rural patterns (simplified)
        urban_indicators = ['city', 'downtown', 'metro', 'urban', 'street', 'avenue', 'boulevard']
        rural_indicators = ['rural', 'farm', 'country', 'village', 'township']
        
        urban_count = sum(1 for loc in location_data if any(ind in str(loc).lower() for ind in urban_indicators))
        rural_count = sum(1 for loc in location_data if any(ind in str(loc).lower() for ind in rural_indicators))
        
        if urban_count > rural_count:
            patterns.append({
                'type': 'area_type',
                'value': 'urban',
                'confidence': urban_count / len(location_data)
            })
        elif rural_count > 0:
            patterns.append({
                'type': 'area_type',
                'value': 'rural',
                'confidence': rural_count / len(location_data)
            })
        
        overall_confidence = statistics.mean([p.get('confidence', 0.0) for p in patterns]) if patterns else 0.0
        
        return {
            'confidence': overall_confidence,
            'patterns': patterns,
            'total_locations': len(location_data)
        }
    
    def _recognize_social_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Recognize social media patterns"""
        social_data = {}
        
        # Extract social media information
        if 'social_profiles' in data and isinstance(data['social_profiles'], dict):
            social_data = data['social_profiles']
        elif 'social' in data:
            social_data = data['social'] if isinstance(data['social'], dict) else {}
        
        if not social_data:
            return {'confidence': 0.0, 'patterns': []}
        
        patterns = []
        
        # Platform presence patterns
        common_platforms = ['twitter', 'linkedin', 'facebook', 'instagram', 'github', 'youtube']
        present_platforms = [platform for platform in common_platforms if platform in social_data]
        
        if present_platforms:
            patterns.append({
                'type': 'platform_diversity',
                'value': len(present_platforms),
                'platforms': present_platforms,
                'confidence': min(len(present_platforms) / 3.0, 1.0)  # Max confidence at 3+ platforms
            })
        
        # Professional vs personal platform patterns
        professional_platforms = ['linkedin', 'github']
        personal_platforms = ['instagram', 'facebook', 'tiktok']
        
        prof_count = sum(1 for p in professional_platforms if p in social_data)
        personal_count = sum(1 for p in personal_platforms if p in social_data)
        
        if prof_count > personal_count:
            patterns.append({
                'type': 'social_context',
                'value': 'professional',
                'confidence': prof_count / len(present_platforms) if present_platforms else 0
            })
        elif personal_count > prof_count:
            patterns.append({
                'type': 'social_context',
                'value': 'personal',
                'confidence': personal_count / len(present_platforms) if present_platforms else 0
            })
        
        overall_confidence = statistics.mean([p.get('confidence', 0.0) for p in patterns]) if patterns else 0.0
        
        return {
            'confidence': overall_confidence,
            'patterns': patterns,
            'total_platforms': len(social_data)
        }
    
    def _recognize_temporal_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Recognize temporal patterns in data"""
        timestamps = []
        
        # Extract timestamp information
        for field in ['timestamp', 'created_at', 'updated_at', 'last_seen']:
            if field in data:
                try:
                    ts = datetime.fromisoformat(str(data[field]).replace('Z', '+00:00'))
                    timestamps.append(ts)
                except (ValueError, TypeError):
                    continue
        
        if not timestamps:
            return {'confidence': 0.0, 'patterns': []}
        
        patterns = []
        
        # Time of day patterns
        hours = [ts.hour for ts in timestamps]
        if hours:
            hour_counts = Counter(hours)
            most_active_hour = hour_counts.most_common(1)[0]
            
            # Determine activity pattern
            if 9 <= most_active_hour[0] <= 17:
                activity_type = 'business_hours'
            elif 18 <= most_active_hour[0] <= 23:
                activity_type = 'evening'
            elif 0 <= most_active_hour[0] <= 6:
                activity_type = 'late_night'
            else:
                activity_type = 'morning'
            
            patterns.append({
                'type': 'activity_timing',
                'value': activity_type,
                'peak_hour': most_active_hour[0],
                'confidence': most_active_hour[1] / len(hours)
            })
        
        # Recency pattern
        if timestamps:
            latest_timestamp = max(timestamps)
            age_days = (datetime.utcnow() - latest_timestamp).days
            
            if age_days <= 1:
                recency = 'very_recent'
                confidence = 1.0
            elif age_days <= 7:
                recency = 'recent'
                confidence = 0.8
            elif age_days <= 30:
                recency = 'moderate'
                confidence = 0.6
            else:
                recency = 'old'
                confidence = 0.3
            
            patterns.append({
                'type': 'data_recency',
                'value': recency,
                'age_days': age_days,
                'confidence': confidence
            })
        
        overall_confidence = statistics.mean([p.get('confidence', 0.0) for p in patterns]) if patterns else 0.0
        
        return {
            'confidence': overall_confidence,
            'patterns': patterns,
            'total_timestamps': len(timestamps)
        }


class ConfidencePredictionModel:
    """ML model for predicting confidence scores"""
    
    def __init__(self):
        self.feature_weights = {
            'source_count': 0.25,
            'verification_status': 0.30,
            'data_consistency': 0.20,
            'temporal_freshness': 0.15,
            'cross_validation': 0.10
        }
        
    def predict_confidence(self, data: Dict[str, Any], metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Predict confidence score using ML-like features"""
        metadata = metadata or {}
        
        features = self._extract_features(data, metadata)
        
        # Calculate confidence score
        confidence_score = sum(
            features[feature] * weight
            for feature, weight in self.feature_weights.items()
            if feature in features
        )
        
        # Normalize to 0-1 range
        confidence_score = max(0.0, min(1.0, confidence_score))
        
        # Generate confidence intervals
        uncertainty = self._calculate_uncertainty(features)
        lower_bound = max(0.0, confidence_score - uncertainty)
        upper_bound = min(1.0, confidence_score + uncertainty)
        
        return {
            'predicted_confidence': confidence_score,
            'confidence_interval': {
                'lower': lower_bound,
                'upper': upper_bound,
                'uncertainty': uncertainty
            },
            'contributing_features': {
                feature: features[feature] * weight
                for feature, weight in self.feature_weights.items()
                if feature in features
            },
            'prediction_metadata': {
                'model_version': '1.0',
                'prediction_timestamp': datetime.utcnow().isoformat(),
                'feature_count': len(features)
            }
        }
    
    def _extract_features(self, data: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, float]:
        """Extract ML features from data"""
        features = {}
        
        # Source count feature
        source_count = data.get('source_count', metadata.get('source_count', 1))
        features['source_count'] = min(source_count / 5.0, 1.0)  # Normalize to max 5 sources
        
        # Verification status feature
        verification_status = data.get('verification_status', {})
        if isinstance(verification_status, dict) and verification_status:
            verified_count = sum(1 for status in verification_status.values() if status == 'verified')
            total_count = len(verification_status)
            features['verification_status'] = verified_count / total_count if total_count > 0 else 0.0
        else:
            features['verification_status'] = 0.5
        
        # Data consistency feature
        features['data_consistency'] = self._calculate_consistency_score(data)
        
        # Temporal freshness feature
        features['temporal_freshness'] = self._calculate_freshness_score(data)
        
        # Cross-validation feature
        features['cross_validation'] = self._calculate_cross_validation_score(data, metadata)
        
        return features
    
    def _calculate_consistency_score(self, data: Dict[str, Any]) -> float:
        """Calculate data consistency score"""
        consistency_indicators = []
        
        # Email format consistency
        if 'emails' in data:
            emails = data['emails'] if isinstance(data['emails'], list) else [data['emails']]
            email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            valid_emails = sum(1 for email in emails if email_pattern.match(str(email)))
            consistency_indicators.append(valid_emails / len(emails) if emails else 1.0)
        
        # Phone format consistency
        if 'phones' in data:
            phones = data['phones'] if isinstance(data['phones'], list) else [data['phones']]
            phone_pattern = re.compile(r'[\+]?[1-9]?[\d\s\-\(\)\.]{7,15}')
            valid_phones = sum(1 for phone in phones if phone_pattern.match(str(phone)))
            consistency_indicators.append(valid_phones / len(phones) if phones else 1.0)
        
        return statistics.mean(consistency_indicators) if consistency_indicators else 0.7
    
    def _calculate_freshness_score(self, data: Dict[str, Any]) -> float:
        """Calculate temporal freshness score"""
        timestamps = []
        current_time = datetime.utcnow()
        
        for field in ['timestamp', 'last_updated', 'created_at']:
            if field in data:
                try:
                    ts = datetime.fromisoformat(str(data[field]).replace('Z', '+00:00'))
                    age_hours = (current_time - ts).total_seconds() / 3600
                    timestamps.append(age_hours)
                except (ValueError, TypeError):
                    continue
        
        if not timestamps:
            return 0.5
        
        avg_age_hours = statistics.mean(timestamps)
        
        # Fresher data gets higher scores
        if avg_age_hours <= 24:
            return 1.0
        elif avg_age_hours <= 168:  # 1 week
            return 0.8
        elif avg_age_hours <= 720:  # 1 month
            return 0.6
        else:
            return 0.3
    
    def _calculate_cross_validation_score(self, data: Dict[str, Any], metadata: Dict[str, Any]) -> float:
        """Calculate cross-validation score"""
        # This would typically involve checking data against multiple sources
        # For now, we'll use a simplified approach
        
        cross_validation_indicators = []
        
        # Check if multiple sources agree on key facts
        if 'sources' in metadata:
            source_count = len(metadata['sources']) if isinstance(metadata['sources'], list) else 1
            cross_validation_indicators.append(min(source_count / 3.0, 1.0))
        
        # Check consistency across data fields
        if 'emails' in data and 'phones' in data:
            # If both email and phone are present, it suggests more complete validation
            cross_validation_indicators.append(0.8)
        
        return statistics.mean(cross_validation_indicators) if cross_validation_indicators else 0.5
    
    def _calculate_uncertainty(self, features: Dict[str, float]) -> float:
        """Calculate prediction uncertainty"""
        # Higher uncertainty when features are inconsistent or incomplete
        feature_values = list(features.values())
        
        if not feature_values:
            return 0.3
        
        # Use standard deviation as uncertainty measure
        if len(feature_values) > 1:
            uncertainty = statistics.stdev(feature_values) * 0.5  # Scale factor
        else:
            uncertainty = 0.2  # Default uncertainty for single feature
        
        return min(uncertainty, 0.5)  # Cap uncertainty at 0.5


class AnomalyDetectionEngine:
    """Advanced anomaly detection for intelligence data"""
    
    def __init__(self):
        self.anomaly_threshold = 2.0  # Standard deviations
        self.known_anomaly_patterns = {}
        
    def detect_anomalies(self, data: Dict[str, Any], historical_data: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Detect anomalies in current data compared to historical patterns"""
        
        anomalies = {
            'structural_anomalies': self._detect_structural_anomalies(data, historical_data),
            'value_anomalies': self._detect_value_anomalies(data, historical_data),
            'pattern_anomalies': self._detect_pattern_anomalies(data, historical_data),
            'temporal_anomalies': self._detect_temporal_anomalies(data, historical_data)
        }
        
        # Calculate overall anomaly score
        all_anomalies = []
        for anomaly_type, anomaly_list in anomalies.items():
            all_anomalies.extend(anomaly_list)
        
        anomaly_score = len(all_anomalies) / 10.0  # Normalize by expected max anomalies
        anomaly_score = min(anomaly_score, 1.0)
        
        severity_counts = Counter([a.get('severity', 'medium') for a in all_anomalies])
        
        return {
            'anomaly_score': anomaly_score,
            'total_anomalies': len(all_anomalies),
            'anomalies_by_type': anomalies,
            'severity_distribution': dict(severity_counts),
            'requires_attention': anomaly_score > 0.3 or severity_counts.get('high', 0) > 0
        }
    
    def _detect_structural_anomalies(self, data: Dict[str, Any], historical_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect structural anomalies in data"""
        anomalies = []
        
        if not historical_data:
            return anomalies
        
        # Expected structure based on historical data
        expected_fields = set()
        for record in historical_data:
            expected_fields.update(record.keys())
        
        current_fields = set(data.keys())
        
        # Missing expected fields
        missing_fields = expected_fields - current_fields
        if missing_fields:
            anomalies.append({
                'type': 'missing_fields',
                'description': f'Missing expected fields: {missing_fields}',
                'severity': 'medium',
                'fields': list(missing_fields)
            })
        
        # Unexpected new fields
        unexpected_fields = current_fields - expected_fields
        if unexpected_fields:
            anomalies.append({
                'type': 'unexpected_fields',
                'description': f'Unexpected new fields: {unexpected_fields}',
                'severity': 'low',
                'fields': list(unexpected_fields)
            })
        
        return anomalies
    
    def _detect_value_anomalies(self, data: Dict[str, Any], historical_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect value-based anomalies"""
        anomalies = []
        
        if not historical_data:
            return anomalies
        
        # Analyze numeric fields for outliers
        numeric_fields = {}
        for record in historical_data:
            for field, value in record.items():
                if isinstance(value, (int, float)):
                    if field not in numeric_fields:
                        numeric_fields[field] = []
                    numeric_fields[field].append(value)
        
        for field, values in numeric_fields.items():
            if field in data and isinstance(data[field], (int, float)) and len(values) > 2:
                mean_val = statistics.mean(values)
                std_val = statistics.stdev(values) if len(values) > 1 else 0
                
                if std_val > 0:
                    z_score = abs(data[field] - mean_val) / std_val
                    
                    if z_score > self.anomaly_threshold:
                        severity = 'high' if z_score > 3.0 else 'medium'
                        anomalies.append({
                            'type': 'value_outlier',
                            'field': field,
                            'current_value': data[field],
                            'expected_range': (mean_val - 2*std_val, mean_val + 2*std_val),
                            'z_score': z_score,
                            'severity': severity,
                            'description': f'Value {data[field]} is unusual for field {field}'
                        })
        
        return anomalies
    
    def _detect_pattern_anomalies(self, data: Dict[str, Any], historical_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect pattern-based anomalies"""
        anomalies = []
        
        if not historical_data:
            return anomalies
        
        # Analyze email domain patterns
        if 'emails' in data or 'email' in data:
            current_emails = []
            if 'emails' in data:
                current_emails = data['emails'] if isinstance(data['emails'], list) else [data['emails']]
            if 'email' in data:
                current_emails.append(data['email'])
            
            # Get historical email domains
            historical_domains = []
            for record in historical_data:
                record_emails = []
                if 'emails' in record:
                    record_emails = record['emails'] if isinstance(record['emails'], list) else [record['emails']]
                if 'email' in record:
                    record_emails.append(record['email'])
                
                for email in record_emails:
                    if '@' in str(email):
                        domain = str(email).split('@')[1]
                        historical_domains.append(domain)
            
            if historical_domains:
                common_domains = Counter(historical_domains)
                current_domains = [email.split('@')[1] for email in current_emails if '@' in str(email)]
                
                for domain in current_domains:
                    if domain not in common_domains:
                        anomalies.append({
                            'type': 'unusual_email_domain',
                            'domain': domain,
                            'severity': 'low',
                            'description': f'Email domain {domain} not seen in historical data'
                        })
        
        return anomalies
    
    def _detect_temporal_anomalies(self, data: Dict[str, Any], historical_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect temporal anomalies"""
        anomalies = []
        
        if not historical_data:
            return anomalies
        
        # Check for unusual timestamp patterns
        current_timestamp = None
        for field in ['timestamp', 'created_at', 'updated_at']:
            if field in data:
                try:
                    current_timestamp = datetime.fromisoformat(str(data[field]).replace('Z', '+00:00'))
                    break
                except (ValueError, TypeError):
                    continue
        
        if current_timestamp:
            # Get historical timestamps
            historical_timestamps = []
            for record in historical_data:
                for field in ['timestamp', 'created_at', 'updated_at']:
                    if field in record:
                        try:
                            ts = datetime.fromisoformat(str(record[field]).replace('Z', '+00:00'))
                            historical_timestamps.append(ts)
                            break
                        except (ValueError, TypeError):
                            continue
            
            if historical_timestamps:
                # Check if current timestamp is unusually old or future
                latest_historical = max(historical_timestamps)
                earliest_historical = min(historical_timestamps)
                
                if current_timestamp < earliest_historical - timedelta(days=1):
                    anomalies.append({
                        'type': 'unusually_old_timestamp',
                        'current_timestamp': current_timestamp.isoformat(),
                        'earliest_historical': earliest_historical.isoformat(),
                        'severity': 'medium',
                        'description': 'Current timestamp is unusually old compared to historical data'
                    })
                
                if current_timestamp > latest_historical + timedelta(days=1):
                    anomalies.append({
                        'type': 'future_timestamp',
                        'current_timestamp': current_timestamp.isoformat(),
                        'latest_historical': latest_historical.isoformat(),
                        'severity': 'high',
                        'description': 'Current timestamp is in the future compared to historical data'
                    })
        
        return anomalies


# Global instances
source_prioritizer = SourcePrioritizationEngine()
pattern_recognizer = PatternRecognitionEngine()
confidence_predictor = ConfidencePredictionModel()
anomaly_detector = AnomalyDetectionEngine()

# Alias for backward compatibility
MLIntelligenceEngine = SourcePrioritizationEngine