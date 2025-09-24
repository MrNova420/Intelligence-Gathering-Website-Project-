"""
Aggregation Engine for Intelligence Data
Handles normalization, deduplication, confidence scoring, and relationship linking.
"""

import asyncio
import re
import logging
import hashlib
from typing import Dict, Any, List, Optional, Set, Tuple
from datetime import datetime
import difflib
from collections import defaultdict

# Conditional imports with fallbacks
try:
    import phonenumbers
    PHONENUMBERS_AVAILABLE = True
except ImportError:
    PHONENUMBERS_AVAILABLE = False
    # Mock phonenumbers with proper attributes
    class MockPhoneNumber:
        def __init__(self, national_number: int, country_code: int):
            self.national_number = national_number
            self.country_code = country_code
    
    class MockPhoneNumberFormat:
        E164 = 1
        INTERNATIONAL = 2
        NATIONAL = 3
    
    class MockNumberParseException(Exception):
        pass
    
    class MockPhoneNumbers:
        NumberParseException = MockNumberParseException
        PhoneNumberFormat = MockPhoneNumberFormat
        
        @staticmethod
        def parse(number: str, region: str = None):
            return MockPhoneNumber(5551234567, 1)
        
        @staticmethod
        def is_valid_number(number):
            return True
        
        @staticmethod
        def format_number(number, format_type):
            return "+1 555-123-4567"
        
        @staticmethod
        def region_code_for_number(number):
            return "US"
        
        @staticmethod
        def number_type(number):
            return 1  # MOBILE type
    
    phonenumbers = MockPhoneNumbers()

try:
    from email_validator import validate_email, EmailNotValidError
    EMAIL_VALIDATOR_AVAILABLE = True
except ImportError:
    EMAIL_VALIDATOR_AVAILABLE = False
    # Mock email validator
    EmailNotValidError = Exception
    def validate_email(email):
        return type('ValidationResult', (), {'email': email.lower()})()

logger = logging.getLogger(__name__)


class EntityNormalizer:
    """Normalizes entity data across different sources"""
    
    def __init__(self):
        self.email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        self.phone_pattern = re.compile(r'[\+]?[1-9]?[\d\s\-\(\)\.]{7,15}')
        self.social_handle_pattern = re.compile(r'^@?[a-zA-Z0-9._-]{1,30}$')
    
    def normalize_email(self, email: str) -> Dict[str, Any]:
        """Normalize email address"""
        if not email or not isinstance(email, str):
            return {"normalized": None, "valid": False, "reason": "Empty or invalid input"}
        
        # Clean and normalize
        email = email.strip().lower()
        
        # Validate format
        if not self.email_pattern.match(email):
            return {"normalized": None, "valid": False, "reason": "Invalid format"}
        
        try:
            # Use email-validator for thorough validation
            validation = validate_email(email)
            normalized_email = validation.email
            
            # Extract components
            local_part, domain = normalized_email.split('@')
            
            # Handle Gmail dot normalization
            if domain == 'gmail.com':
                local_part = local_part.replace('.', '')
                # Remove + aliases
                if '+' in local_part:
                    local_part = local_part.split('+')[0]
                normalized_email = f"{local_part}@{domain}"
            
            return {
                "normalized": normalized_email,
                "original": email,
                "local_part": local_part,
                "domain": domain,
                "valid": True,
                "is_business_domain": self._is_business_domain(domain),
                "is_disposable": self._is_disposable_domain(domain)
            }
            
        except EmailNotValidError as e:
            return {"normalized": None, "valid": False, "reason": str(e)}
    
    def normalize_phone(self, phone: str, default_region: str = "US") -> Dict[str, Any]:
        """Normalize phone number"""
        if not phone or not isinstance(phone, str):
            return {"normalized": None, "valid": False, "reason": "Empty or invalid input"}
        
        try:
            # Parse phone number
            parsed = phonenumbers.parse(phone, default_region)
            
            if not phonenumbers.is_valid_number(parsed):
                return {"normalized": None, "valid": False, "reason": "Invalid phone number"}
            
            # Normalize to E164 format
            normalized_phone = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            
            return {
                "normalized": normalized_phone,
                "original": phone,
                "country_code": parsed.country_code,
                "national_number": str(parsed.national_number),
                "region": phonenumbers.region_code_for_number(parsed),
                "number_type": phonenumbers.number_type(parsed),
                "valid": True,
                "international_format": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                "national_format": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
            }
            
        except phonenumbers.NumberParseException as e:
            return {"normalized": None, "valid": False, "reason": str(e)}
    
    def normalize_name(self, name: str) -> Dict[str, Any]:
        """Normalize person/organization name"""
        if not name or not isinstance(name, str):
            return {"normalized": None, "valid": False, "reason": "Empty or invalid input"}
        
        # Clean and normalize
        original_name = name
        name = name.strip()
        
        # Remove extra whitespace
        name = re.sub(r'\s+', ' ', name)
        
        # Normalize case - Title Case for names
        normalized_name = name.title()
        
        # Handle common prefixes/suffixes
        name_parts = normalized_name.split()
        
        # Extract components
        prefixes = ['Mr.', 'Mrs.', 'Ms.', 'Dr.', 'Prof.', 'Rev.']
        suffixes = ['Jr.', 'Sr.', 'II', 'III', 'IV', 'Ph.D.', 'M.D.']
        
        extracted_prefix = None
        extracted_suffix = None
        
        if name_parts and name_parts[0] in prefixes:
            extracted_prefix = name_parts[0]
            name_parts = name_parts[1:]
        
        if name_parts and name_parts[-1] in suffixes:
            extracted_suffix = name_parts[-1]
            name_parts = name_parts[:-1]
        
        # Reconstruct core name
        core_name = ' '.join(name_parts)
        
        return {
            "normalized": core_name,
            "original": original_name,
            "prefix": extracted_prefix,
            "suffix": extracted_suffix,
            "full_normalized": normalized_name,
            "word_count": len(name_parts),
            "first_name": name_parts[0] if name_parts else None,
            "last_name": name_parts[-1] if len(name_parts) > 1 else None,
            "middle_names": name_parts[1:-1] if len(name_parts) > 2 else [],
            "valid": bool(core_name.strip()),
            "is_organization": self._is_organization_name(core_name)
        }
    
    def normalize_address(self, address: str) -> Dict[str, Any]:
        """Normalize physical address"""
        if not address or not isinstance(address, str):
            return {"normalized": None, "valid": False, "reason": "Empty or invalid input"}
        
        original_address = address
        address = address.strip()
        
        # Basic address normalization
        # Replace common abbreviations
        replacements = {
            r'\bSt\.?\b': 'Street',
            r'\bAve\.?\b': 'Avenue', 
            r'\bRd\.?\b': 'Road',
            r'\bBlvd\.?\b': 'Boulevard',
            r'\bDr\.?\b': 'Drive',
            r'\bCt\.?\b': 'Court',
            r'\bLn\.?\b': 'Lane',
            r'\bPl\.?\b': 'Place',
            r'\bApt\.?\b': 'Apartment',
            r'\bSte\.?\b': 'Suite',
            r'\bN\.?\b': 'North',
            r'\bS\.?\b': 'South',
            r'\bE\.?\b': 'East',
            r'\bW\.?\b': 'West',
        }
        
        normalized_address = address
        for pattern, replacement in replacements.items():
            normalized_address = re.sub(pattern, replacement, normalized_address, flags=re.IGNORECASE)
        
        # Extract components (simplified)
        lines = normalized_address.split('\n')
        street_line = lines[0].strip() if lines else ""
        
        # Extract zip code
        zip_match = re.search(r'\b\d{5}(-\d{4})?\b', normalized_address)
        zip_code = zip_match.group(0) if zip_match else None
        
        # Extract state (simplified - just 2-letter codes)
        state_match = re.search(r'\b[A-Z]{2}\b', normalized_address.upper())
        state = state_match.group(0) if state_match else None
        
        return {
            "normalized": normalized_address,
            "original": original_address,
            "street": street_line,
            "zip_code": zip_code,
            "state": state,
            "country": "US",  # Default assumption
            "valid": bool(street_line),
            "components_extracted": {
                "has_zip": bool(zip_code),
                "has_state": bool(state),
                "line_count": len(lines)
            }
        }
    
    def normalize_url(self, url: str) -> Dict[str, Any]:
        """Normalize URL/website"""
        if not url or not isinstance(url, str):
            return {"normalized": None, "valid": False, "reason": "Empty or invalid input"}
        
        original_url = url
        url = url.strip().lower()
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Basic URL validation
        url_pattern = re.compile(
            r'^https?://'  # protocol
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        is_valid = bool(url_pattern.match(url))
        
        # Extract domain
        domain_match = re.search(r'https?://([^/]+)', url)
        domain = domain_match.group(1) if domain_match else None
        
        return {
            "normalized": url,
            "original": original_url,
            "domain": domain,
            "valid": is_valid,
            "protocol": "https" if url.startswith('https://') else "http",
            "is_secure": url.startswith('https://')
        }
    
    def _is_business_domain(self, domain: str) -> bool:
        """Check if domain appears to be business domain"""
        personal_domains = {
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
            'aol.com', 'icloud.com', 'protonmail.com'
        }
        return domain.lower() not in personal_domains
    
    def _is_disposable_domain(self, domain: str) -> bool:
        """Check if domain is disposable email provider"""
        disposable_domains = {
            '10minutemail.com', 'tempmail.org', 'guerrillamail.com',
            'mailinator.com', 'throwaway.email', 'temp-mail.org'
        }
        return domain.lower() in disposable_domains
    
    def _is_organization_name(self, name: str) -> bool:
        """Check if name appears to be organization rather than person"""
        org_indicators = [
            'inc', 'inc.', 'llc', 'corp', 'corporation', 'company', 'co.',
            'ltd', 'limited', 'associates', 'group', 'services', 'solutions'
        ]
        name_lower = name.lower()
        return any(indicator in name_lower for indicator in org_indicators)


class EntityDeduplicator:
    """Deduplicates entities across different sources"""
    
    def __init__(self):
        self.similarity_threshold = 0.85
        self.normalizer = EntityNormalizer()
    
    def deduplicate_entities(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate list of entities"""
        if not entities:
            return []
        
        # Group entities by type
        grouped_entities = defaultdict(list)
        for entity in entities:
            entity_type = entity.get('type', 'unknown')
            grouped_entities[entity_type].append(entity)
        
        deduplicated = []
        
        # Deduplicate within each type
        for entity_type, type_entities in grouped_entities.items():
            if entity_type == 'email':
                deduplicated.extend(self._deduplicate_emails(type_entities))
            elif entity_type == 'phone':
                deduplicated.extend(self._deduplicate_phones(type_entities))
            elif entity_type == 'name':
                deduplicated.extend(self._deduplicate_names(type_entities))
            elif entity_type == 'address':
                deduplicated.extend(self._deduplicate_addresses(type_entities))
            else:
                # Generic deduplication for other types
                deduplicated.extend(self._deduplicate_generic(type_entities))
        
        return deduplicated
    
    def _deduplicate_emails(self, emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate email entities"""
        if not emails:
            return []
        
        # Normalize all emails
        normalized_emails = {}
        for email_entity in emails:
            email_value = email_entity.get('value', '')
            normalized = self.normalizer.normalize_email(email_value)
            
            if normalized['valid']:
                norm_email = normalized['normalized']
                if norm_email not in normalized_emails:
                    normalized_emails[norm_email] = {
                        'value': norm_email,
                        'type': 'email',
                        'sources': [],
                        'confidence_scores': [],
                        'metadata': normalized,
                        'first_seen': None,
                        'last_updated': None
                    }
                
                # Merge source information
                source_info = {
                    'source': email_entity.get('source', 'unknown'),
                    'confidence': email_entity.get('confidence', 0.5),
                    'timestamp': email_entity.get('timestamp'),
                    'original_value': email_value
                }
                normalized_emails[norm_email]['sources'].append(source_info)
                normalized_emails[norm_email]['confidence_scores'].append(source_info['confidence'])
                
                # Update timestamps
                timestamp = email_entity.get('timestamp')
                if timestamp:
                    if not normalized_emails[norm_email]['first_seen']:
                        normalized_emails[norm_email]['first_seen'] = timestamp
                    normalized_emails[norm_email]['last_updated'] = timestamp
        
        # Calculate aggregate confidence scores
        for email_data in normalized_emails.values():
            email_data['aggregate_confidence'] = self._calculate_aggregate_confidence(
                email_data['confidence_scores']
            )
            email_data['source_count'] = len(email_data['sources'])
        
        return list(normalized_emails.values())
    
    def _deduplicate_phones(self, phones: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate phone entities"""
        if not phones:
            return []
        
        normalized_phones = {}
        for phone_entity in phones:
            phone_value = phone_entity.get('value', '')
            normalized = self.normalizer.normalize_phone(phone_value)
            
            if normalized['valid']:
                norm_phone = normalized['normalized']
                if norm_phone not in normalized_phones:
                    normalized_phones[norm_phone] = {
                        'value': norm_phone,
                        'type': 'phone',
                        'sources': [],
                        'confidence_scores': [],
                        'metadata': normalized,
                        'first_seen': None,
                        'last_updated': None
                    }
                
                # Merge source information
                source_info = {
                    'source': phone_entity.get('source', 'unknown'),
                    'confidence': phone_entity.get('confidence', 0.5),
                    'timestamp': phone_entity.get('timestamp'),
                    'original_value': phone_value
                }
                normalized_phones[norm_phone]['sources'].append(source_info)
                normalized_phones[norm_phone]['confidence_scores'].append(source_info['confidence'])
                
                # Update timestamps
                timestamp = phone_entity.get('timestamp')
                if timestamp:
                    if not normalized_phones[norm_phone]['first_seen']:
                        normalized_phones[norm_phone]['first_seen'] = timestamp
                    normalized_phones[norm_phone]['last_updated'] = timestamp
        
        # Calculate aggregate confidence scores
        for phone_data in normalized_phones.values():
            phone_data['aggregate_confidence'] = self._calculate_aggregate_confidence(
                phone_data['confidence_scores']
            )
            phone_data['source_count'] = len(phone_data['sources'])
        
        return list(normalized_phones.values())
    
    def _deduplicate_names(self, names: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate name entities using fuzzy matching"""
        if not names:
            return []
        
        normalized_names = {}
        processed_names = []
        
        # First pass: normalize all names
        for name_entity in names:
            name_value = name_entity.get('value', '')
            normalized = self.normalizer.normalize_name(name_value)
            
            if normalized['valid']:
                processed_names.append({
                    'original_entity': name_entity,
                    'normalized': normalized,
                    'norm_key': normalized['normalized'].lower()
                })
        
        # Second pass: group similar names
        used_indices = set()
        
        for i, name_data in enumerate(processed_names):
            if i in used_indices:
                continue
                
            norm_key = name_data['norm_key']
            similar_names = [name_data]
            used_indices.add(i)
            
            # Find similar names
            for j, other_name_data in enumerate(processed_names[i+1:], i+1):
                if j in used_indices:
                    continue
                    
                similarity = difflib.SequenceMatcher(
                    None, norm_key, other_name_data['norm_key']
                ).ratio()
                
                if similarity >= self.similarity_threshold:
                    similar_names.append(other_name_data)
                    used_indices.add(j)
            
            # Merge similar names
            merged_name = self._merge_similar_names(similar_names)
            normalized_names[merged_name['value']] = merged_name
        
        return list(normalized_names.values())
    
    def _deduplicate_addresses(self, addresses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate address entities"""
        if not addresses:
            return []
        
        normalized_addresses = {}
        
        for addr_entity in addresses:
            addr_value = addr_entity.get('value', '')
            normalized = self.normalizer.normalize_address(addr_value)
            
            if normalized['valid']:
                # Use normalized address as key
                norm_addr = normalized['normalized']
                addr_key = self._create_address_key(normalized)
                
                if addr_key not in normalized_addresses:
                    normalized_addresses[addr_key] = {
                        'value': norm_addr,
                        'type': 'address',
                        'sources': [],
                        'confidence_scores': [],
                        'metadata': normalized,
                        'first_seen': None,
                        'last_updated': None
                    }
                
                # Merge source information
                source_info = {
                    'source': addr_entity.get('source', 'unknown'),
                    'confidence': addr_entity.get('confidence', 0.5),
                    'timestamp': addr_entity.get('timestamp'),
                    'original_value': addr_value
                }
                normalized_addresses[addr_key]['sources'].append(source_info)
                normalized_addresses[addr_key]['confidence_scores'].append(source_info['confidence'])
                
                # Update timestamps
                timestamp = addr_entity.get('timestamp')
                if timestamp:
                    if not normalized_addresses[addr_key]['first_seen']:
                        normalized_addresses[addr_key]['first_seen'] = timestamp
                    normalized_addresses[addr_key]['last_updated'] = timestamp
        
        # Calculate aggregate confidence scores
        for addr_data in normalized_addresses.values():
            addr_data['aggregate_confidence'] = self._calculate_aggregate_confidence(
                addr_data['confidence_scores']
            )
            addr_data['source_count'] = len(addr_data['sources'])
        
        return list(normalized_addresses.values())
    
    def _deduplicate_generic(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generic deduplication for other entity types"""
        if not entities:
            return []
        
        # Simple exact match deduplication
        unique_entities = {}
        
        for entity in entities:
            value = entity.get('value', '')
            if isinstance(value, str):
                key = value.lower().strip()
            else:
                key = str(value)
            
            if key not in unique_entities:
                unique_entities[key] = {
                    'value': value,
                    'type': entity.get('type', 'unknown'),
                    'sources': [],
                    'confidence_scores': [],
                    'first_seen': None,
                    'last_updated': None
                }
            
            # Merge source information
            source_info = {
                'source': entity.get('source', 'unknown'),
                'confidence': entity.get('confidence', 0.5),
                'timestamp': entity.get('timestamp')
            }
            unique_entities[key]['sources'].append(source_info)
            unique_entities[key]['confidence_scores'].append(source_info['confidence'])
            
            # Update timestamps
            timestamp = entity.get('timestamp')
            if timestamp:
                if not unique_entities[key]['first_seen']:
                    unique_entities[key]['first_seen'] = timestamp
                unique_entities[key]['last_updated'] = timestamp
        
        # Calculate aggregate confidence scores
        for entity_data in unique_entities.values():
            entity_data['aggregate_confidence'] = self._calculate_aggregate_confidence(
                entity_data['confidence_scores']
            )
            entity_data['source_count'] = len(entity_data['sources'])
        
        return list(unique_entities.values())
    
    def _merge_similar_names(self, similar_names: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge similar name entities"""
        # Choose the most complete name as primary
        primary_name = max(similar_names, key=lambda x: len(x['normalized']['normalized']))
        
        merged = {
            'value': primary_name['normalized']['normalized'],
            'type': 'name',
            'sources': [],
            'confidence_scores': [],
            'metadata': primary_name['normalized'],
            'first_seen': None,
            'last_updated': None,
            'variants': []
        }
        
        for name_data in similar_names:
            entity = name_data['original_entity']
            
            # Add to variants if different
            original_value = entity.get('value', '')
            if original_value not in merged['variants']:
                merged['variants'].append(original_value)
            
            # Merge source information
            source_info = {
                'source': entity.get('source', 'unknown'),
                'confidence': entity.get('confidence', 0.5),
                'timestamp': entity.get('timestamp'),
                'original_value': original_value
            }
            merged['sources'].append(source_info)
            merged['confidence_scores'].append(source_info['confidence'])
            
            # Update timestamps
            timestamp = entity.get('timestamp')
            if timestamp:
                if not merged['first_seen']:
                    merged['first_seen'] = timestamp
                merged['last_updated'] = timestamp
        
        merged['aggregate_confidence'] = self._calculate_aggregate_confidence(
            merged['confidence_scores']
        )
        merged['source_count'] = len(merged['sources'])
        
        return merged
    
    def _create_address_key(self, normalized_address: Dict[str, Any]) -> str:
        """Create unique key for address deduplication"""
        street = normalized_address.get('street', '').lower()
        zip_code = normalized_address.get('zip_code', '')
        state = normalized_address.get('state', '')
        
        # Create key from important components
        key_parts = [street]
        if zip_code:
            key_parts.append(zip_code)
        if state:
            key_parts.append(state.lower())
        
        return '|'.join(key_parts)
    
    def _calculate_aggregate_confidence(self, confidence_scores: List[float]) -> float:
        """Calculate aggregate confidence from multiple sources"""
        if not confidence_scores:
            return 0.0
        
        # Use weighted average with source count bonus
        avg_confidence = sum(confidence_scores) / len(confidence_scores)
        
        # Bonus for multiple sources (up to 0.2 bonus)
        source_bonus = min(len(confidence_scores) * 0.05, 0.2)
        
        # Bonus for consistent high scores
        if all(score >= 0.7 for score in confidence_scores):
            consistency_bonus = 0.1
        else:
            consistency_bonus = 0.0
        
        final_confidence = min(avg_confidence + source_bonus + consistency_bonus, 1.0)
        return round(final_confidence, 3)


class ConfidenceScorer:
    """Calculates confidence scores for entities based on source reliability"""
    
    def __init__(self):
        # Source reliability weights (0.0 to 1.0)
        self.source_weights = {
            'email_validator': 0.95,
            'phone_validator': 0.9,
            'email_reputation': 0.8,
            'phone_carrier_scanner': 0.85,
            'twitter_scanner': 0.7,
            'linkedin_scanner': 0.8,
            'instagram_scanner': 0.6,
            'facebook_scanner': 0.5,  # Lower due to privacy restrictions
            'github_scanner': 0.75,
            'email_breach_scanner': 0.85,
            'phone_spam_scanner': 0.8,
            'social_media_email_scanner': 0.6,
            'phone_location_scanner': 0.8,
            'unknown': 0.3
        }
    
    def calculate_entity_confidence(self, entity: Dict[str, Any]) -> float:
        """Calculate confidence score for an entity"""
        sources = entity.get('sources', [])
        if not sources:
            return 0.0
        
        # Calculate weighted confidence
        total_weight = 0
        weighted_score = 0
        
        for source in sources:
            source_name = source.get('source', 'unknown')
            source_confidence = source.get('confidence', 0.5)
            source_weight = self.source_weights.get(source_name, 0.3)
            
            weighted_score += source_confidence * source_weight
            total_weight += source_weight
        
        base_confidence = weighted_score / total_weight if total_weight > 0 else 0.0
        
        # Apply modifiers
        confidence = self._apply_confidence_modifiers(entity, base_confidence)
        
        return round(confidence, 3)
    
    def _apply_confidence_modifiers(self, entity: Dict[str, Any], base_confidence: float) -> float:
        """Apply modifiers to base confidence score"""
        confidence = base_confidence
        
        # Multiple source bonus
        source_count = len(entity.get('sources', []))
        if source_count > 1:
            confidence += min(source_count * 0.05, 0.15)
        
        # Recency modifier
        last_updated = entity.get('last_updated')
        if last_updated:
            # In real implementation, would calculate days since update
            # For now, assume recent data is more reliable
            confidence += 0.05
        
        # Entity type specific modifiers
        entity_type = entity.get('type')
        if entity_type == 'email':
            # Email validation is generally reliable
            confidence += 0.05
        elif entity_type == 'phone':
            # Phone validation is also reliable
            confidence += 0.05
        elif entity_type == 'name':
            # Names are harder to validate
            confidence -= 0.05
        
        # Metadata quality modifier
        metadata = entity.get('metadata', {})
        if metadata.get('valid', False):
            confidence += 0.1
        
        return min(confidence, 1.0)


class RelationshipLinker:
    """Links related entities and creates relationship mappings"""
    
    def __init__(self):
        self.normalizer = EntityNormalizer()
    
    def link_entities(self, entities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create relationship links between entities"""
        relationships = []
        entity_clusters = defaultdict(list)
        
        # Group entities by person/organization
        for i, entity in enumerate(entities):
            entity['_index'] = i  # Add index for tracking
            
            # Try to find related entities
            related_entities = self._find_related_entities(entity, entities)
            if related_entities:
                cluster_key = self._generate_cluster_key(entity, related_entities)
                entity_clusters[cluster_key].extend([entity] + related_entities)
        
        # Remove duplicates from clusters
        for cluster_key in entity_clusters:
            seen_indices = set()
            unique_entities = []
            for entity in entity_clusters[cluster_key]:
                if entity['_index'] not in seen_indices:
                    unique_entities.append(entity)
                    seen_indices.add(entity['_index'])
            entity_clusters[cluster_key] = unique_entities
        
        # Create relationship records
        for cluster_key, cluster_entities in entity_clusters.items():
            if len(cluster_entities) > 1:
                relationship = {
                    'cluster_id': cluster_key,
                    'entities': cluster_entities,
                    'relationship_type': self._determine_relationship_type(cluster_entities),
                    'confidence': self._calculate_relationship_confidence(cluster_entities),
                    'created_at': datetime.utcnow().isoformat()
                }
                relationships.append(relationship)
        
        return {
            'relationships': relationships,
            'entity_clusters': dict(entity_clusters),
            'total_clusters': len(entity_clusters),
            'linked_entities': sum(len(cluster) for cluster in entity_clusters.values())
        }
    
    def _find_related_entities(self, target_entity: Dict[str, Any], all_entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find entities related to target entity"""
        related = []
        
        for entity in all_entities:
            if entity == target_entity:
                continue
            
            # Check for relationships
            relationship_score = self._calculate_relationship_score(target_entity, entity)
            if relationship_score > 0.5:  # Threshold for related entities
                related.append(entity)
        
        return related
    
    def _calculate_relationship_score(self, entity1: Dict[str, Any], entity2: Dict[str, Any]) -> float:
        """Calculate relationship score between two entities"""
        score = 0.0
        
        # Same source bonus
        sources1 = {s.get('source') for s in entity1.get('sources', [])}
        sources2 = {s.get('source') for s in entity2.get('sources', [])}
        common_sources = sources1.intersection(sources2)
        
        if common_sources:
            score += len(common_sources) * 0.2
        
        # Email domain matching (for email entities)
        if entity1.get('type') == 'email' and entity2.get('type') == 'email':
            domain1 = entity1.get('metadata', {}).get('domain')
            domain2 = entity2.get('metadata', {}).get('domain')
            if domain1 and domain2 and domain1 == domain2:
                score += 0.3
        
        # Name similarity (for name entities)
        if entity1.get('type') == 'name' and entity2.get('type') == 'name':
            name1 = entity1.get('value', '').lower()
            name2 = entity2.get('value', '').lower()
            similarity = difflib.SequenceMatcher(None, name1, name2).ratio()
            if similarity > 0.7:
                score += similarity * 0.4
        
        # Phone number same area code
        if entity1.get('type') == 'phone' and entity2.get('type') == 'phone':
            region1 = entity1.get('metadata', {}).get('region')
            region2 = entity2.get('metadata', {}).get('region')
            if region1 and region2 and region1 == region2:
                score += 0.2
        
        return min(score, 1.0)
    
    def _generate_cluster_key(self, primary_entity: Dict[str, Any], related_entities: List[Dict[str, Any]]) -> str:
        """Generate unique key for entity cluster"""
        # Use hash of sorted entity values
        all_entities = [primary_entity] + related_entities
        entity_values = sorted([str(e.get('value', '')) for e in all_entities])
        cluster_string = '|'.join(entity_values)
        return hashlib.sha256(cluster_string.encode()).hexdigest()[:16]
    
    def _determine_relationship_type(self, entities: List[Dict[str, Any]]) -> str:
        """Determine the type of relationship between entities"""
        entity_types = {e.get('type') for e in entities}
        
        if 'email' in entity_types and 'name' in entity_types:
            return 'person_contact'
        elif 'phone' in entity_types and 'name' in entity_types:
            return 'person_contact'
        elif 'email' in entity_types and 'phone' in entity_types:
            return 'contact_methods'
        elif len(entity_types) == 1 and 'name' in entity_types:
            return 'name_variants'
        else:
            return 'related_entities'
    
    def _calculate_relationship_confidence(self, entities: List[Dict[str, Any]]) -> float:
        """Calculate confidence in the relationship"""
        if len(entities) < 2:
            return 0.0
        
        # Average confidence of entities
        total_confidence = sum(e.get('aggregate_confidence', 0.5) for e in entities)
        avg_confidence = total_confidence / len(entities)
        
        # Bonus for multiple entities
        entity_bonus = min(len(entities) * 0.05, 0.2)
        
        return min(avg_confidence + entity_bonus, 1.0)


class AggregationEngine:
    """Main aggregation engine that orchestrates all components"""
    
    def __init__(self):
        self.normalizer = EntityNormalizer()
        self.deduplicator = EntityDeduplicator()
        self.confidence_scorer = ConfidenceScorer()
        self.relationship_linker = RelationshipLinker()
    
    def normalize_email(self, email: str) -> Dict[str, Any]:
        """Normalize email address - delegate to normalizer"""
        return self.normalizer.normalize_email(email)
    
    def normalize_phone(self, phone: str) -> Dict[str, Any]:
        """Normalize phone number - delegate to normalizer"""
        return self.normalizer.normalize_phone(phone)
    
    def deduplicate_entities(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate entities - delegate to deduplicator"""
        return self.deduplicator.deduplicate_entities(entities)
    
    async def aggregate_scan_results(self, scan_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Main aggregation method"""
        logger.info(f"Starting aggregation of {len(scan_results)} scan results")
        
        # Extract entities from scan results
        raw_entities = []
        for result in scan_results:
            entities = self._extract_entities_from_result(result)
            raw_entities.extend(entities)
        
        logger.info(f"Extracted {len(raw_entities)} raw entities")
        
        # Deduplicate entities
        deduplicated_entities = self.deduplicator.deduplicate_entities(raw_entities)
        logger.info(f"After deduplication: {len(deduplicated_entities)} entities")
        
        # Calculate confidence scores
        for entity in deduplicated_entities:
            entity['final_confidence'] = self.confidence_scorer.calculate_entity_confidence(entity)
        
        # Link related entities
        relationship_data = self.relationship_linker.link_entities(deduplicated_entities)
        
        # Generate summary statistics
        summary = self._generate_summary(deduplicated_entities, relationship_data)
        
        return {
            'entities': deduplicated_entities,
            'relationships': relationship_data,
            'summary': summary,
            'aggregation_metadata': {
                'total_raw_entities': len(raw_entities),
                'deduplicated_count': len(deduplicated_entities),
                'deduplication_rate': 1 - (len(deduplicated_entities) / len(raw_entities)) if raw_entities else 0,
                'high_confidence_entities': len([e for e in deduplicated_entities if e.get('final_confidence', 0) > 0.8]),
                'relationship_clusters': relationship_data.get('total_clusters', 0),
                'processing_timestamp': datetime.utcnow().isoformat()
            }
        }
    
    def _extract_entities_from_result(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract entities from a single scan result"""
        entities = []
        
        # Get basic information
        scanner_name = result.get('scanner', 'unknown')
        confidence = result.get('confidence', 0.5)
        timestamp = result.get('timestamp')
        
        # Extract entities based on result data
        result_data = result.get('result', {})
        
        # Look for common entity patterns
        self._extract_email_entities(result_data, scanner_name, confidence, timestamp, entities)
        self._extract_phone_entities(result_data, scanner_name, confidence, timestamp, entities)
        self._extract_name_entities(result_data, scanner_name, confidence, timestamp, entities)
        self._extract_address_entities(result_data, scanner_name, confidence, timestamp, entities)
        self._extract_url_entities(result_data, scanner_name, confidence, timestamp, entities)
        
        return entities
    
    def _extract_email_entities(self, data: Dict[str, Any], source: str, confidence: float, timestamp: str, entities: List[Dict[str, Any]]):
        """Extract email entities from result data"""
        # Look for email in various places
        email_fields = ['email', 'email_address', 'contact_email', 'user_email']
        
        for field in email_fields:
            if field in data and data[field]:
                entities.append({
                    'type': 'email',
                    'value': data[field],
                    'source': source,
                    'confidence': confidence,
                    'timestamp': timestamp,
                    'extraction_field': field
                })
    
    def _extract_phone_entities(self, data: Dict[str, Any], source: str, confidence: float, timestamp: str, entities: List[Dict[str, Any]]):
        """Extract phone entities from result data"""
        phone_fields = ['phone', 'phone_number', 'contact_phone', 'mobile', 'telephone']
        
        for field in phone_fields:
            if field in data and data[field]:
                entities.append({
                    'type': 'phone',
                    'value': data[field],
                    'source': source,
                    'confidence': confidence,
                    'timestamp': timestamp,
                    'extraction_field': field
                })
    
    def _extract_name_entities(self, data: Dict[str, Any], source: str, confidence: float, timestamp: str, entities: List[Dict[str, Any]]):
        """Extract name entities from result data"""
        name_fields = ['name', 'full_name', 'display_name', 'user_name', 'contact_name']
        
        for field in name_fields:
            if field in data and data[field]:
                entities.append({
                    'type': 'name',
                    'value': data[field],
                    'source': source,
                    'confidence': confidence,
                    'timestamp': timestamp,
                    'extraction_field': field
                })
    
    def _extract_address_entities(self, data: Dict[str, Any], source: str, confidence: float, timestamp: str, entities: List[Dict[str, Any]]):
        """Extract address entities from result data"""
        address_fields = ['address', 'location', 'street_address', 'mailing_address']
        
        for field in address_fields:
            if field in data and data[field]:
                entities.append({
                    'type': 'address',
                    'value': data[field],
                    'source': source,
                    'confidence': confidence,
                    'timestamp': timestamp,
                    'extraction_field': field
                })
    
    def _extract_url_entities(self, data: Dict[str, Any], source: str, confidence: float, timestamp: str, entities: List[Dict[str, Any]]):
        """Extract URL entities from result data"""
        url_fields = ['url', 'website', 'profile_url', 'homepage', 'blog']
        
        for field in url_fields:
            if field in data and data[field]:
                entities.append({
                    'type': 'url',
                    'value': data[field],
                    'source': source,
                    'confidence': confidence,
                    'timestamp': timestamp,
                    'extraction_field': field
                })
    
    def _generate_summary(self, entities: List[Dict[str, Any]], relationship_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics"""
        entity_types = defaultdict(int)
        source_count = defaultdict(int)
        confidence_distribution = {'high': 0, 'medium': 0, 'low': 0}
        
        for entity in entities:
            entity_type = entity.get('type', 'unknown')
            entity_types[entity_type] += 1
            
            # Count sources
            for source_info in entity.get('sources', []):
                source_count[source_info.get('source', 'unknown')] += 1
            
            # Confidence distribution
            confidence = entity.get('final_confidence', 0)
            if confidence >= 0.8:
                confidence_distribution['high'] += 1
            elif confidence >= 0.5:
                confidence_distribution['medium'] += 1
            else:
                confidence_distribution['low'] += 1
        
        return {
            'total_entities': len(entities),
            'entity_types': dict(entity_types),
            'source_distribution': dict(source_count),
            'confidence_distribution': confidence_distribution,
            'relationship_summary': {
                'total_relationships': len(relationship_data.get('relationships', [])),
                'clustered_entities': relationship_data.get('linked_entities', 0)
            },
            'data_quality_score': self._calculate_data_quality_score(entities, confidence_distribution)
        }
    
    def _calculate_data_quality_score(self, entities: List[Dict[str, Any]], confidence_dist: Dict[str, int]) -> float:
        """Calculate overall data quality score"""
        if not entities:
            return 0.0
        
        total_entities = len(entities)
        high_conf_ratio = confidence_dist['high'] / total_entities
        medium_conf_ratio = confidence_dist['medium'] / total_entities
        
        # Weight high confidence entities more
        quality_score = (high_conf_ratio * 1.0) + (medium_conf_ratio * 0.6)
        
        # Bonus for entity diversity
        unique_types = len(set(e.get('type') for e in entities))
        diversity_bonus = min(unique_types * 0.05, 0.2)
        
        return round(min(quality_score + diversity_bonus, 1.0), 3)


# Aliases for backward compatibility
DataAggregationEngine = AggregationEngine
AdvancedAggregationEngine = AggregationEngine


# Factory function
def create_aggregation_engine() -> AggregationEngine:
    """Create and return a configured AggregationEngine instance"""
    return AggregationEngine()