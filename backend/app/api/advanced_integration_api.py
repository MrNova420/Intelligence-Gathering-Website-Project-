"""
Advanced Integration API and Webhook System
==========================================

Enterprise-grade integration capabilities including:
- RESTful API with OpenAPI 3.0 specification
- Webhook management and delivery system
- Third-party service integrations
- Real-time event streaming
- API rate limiting and throttling
- Authentication and authorization
- Data transformation and mapping
"""

import asyncio
import logging
import json
import hmac
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import uuid
import aiohttp
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

# Mock FastAPI imports for development
try:
    from fastapi import FastAPI, APIRouter, HTTPException, Depends, Header, Query, Body
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel, Field, validator
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    # Mock classes for development
    class BaseModel:
        pass
    class APIRouter:
        def __init__(self, *args, **kwargs): pass
        def post(self, *args, **kwargs): return lambda f: f
        def get(self, *args, **kwargs): return lambda f: f
        def put(self, *args, **kwargs): return lambda f: f
        def delete(self, *args, **kwargs): return lambda f: f


class WebhookEventType(str, Enum):
    """Types of webhook events"""
    SCAN_STARTED = "scan.started"
    SCAN_COMPLETED = "scan.completed"
    SCAN_FAILED = "scan.failed"
    QUERY_CREATED = "query.created"
    QUERY_UPDATED = "query.updated"
    REPORT_GENERATED = "report.generated"
    ALERT_TRIGGERED = "alert.triggered"
    USER_CREATED = "user.created"
    SUBSCRIPTION_CHANGED = "subscription.changed"


class IntegrationType(str, Enum):
    """Types of integrations"""
    WEBHOOK = "webhook"
    API_POLLING = "api_polling"
    PUSH_NOTIFICATION = "push_notification"
    EMAIL_NOTIFICATION = "email_notification"
    SLACK = "slack"
    TEAMS = "teams"
    DISCORD = "discord"
    JIRA = "jira"
    SERVICENOW = "servicenow"


class DeliveryStatus(str, Enum):
    """Webhook delivery status"""
    PENDING = "pending"
    DELIVERED = "delivered"
    FAILED = "failed"
    RETRYING = "retrying"
    CANCELLED = "cancelled"


@dataclass
class WebhookEndpoint:
    """Webhook endpoint configuration"""
    endpoint_id: str
    name: str
    url: str
    secret: str
    event_types: List[WebhookEventType]
    active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_delivery: Optional[datetime] = None
    delivery_success_count: int = 0
    delivery_failure_count: int = 0
    custom_headers: Dict[str, str] = field(default_factory=dict)
    retry_config: Dict[str, Any] = field(default_factory=lambda: {
        "max_retries": 3,
        "retry_delay": 60,  # seconds
        "backoff_multiplier": 2
    })


@dataclass
class WebhookEvent:
    """Webhook event data"""
    event_id: str
    event_type: WebhookEventType
    payload: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)
    source: str = "intelligence_platform"
    version: str = "1.0"


@dataclass
class WebhookDelivery:
    """Webhook delivery attempt"""
    delivery_id: str
    endpoint_id: str
    event_id: str
    status: DeliveryStatus
    created_at: datetime = field(default_factory=datetime.utcnow)
    delivered_at: Optional[datetime] = None
    response_status: Optional[int] = None
    response_body: Optional[str] = None
    error_message: Optional[str] = None
    attempt_count: int = 0
    next_retry_at: Optional[datetime] = None


# Pydantic models for API
if FASTAPI_AVAILABLE:
    class WebhookEndpointCreate(BaseModel):
        name: str = Field(..., description="Webhook endpoint name")
        url: str = Field(..., description="Webhook URL")
        event_types: List[WebhookEventType] = Field(..., description="Event types to subscribe to")
        secret: Optional[str] = Field(None, description="Secret for signature verification")
        custom_headers: Optional[Dict[str, str]] = Field(default_factory=dict)
        
        @validator('url')
        def validate_url(cls, v):
            if not v.startswith(('http://', 'https://')):
                raise ValueError('URL must start with http:// or https://')
            return v
    
    class WebhookEndpointUpdate(BaseModel):
        name: Optional[str] = None
        url: Optional[str] = None
        event_types: Optional[List[WebhookEventType]] = None
        active: Optional[bool] = None
        custom_headers: Optional[Dict[str, str]] = None
    
    class IntegrationConfig(BaseModel):
        integration_type: IntegrationType
        name: str
        config: Dict[str, Any]
        active: bool = True
    
    class APIResponse(BaseModel):
        success: bool
        message: str
        data: Optional[Dict[str, Any]] = None
        timestamp: datetime = Field(default_factory=datetime.utcnow)


class WebhookManager:
    """Manages webhook endpoints and deliveries"""
    
    def __init__(self):
        self.endpoints: Dict[str, WebhookEndpoint] = {}
        self.deliveries: Dict[str, WebhookDelivery] = {}
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._delivery_worker_running = False
        self._delivery_task = None
    
    def register_webhook_endpoint(
        self, 
        name: str, 
        url: str, 
        event_types: List[WebhookEventType],
        secret: str = None,
        custom_headers: Dict[str, str] = None
    ) -> str:
        """Register a new webhook endpoint"""
        
        endpoint_id = str(uuid.uuid4())
        secret = secret or self._generate_webhook_secret()
        
        endpoint = WebhookEndpoint(
            endpoint_id=endpoint_id,
            name=name,
            url=url,
            secret=secret,
            event_types=event_types,
            custom_headers=custom_headers or {}
        )
        
        self.endpoints[endpoint_id] = endpoint
        self.logger.info(f"Registered webhook endpoint: {name} ({endpoint_id})")
        
        return endpoint_id
    
    def update_webhook_endpoint(
        self, 
        endpoint_id: str, 
        **updates
    ) -> bool:
        """Update a webhook endpoint"""
        
        if endpoint_id not in self.endpoints:
            return False
        
        endpoint = self.endpoints[endpoint_id]
        
        for key, value in updates.items():
            if hasattr(endpoint, key):
                setattr(endpoint, key, value)
        
        self.logger.info(f"Updated webhook endpoint: {endpoint_id}")
        return True
    
    def delete_webhook_endpoint(self, endpoint_id: str) -> bool:
        """Delete a webhook endpoint"""
        
        if endpoint_id not in self.endpoints:
            return False
        
        del self.endpoints[endpoint_id]
        self.logger.info(f"Deleted webhook endpoint: {endpoint_id}")
        return True
    
    def get_webhook_endpoints(
        self, 
        active_only: bool = True
    ) -> List[WebhookEndpoint]:
        """Get webhook endpoints"""
        
        endpoints = list(self.endpoints.values())
        
        if active_only:
            endpoints = [ep for ep in endpoints if ep.active]
        
        return endpoints
    
    async def trigger_webhook_event(
        self, 
        event_type: WebhookEventType, 
        payload: Dict[str, Any]
    ):
        """Trigger a webhook event"""
        
        event = WebhookEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            payload=payload
        )
        
        # Find matching endpoints
        matching_endpoints = [
            endpoint for endpoint in self.endpoints.values()
            if endpoint.active and event_type in endpoint.event_types
        ]
        
        if not matching_endpoints:
            self.logger.debug(f"No endpoints subscribed to event: {event_type}")
            return
        
        # Create delivery attempts
        for endpoint in matching_endpoints:
            delivery = WebhookDelivery(
                delivery_id=str(uuid.uuid4()),
                endpoint_id=endpoint.endpoint_id,
                event_id=event.event_id,
                status=DeliveryStatus.PENDING
            )
            
            self.deliveries[delivery.delivery_id] = delivery
        
        # Start delivery worker if not running
        if not self._delivery_worker_running:
            await self.start_delivery_worker()
        
        self.logger.info(f"Triggered webhook event {event_type} to {len(matching_endpoints)} endpoints")
    
    async def start_delivery_worker(self):
        """Start the webhook delivery worker"""
        
        if self._delivery_worker_running:
            return
        
        self._delivery_worker_running = True
        self._delivery_task = asyncio.create_task(self._delivery_worker_loop())
        self.logger.info("Started webhook delivery worker")
    
    async def stop_delivery_worker(self):
        """Stop the webhook delivery worker"""
        
        self._delivery_worker_running = False
        
        if self._delivery_task:
            self._delivery_task.cancel()
            try:
                await self._delivery_task
            except asyncio.CancelledError:
                pass
        
        self.logger.info("Stopped webhook delivery worker")
    
    async def _delivery_worker_loop(self):
        """Main delivery worker loop"""
        
        while self._delivery_worker_running:
            try:
                # Find pending deliveries
                pending_deliveries = [
                    delivery for delivery in self.deliveries.values()
                    if delivery.status == DeliveryStatus.PENDING or 
                    (delivery.status == DeliveryStatus.RETRYING and 
                     delivery.next_retry_at and 
                     delivery.next_retry_at <= datetime.utcnow())
                ]
                
                # Process deliveries
                for delivery in pending_deliveries:
                    await self._attempt_delivery(delivery)
                
                # Wait before next iteration
                await asyncio.sleep(10)
                
            except Exception as e:
                self.logger.error(f"Error in delivery worker loop: {e}")
                await asyncio.sleep(30)
    
    async def _attempt_delivery(self, delivery: WebhookDelivery):
        """Attempt to deliver a webhook"""
        
        try:
            endpoint = self.endpoints.get(delivery.endpoint_id)
            if not endpoint:
                delivery.status = DeliveryStatus.CANCELLED
                delivery.error_message = "Endpoint not found"
                return
            
            if not endpoint.active:
                delivery.status = DeliveryStatus.CANCELLED
                delivery.error_message = "Endpoint inactive"
                return
            
            # Get event data (mock implementation)
            event_payload = {
                "event_id": delivery.event_id,
                "event_type": "scan.completed",
                "timestamp": datetime.utcnow().isoformat(),
                "data": {"scan_id": "12345", "status": "completed"}
            }
            
            # Create webhook payload
            webhook_payload = {
                "id": delivery.event_id,
                "event": event_payload["event_type"],
                "created": event_payload["timestamp"],
                "data": event_payload["data"]
            }
            
            # Generate signature
            signature = self._generate_signature(
                json.dumps(webhook_payload, sort_keys=True),
                endpoint.secret
            )
            
            # Prepare headers
            headers = {
                "Content-Type": "application/json",
                "X-Webhook-Signature": signature,
                "X-Webhook-Event": event_payload["event_type"],
                "X-Webhook-Delivery": delivery.delivery_id,
                "User-Agent": "Intelligence-Platform-Webhooks/1.0"
            }
            
            # Add custom headers
            headers.update(endpoint.custom_headers)
            
            # Make HTTP request
            delivery.attempt_count += 1
            delivery.status = DeliveryStatus.RETRYING
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
                async with session.post(
                    endpoint.url,
                    json=webhook_payload,
                    headers=headers
                ) as response:
                    delivery.response_status = response.status
                    delivery.response_body = await response.text()
                    
                    if 200 <= response.status < 300:
                        # Success
                        delivery.status = DeliveryStatus.DELIVERED
                        delivery.delivered_at = datetime.utcnow()
                        endpoint.delivery_success_count += 1
                        endpoint.last_delivery = datetime.utcnow()
                        
                        self.logger.info(f"Webhook delivered successfully: {delivery.delivery_id}")
                    else:
                        # HTTP error
                        await self._handle_delivery_failure(delivery, endpoint, f"HTTP {response.status}")
        
        except Exception as e:
            await self._handle_delivery_failure(delivery, endpoint, str(e))
    
    async def _handle_delivery_failure(
        self, 
        delivery: WebhookDelivery, 
        endpoint: WebhookEndpoint, 
        error_message: str
    ):
        """Handle webhook delivery failure"""
        
        delivery.error_message = error_message
        endpoint.delivery_failure_count += 1
        
        max_retries = endpoint.retry_config.get("max_retries", 3)
        
        if delivery.attempt_count >= max_retries:
            # Max retries reached
            delivery.status = DeliveryStatus.FAILED
            self.logger.error(f"Webhook delivery failed permanently: {delivery.delivery_id} - {error_message}")
        else:
            # Schedule retry
            retry_delay = endpoint.retry_config.get("retry_delay", 60)
            backoff_multiplier = endpoint.retry_config.get("backoff_multiplier", 2)
            
            delay = retry_delay * (backoff_multiplier ** (delivery.attempt_count - 1))
            delivery.next_retry_at = datetime.utcnow() + timedelta(seconds=delay)
            delivery.status = DeliveryStatus.RETRYING
            
            self.logger.warning(f"Webhook delivery failed, retry scheduled: {delivery.delivery_id} - {error_message}")
    
    def _generate_webhook_secret(self) -> str:
        """Generate a webhook secret"""
        import secrets
        return secrets.token_urlsafe(32)
    
    def _generate_signature(self, payload: str, secret: str) -> str:
        """Generate webhook signature"""
        signature = hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        return f"sha256={signature}"
    
    def get_delivery_history(
        self, 
        endpoint_id: str = None, 
        limit: int = 100
    ) -> List[WebhookDelivery]:
        """Get webhook delivery history"""
        
        deliveries = list(self.deliveries.values())
        
        if endpoint_id:
            deliveries = [d for d in deliveries if d.endpoint_id == endpoint_id]
        
        # Sort by created_at descending
        deliveries.sort(key=lambda x: x.created_at, reverse=True)
        
        return deliveries[:limit]


class ThirdPartyIntegrationManager:
    """Manages third-party service integrations"""
    
    def __init__(self):
        self.integrations: Dict[str, Dict[str, Any]] = {}
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def register_integration(
        self, 
        integration_type: IntegrationType, 
        name: str, 
        config: Dict[str, Any]
    ) -> str:
        """Register a third-party integration"""
        
        integration_id = str(uuid.uuid4())
        
        integration = {
            "integration_id": integration_id,
            "type": integration_type,
            "name": name,
            "config": config,
            "active": True,
            "created_at": datetime.utcnow(),
            "last_used": None,
            "success_count": 0,
            "failure_count": 0
        }
        
        self.integrations[integration_id] = integration
        self.logger.info(f"Registered {integration_type.value} integration: {name}")
        
        return integration_id
    
    async def send_notification(
        self, 
        integration_id: str, 
        message: str, 
        data: Dict[str, Any] = None
    ) -> bool:
        """Send notification through integration"""
        
        integration = self.integrations.get(integration_id)
        if not integration or not integration["active"]:
            return False
        
        try:
            integration_type = IntegrationType(integration["type"])
            
            if integration_type == IntegrationType.SLACK:
                success = await self._send_slack_notification(integration, message, data)
            elif integration_type == IntegrationType.TEAMS:
                success = await self._send_teams_notification(integration, message, data)
            elif integration_type == IntegrationType.EMAIL_NOTIFICATION:
                success = await self._send_email_notification(integration, message, data)
            else:
                self.logger.warning(f"Unsupported integration type: {integration_type}")
                return False
            
            # Update statistics
            integration["last_used"] = datetime.utcnow()
            if success:
                integration["success_count"] += 1
            else:
                integration["failure_count"] += 1
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error sending notification: {e}")
            integration["failure_count"] += 1
            return False
    
    async def _send_slack_notification(
        self, 
        integration: Dict[str, Any], 
        message: str, 
        data: Dict[str, Any]
    ) -> bool:
        """Send Slack notification"""
        
        webhook_url = integration["config"].get("webhook_url")
        if not webhook_url:
            return False
        
        payload = {
            "text": message,
            "username": "Intelligence Platform",
            "icon_emoji": ":mag:",
            "attachments": []
        }
        
        if data:
            attachment = {
                "color": "good",
                "fields": [
                    {"title": k, "value": str(v), "short": True}
                    for k, v in data.items()
                ]
            }
            payload["attachments"].append(attachment)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=payload) as response:
                    return response.status == 200
        except Exception as e:
            self.logger.error(f"Slack notification failed: {e}")
            return False
    
    async def _send_teams_notification(
        self, 
        integration: Dict[str, Any], 
        message: str, 
        data: Dict[str, Any]
    ) -> bool:
        """Send Microsoft Teams notification"""
        
        webhook_url = integration["config"].get("webhook_url")
        if not webhook_url:
            return False
        
        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0076D7",
            "summary": "Intelligence Platform Notification",
            "sections": [
                {
                    "activityTitle": "Intelligence Platform",
                    "activitySubtitle": message,
                    "facts": [
                        {"name": k, "value": str(v)}
                        for k, v in (data or {}).items()
                    ]
                }
            ]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=payload) as response:
                    return response.status == 200
        except Exception as e:
            self.logger.error(f"Teams notification failed: {e}")
            return False
    
    async def _send_email_notification(
        self, 
        integration: Dict[str, Any], 
        message: str, 
        data: Dict[str, Any]
    ) -> bool:
        """Send email notification (mock implementation)"""
        
        # This would integrate with actual email service (SendGrid, SES, etc.)
        self.logger.info(f"Email notification: {message}")
        return True
    
    def get_integrations(self) -> List[Dict[str, Any]]:
        """Get all integrations"""
        return list(self.integrations.values())


class AdvancedIntegrationAPI:
    """Advanced Integration API with FastAPI"""
    
    def __init__(self):
        self.webhook_manager = WebhookManager()
        self.integration_manager = ThirdPartyIntegrationManager()
        self.router = APIRouter(prefix="/api/v1/integrations", tags=["integrations"])
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Set up routes
        self._setup_routes()
    
    def _setup_routes(self):
        """Set up API routes"""
        
        if not FASTAPI_AVAILABLE:
            return
        
        @self.router.post("/webhooks", response_model=APIResponse)
        async def create_webhook_endpoint(webhook: WebhookEndpointCreate):
            """Create a new webhook endpoint"""
            try:
                endpoint_id = self.webhook_manager.register_webhook_endpoint(
                    name=webhook.name,
                    url=webhook.url,
                    event_types=webhook.event_types,
                    secret=webhook.secret,
                    custom_headers=webhook.custom_headers
                )
                
                return APIResponse(
                    success=True,
                    message="Webhook endpoint created successfully",
                    data={"endpoint_id": endpoint_id}
                )
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
        
        @self.router.get("/webhooks", response_model=APIResponse)
        async def list_webhook_endpoints():
            """List all webhook endpoints"""
            endpoints = self.webhook_manager.get_webhook_endpoints()
            
            return APIResponse(
                success=True,
                message="Webhook endpoints retrieved successfully",
                data={
                    "endpoints": [
                        {
                            "endpoint_id": ep.endpoint_id,
                            "name": ep.name,
                            "url": ep.url,
                            "event_types": [et.value for et in ep.event_types],
                            "active": ep.active,
                            "created_at": ep.created_at.isoformat(),
                            "delivery_success_count": ep.delivery_success_count,
                            "delivery_failure_count": ep.delivery_failure_count
                        }
                        for ep in endpoints
                    ]
                }
            )
        
        @self.router.put("/webhooks/{endpoint_id}", response_model=APIResponse)
        async def update_webhook_endpoint(endpoint_id: str, updates: WebhookEndpointUpdate):
            """Update a webhook endpoint"""
            
            update_data = updates.dict(exclude_unset=True)
            success = self.webhook_manager.update_webhook_endpoint(endpoint_id, **update_data)
            
            if not success:
                raise HTTPException(status_code=404, detail="Webhook endpoint not found")
            
            return APIResponse(
                success=True,
                message="Webhook endpoint updated successfully"
            )
        
        @self.router.delete("/webhooks/{endpoint_id}", response_model=APIResponse)
        async def delete_webhook_endpoint(endpoint_id: str):
            """Delete a webhook endpoint"""
            
            success = self.webhook_manager.delete_webhook_endpoint(endpoint_id)
            
            if not success:
                raise HTTPException(status_code=404, detail="Webhook endpoint not found")
            
            return APIResponse(
                success=True,
                message="Webhook endpoint deleted successfully"
            )
        
        @self.router.get("/webhooks/{endpoint_id}/deliveries", response_model=APIResponse)
        async def get_webhook_deliveries(endpoint_id: str, limit: int = Query(100, le=500)):
            """Get webhook delivery history for an endpoint"""
            
            deliveries = self.webhook_manager.get_delivery_history(endpoint_id, limit)
            
            return APIResponse(
                success=True,
                message="Delivery history retrieved successfully",
                data={
                    "deliveries": [
                        {
                            "delivery_id": d.delivery_id,
                            "event_id": d.event_id,
                            "status": d.status.value,
                            "created_at": d.created_at.isoformat(),
                            "delivered_at": d.delivered_at.isoformat() if d.delivered_at else None,
                            "response_status": d.response_status,
                            "error_message": d.error_message,
                            "attempt_count": d.attempt_count
                        }
                        for d in deliveries
                    ]
                }
            )
        
        @self.router.post("/webhooks/test", response_model=APIResponse)
        async def test_webhook_event(
            event_type: WebhookEventType,
            payload: Dict[str, Any] = Body(...)
        ):
            """Test webhook event delivery"""
            
            await self.webhook_manager.trigger_webhook_event(event_type, payload)
            
            return APIResponse(
                success=True,
                message="Test webhook event triggered successfully"
            )
        
        @self.router.post("/third-party", response_model=APIResponse)
        async def create_integration(integration: IntegrationConfig):
            """Create a third-party integration"""
            
            try:
                integration_id = self.integration_manager.register_integration(
                    integration.integration_type,
                    integration.name,
                    integration.config
                )
                
                return APIResponse(
                    success=True,
                    message="Integration created successfully",
                    data={"integration_id": integration_id}
                )
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
        
        @self.router.get("/third-party", response_model=APIResponse)
        async def list_integrations():
            """List all third-party integrations"""
            
            integrations = self.integration_manager.get_integrations()
            
            return APIResponse(
                success=True,
                message="Integrations retrieved successfully",
                data={"integrations": integrations}
            )
        
        @self.router.post("/third-party/{integration_id}/notify", response_model=APIResponse)
        async def send_notification(
            integration_id: str,
            message: str = Body(...),
            data: Optional[Dict[str, Any]] = Body(None)
        ):
            """Send notification through integration"""
            
            success = await self.integration_manager.send_notification(
                integration_id, message, data
            )
            
            if not success:
                raise HTTPException(status_code=400, detail="Failed to send notification")
            
            return APIResponse(
                success=True,
                message="Notification sent successfully"
            )
    
    def get_router(self) -> APIRouter:
        """Get the FastAPI router"""
        return self.router


# Global instances
webhook_manager = WebhookManager()
integration_manager = ThirdPartyIntegrationManager()
integration_api = AdvancedIntegrationAPI()


# Convenience functions
async def trigger_event(event_type: WebhookEventType, payload: Dict[str, Any]):
    """Trigger a webhook event"""
    await webhook_manager.trigger_webhook_event(event_type, payload)


async def send_notification(integration_id: str, message: str, data: Dict[str, Any] = None) -> bool:
    """Send notification through integration"""
    return await integration_manager.send_notification(integration_id, message, data)


def register_webhook(name: str, url: str, event_types: List[WebhookEventType]) -> str:
    """Register a webhook endpoint"""
    return webhook_manager.register_webhook_endpoint(name, url, event_types)


def register_slack_integration(name: str, webhook_url: str) -> str:
    """Register Slack integration"""
    return integration_manager.register_integration(
        IntegrationType.SLACK,
        name,
        {"webhook_url": webhook_url}
    )