"""
Database Models for Intelligence Gathering Platform
"""

import enum
from typing import Optional
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON, Enum, Float, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class QueryType(str, enum.Enum):
    """Types of queries supported."""
    NAME = "name"
    EMAIL = "email"
    PHONE = "phone"
    USERNAME = "username"
    IMAGE = "image"
    DOMAIN = "domain"
    IP_ADDRESS = "ip_address"
    SOCIAL_PROFILE = "social_profile"


class QueryStatus(str, enum.Enum):
    """Status of a query."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ScannerType(str, enum.Enum):
    """Types of scanner modules."""
    API = "api"
    SOCIAL_MEDIA = "social_media"
    PUBLIC_RECORDS = "public_records"
    DEVICE_NETWORK = "device_network"
    IMAGE_MEDIA = "image_media"
    FORUM_COMMUNITY = "forum_community"
    DEEP_WEB = "deep_web"
    AI_CORRELATION = "ai_correlation"
    EMAIL_VERIFICATION = "email_verification"
    PHONE_LOOKUP = "phone_lookup"
    REVERSE_SEARCH = "reverse_search"


class UserRole(str, enum.Enum):
    """User roles."""
    USER = "user"
    PREMIUM = "premium"
    ADMIN = "admin"


class SubscriptionPlan(str, enum.Enum):
    """Subscription plans."""
    FREE = "free"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.FREE)
    queries_this_month = Column(Integer, default=0)
    last_query_reset = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))


class APIKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    key_hash = Column(String(255), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    requests_made = Column(Integer, default=0)
    rate_limit = Column(Integer, default=1000)  # per month
    last_used = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Query(Base):
    __tablename__ = "queries"
    
    id = Column(Integer, primary_key=True, index=True)
    query_text = Column(String(500), nullable=False)
    query_type = Column(Enum(QueryType), nullable=False)
    status = Column(Enum(QueryStatus), default=QueryStatus.PENDING)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    results_count = Column(Integer, default=0)
    processing_time = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    query_metadata = Column(JSON)


class ScanResult(Base):
    __tablename__ = "scan_results"
    
    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("queries.id"), nullable=False)
    scanner_name = Column(String(100), nullable=False)
    scanner_type = Column(Enum(ScannerType), nullable=False)
    result_data = Column(JSON)
    confidence_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("queries.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    report_data = Column(JSON)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Entity(Base):
    __tablename__ = "entities"
    
    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(50), nullable=False)  # person, organization, etc.
    name = Column(String(200), nullable=False)
    description = Column(Text)
    entity_metadata = Column(JSON)
    confidence_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class EntityRelationship(Base):
    __tablename__ = "entity_relationships"
    
    id = Column(Integer, primary_key=True, index=True)
    source_entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    target_entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    relationship_type = Column(String(50), nullable=False)
    confidence_score = Column(Float)
    relationship_metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan = Column(Enum(SubscriptionPlan), nullable=False)
    stripe_subscription_id = Column(String(100))
    status = Column(String(20), default="active")
    current_period_start = Column(DateTime(timezone=True))
    current_period_end = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"))
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    stripe_payment_intent_id = Column(String(100))
    status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(Integer)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    details = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ScannerConfig(Base):
    __tablename__ = "scanner_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    scanner_name = Column(String(100), nullable=False, unique=True)
    scanner_type = Column(Enum(ScannerType), nullable=False)
    is_enabled = Column(Boolean, default=True)
    config_data = Column(JSON)
    rate_limit = Column(Integer, default=100)
    timeout = Column(Integer, default=30)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ScannerMetrics(Base):
    __tablename__ = "scanner_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    scanner_name = Column(String(100), nullable=False)
    requests_made = Column(Integer, default=0)
    successful_requests = Column(Integer, default=0)
    failed_requests = Column(Integer, default=0)
    average_response_time = Column(Float)
    last_used = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class DataSource(Base):
    __tablename__ = "data_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    base_url = Column(String(500))
    api_key_required = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    description = Column(Text)
    source_metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())