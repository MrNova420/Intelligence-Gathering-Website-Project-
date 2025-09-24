"""
Enterprise Integration Hub
Comprehensive enterprise integration capabilities including API gateways,
webhook management, SIEM integration, and third-party service connectors.
"""

import asyncio
import logging
import json
import hmac
import hashlib
import time
from typing import Dict, List, Any, Optional, Callable, Set, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
import aiohttp
import jwt
from cryptography.fernet import Fernet
import base64
import xml.etree.ElementTree as ET
from collections import defaultdict, deque
import uuid
import asyncpg
import aiormq
import websockets

logger = logging.getLogger(__name__)

class IntegrationType(Enum):
    """Types of enterprise integrations"""
    SIEM = "siem"
    WEBHOOK = "webhook"
    API_GATEWAY = "api_gateway"
    DATABASE = "database"
    MESSAGE_QUEUE = "message_queue"
    SSO = "sso"
    LDAP = "ldap"
    CLOUD_STORAGE = "cloud_storage"

class AuthenticationType(Enum):
    """Authentication types for integrations"""
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    JWT = "jwt"
    BASIC = "basic"
    CERTIFICATE = "certificate"
    HMAC = "hmac"

@dataclass
class IntegrationConfig:
    """Configuration for an enterprise integration"""
    id: str
    name: str
    integration_type: IntegrationType
    auth_type: AuthenticationType
    endpoint: str
    credentials: Dict[str, Any]
    headers: Dict[str, str] = field(default_factory=dict)
    timeout: int = 30
    retry_attempts: int = 3
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class IntegrationEvent:
    """Event to be sent to integrations"""
    id: str
    event_type: str
    source: str
    timestamp: datetime
    data: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    priority: int = 5  # 1=high, 5=low

class WebhookManager:
    """Manages webhook integrations and delivery"""
    
    def __init__(self):
        self.webhooks: Dict[str, IntegrationConfig] = {}
        self.event_queue: deque = deque(maxlen=10000)
        self.delivery_stats: Dict[str, Dict[str, int]] = defaultdict(lambda: {"success": 0, "failure": 0})
        self.running = False
        self._delivery_task: Optional[asyncio.Task] = None
        
    async def start(self):
        """Start webhook delivery service"""
        self.running = True
        self._delivery_task = asyncio.create_task(self._delivery_loop())
        logger.info("Webhook manager started")
    
    async def stop(self):
        """Stop webhook delivery service"""
        self.running = False
        if self._delivery_task:
            self._delivery_task.cancel()
            try:
                await self._delivery_task
            except asyncio.CancelledError:
                pass
        logger.info("Webhook manager stopped")
    
    def register_webhook(self, config: IntegrationConfig):
        """Register a webhook integration"""
        if config.integration_type != IntegrationType.WEBHOOK:
            raise ValueError("Config must be for webhook integration")
        
        self.webhooks[config.id] = config
        logger.info(f"Registered webhook: {config.name}")
    
    def unregister_webhook(self, webhook_id: str):
        """Unregister a webhook"""
        if webhook_id in self.webhooks:
            del self.webhooks[webhook_id]
            logger.info(f"Unregistered webhook: {webhook_id}")
    
    async def send_event(self, event: IntegrationEvent, webhook_ids: Optional[List[str]] = None):
        """Send event to webhooks"""
        target_webhooks = webhook_ids or list(self.webhooks.keys())
        
        for webhook_id in target_webhooks:
            if webhook_id in self.webhooks and self.webhooks[webhook_id].enabled:
                self.event_queue.append((webhook_id, event))
    
    async def _delivery_loop(self):
        """Main webhook delivery loop"""
        while self.running:
            try:
                if not self.event_queue:
                    await asyncio.sleep(1)
                    continue
                
                webhook_id, event = self.event_queue.popleft()
                await self._deliver_webhook(webhook_id, event)
                
            except Exception as e:
                logger.error(f"Error in webhook delivery loop: {e}")
                await asyncio.sleep(1)
    
    async def _deliver_webhook(self, webhook_id: str, event: IntegrationEvent):
        """Deliver event to specific webhook"""
        if webhook_id not in self.webhooks:
            return
        
        config = self.webhooks[webhook_id]
        
        for attempt in range(config.retry_attempts):
            try:
                # Prepare payload
                payload = {
                    'event_id': event.id,
                    'event_type': event.event_type,
                    'source': event.source,
                    'timestamp': event.timestamp.isoformat(),
                    'data': event.data,
                    'metadata': event.metadata
                }
                
                # Prepare headers
                headers = dict(config.headers)
                headers['Content-Type'] = 'application/json'
                
                # Add authentication
                await self._add_authentication(config, headers, payload)
                
                # Send webhook
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        config.endpoint,
                        json=payload,
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=config.timeout)
                    ) as response:
                        if response.status < 400:
                            self.delivery_stats[webhook_id]["success"] += 1
                            logger.debug(f"Webhook delivered successfully: {webhook_id}")
                            return
                        else:
                            logger.warning(f"Webhook delivery failed with status {response.status}: {webhook_id}")
                
            except Exception as e:
                logger.error(f"Webhook delivery attempt {attempt + 1} failed for {webhook_id}: {e}")
                
                if attempt < config.retry_attempts - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        self.delivery_stats[webhook_id]["failure"] += 1
    
    async def _add_authentication(self, config: IntegrationConfig, headers: Dict[str, str], payload: Dict[str, Any]):
        """Add authentication to webhook request"""
        if config.auth_type == AuthenticationType.API_KEY:
            api_key = config.credentials.get('api_key')
            if api_key:
                headers['Authorization'] = f"Bearer {api_key}"
        
        elif config.auth_type == AuthenticationType.BASIC:
            username = config.credentials.get('username')
            password = config.credentials.get('password')
            if username and password:
                credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
                headers['Authorization'] = f"Basic {credentials}"
        
        elif config.auth_type == AuthenticationType.HMAC:
            secret = config.credentials.get('secret')
            if secret:
                payload_str = json.dumps(payload, sort_keys=True)
                signature = hmac.new(
                    secret.encode(),
                    payload_str.encode(),
                    hashlib.sha256
                ).hexdigest()
                headers['X-Signature'] = f"sha256={signature}"
        
        elif config.auth_type == AuthenticationType.JWT:
            secret = config.credentials.get('secret')
            if secret:
                token_payload = {
                    'iss': config.credentials.get('issuer', 'intelligence-platform'),
                    'exp': int(time.time()) + 300,  # 5 minutes
                    'iat': int(time.time())
                }
                token = jwt.encode(token_payload, secret, algorithm='HS256')
                headers['Authorization'] = f"Bearer {token}"
    
    def get_delivery_stats(self) -> Dict[str, Dict[str, int]]:
        """Get webhook delivery statistics"""
        return dict(self.delivery_stats)

class SIEMIntegration:
    """Security Information and Event Management integration"""
    
    def __init__(self):
        self.siem_configs: Dict[str, IntegrationConfig] = {}
        self.event_buffer: deque = deque(maxlen=1000)
        self.running = False
        self._forwarding_task: Optional[asyncio.Task] = None
        
    async def start(self):
        """Start SIEM integration"""
        self.running = True
        self._forwarding_task = asyncio.create_task(self._forwarding_loop())
        logger.info("SIEM integration started")
    
    async def stop(self):
        """Stop SIEM integration"""
        self.running = False
        if self._forwarding_task:
            self._forwarding_task.cancel()
            try:
                await self._forwarding_task
            except asyncio.CancelledError:
                pass
        logger.info("SIEM integration stopped")
    
    def register_siem(self, config: IntegrationConfig):
        """Register SIEM integration"""
        if config.integration_type != IntegrationType.SIEM:
            raise ValueError("Config must be for SIEM integration")
        
        self.siem_configs[config.id] = config
        logger.info(f"Registered SIEM: {config.name}")
    
    async def forward_security_event(self, event_data: Dict[str, Any]):
        """Forward security event to SIEM systems"""
        # Create standardized SIEM event
        siem_event = {
            'timestamp': datetime.utcnow().isoformat(),
            'source': 'intelligence-platform',
            'severity': event_data.get('severity', 'medium'),
            'category': event_data.get('category', 'security'),
            'event_type': event_data.get('event_type', 'unknown'),
            'description': event_data.get('description', ''),
            'source_ip': event_data.get('source_ip', ''),
            'user_id': event_data.get('user_id', ''),
            'raw_data': event_data
        }
        
        self.event_buffer.append(siem_event)
    
    async def _forwarding_loop(self):
        """Main SIEM forwarding loop"""
        while self.running:
            try:
                if not self.event_buffer:
                    await asyncio.sleep(5)
                    continue
                
                # Process events in batches
                batch_size = min(10, len(self.event_buffer))
                events_batch = []
                
                for _ in range(batch_size):
                    if self.event_buffer:
                        events_batch.append(self.event_buffer.popleft())
                
                # Forward to all SIEM systems
                await self._forward_events_batch(events_batch)
                
            except Exception as e:
                logger.error(f"Error in SIEM forwarding loop: {e}")
                await asyncio.sleep(5)
    
    async def _forward_events_batch(self, events: List[Dict[str, Any]]):
        """Forward batch of events to SIEM systems"""
        for config in self.siem_configs.values():
            if not config.enabled:
                continue
            
            try:
                # Format events for specific SIEM
                formatted_events = await self._format_for_siem(events, config)
                
                # Send to SIEM
                await self._send_to_siem(formatted_events, config)
                
            except Exception as e:
                logger.error(f"Error forwarding to SIEM {config.name}: {e}")
    
    async def _format_for_siem(self, events: List[Dict[str, Any]], config: IntegrationConfig) -> str:
        """Format events for specific SIEM system"""
        siem_type = config.metadata.get('siem_type', 'generic')
        
        if siem_type == 'splunk':
            # Splunk format
            formatted = []
            for event in events:
                formatted.append(json.dumps(event))
            return '\n'.join(formatted)
        
        elif siem_type == 'elastic':
            # Elasticsearch format
            formatted = []
            for event in events:
                formatted.append('{"index": {}}')
                formatted.append(json.dumps(event))
            return '\n'.join(formatted)
        
        elif siem_type == 'qradar':
            # QRadar CEF format
            formatted = []
            for event in events:
                cef_event = (
                    f"CEF:0|IntelligencePlatform|Scanner|1.0|{event.get('event_type', 'unknown')}"
                    f"|{event.get('description', 'Security Event')}|{self._severity_to_cef(event.get('severity', 'medium'))}"
                    f"|src={event.get('source_ip', '')} suser={event.get('user_id', '')}"
                )
                formatted.append(cef_event)
            return '\n'.join(formatted)
        
        else:
            # Generic JSON format
            return json.dumps(events, indent=2)
    
    def _severity_to_cef(self, severity: str) -> int:
        """Convert severity to CEF numeric value"""
        severity_map = {
            'low': 3,
            'medium': 5,
            'high': 8,
            'critical': 10
        }
        return severity_map.get(severity.lower(), 5)
    
    async def _send_to_siem(self, formatted_events: str, config: IntegrationConfig):
        """Send formatted events to SIEM system"""
        headers = dict(config.headers)
        headers['Content-Type'] = 'application/json'
        
        # Add authentication
        if config.auth_type == AuthenticationType.API_KEY:
            api_key = config.credentials.get('api_key')
            if api_key:
                headers['Authorization'] = f"Bearer {api_key}"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                config.endpoint,
                data=formatted_events,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=config.timeout)
            ) as response:
                if response.status >= 400:
                    logger.error(f"SIEM forwarding failed with status {response.status}")

class APIGateway:
    """Enterprise API Gateway with rate limiting and authentication"""
    
    def __init__(self):
        self.api_keys: Dict[str, Dict[str, Any]] = {}
        self.rate_limits: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.request_stats: Dict[str, Dict[str, int]] = defaultdict(lambda: {"requests": 0, "errors": 0})
        self.middleware_stack: List[Callable] = []
        
    def register_api_key(self, api_key: str, metadata: Dict[str, Any]):
        """Register API key with metadata"""
        self.api_keys[api_key] = {
            'created_at': datetime.utcnow(),
            'rate_limit': metadata.get('rate_limit', 1000),  # requests per hour
            'scopes': metadata.get('scopes', ['read']),
            'client_id': metadata.get('client_id', ''),
            'enabled': metadata.get('enabled', True),
            **metadata
        }
        logger.info(f"Registered API key for client: {metadata.get('client_id', 'unknown')}")
    
    def add_middleware(self, middleware: Callable):
        """Add middleware to the stack"""
        self.middleware_stack.append(middleware)
    
    async def authenticate_request(self, api_key: str) -> Tuple[bool, Dict[str, Any]]:
        """Authenticate API request"""
        if api_key not in self.api_keys:
            return False, {'error': 'Invalid API key'}
        
        key_info = self.api_keys[api_key]
        
        if not key_info.get('enabled', True):
            return False, {'error': 'API key disabled'}
        
        # Check rate limiting
        if not await self._check_rate_limit(api_key, key_info['rate_limit']):
            return False, {'error': 'Rate limit exceeded'}
        
        return True, key_info
    
    async def _check_rate_limit(self, api_key: str, limit: int) -> bool:
        """Check rate limiting for API key"""
        now = time.time()
        hour_ago = now - 3600
        
        # Clean old requests
        request_times = self.rate_limits[api_key]
        while request_times and request_times[0] < hour_ago:
            request_times.popleft()
        
        # Check limit
        if len(request_times) >= limit:
            return False
        
        # Record request
        request_times.append(now)
        return True
    
    async def process_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process API request through middleware stack"""
        context = {'request': request_data, 'response': {}}
        
        # Execute middleware stack
        for middleware in self.middleware_stack:
            try:
                context = await middleware(context)
                if context.get('stop_processing'):
                    break
            except Exception as e:
                logger.error(f"Middleware error: {e}")
                context['response'] = {'error': 'Internal server error'}
                break
        
        return context.get('response', {})
    
    def get_api_stats(self) -> Dict[str, Any]:
        """Get API gateway statistics"""
        total_requests = sum(stats['requests'] for stats in self.request_stats.values())
        total_errors = sum(stats['errors'] for stats in self.request_stats.values())
        
        return {
            'total_api_keys': len(self.api_keys),
            'total_requests': total_requests,
            'total_errors': total_errors,
            'error_rate': total_errors / total_requests if total_requests > 0 else 0,
            'active_keys': len([k for k, v in self.api_keys.items() if v.get('enabled', True)]),
            'request_stats_by_key': dict(self.request_stats)
        }

class MessageQueueIntegration:
    """Message queue integration for enterprise messaging"""
    
    def __init__(self):
        self.connections: Dict[str, Any] = {}
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self.message_stats: Dict[str, int] = defaultdict(int)
        
    async def connect_rabbitmq(self, connection_id: str, url: str):
        """Connect to RabbitMQ"""
        try:
            connection = await aiormq.connect(url)
            channel = await connection.channel()
            
            self.connections[connection_id] = {
                'type': 'rabbitmq',
                'connection': connection,
                'channel': channel
            }
            
            logger.info(f"Connected to RabbitMQ: {connection_id}")
            
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ {connection_id}: {e}")
    
    async def publish_message(self, connection_id: str, queue_name: str, message: Dict[str, Any]):
        """Publish message to queue"""
        if connection_id not in self.connections:
            raise ValueError(f"Connection {connection_id} not found")
        
        conn_info = self.connections[connection_id]
        
        if conn_info['type'] == 'rabbitmq':
            channel = conn_info['channel']
            
            # Declare queue
            await channel.queue_declare(queue_name, durable=True)
            
            # Publish message
            await channel.basic_publish(
                json.dumps(message).encode(),
                routing_key=queue_name
            )
            
            self.message_stats[f"{connection_id}:{queue_name}:published"] += 1
            logger.debug(f"Published message to {queue_name}")
    
    async def subscribe_to_queue(self, connection_id: str, queue_name: str, callback: Callable):
        """Subscribe to queue messages"""
        if connection_id not in self.connections:
            raise ValueError(f"Connection {connection_id} not found")
        
        conn_info = self.connections[connection_id]
        
        if conn_info['type'] == 'rabbitmq':
            channel = conn_info['channel']
            
            # Declare queue
            await channel.queue_declare(queue_name, durable=True)
            
            # Set up consumer
            async def message_handler(message):
                try:
                    data = json.loads(message.body.decode())
                    await callback(data)
                    await message.ack()
                    self.message_stats[f"{connection_id}:{queue_name}:consumed"] += 1
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    await message.nack()
            
            await channel.basic_consume(queue_name, message_handler)
            self.subscribers[f"{connection_id}:{queue_name}"].append(callback)
            
            logger.info(f"Subscribed to queue {queue_name}")
    
    def get_message_stats(self) -> Dict[str, int]:
        """Get message queue statistics"""
        return dict(self.message_stats)

class CloudStorageIntegration:
    """Cloud storage integration for data archiving"""
    
    def __init__(self):
        self.storage_configs: Dict[str, IntegrationConfig] = {}
        self.upload_stats: Dict[str, Dict[str, int]] = defaultdict(lambda: {"uploads": 0, "failures": 0})
        
    def register_storage(self, config: IntegrationConfig):
        """Register cloud storage configuration"""
        if config.integration_type != IntegrationType.CLOUD_STORAGE:
            raise ValueError("Config must be for cloud storage integration")
        
        self.storage_configs[config.id] = config
        logger.info(f"Registered cloud storage: {config.name}")
    
    async def upload_data(self, storage_id: str, key: str, data: bytes, metadata: Dict[str, Any] = None):
        """Upload data to cloud storage"""
        if storage_id not in self.storage_configs:
            raise ValueError(f"Storage {storage_id} not configured")
        
        config = self.storage_configs[storage_id]
        storage_type = config.metadata.get('storage_type', 'generic')
        
        try:
            if storage_type == 's3':
                await self._upload_to_s3(config, key, data, metadata)
            elif storage_type == 'azure':
                await self._upload_to_azure(config, key, data, metadata)
            elif storage_type == 'gcs':
                await self._upload_to_gcs(config, key, data, metadata)
            else:
                raise ValueError(f"Unsupported storage type: {storage_type}")
            
            self.upload_stats[storage_id]["uploads"] += 1
            logger.info(f"Successfully uploaded {key} to {storage_id}")
            
        except Exception as e:
            self.upload_stats[storage_id]["failures"] += 1
            logger.error(f"Failed to upload {key} to {storage_id}: {e}")
            raise
    
    async def _upload_to_s3(self, config: IntegrationConfig, key: str, data: bytes, metadata: Dict[str, Any]):
        """Upload to AWS S3"""
        # Implement S3 upload logic
        logger.info(f"Uploading to S3: {key}")
    
    async def _upload_to_azure(self, config: IntegrationConfig, key: str, data: bytes, metadata: Dict[str, Any]):
        """Upload to Azure Blob Storage"""
        # Implement Azure upload logic
        logger.info(f"Uploading to Azure: {key}")
    
    async def _upload_to_gcs(self, config: IntegrationConfig, key: str, data: bytes, metadata: Dict[str, Any]):
        """Upload to Google Cloud Storage"""
        # Implement GCS upload logic
        logger.info(f"Uploading to GCS: {key}")
    
    def get_upload_stats(self) -> Dict[str, Dict[str, int]]:
        """Get upload statistics"""
        return dict(self.upload_stats)

class EnterpriseIntegrationHub:
    """Main hub coordinating all enterprise integrations"""
    
    def __init__(self):
        self.webhook_manager = WebhookManager()
        self.siem_integration = SIEMIntegration()
        self.api_gateway = APIGateway()
        self.message_queue = MessageQueueIntegration()
        self.cloud_storage = CloudStorageIntegration()
        self.running = False
        
    async def start(self):
        """Start all integration services"""
        await self.webhook_manager.start()
        await self.siem_integration.start()
        
        self.running = True
        logger.info("Enterprise Integration Hub started")
    
    async def stop(self):
        """Stop all integration services"""
        self.running = False
        
        await self.webhook_manager.stop()
        await self.siem_integration.stop()
        
        logger.info("Enterprise Integration Hub stopped")
    
    async def send_intelligence_alert(self, alert_data: Dict[str, Any]):
        """Send intelligence alert through all configured channels"""
        # Create integration event
        event = IntegrationEvent(
            id=str(uuid.uuid4()),
            event_type="intelligence_alert",
            source="intelligence_platform",
            timestamp=datetime.utcnow(),
            data=alert_data,
            priority=1 if alert_data.get('severity') == 'critical' else 3
        )
        
        # Send to webhooks
        await self.webhook_manager.send_event(event)
        
        # Forward to SIEM
        await self.siem_integration.forward_security_event(alert_data)
        
        logger.info(f"Intelligence alert sent: {alert_data.get('title', 'Unknown')}")
    
    async def archive_scan_results(self, scan_id: str, results: Dict[str, Any]):
        """Archive scan results to cloud storage"""
        # Serialize results
        data = json.dumps(results, indent=2).encode('utf-8')
        
        # Upload to all configured storage
        for storage_id in self.cloud_storage.storage_configs:
            try:
                key = f"scan_results/{datetime.utcnow().strftime('%Y/%m/%d')}/{scan_id}.json"
                await self.cloud_storage.upload_data(storage_id, key, data)
            except Exception as e:
                logger.error(f"Failed to archive to {storage_id}: {e}")
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get status of all integrations"""
        return {
            'webhook_delivery_stats': self.webhook_manager.get_delivery_stats(),
            'api_gateway_stats': self.api_gateway.get_api_stats(),
            'message_queue_stats': self.message_queue.get_message_stats(),
            'cloud_storage_stats': self.cloud_storage.get_upload_stats(),
            'active_webhooks': len(self.webhook_manager.webhooks),
            'active_siem_configs': len(self.siem_integration.siem_configs),
            'registered_api_keys': len(self.api_gateway.api_keys),
            'status': 'running' if self.running else 'stopped'
        }

# Global integration hub instance
integration_hub = EnterpriseIntegrationHub()

async def start_enterprise_integrations():
    """Start enterprise integration services"""
    await integration_hub.start()

async def stop_enterprise_integrations():
    """Stop enterprise integration services"""
    await integration_hub.stop()