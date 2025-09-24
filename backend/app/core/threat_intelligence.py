"""
Advanced Threat Intelligence Platform
Comprehensive threat analysis, IOC processing, and MITRE ATT&CK framework integration
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum
import hashlib
import re
import ipaddress
from urllib.parse import urlparse
import requests
import aiohttp
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class ThreatLevel(Enum):
    """Threat severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class IOCType(Enum):
    """Indicator of Compromise types"""
    IP_ADDRESS = "ip_address"
    DOMAIN = "domain"
    URL = "url"
    FILE_HASH = "file_hash"
    EMAIL = "email"
    REGISTRY_KEY = "registry_key"
    MUTEX = "mutex"
    USER_AGENT = "user_agent"

@dataclass
class ThreatIOC:
    """Threat Indicator of Compromise"""
    value: str
    ioc_type: IOCType
    threat_level: ThreatLevel
    confidence: float
    first_seen: datetime
    last_seen: datetime
    sources: List[str]
    tags: List[str]
    description: str = ""
    context: Dict[str, Any] = None

    def __post_init__(self):
        if self.context is None:
            self.context = {}

class MITREAttackFramework:
    """MITRE ATT&CK Framework integration"""
    
    def __init__(self):
        self.tactics = self._load_tactics()
        self.techniques = self._load_techniques()
        self.mitigations = self._load_mitigations()
    
    def _load_tactics(self) -> Dict[str, Dict[str, Any]]:
        """Load MITRE ATT&CK tactics"""
        return {
            "TA0001": {
                "name": "Initial Access",
                "description": "Adversary trying to get into your network",
                "techniques": ["T1190", "T1566", "T1078", "T1133", "T1200"]
            },
            "TA0002": {
                "name": "Execution", 
                "description": "Adversary trying to run malicious code",
                "techniques": ["T1059", "T1053", "T1106", "T1129", "T1204"]
            },
            "TA0003": {
                "name": "Persistence",
                "description": "Adversary trying to maintain access",
                "techniques": ["T1547", "T1053", "T1136", "T1098", "T1574"]
            },
            "TA0004": {
                "name": "Privilege Escalation",
                "description": "Adversary trying to gain higher-level permissions",
                "techniques": ["T1548", "T1134", "T1055", "T1068", "T1574"]
            },
            "TA0005": {
                "name": "Defense Evasion",
                "description": "Adversary trying to avoid being detected",
                "techniques": ["T1562", "T1070", "T1055", "T1027", "T1218"]
            }
        }
    
    def _load_techniques(self) -> Dict[str, Dict[str, Any]]:
        """Load MITRE ATT&CK techniques"""
        return {
            "T1190": {
                "name": "Exploit Public-Facing Application",
                "tactic": "TA0001",
                "description": "Adversaries may attempt to take advantage of a weakness in an Internet-facing computer or program",
                "mitigations": ["M1048", "M1030", "M1026"]
            },
            "T1566": {
                "name": "Phishing",
                "tactic": "TA0001", 
                "description": "Adversaries may send phishing messages to gain access to victim systems",
                "mitigations": ["M1049", "M1031", "M1017"]
            },
            "T1059": {
                "name": "Command and Scripting Interpreter",
                "tactic": "TA0002",
                "description": "Adversaries may abuse command and script interpreters to execute commands",
                "mitigations": ["M1038", "M1042", "M1026"]
            }
        }
    
    def _load_mitigations(self) -> Dict[str, Dict[str, Any]]:
        """Load MITRE ATT&CK mitigations"""
        return {
            "M1048": {
                "name": "Application Isolation and Sandboxing",
                "description": "Restrict execution of code to a virtual environment"
            },
            "M1030": {
                "name": "Network Segmentation",
                "description": "Architect sections of the network to isolate critical systems"
            },
            "M1049": {
                "name": "Antivirus/Antimalware",
                "description": "Use signatures or heuristics to identify malicious software"
            }
        }
    
    def map_ioc_to_techniques(self, ioc: ThreatIOC) -> List[str]:
        """Map IOC to relevant MITRE techniques"""
        techniques = []
        
        if ioc.ioc_type == IOCType.IP_ADDRESS:
            techniques.extend(["T1190", "T1071", "T1105"])
        elif ioc.ioc_type == IOCType.DOMAIN:
            techniques.extend(["T1071", "T1568", "T1583"])
        elif ioc.ioc_type == IOCType.URL:
            techniques.extend(["T1190", "T1566", "T1071"])
        elif ioc.ioc_type == IOCType.FILE_HASH:
            techniques.extend(["T1204", "T1105", "T1059"])
        elif ioc.ioc_type == IOCType.EMAIL:
            techniques.extend(["T1566", "T1598", "T1534"])
        
        return techniques

class ThreatIntelligenceProcessor:
    """Advanced threat intelligence processing engine"""
    
    def __init__(self):
        self.mitre_framework = MITREAttackFramework()
        self.ioc_database = {}
        self.threat_actors = {}
        self.campaigns = {}
        self.feed_sources = self._initialize_feed_sources()
        self.correlation_engine = ThreatCorrelationEngine()
        
    def _initialize_feed_sources(self) -> Dict[str, Dict[str, Any]]:
        """Initialize threat intelligence feed sources"""
        return {
            "misp": {
                "name": "MISP Threat Sharing",
                "url": "https://misppriv.circl.lu",
                "api_key": None,
                "enabled": False,
                "priority": 9
            },
            "otx": {
                "name": "AlienVault OTX",
                "url": "https://otx.alienvault.com",
                "api_key": None,
                "enabled": False,
                "priority": 8
            },
            "virustotal": {
                "name": "VirusTotal",
                "url": "https://www.virustotal.com/api/v3",
                "api_key": None,
                "enabled": False,
                "priority": 9
            },
            "threatcrowd": {
                "name": "ThreatCrowd",
                "url": "https://www.threatcrowd.org/searchApi/v2",
                "api_key": None,
                "enabled": True,
                "priority": 6
            },
            "malware_bazaar": {
                "name": "Malware Bazaar",
                "url": "https://mb-api.abuse.ch/api/v1",
                "api_key": None,
                "enabled": True,
                "priority": 7
            }
        }
    
    async def process_ioc(self, value: str, ioc_type: IOCType) -> ThreatIOC:
        """Process and enrich a single IOC"""
        try:
            # Validate IOC format
            if not self._validate_ioc_format(value, ioc_type):
                raise ValueError(f"Invalid IOC format: {value}")
            
            # Create base IOC
            ioc = ThreatIOC(
                value=value,
                ioc_type=ioc_type,
                threat_level=ThreatLevel.INFO,
                confidence=0.0,
                first_seen=datetime.utcnow(),
                last_seen=datetime.utcnow(),
                sources=[],
                tags=[],
                context={}
            )
            
            # Enrich IOC with threat intelligence
            await self._enrich_ioc(ioc)
            
            # Map to MITRE techniques
            ioc.context['mitre_techniques'] = self.mitre_framework.map_ioc_to_techniques(ioc)
            
            # Store in database
            self.ioc_database[value] = ioc
            
            return ioc
            
        except Exception as e:
            logger.error(f"Error processing IOC {value}: {e}")
            raise
    
    def _validate_ioc_format(self, value: str, ioc_type: IOCType) -> bool:
        """Validate IOC format based on type"""
        try:
            if ioc_type == IOCType.IP_ADDRESS:
                ipaddress.ip_address(value)
                return True
            elif ioc_type == IOCType.DOMAIN:
                return bool(re.match(r'^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.([a-zA-Z]{2,})+$', value))
            elif ioc_type == IOCType.URL:
                parsed = urlparse(value)
                return bool(parsed.scheme and parsed.netloc)
            elif ioc_type == IOCType.FILE_HASH:
                return len(value) in [32, 40, 64] and bool(re.match(r'^[a-fA-F0-9]+$', value))
            elif ioc_type == IOCType.EMAIL:
                return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value))
            return True
        except:
            return False
    
    async def _enrich_ioc(self, ioc: ThreatIOC):
        """Enrich IOC with threat intelligence from multiple sources"""
        enrichment_tasks = []
        
        for source_id, source_config in self.feed_sources.items():
            if source_config['enabled']:
                enrichment_tasks.append(
                    self._enrich_from_source(ioc, source_id, source_config)
                )
        
        if enrichment_tasks:
            results = await asyncio.gather(*enrichment_tasks, return_exceptions=True)
            
            # Process enrichment results
            for result in results:
                if isinstance(result, dict) and not isinstance(result, Exception):
                    self._merge_enrichment_data(ioc, result)
    
    async def _enrich_from_source(self, ioc: ThreatIOC, source_id: str, source_config: Dict) -> Dict:
        """Enrich IOC from specific threat intelligence source"""
        try:
            if source_id == "threatcrowd":
                return await self._enrich_from_threatcrowd(ioc)
            elif source_id == "virustotal":
                return await self._enrich_from_virustotal(ioc, source_config.get('api_key'))
            elif source_id == "malware_bazaar":
                return await self._enrich_from_malware_bazaar(ioc)
            else:
                return {}
        except Exception as e:
            logger.warning(f"Enrichment failed for {source_id}: {e}")
            return {}
    
    async def _enrich_from_threatcrowd(self, ioc: ThreatIOC) -> Dict:
        """Enrich IOC using ThreatCrowd API"""
        base_url = "https://www.threatcrowd.org/searchApi/v2"
        
        try:
            async with aiohttp.ClientSession() as session:
                if ioc.ioc_type == IOCType.IP_ADDRESS:
                    url = f"{base_url}/ip/report/?ip={ioc.value}"
                elif ioc.ioc_type == IOCType.DOMAIN:
                    url = f"{base_url}/domain/report/?domain={ioc.value}"
                else:
                    return {}
                
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'source': 'threatcrowd',
                            'data': data,
                            'confidence': 0.7 if data.get('response_code') == '1' else 0.3
                        }
        except Exception as e:
            logger.warning(f"ThreatCrowd enrichment failed: {e}")
        
        return {}
    
    async def _enrich_from_virustotal(self, ioc: ThreatIOC, api_key: str) -> Dict:
        """Enrich IOC using VirusTotal API"""
        if not api_key:
            return {}
        
        base_url = "https://www.virustotal.com/vtapi/v2"
        headers = {'apikey': api_key}
        
        try:
            async with aiohttp.ClientSession() as session:
                if ioc.ioc_type == IOCType.IP_ADDRESS:
                    url = f"{base_url}/ip-address/report"
                    params = {'ip': ioc.value}
                elif ioc.ioc_type == IOCType.DOMAIN:
                    url = f"{base_url}/domain/report"
                    params = {'domain': ioc.value}
                elif ioc.ioc_type == IOCType.FILE_HASH:
                    url = f"{base_url}/file/report"
                    params = {'resource': ioc.value}
                else:
                    return {}
                
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'source': 'virustotal',
                            'data': data,
                            'confidence': 0.9 if data.get('response_code') == 1 else 0.4
                        }
        except Exception as e:
            logger.warning(f"VirusTotal enrichment failed: {e}")
        
        return {}
    
    async def _enrich_from_malware_bazaar(self, ioc: ThreatIOC) -> Dict:
        """Enrich IOC using Malware Bazaar API"""
        if ioc.ioc_type != IOCType.FILE_HASH:
            return {}
        
        url = "https://mb-api.abuse.ch/api/v1/"
        
        try:
            async with aiohttp.ClientSession() as session:
                data = {
                    'query': 'get_info',
                    'hash': ioc.value
                }
                
                async with session.post(url, data=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            'source': 'malware_bazaar',
                            'data': result,
                            'confidence': 0.8 if result.get('query_status') == 'ok' else 0.2
                        }
        except Exception as e:
            logger.warning(f"Malware Bazaar enrichment failed: {e}")
        
        return {}
    
    def _merge_enrichment_data(self, ioc: ThreatIOC, enrichment: Dict):
        """Merge enrichment data into IOC"""
        source = enrichment.get('source', 'unknown')
        confidence = enrichment.get('confidence', 0.0)
        data = enrichment.get('data', {})
        
        # Add source
        if source not in ioc.sources:
            ioc.sources.append(source)
        
        # Update confidence (weighted average)
        current_weight = len(ioc.sources) - 1
        total_weight = len(ioc.sources)
        ioc.confidence = ((ioc.confidence * current_weight) + confidence) / total_weight
        
        # Extract and merge threat level
        if data:
            threat_level = self._extract_threat_level(data, source)
            if threat_level.value > ioc.threat_level.value:
                ioc.threat_level = threat_level
        
        # Store enrichment data
        ioc.context[f'{source}_data'] = data
    
    def _extract_threat_level(self, data: Dict, source: str) -> ThreatLevel:
        """Extract threat level from enrichment data"""
        if source == 'virustotal':
            positives = data.get('positives', 0)
            total = data.get('total', 1)
            ratio = positives / max(total, 1)
            
            if ratio >= 0.7:
                return ThreatLevel.CRITICAL
            elif ratio >= 0.4:
                return ThreatLevel.HIGH
            elif ratio >= 0.2:
                return ThreatLevel.MEDIUM
            elif ratio > 0:
                return ThreatLevel.LOW
        
        elif source == 'threatcrowd':
            if data.get('response_code') == '1':
                return ThreatLevel.MEDIUM
        
        return ThreatLevel.INFO

class ThreatCorrelationEngine:
    """Correlate and link related threats"""
    
    def __init__(self):
        self.correlation_rules = self._load_correlation_rules()
        self.threat_clusters = {}
    
    def _load_correlation_rules(self) -> List[Dict]:
        """Load threat correlation rules"""
        return [
            {
                'name': 'IP_Domain_Correlation',
                'description': 'Correlate IPs and domains from same infrastructure',
                'conditions': ['same_asn', 'same_geolocation', 'temporal_proximity'],
                'weight': 0.8
            },
            {
                'name': 'Hash_Family_Correlation',
                'description': 'Correlate file hashes from same malware family',
                'conditions': ['similar_behavior', 'same_packer', 'code_similarity'],
                'weight': 0.9
            },
            {
                'name': 'Campaign_Attribution',
                'description': 'Attribution to threat campaigns',
                'conditions': ['tactical_similarity', 'infrastructure_overlap', 'temporal_clustering'],
                'weight': 0.7
            }
        ]
    
    def correlate_threats(self, iocs: List[ThreatIOC]) -> Dict[str, List[ThreatIOC]]:
        """Correlate threats and group related IOCs"""
        clusters = {}
        
        for ioc in iocs:
            cluster_id = self._find_or_create_cluster(ioc, clusters)
            if cluster_id not in clusters:
                clusters[cluster_id] = []
            clusters[cluster_id].append(ioc)
        
        return clusters
    
    def _find_or_create_cluster(self, ioc: ThreatIOC, existing_clusters: Dict) -> str:
        """Find existing cluster or create new one"""
        for cluster_id, cluster_iocs in existing_clusters.items():
            if self._should_cluster_together(ioc, cluster_iocs):
                return cluster_id
        
        # Create new cluster
        return f"cluster_{len(existing_clusters) + 1}"
    
    def _should_cluster_together(self, ioc: ThreatIOC, cluster_iocs: List[ThreatIOC]) -> bool:
        """Determine if IOC should be clustered with existing IOCs"""
        for cluster_ioc in cluster_iocs:
            similarity_score = self._calculate_similarity(ioc, cluster_ioc)
            if similarity_score > 0.6:  # Clustering threshold
                return True
        return False
    
    def _calculate_similarity(self, ioc1: ThreatIOC, ioc2: ThreatIOC) -> float:
        """Calculate similarity score between two IOCs"""
        similarity_factors = []
        
        # Source overlap
        common_sources = set(ioc1.sources) & set(ioc2.sources)
        source_similarity = len(common_sources) / max(len(set(ioc1.sources) | set(ioc2.sources)), 1)
        similarity_factors.append(source_similarity * 0.3)
        
        # Tag overlap
        common_tags = set(ioc1.tags) & set(ioc2.tags)
        tag_similarity = len(common_tags) / max(len(set(ioc1.tags) | set(ioc2.tags)), 1)
        similarity_factors.append(tag_similarity * 0.2)
        
        # Temporal proximity
        time_diff = abs((ioc1.first_seen - ioc2.first_seen).total_seconds())
        temporal_similarity = max(0, 1 - (time_diff / (7 * 24 * 3600)))  # 7 days window
        similarity_factors.append(temporal_similarity * 0.2)
        
        # Threat level similarity
        level_similarity = 1.0 if ioc1.threat_level == ioc2.threat_level else 0.5
        similarity_factors.append(level_similarity * 0.3)
        
        return sum(similarity_factors)

class ThreatReportGenerator:
    """Generate comprehensive threat intelligence reports"""
    
    def __init__(self, processor: ThreatIntelligenceProcessor):
        self.processor = processor
        self.mitre_framework = processor.mitre_framework
    
    def generate_threat_report(self, iocs: List[ThreatIOC], format_type: str = 'json') -> str:
        """Generate comprehensive threat report"""
        # Correlate threats
        clusters = self.processor.correlation_engine.correlate_threats(iocs)
        
        # Generate report data
        report_data = {
            'metadata': {
                'generated_at': datetime.utcnow().isoformat(),
                'total_iocs': len(iocs),
                'threat_clusters': len(clusters),
                'generator': 'Advanced Threat Intelligence Platform'
            },
            'executive_summary': self._generate_executive_summary(iocs, clusters),
            'threat_landscape': self._analyze_threat_landscape(iocs),
            'ioc_analysis': self._analyze_iocs(iocs),
            'mitre_mapping': self._generate_mitre_mapping(iocs),
            'threat_clusters': self._format_clusters(clusters),
            'recommendations': self._generate_recommendations(iocs, clusters)
        }
        
        if format_type == 'json':
            return json.dumps(report_data, indent=2, default=str)
        elif format_type == 'html':
            return self._generate_html_report(report_data)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _generate_executive_summary(self, iocs: List[ThreatIOC], clusters: Dict) -> Dict:
        """Generate executive summary"""
        threat_levels = [ioc.threat_level for ioc in iocs]
        
        return {
            'total_indicators': len(iocs),
            'critical_threats': sum(1 for t in threat_levels if t == ThreatLevel.CRITICAL),
            'high_threats': sum(1 for t in threat_levels if t == ThreatLevel.HIGH),
            'threat_clusters': len(clusters),
            'avg_confidence': sum(ioc.confidence for ioc in iocs) / max(len(iocs), 1),
            'key_findings': self._extract_key_findings(iocs, clusters)
        }
    
    def _analyze_threat_landscape(self, iocs: List[ThreatIOC]) -> Dict:
        """Analyze overall threat landscape"""
        ioc_types = {}
        threat_levels = {}
        sources = set()
        
        for ioc in iocs:
            # Count IOC types
            ioc_type = ioc.ioc_type.value
            ioc_types[ioc_type] = ioc_types.get(ioc_type, 0) + 1
            
            # Count threat levels
            threat_level = ioc.threat_level.value
            threat_levels[threat_level] = threat_levels.get(threat_level, 0) + 1
            
            # Collect sources
            sources.update(ioc.sources)
        
        return {
            'ioc_distribution': ioc_types,
            'threat_level_distribution': threat_levels,
            'intelligence_sources': list(sources),
            'coverage_analysis': {
                'source_diversity': len(sources),
                'data_freshness': self._calculate_data_freshness(iocs)
            }
        }
    
    def _analyze_iocs(self, iocs: List[ThreatIOC]) -> List[Dict]:
        """Analyze individual IOCs"""
        return [
            {
                'value': ioc.value,
                'type': ioc.ioc_type.value,
                'threat_level': ioc.threat_level.value,
                'confidence': ioc.confidence,
                'sources': ioc.sources,
                'tags': ioc.tags,
                'first_seen': ioc.first_seen.isoformat(),
                'last_seen': ioc.last_seen.isoformat(),
                'mitre_techniques': ioc.context.get('mitre_techniques', []),
                'description': ioc.description
            }
            for ioc in iocs
        ]
    
    def _generate_mitre_mapping(self, iocs: List[ThreatIOC]) -> Dict:
        """Generate MITRE ATT&CK mapping"""
        technique_counts = {}
        tactic_counts = {}
        
        for ioc in iocs:
            techniques = ioc.context.get('mitre_techniques', [])
            for technique_id in techniques:
                technique_counts[technique_id] = technique_counts.get(technique_id, 0) + 1
                
                # Map to tactic
                technique_info = self.mitre_framework.techniques.get(technique_id, {})
                tactic_id = technique_info.get('tactic')
                if tactic_id:
                    tactic_counts[tactic_id] = tactic_counts.get(tactic_id, 0) + 1
        
        return {
            'technique_coverage': technique_counts,
            'tactic_coverage': tactic_counts,
            'attack_patterns': self._identify_attack_patterns(technique_counts),
            'defensive_recommendations': self._generate_defensive_recommendations(technique_counts)
        }
    
    def _format_clusters(self, clusters: Dict) -> List[Dict]:
        """Format threat clusters for report"""
        formatted_clusters = []
        
        for cluster_id, cluster_iocs in clusters.items():
            cluster_info = {
                'cluster_id': cluster_id,
                'ioc_count': len(cluster_iocs),
                'threat_levels': [ioc.threat_level.value for ioc in cluster_iocs],
                'ioc_types': [ioc.ioc_type.value for ioc in cluster_iocs],
                'common_sources': self._find_common_sources(cluster_iocs),
                'time_range': {
                    'first_seen': min(ioc.first_seen for ioc in cluster_iocs).isoformat(),
                    'last_seen': max(ioc.last_seen for ioc in cluster_iocs).isoformat()
                },
                'cluster_analysis': self._analyze_cluster(cluster_iocs)
            }
            formatted_clusters.append(cluster_info)
        
        return formatted_clusters
    
    def _generate_recommendations(self, iocs: List[ThreatIOC], clusters: Dict) -> List[Dict]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # High-priority IOC recommendations
        critical_iocs = [ioc for ioc in iocs if ioc.threat_level == ThreatLevel.CRITICAL]
        if critical_iocs:
            recommendations.append({
                'priority': 'Critical',
                'category': 'Immediate Action',
                'recommendation': 'Block critical IOCs immediately',
                'details': f'Found {len(critical_iocs)} critical indicators requiring immediate blocking',
                'affected_indicators': [ioc.value for ioc in critical_iocs[:5]]  # Limit to top 5
            })
        
        # Clustering recommendations
        large_clusters = [c for c in clusters.values() if len(c) >= 3]
        if large_clusters:
            recommendations.append({
                'priority': 'High',
                'category': 'Threat Hunting',
                'recommendation': 'Investigate threat clusters',
                'details': f'Found {len(large_clusters)} threat clusters suggesting coordinated activity',
                'affected_indicators': []
            })
        
        # MITRE-based recommendations
        technique_counts = {}
        for ioc in iocs:
            for technique in ioc.context.get('mitre_techniques', []):
                technique_counts[technique] = technique_counts.get(technique, 0) + 1
        
        if technique_counts:
            top_technique = max(technique_counts.items(), key=lambda x: x[1])
            technique_info = self.mitre_framework.techniques.get(top_technique[0], {})
            
            recommendations.append({
                'priority': 'Medium',
                'category': 'Defense Enhancement',
                'recommendation': f'Implement mitigations for {technique_info.get("name", top_technique[0])}',
                'details': f'Technique {top_technique[0]} observed in {top_technique[1]} indicators',
                'affected_indicators': []
            })
        
        return recommendations
    
    def _extract_key_findings(self, iocs: List[ThreatIOC], clusters: Dict) -> List[str]:
        """Extract key findings from analysis"""
        findings = []
        
        # Critical threat finding
        critical_count = sum(1 for ioc in iocs if ioc.threat_level == ThreatLevel.CRITICAL)
        if critical_count > 0:
            findings.append(f"Identified {critical_count} critical threat indicators requiring immediate attention")
        
        # Clustering finding
        if len(clusters) < len(iocs) * 0.8:  # High clustering
            findings.append(f"Strong threat clustering detected - {len(clusters)} clusters from {len(iocs)} indicators")
        
        # Source diversity finding
        all_sources = set()
        for ioc in iocs:
            all_sources.update(ioc.sources)
        
        if len(all_sources) > 3:
            findings.append(f"High source diversity with {len(all_sources)} intelligence feeds contributing")
        
        return findings
    
    def _calculate_data_freshness(self, iocs: List[ThreatIOC]) -> float:
        """Calculate data freshness score"""
        now = datetime.utcnow()
        freshness_scores = []
        
        for ioc in iocs:
            age_hours = (now - ioc.last_seen).total_seconds() / 3600
            # Exponential decay: fresh data (0-24h) = 1.0, older data decays
            freshness = max(0, 1.0 - (age_hours / (24 * 7)))  # Week decay
            freshness_scores.append(freshness)
        
        return sum(freshness_scores) / max(len(freshness_scores), 1)
    
    def _identify_attack_patterns(self, technique_counts: Dict) -> List[Dict]:
        """Identify attack patterns from technique usage"""
        patterns = []
        
        # Look for common attack patterns
        if 'T1566' in technique_counts and 'T1204' in technique_counts:
            patterns.append({
                'pattern': 'Phishing Campaign',
                'confidence': 0.8,
                'techniques': ['T1566', 'T1204'],
                'description': 'Phishing emails leading to user execution'
            })
        
        if 'T1190' in technique_counts and 'T1059' in technique_counts:
            patterns.append({
                'pattern': 'Web Application Exploit',
                'confidence': 0.7,
                'techniques': ['T1190', 'T1059'],
                'description': 'Web application exploitation with command execution'
            })
        
        return patterns
    
    def _generate_defensive_recommendations(self, technique_counts: Dict) -> List[Dict]:
        """Generate defensive recommendations based on techniques"""
        recommendations = []
        
        for technique_id, count in technique_counts.items():
            technique_info = self.mitre_framework.techniques.get(technique_id, {})
            mitigations = technique_info.get('mitigations', [])
            
            for mitigation_id in mitigations:
                mitigation_info = self.mitre_framework.mitigations.get(mitigation_id, {})
                recommendations.append({
                    'technique': technique_id,
                    'technique_name': technique_info.get('name', ''),
                    'mitigation': mitigation_id,
                    'mitigation_name': mitigation_info.get('name', ''),
                    'description': mitigation_info.get('description', ''),
                    'priority': 'High' if count > 2 else 'Medium'
                })
        
        return recommendations
    
    def _find_common_sources(self, cluster_iocs: List[ThreatIOC]) -> List[str]:
        """Find common sources across cluster IOCs"""
        if not cluster_iocs:
            return []
        
        common_sources = set(cluster_iocs[0].sources)
        for ioc in cluster_iocs[1:]:
            common_sources &= set(ioc.sources)
        
        return list(common_sources)
    
    def _analyze_cluster(self, cluster_iocs: List[ThreatIOC]) -> Dict:
        """Analyze a threat cluster"""
        return {
            'size': len(cluster_iocs),
            'avg_confidence': sum(ioc.confidence for ioc in cluster_iocs) / len(cluster_iocs),
            'dominant_threat_level': max(cluster_iocs, key=lambda x: x.threat_level.value).threat_level.value,
            'time_span_hours': (max(ioc.last_seen for ioc in cluster_iocs) - 
                               min(ioc.first_seen for ioc in cluster_iocs)).total_seconds() / 3600,
            'unique_sources': len(set().union(*[ioc.sources for ioc in cluster_iocs]))
        }
    
    def _generate_html_report(self, report_data: Dict) -> str:
        """Generate HTML format report"""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Threat Intelligence Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; }}
                .section {{ margin: 20px 0; padding: 15px; border-left: 4px solid #3498db; }}
                .critical {{ border-left-color: #e74c3c; }}
                .high {{ border-left-color: #f39c12; }}
                .medium {{ border-left-color: #f1c40f; }}
                .low {{ border-left-color: #27ae60; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #34495e; color: white; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Threat Intelligence Report</h1>
                <p>Generated: {generated_at}</p>
            </div>
            
            <div class="section">
                <h2>Executive Summary</h2>
                <p>Total Indicators: {total_indicators}</p>
                <p>Critical Threats: {critical_threats}</p>
                <p>High Threats: {high_threats}</p>
                <p>Threat Clusters: {threat_clusters}</p>
            </div>
            
            <div class="section">
                <h2>Key Findings</h2>
                <ul>
                {key_findings}
                </ul>
            </div>
            
            <div class="section">
                <h2>IOC Analysis</h2>
                <table>
                    <tr><th>Indicator</th><th>Type</th><th>Threat Level</th><th>Confidence</th><th>Sources</th></tr>
                    {ioc_rows}
                </table>
            </div>
        </body>
        </html>
        """
        
        # Format key findings
        key_findings = '\n'.join([f'<li>{finding}</li>' for finding in report_data['executive_summary']['key_findings']])
        
        # Format IOC rows
        ioc_rows = []
        for ioc in report_data['ioc_analysis'][:20]:  # Limit to first 20
            row = f"""
            <tr class="{ioc['threat_level']}">
                <td>{ioc['value']}</td>
                <td>{ioc['type']}</td>
                <td>{ioc['threat_level'].upper()}</td>
                <td>{ioc['confidence']:.2f}</td>
                <td>{', '.join(ioc['sources'])}</td>
            </tr>
            """
            ioc_rows.append(row)
        
        return html_template.format(
            generated_at=report_data['metadata']['generated_at'],
            total_indicators=report_data['executive_summary']['total_indicators'],
            critical_threats=report_data['executive_summary']['critical_threats'],
            high_threats=report_data['executive_summary']['high_threats'],
            threat_clusters=report_data['executive_summary']['threat_clusters'],
            key_findings=key_findings,
            ioc_rows=''.join(ioc_rows)
        )

class ThreatIntelligencePlatform:
    """Main threat intelligence platform"""
    
    def __init__(self):
        self.processor = ThreatIntelligenceProcessor()
        self.report_generator = ThreatReportGenerator(self.processor)
        self.alert_manager = ThreatAlertManager()
        
    async def analyze_indicators(self, indicators: List[Tuple[str, str]]) -> Dict[str, Any]:
        """Analyze list of indicators"""
        try:
            iocs = []
            
            for value, ioc_type_str in indicators:
                try:
                    ioc_type = IOCType(ioc_type_str.lower())
                    ioc = await self.processor.process_ioc(value, ioc_type)
                    iocs.append(ioc)
                except Exception as e:
                    logger.warning(f"Failed to process IOC {value}: {e}")
                    continue
            
            # Generate comprehensive analysis
            analysis_result = {
                'total_processed': len(iocs),
                'processing_time': time.time(),
                'threat_summary': self._generate_threat_summary(iocs),
                'high_priority_alerts': self.alert_manager.generate_alerts(iocs),
                'report': self.report_generator.generate_threat_report(iocs, 'json')
            }
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            raise
    
    def _generate_threat_summary(self, iocs: List[ThreatIOC]) -> Dict[str, Any]:
        """Generate quick threat summary"""
        if not iocs:
            return {'status': 'no_threats', 'summary': 'No indicators processed'}
        
        threat_levels = [ioc.threat_level for ioc in iocs]
        avg_confidence = sum(ioc.confidence for ioc in iocs) / len(iocs)
        
        critical_count = sum(1 for t in threat_levels if t == ThreatLevel.CRITICAL)
        high_count = sum(1 for t in threat_levels if t == ThreatLevel.HIGH)
        
        if critical_count > 0:
            status = 'critical_threats_detected'
            summary = f"CRITICAL: {critical_count} critical threats identified"
        elif high_count > 0:
            status = 'high_threats_detected'
            summary = f"HIGH: {high_count} high-priority threats identified"
        else:
            status = 'threats_detected'
            summary = f"Threats identified with average confidence {avg_confidence:.2f}"
        
        return {
            'status': status,
            'summary': summary,
            'counts': {
                'critical': critical_count,
                'high': high_count,
                'medium': sum(1 for t in threat_levels if t == ThreatLevel.MEDIUM),
                'low': sum(1 for t in threat_levels if t == ThreatLevel.LOW)
            },
            'avg_confidence': avg_confidence
        }

class ThreatAlertManager:
    """Manage threat alerts and notifications"""
    
    def __init__(self):
        self.alert_rules = self._load_alert_rules()
    
    def _load_alert_rules(self) -> List[Dict]:
        """Load alert generation rules"""
        return [
            {
                'name': 'Critical Threat Alert',
                'condition': lambda ioc: ioc.threat_level == ThreatLevel.CRITICAL,
                'severity': 'critical',
                'message': 'Critical threat indicator detected'
            },
            {
                'name': 'High Confidence Alert',
                'condition': lambda ioc: ioc.confidence > 0.8 and ioc.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL],
                'severity': 'high',
                'message': 'High confidence threat detected'
            },
            {
                'name': 'Multiple Source Alert',
                'condition': lambda ioc: len(ioc.sources) >= 3,
                'severity': 'medium',
                'message': 'Threat confirmed by multiple sources'
            }
        ]
    
    def generate_alerts(self, iocs: List[ThreatIOC]) -> List[Dict]:
        """Generate alerts based on IOC analysis"""
        alerts = []
        
        for ioc in iocs:
            for rule in self.alert_rules:
                if rule['condition'](ioc):
                    alert = {
                        'alert_id': f"alert_{int(time.time())}_{hash(ioc.value) % 10000}",
                        'timestamp': datetime.utcnow().isoformat(),
                        'severity': rule['severity'],
                        'message': rule['message'],
                        'indicator': {
                            'value': ioc.value,
                            'type': ioc.ioc_type.value,
                            'threat_level': ioc.threat_level.value,
                            'confidence': ioc.confidence
                        },
                        'rule_name': rule['name'],
                        'recommended_actions': self._get_recommended_actions(ioc, rule['severity'])
                    }
                    alerts.append(alert)
        
        return alerts
    
    def _get_recommended_actions(self, ioc: ThreatIOC, severity: str) -> List[str]:
        """Get recommended actions for alert"""
        actions = []
        
        if severity == 'critical':
            actions.extend([
                'Block indicator immediately',
                'Initiate incident response',
                'Check for signs of compromise',
                'Notify security team'
            ])
        elif severity == 'high':
            actions.extend([
                'Add to watchlist',
                'Increase monitoring',
                'Review related activities',
                'Consider blocking'
            ])
        else:
            actions.extend([
                'Monitor for additional activity',
                'Document in threat database',
                'Review periodically'
            ])
        
        return actions

# Example usage and testing
async def example_usage():
    """Example usage of the threat intelligence platform"""
    platform = ThreatIntelligencePlatform()
    
    # Example indicators to analyze
    test_indicators = [
        ("8.8.8.8", "ip_address"),
        ("malicious-domain.com", "domain"),
        ("http://evil-site.com/malware.exe", "url"),
        ("d41d8cd98f00b204e9800998ecf8427e", "file_hash"),
        ("attacker@evil.com", "email")
    ]
    
    try:
        # Analyze indicators
        print("Analyzing threat indicators...")
        result = await platform.analyze_indicators(test_indicators)
        
        print(f"Processed {result['total_processed']} indicators")
        print(f"Threat Status: {result['threat_summary']['status']}")
        print(f"Summary: {result['threat_summary']['summary']}")
        
        if result['high_priority_alerts']:
            print(f"\nHigh Priority Alerts: {len(result['high_priority_alerts'])}")
            for alert in result['high_priority_alerts'][:3]:  # Show first 3
                print(f"- {alert['severity'].upper()}: {alert['message']}")
        
        print("\nThreat intelligence analysis completed successfully!")
        
    except Exception as e:
        print(f"Analysis failed: {e}")

if __name__ == "__main__":
    # Run example
    asyncio.run(example_usage())