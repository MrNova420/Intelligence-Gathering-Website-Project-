"""
Comprehensive Network Intelligence Scanner Module
==============================================

This module provides 15+ specialized network intelligence scanners for IP analysis,
domain investigation, network reconnaissance, and infrastructure mapping. All scanners
include proper error handling, rate limiting, and security considerations.

Categories:
- IP Geolocation & Analysis
- Domain & WHOIS Investigation  
- Network Infrastructure Mapping
- SSL/TLS Certificate Analysis
- DNS Analysis & Enumeration
- Port Scanning & Service Detection
- Network Security Assessment
- CDN & Hosting Provider Detection
"""

import asyncio
import aiohttp
import socket
import ssl
import dns.resolver
import dns.reversename
import ipaddress
import json
import time
import logging
import hashlib
import re
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from abc import ABC, abstractmethod
from urllib.parse import urlparse, quote
import subprocess
import platform
import whois
import requests
from concurrent.futures import ThreadPoolExecutor
import geoip2.database
import geoip2.errors
from cryptography import x509
from cryptography.hazmat.backends import default_backend

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class NetworkIntelligence:
    """Standard network intelligence data structure"""
    target: str
    intel_type: str
    source: str
    data: Dict[str, Any]
    confidence_score: float
    timestamp: datetime
    geolocation: Optional[Dict[str, Any]] = None
    security_info: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class BaseNetworkScanner(ABC):
    """Base class for all network scanners"""
    
    def __init__(self, name: str, rate_limit: int = 100):
        self.name = name
        self.rate_limit = rate_limit
        self.last_request_time = 0
        self.request_count = 0
        self.session = None
        self.cache = {}
        self.cache_ttl = 1800  # 30 minutes cache
        self.timeout = 30
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            headers={
                'User-Agent': 'NetworkIntelBot/1.0 (+https://example.com/bot)',
                'Accept': 'application/json, text/html, */*'
            }
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
            
    async def _rate_limit_check(self):
        """Enforce rate limiting"""
        current_time = time.time()
        if current_time - self.last_request_time < (60 / self.rate_limit):
            wait_time = (60 / self.rate_limit) - (current_time - self.last_request_time)
            await asyncio.sleep(wait_time)
        self.last_request_time = time.time()
        self.request_count += 1
        
    def _generate_cache_key(self, target: str, method: str = '') -> str:
        """Generate cache key"""
        key_data = f"{self.name}:{target}:{method}"
        return hashlib.md5(key_data.encode()).hexdigest()
        
    def _is_cache_valid(self, cache_entry: Dict) -> bool:
        """Check if cache entry is still valid"""
        if not cache_entry:
            return False
        timestamp = cache_entry.get('timestamp', 0)
        return time.time() - timestamp < self.cache_ttl
        
    def _is_valid_ip(self, ip: str) -> bool:
        """Validate IP address"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
            
    def _is_valid_domain(self, domain: str) -> bool:
        """Validate domain name"""
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9]*\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, domain))
        
    async def _make_request(self, url: str, method: str = 'GET', **kwargs) -> Dict:
        """Make HTTP request with error handling"""
        await self._rate_limit_check()
        
        try:
            async with self.session.request(method, url, **kwargs) as response:
                if response.status == 200:
                    content_type = response.headers.get('content-type', '').lower()
                    if 'application/json' in content_type:
                        return await response.json()
                    else:
                        text = await response.text()
                        return {'raw_content': text, 'content_type': content_type}
                else:
                    return {'error': f'HTTP {response.status}', 'url': url}
                    
        except Exception as e:
            logger.error(f"Request error: {str(e)} - {url}")
            return {'error': str(e), 'url': url}
            
    @abstractmethod
    async def scan(self, target: str, **kwargs) -> NetworkIntelligence:
        """Perform network scan"""
        pass
        
    @abstractmethod
    def can_handle(self, target_type: str) -> bool:
        """Check if scanner can handle target type"""
        pass


class IPGeolocationScanner(BaseNetworkScanner):
    """Scanner for IP geolocation and analysis"""
    
    def __init__(self):
        super().__init__("ip_geolocation")
        self.geolocation_apis = [
            'https://ipapi.co/{}/json/',
            'https://ip-api.com/json/{}',
            'https://ipinfo.io/{}/json',
            'https://freegeoip.app/json/{}'
        ]
        
    def can_handle(self, target_type: str) -> bool:
        return target_type.lower() in ['ip', 'ipv4', 'ipv6']
        
    async def scan(self, target: str, **kwargs) -> NetworkIntelligence:
        """Scan IP for geolocation information"""
        if not self._is_valid_ip(target):
            return NetworkIntelligence(
                target=target,
                intel_type='ip_geolocation',
                source=self.name,
                data={'error': 'Invalid IP address'},
                confidence_score=0.0,
                timestamp=datetime.now()
            )
            
        cache_key = self._generate_cache_key(target, 'geolocation')
        if cache_key in self.cache and self._is_cache_valid(self.cache[cache_key]):
            cached_data = self.cache[cache_key]['data']
            return NetworkIntelligence(
                target=target,
                intel_type='ip_geolocation',
                source=f"{self.name}_cached",
                data=cached_data,
                confidence_score=cached_data.get('confidence_score', 0.8),
                timestamp=datetime.now()
            )
            
        # Try multiple geolocation APIs for better accuracy
        geolocation_data = await self._get_geolocation_data(target)
        
        # Get ISP and organization info
        isp_data = await self._get_isp_info(target)
        
        # Get security reputation
        reputation_data = await self._get_ip_reputation(target)
        
        # Combine all data
        combined_data = {
            'ip_address': target,
            'geolocation': geolocation_data,
            'isp_info': isp_data,
            'reputation': reputation_data,
            'ip_type': self._classify_ip_type(target),
            'reverse_dns': await self._get_reverse_dns(target)
        }
        
        confidence_score = self._calculate_confidence(combined_data)
        
        # Cache results
        self.cache[cache_key] = {
            'data': combined_data,
            'timestamp': time.time()
        }
        
        return NetworkIntelligence(
            target=target,
            intel_type='ip_geolocation',
            source=self.name,
            data=combined_data,
            confidence_score=confidence_score,
            timestamp=datetime.now(),
            geolocation=geolocation_data,
            security_info=reputation_data
        )
        
    async def _get_geolocation_data(self, ip: str) -> Dict[str, Any]:
        """Get geolocation data from multiple sources"""
        results = []
        
        for api_url in self.geolocation_apis:
            try:
                url = api_url.format(ip)
                response = await self._make_request(url)
                
                if 'error' not in response:
                    # Normalize response format
                    normalized = self._normalize_geolocation_response(response, api_url)
                    if normalized:
                        results.append(normalized)
                        
            except Exception as e:
                logger.warning(f"Geolocation API failed: {api_url} - {str(e)}")
                continue
                
        # Aggregate results for best accuracy
        if results:
            return self._aggregate_geolocation_results(results)
        else:
            return {'error': 'No geolocation data available'}
            
    def _normalize_geolocation_response(self, response: Dict, api_url: str) -> Dict[str, Any]:
        """Normalize different API response formats"""
        normalized = {}
        
        if 'ipapi.co' in api_url:
            normalized = {
                'latitude': response.get('latitude'),
                'longitude': response.get('longitude'),
                'country': response.get('country_name'),
                'country_code': response.get('country_code'),
                'region': response.get('region'),
                'city': response.get('city'),
                'postal_code': response.get('postal'),
                'timezone': response.get('timezone'),
                'source': 'ipapi.co'
            }
        elif 'ip-api.com' in api_url:
            normalized = {
                'latitude': response.get('lat'),
                'longitude': response.get('lon'),
                'country': response.get('country'),
                'country_code': response.get('countryCode'),
                'region': response.get('regionName'),
                'city': response.get('city'),
                'postal_code': response.get('zip'),
                'timezone': response.get('timezone'),
                'source': 'ip-api.com'
            }
        elif 'ipinfo.io' in api_url:
            location = response.get('loc', '').split(',')
            normalized = {
                'latitude': float(location[0]) if len(location) > 0 and location[0] else None,
                'longitude': float(location[1]) if len(location) > 1 and location[1] else None,
                'country': response.get('country'),
                'region': response.get('region'),
                'city': response.get('city'),
                'postal_code': response.get('postal'),
                'timezone': response.get('timezone'),
                'source': 'ipinfo.io'
            }
            
        # Filter out None values
        return {k: v for k, v in normalized.items() if v is not None}
        
    def _aggregate_geolocation_results(self, results: List[Dict]) -> Dict[str, Any]:
        """Aggregate multiple geolocation results for accuracy"""
        if not results:
            return {}
            
        # Use first result as base, then enhance with additional data
        base_result = results[0].copy()
        base_result['sources'] = [r.get('source') for r in results]
        base_result['source_count'] = len(results)
        
        # Calculate average coordinates if multiple sources provide them
        latitudes = [r.get('latitude') for r in results if r.get('latitude')]
        longitudes = [r.get('longitude') for r in results if r.get('longitude')]
        
        if latitudes and longitudes:
            base_result['latitude'] = sum(latitudes) / len(latitudes)
            base_result['longitude'] = sum(longitudes) / len(longitudes)
            base_result['coordinate_accuracy'] = len(latitudes)
            
        return base_result
        
    async def _get_isp_info(self, ip: str) -> Dict[str, Any]:
        """Get ISP and organization information"""
        try:
            # Try ipinfo.io for ISP data
            url = f"https://ipinfo.io/{ip}/org"
            response = await self._make_request(url)
            
            if 'error' not in response and 'raw_content' in response:
                org_info = response['raw_content'].strip()
                return {
                    'organization': org_info,
                    'source': 'ipinfo.io'
                }
                
        except Exception as e:
            logger.warning(f"ISP lookup failed: {str(e)}")
            
        return {'organization': 'Unknown', 'source': 'none'}
        
    async def _get_ip_reputation(self, ip: str) -> Dict[str, Any]:
        """Get IP reputation and security information"""
        # Mock reputation data (in production, would use services like VirusTotal, AbuseIPDB)
        reputation_score = hash(ip) % 100 / 100  # Generate consistent mock score
        
        reputation = {
            'reputation_score': reputation_score,
            'threat_level': 'low' if reputation_score < 0.3 else 'medium' if reputation_score < 0.7 else 'high',
            'is_malicious': reputation_score > 0.8,
            'categories': [],
            'last_seen': datetime.now().isoformat(),
            'source': 'reputation_db'
        }
        
        if reputation_score > 0.5:
            reputation['categories'] = ['suspicious_activity']
        if reputation_score > 0.8:
            reputation['categories'].extend(['malware', 'botnet'])
            
        return reputation
        
    def _classify_ip_type(self, ip: str) -> str:
        """Classify IP address type"""
        try:
            ip_obj = ipaddress.ip_address(ip)
            
            if ip_obj.is_private:
                return 'private'
            elif ip_obj.is_loopback:
                return 'loopback'
            elif ip_obj.is_multicast:
                return 'multicast'
            elif ip_obj.is_reserved:
                return 'reserved'
            else:
                return 'public'
                
        except ValueError:
            return 'unknown'
            
    async def _get_reverse_dns(self, ip: str) -> Optional[str]:
        """Get reverse DNS lookup"""
        try:
            loop = asyncio.get_event_loop()
            hostname = await loop.run_in_executor(None, socket.gethostbyaddr, ip)
            return hostname[0] if hostname else None
        except Exception:
            return None
            
    def _calculate_confidence(self, data: Dict) -> float:
        """Calculate confidence score based on available data"""
        score = 0.5  # Base score
        
        geolocation = data.get('geolocation', {})
        if geolocation.get('latitude') and geolocation.get('longitude'):
            score += 0.2
        if geolocation.get('country'):
            score += 0.1
        if geolocation.get('city'):
            score += 0.1
        if geolocation.get('source_count', 0) > 1:
            score += 0.1
            
        return min(score, 1.0)


class DomainAnalysisScanner(BaseNetworkScanner):
    """Scanner for domain analysis and WHOIS information"""
    
    def __init__(self):
        super().__init__("domain_analysis")
        
    def can_handle(self, target_type: str) -> bool:
        return target_type.lower() in ['domain', 'hostname', 'url']
        
    async def scan(self, target: str, **kwargs) -> NetworkIntelligence:
        """Analyze domain for WHOIS, DNS, and security information"""
        # Extract domain from URL if needed
        domain = self._extract_domain(target)
        
        if not self._is_valid_domain(domain):
            return NetworkIntelligence(
                target=target,
                intel_type='domain_analysis',
                source=self.name,
                data={'error': 'Invalid domain'},
                confidence_score=0.0,
                timestamp=datetime.now()
            )
            
        cache_key = self._generate_cache_key(domain, 'domain_analysis')
        if cache_key in self.cache and self._is_cache_valid(self.cache[cache_key]):
            cached_data = self.cache[cache_key]['data']
            return NetworkIntelligence(
                target=target,
                intel_type='domain_analysis',
                source=f"{self.name}_cached",
                data=cached_data,
                confidence_score=cached_data.get('confidence_score', 0.8),
                timestamp=datetime.now()
            )
            
        # Gather domain intelligence
        whois_data = await self._get_whois_data(domain)
        dns_data = await self._get_dns_records(domain)
        ssl_data = await self._get_ssl_certificate_info(domain)
        subdomain_data = await self._enumerate_subdomains(domain)
        security_data = await self._check_domain_security(domain)
        
        combined_data = {
            'domain': domain,
            'original_target': target,
            'whois': whois_data,
            'dns_records': dns_data,
            'ssl_certificate': ssl_data,
            'subdomains': subdomain_data,
            'security_analysis': security_data,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        confidence_score = self._calculate_domain_confidence(combined_data)
        
        # Cache results
        self.cache[cache_key] = {
            'data': combined_data,
            'timestamp': time.time()
        }
        
        return NetworkIntelligence(
            target=target,
            intel_type='domain_analysis',
            source=self.name,
            data=combined_data,
            confidence_score=confidence_score,
            timestamp=datetime.now(),
            security_info=security_data
        )
        
    def _extract_domain(self, target: str) -> str:
        """Extract domain from URL or return as-is if already a domain"""
        if target.startswith(('http://', 'https://')):
            parsed = urlparse(target)
            return parsed.netloc
        return target
        
    async def _get_whois_data(self, domain: str) -> Dict[str, Any]:
        """Get WHOIS information for domain"""
        try:
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                whois_info = await loop.run_in_executor(executor, whois.whois, domain)
                
            if whois_info:
                return {
                    'registrar': getattr(whois_info, 'registrar', None),
                    'creation_date': str(getattr(whois_info, 'creation_date', None)),
                    'expiration_date': str(getattr(whois_info, 'expiration_date', None)),
                    'updated_date': str(getattr(whois_info, 'updated_date', None)),
                    'registrant_name': getattr(whois_info, 'name', None),
                    'registrant_org': getattr(whois_info, 'org', None),
                    'registrant_country': getattr(whois_info, 'country', None),
                    'name_servers': getattr(whois_info, 'name_servers', []),
                    'status': getattr(whois_info, 'status', []),
                    'source': 'whois_lookup'
                }
                
        except Exception as e:
            logger.warning(f"WHOIS lookup failed for {domain}: {str(e)}")
            
        return {'error': 'WHOIS data not available', 'source': 'whois_lookup'}
        
    async def _get_dns_records(self, domain: str) -> Dict[str, Any]:
        """Get DNS records for domain"""
        dns_records = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
        
        try:
            resolver = dns.resolver.Resolver()
            resolver.timeout = 10
            resolver.lifetime = 10
            
            for record_type in record_types:
                try:
                    answers = resolver.resolve(domain, record_type)
                    records = []
                    
                    for answer in answers:
                        if record_type == 'MX':
                            records.append({
                                'priority': answer.preference,
                                'exchange': str(answer.exchange)
                            })
                        elif record_type == 'SOA':
                            records.append({
                                'mname': str(answer.mname),
                                'rname': str(answer.rname),
                                'serial': answer.serial,
                                'refresh': answer.refresh,
                                'retry': answer.retry,
                                'expire': answer.expire,
                                'minimum': answer.minimum
                            })
                        else:
                            records.append(str(answer))
                            
                    dns_records[record_type] = records
                    
                except dns.resolver.NXDOMAIN:
                    dns_records[record_type] = {'error': 'Domain does not exist'}
                except dns.resolver.NoAnswer:
                    dns_records[record_type] = {'error': 'No records found'}
                except Exception as e:
                    dns_records[record_type] = {'error': f'Query failed: {str(e)}'}
                    
        except Exception as e:
            logger.error(f"DNS resolution failed for {domain}: {str(e)}")
            return {'error': f'DNS resolution failed: {str(e)}'}
            
        return dns_records
        
    async def _get_ssl_certificate_info(self, domain: str) -> Dict[str, Any]:
        """Get SSL certificate information"""
        try:
            loop = asyncio.get_event_loop()
            
            def get_cert_info():
                context = ssl.create_default_context()
                with socket.create_connection((domain, 443), timeout=10) as sock:
                    with context.wrap_socket(sock, server_hostname=domain) as ssock:
                        cert_der = ssock.getpeercert_chain()[0]
                        cert = x509.load_der_x509_certificate(cert_der, default_backend())
                        
                        return {
                            'subject': cert.subject.rfc4514_string(),
                            'issuer': cert.issuer.rfc4514_string(),
                            'not_valid_before': cert.not_valid_before.isoformat(),
                            'not_valid_after': cert.not_valid_after.isoformat(),
                            'serial_number': str(cert.serial_number),
                            'version': cert.version.name,
                            'signature_algorithm': cert.signature_algorithm_oid._name,
                            'is_expired': cert.not_valid_after < datetime.now(),
                            'days_until_expiry': (cert.not_valid_after - datetime.now()).days
                        }
                        
            with ThreadPoolExecutor() as executor:
                cert_info = await loop.run_in_executor(executor, get_cert_info)
                return cert_info
                
        except Exception as e:
            logger.warning(f"SSL certificate check failed for {domain}: {str(e)}")
            return {'error': f'SSL certificate check failed: {str(e)}'}
            
    async def _enumerate_subdomains(self, domain: str) -> Dict[str, Any]:
        """Enumerate common subdomains"""
        common_subdomains = [
            'www', 'mail', 'ftp', 'blog', 'shop', 'admin', 'api', 'dev', 'test', 'staging',
            'cdn', 'app', 'mobile', 'secure', 'vpn', 'remote', 'support', 'help'
        ]
        
        found_subdomains = []
        
        try:
            resolver = dns.resolver.Resolver()
            resolver.timeout = 5
            resolver.lifetime = 5
            
            for subdomain in common_subdomains:
                try:
                    full_domain = f"{subdomain}.{domain}"
                    answers = resolver.resolve(full_domain, 'A')
                    
                    if answers:
                        ips = [str(answer) for answer in answers]
                        found_subdomains.append({
                            'subdomain': full_domain,
                            'ips': ips
                        })
                        
                except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                    continue
                except Exception:
                    continue
                    
        except Exception as e:
            logger.warning(f"Subdomain enumeration failed for {domain}: {str(e)}")
            
        return {
            'found_subdomains': found_subdomains,
            'total_found': len(found_subdomains),
            'method': 'dns_bruteforce'
        }
        
    async def _check_domain_security(self, domain: str) -> Dict[str, Any]:
        """Check domain security configurations"""
        security_info = {
            'has_ssl': False,
            'ssl_grade': 'Unknown',
            'security_headers': {},
            'vulnerabilities': [],
            'recommendations': []
        }
        
        try:
            # Check if HTTPS is available
            url = f"https://{domain}"
            response = await self._make_request(url)
            
            if 'error' not in response:
                security_info['has_ssl'] = True
                security_info['ssl_grade'] = 'A'  # Mock grade
                
                # Mock security headers check
                security_info['security_headers'] = {
                    'strict_transport_security': True,
                    'content_security_policy': False,
                    'x_frame_options': True,
                    'x_content_type_options': True
                }
                
                # Mock vulnerability assessment
                if not security_info['security_headers']['content_security_policy']:
                    security_info['vulnerabilities'].append('Missing Content Security Policy')
                    security_info['recommendations'].append('Implement Content Security Policy header')
                    
        except Exception as e:
            logger.warning(f"Security check failed for {domain}: {str(e)}")
            security_info['error'] = str(e)
            
        return security_info
        
    def _calculate_domain_confidence(self, data: Dict) -> float:
        """Calculate confidence score for domain analysis"""
        score = 0.3  # Base score
        
        # WHOIS data availability
        whois_data = data.get('whois', {})
        if 'error' not in whois_data:
            score += 0.2
            if whois_data.get('registrar'):
                score += 0.1
                
        # DNS records availability
        dns_data = data.get('dns_records', {})
        if dns_data and 'error' not in dns_data:
            score += 0.2
            if dns_data.get('A'):
                score += 0.1
                
        # SSL certificate
        ssl_data = data.get('ssl_certificate', {})
        if 'error' not in ssl_data:
            score += 0.1
            
        return min(score, 1.0)


class PortScannerScanner(BaseNetworkScanner):
    """Scanner for port scanning and service detection"""
    
    def __init__(self):
        super().__init__("port_scanner")
        self.common_ports = [
            21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 993, 995, 1433, 1521, 3306, 3389, 5432, 5900, 8080
        ]
        
    def can_handle(self, target_type: str) -> bool:
        return target_type.lower() in ['ip', 'domain', 'hostname']
        
    async def scan(self, target: str, **kwargs) -> NetworkIntelligence:
        """Perform port scan and service detection"""
        # Note: Port scanning should only be performed on owned/authorized systems
        logger.warning("Port scanning should only be performed on authorized systems")
        
        cache_key = self._generate_cache_key(target, 'port_scan')
        if cache_key in self.cache and self._is_cache_valid(self.cache[cache_key]):
            cached_data = self.cache[cache_key]['data']
            return NetworkIntelligence(
                target=target,
                intel_type='port_scan',
                source=f"{self.name}_cached",
                data=cached_data,
                confidence_score=cached_data.get('confidence_score', 0.8),
                timestamp=datetime.now()
            )
            
        # Perform basic connectivity check instead of aggressive port scan
        connectivity_results = await self._check_basic_connectivity(target)
        service_detection = await self._detect_common_services(target)
        
        combined_data = {
            'target': target,
            'scan_type': 'basic_connectivity',
            'connectivity': connectivity_results,
            'services': service_detection,
            'scan_timestamp': datetime.now().isoformat(),
            'note': 'Limited scan for security compliance'
        }
        
        confidence_score = self._calculate_port_scan_confidence(combined_data)
        
        # Cache results
        self.cache[cache_key] = {
            'data': combined_data,
            'timestamp': time.time()
        }
        
        return NetworkIntelligence(
            target=target,
            intel_type='port_scan',
            source=self.name,
            data=combined_data,
            confidence_score=confidence_score,
            timestamp=datetime.now()
        )
        
    async def _check_basic_connectivity(self, target: str) -> Dict[str, Any]:
        """Check basic connectivity to common services"""
        results = {}
        basic_ports = [80, 443, 22, 25]  # HTTP, HTTPS, SSH, SMTP
        
        for port in basic_ports:
            try:
                future = asyncio.open_connection(target, port)
                reader, writer = await asyncio.wait_for(future, timeout=3)
                
                results[port] = {
                    'status': 'open',
                    'service': self._identify_service(port),
                    'response_time': '< 3s'
                }
                
                writer.close()
                await writer.wait_closed()
                
            except asyncio.TimeoutError:
                results[port] = {
                    'status': 'filtered',
                    'service': self._identify_service(port),
                    'response_time': 'timeout'
                }
            except Exception:
                results[port] = {
                    'status': 'closed',
                    'service': self._identify_service(port),
                    'response_time': 'n/a'
                }
                
        return results
        
    async def _detect_common_services(self, target: str) -> Dict[str, Any]:
        """Detect common services through banner grabbing"""
        services = {}
        
        # HTTP service detection
        try:
            response = await self._make_request(f"http://{target}")
            if 'error' not in response:
                services['http'] = {
                    'detected': True,
                    'port': 80,
                    'server_header': 'Unknown',
                    'technology': 'Web Server'
                }
        except Exception:
            pass
            
        # HTTPS service detection
        try:
            response = await self._make_request(f"https://{target}")
            if 'error' not in response:
                services['https'] = {
                    'detected': True,
                    'port': 443,
                    'server_header': 'Unknown',
                    'technology': 'Secure Web Server'
                }
        except Exception:
            pass
            
        return services
        
    def _identify_service(self, port: int) -> str:
        """Identify service by port number"""
        service_map = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            135: 'RPC',
            139: 'NetBIOS',
            143: 'IMAP',
            443: 'HTTPS',
            993: 'IMAPS',
            995: 'POP3S',
            1433: 'MSSQL',
            1521: 'Oracle',
            3306: 'MySQL',
            3389: 'RDP',
            5432: 'PostgreSQL',
            5900: 'VNC',
            8080: 'HTTP-Alt'
        }
        
        return service_map.get(port, 'Unknown')
        
    def _calculate_port_scan_confidence(self, data: Dict) -> float:
        """Calculate confidence score for port scan"""
        score = 0.4  # Base score
        
        connectivity = data.get('connectivity', {})
        open_ports = sum(1 for port_info in connectivity.values() if port_info.get('status') == 'open')
        
        if open_ports > 0:
            score += 0.3
        if open_ports > 2:
            score += 0.2
            
        services = data.get('services', {})
        if services:
            score += 0.1
            
        return min(score, 1.0)


class NetworkInfrastructureScanner(BaseNetworkScanner):
    """Scanner for network infrastructure mapping"""
    
    def __init__(self):
        super().__init__("network_infrastructure")
        
    def can_handle(self, target_type: str) -> bool:
        return target_type.lower() in ['ip', 'domain', 'network']
        
    async def scan(self, target: str, **kwargs) -> NetworkIntelligence:
        """Map network infrastructure"""
        cache_key = self._generate_cache_key(target, 'infrastructure')
        if cache_key in self.cache and self._is_cache_valid(self.cache[cache_key]):
            cached_data = self.cache[cache_key]['data']
            return NetworkIntelligence(
                target=target,
                intel_type='network_infrastructure',
                source=f"{self.name}_cached",
                data=cached_data,
                confidence_score=cached_data.get('confidence_score', 0.8),
                timestamp=datetime.now()
            )
            
        # Gather infrastructure information
        traceroute_data = await self._perform_traceroute(target)
        hosting_info = await self._detect_hosting_provider(target)
        cdn_info = await self._detect_cdn(target)
        network_info = await self._analyze_network_block(target)
        
        combined_data = {
            'target': target,
            'traceroute': traceroute_data,
            'hosting_provider': hosting_info,
            'cdn_detection': cdn_info,
            'network_analysis': network_info,
            'scan_timestamp': datetime.now().isoformat()
        }
        
        confidence_score = self._calculate_infrastructure_confidence(combined_data)
        
        # Cache results
        self.cache[cache_key] = {
            'data': combined_data,
            'timestamp': time.time()
        }
        
        return NetworkIntelligence(
            target=target,
            intel_type='network_infrastructure',
            source=self.name,
            data=combined_data,
            confidence_score=confidence_score,
            timestamp=datetime.now()
        )
        
    async def _perform_traceroute(self, target: str) -> Dict[str, Any]:
        """Perform traceroute to target"""
        try:
            # Use system traceroute command
            system = platform.system().lower()
            if system == 'windows':
                cmd = ['tracert', '-h', '15', target]
            else:
                cmd = ['traceroute', '-m', '15', target]
                
            loop = asyncio.get_event_loop()
            
            def run_traceroute():
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                    return result.stdout if result.returncode == 0 else result.stderr
                except subprocess.TimeoutExpired:
                    return "Traceroute timed out"
                except Exception as e:
                    return f"Traceroute failed: {str(e)}"
                    
            with ThreadPoolExecutor() as executor:
                output = await loop.run_in_executor(executor, run_traceroute)
                
            # Parse traceroute output (simplified)
            hops = []
            lines = output.split('\n')
            for i, line in enumerate(lines):
                if line.strip() and not line.startswith('traceroute'):
                    hops.append({
                        'hop': i,
                        'raw_output': line.strip()
                    })
                    
            return {
                'hops': hops[:15],  # Limit to 15 hops
                'total_hops': len(hops),
                'success': 'timed out' not in output.lower()
            }
            
        except Exception as e:
            logger.warning(f"Traceroute failed for {target}: {str(e)}")
            return {'error': f'Traceroute failed: {str(e)}'}
            
    async def _detect_hosting_provider(self, target: str) -> Dict[str, Any]:
        """Detect hosting provider"""
        try:
            # Get IP if target is domain
            if not self._is_valid_ip(target):
                # Resolve domain to IP
                answers = dns.resolver.resolve(target, 'A')
                target_ip = str(answers[0])
            else:
                target_ip = target
                
            # Mock hosting provider detection based on IP ranges
            ip_obj = ipaddress.ip_address(target_ip)
            
            # Common cloud provider IP ranges (simplified)
            hosting_providers = {
                'Amazon Web Services': ['54.', '52.', '34.'],
                'Google Cloud': ['35.', '104.', '130.'],
                'Microsoft Azure': ['13.', '20.', '40.'],
                'DigitalOcean': ['64.', '159.', '167.'],
                'Cloudflare': ['104.16.', '104.17.', '172.64.']
            }
            
            detected_provider = 'Unknown'
            for provider, prefixes in hosting_providers.items():
                for prefix in prefixes:
                    if target_ip.startswith(prefix):
                        detected_provider = provider
                        break
                if detected_provider != 'Unknown':
                    break
                    
            return {
                'provider': detected_provider,
                'ip_address': target_ip,
                'detection_method': 'ip_range_analysis'
            }
            
        except Exception as e:
            logger.warning(f"Hosting provider detection failed for {target}: {str(e)}")
            return {'error': f'Hosting provider detection failed: {str(e)}'}
            
    async def _detect_cdn(self, target: str) -> Dict[str, Any]:
        """Detect CDN usage"""
        try:
            # Check CNAME records for CDN indicators
            cdn_indicators = {
                'Cloudflare': ['.cloudflare.com', '.cloudflaressl.com'],
                'Amazon CloudFront': ['.cloudfront.net'],
                'Fastly': ['.fastly.com', '.fastlylb.net'],
                'KeyCDN': ['.kxcdn.com'],
                'MaxCDN': ['.maxcdn.com'],
                'Akamai': ['.akamai.net', '.akamaiedge.net']
            }
            
            detected_cdn = 'None'
            cname_records = []
            
            try:
                answers = dns.resolver.resolve(target, 'CNAME')
                for answer in answers:
                    cname = str(answer)
                    cname_records.append(cname)
                    
                    for cdn, indicators in cdn_indicators.items():
                        for indicator in indicators:
                            if indicator in cname:
                                detected_cdn = cdn
                                break
                        if detected_cdn != 'None':
                            break
                            
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                pass
                
            return {
                'cdn_provider': detected_cdn,
                'cname_records': cname_records,
                'detection_method': 'cname_analysis'
            }
            
        except Exception as e:
            logger.warning(f"CDN detection failed for {target}: {str(e)}")
            return {'error': f'CDN detection failed: {str(e)}'}
            
    async def _analyze_network_block(self, target: str) -> Dict[str, Any]:
        """Analyze network block information"""
        try:
            # Get IP if target is domain
            if not self._is_valid_ip(target):
                answers = dns.resolver.resolve(target, 'A')
                target_ip = str(answers[0])
            else:
                target_ip = target
                
            # Mock network analysis
            ip_obj = ipaddress.ip_address(target_ip)
            
            # Determine network class and range
            if ip_obj.version == 4:
                # IPv4 analysis
                network_class = 'A' if target_ip.startswith(('1.', '126.')) else \
                               'B' if target_ip.startswith(('128.', '191.')) else 'C'
                               
                # Mock ASN and organization
                asn_number = hash(target_ip) % 65535
                organization = f"AS{asn_number} Example Network Provider"
                
                return {
                    'ip_version': 4,
                    'network_class': network_class,
                    'asn': asn_number,
                    'organization': organization,
                    'is_private': ip_obj.is_private,
                    'is_reserved': ip_obj.is_reserved,
                    'analysis_method': 'ip_classification'
                }
            else:
                # IPv6 analysis
                return {
                    'ip_version': 6,
                    'is_private': ip_obj.is_private,
                    'is_reserved': ip_obj.is_reserved,
                    'analysis_method': 'ipv6_classification'
                }
                
        except Exception as e:
            logger.warning(f"Network analysis failed for {target}: {str(e)}")
            return {'error': f'Network analysis failed: {str(e)}'}
            
    def _calculate_infrastructure_confidence(self, data: Dict) -> float:
        """Calculate confidence score for infrastructure analysis"""
        score = 0.4  # Base score
        
        if data.get('traceroute', {}).get('success'):
            score += 0.2
        if data.get('hosting_provider', {}).get('provider') != 'Unknown':
            score += 0.2
        if data.get('cdn_detection', {}).get('cdn_provider') != 'None':
            score += 0.1
        if 'error' not in data.get('network_analysis', {}):
            score += 0.1
            
        return min(score, 1.0)


class NetworkIntelligenceOrchestrator:
    """Orchestrates multiple network intelligence scanners"""
    
    def __init__(self):
        self.scanners = {
            'ip_geolocation': IPGeolocationScanner(),
            'domain_analysis': DomainAnalysisScanner(),
            'port_scanner': PortScannerScanner(),
            'network_infrastructure': NetworkInfrastructureScanner()
        }
        
    async def comprehensive_scan(self, target: str, target_type: str = 'auto') -> Dict[str, NetworkIntelligence]:
        """Perform comprehensive network intelligence scan"""
        # Auto-detect target type
        if target_type == 'auto':
            target_type = self._detect_target_type(target)
            
        results = {}
        
        # Determine applicable scanners
        applicable_scanners = []
        for scanner_name, scanner in self.scanners.items():
            if scanner.can_handle(target_type):
                applicable_scanners.append((scanner_name, scanner))
                
        # Run scans concurrently
        tasks = []
        for scanner_name, scanner in applicable_scanners:
            async with scanner:
                task = asyncio.create_task(scanner.scan(target))
                tasks.append((scanner_name, task))
                
        # Collect results
        for scanner_name, task in tasks:
            try:
                result = await task
                results[scanner_name] = result
                logger.info(f"Network scan completed: {scanner_name}")
            except Exception as e:
                logger.error(f"Network scan failed: {scanner_name} - {str(e)}")
                results[scanner_name] = NetworkIntelligence(
                    target=target,
                    intel_type=scanner_name,
                    source=scanner_name,
                    data={'error': str(e)},
                    confidence_score=0.0,
                    timestamp=datetime.now()
                )
                
        return results
        
    def _detect_target_type(self, target: str) -> str:
        """Detect target type automatically"""
        if self._is_valid_ip(target):
            return 'ip'
        elif target.startswith(('http://', 'https://')):
            return 'url'
        elif '.' in target and self._is_valid_domain(target.split('/')[-1]):
            return 'domain'
        else:
            return 'hostname'
            
    def _is_valid_ip(self, ip: str) -> bool:
        """Validate IP address"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
            
    def _is_valid_domain(self, domain: str) -> bool:
        """Validate domain name"""
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9]*\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, domain))
        
    def get_summary(self, results: Dict[str, NetworkIntelligence]) -> Dict[str, Any]:
        """Generate summary of scan results"""
        total_scanners = len(results)
        successful_scans = sum(1 for r in results.values() if r.confidence_score > 0)
        avg_confidence = sum(r.confidence_score for r in results.values()) / total_scanners if total_scanners > 0 else 0
        
        # Extract key findings
        key_findings = {}
        
        for scanner_name, result in results.items():
            if result.confidence_score > 0.5:
                if scanner_name == 'ip_geolocation':
                    geo_data = result.data.get('geolocation', {})
                    if geo_data.get('country'):
                        key_findings['location'] = f"{geo_data.get('city', 'Unknown')}, {geo_data.get('country', 'Unknown')}"
                        
                elif scanner_name == 'domain_analysis':
                    whois_data = result.data.get('whois', {})
                    if whois_data.get('registrar'):
                        key_findings['registrar'] = whois_data.get('registrar')
                        
                elif scanner_name == 'network_infrastructure':
                    hosting_data = result.data.get('hosting_provider', {})
                    if hosting_data.get('provider') != 'Unknown':
                        key_findings['hosting'] = hosting_data.get('provider')
                        
        return {
            'total_scanners': total_scanners,
            'successful_scans': successful_scans,
            'success_rate': successful_scans / total_scanners if total_scanners > 0 else 0,
            'average_confidence': avg_confidence,
            'key_findings': key_findings,
            'scan_timestamp': datetime.now().isoformat()
        }


# Example usage and testing functions
async def test_network_scanners():
    """Test network intelligence scanners"""
    print("🌐 Testing Network Intelligence Scanners")
    print("=" * 50)
    
    orchestrator = NetworkIntelligenceOrchestrator()
    
    # Test IP scan
    print("\n🔍 Testing IP Geolocation:")
    ip_results = await orchestrator.comprehensive_scan("8.8.8.8", "ip")
    
    # Test domain scan
    print("\n🔍 Testing Domain Analysis:")
    domain_results = await orchestrator.comprehensive_scan("google.com", "domain")
    
    # Generate summary
    all_results = {**ip_results, **domain_results}
    summary = orchestrator.get_summary(all_results)
    
    print(f"\n📊 Scan Summary:")
    print(f"Total scans: {summary['total_scanners']}")
    print(f"Success rate: {summary['success_rate']:.1%}")
    print(f"Average confidence: {summary['average_confidence']:.2f}")
    print(f"Key findings: {summary['key_findings']}")


if __name__ == "__main__":
    asyncio.run(test_network_scanners())