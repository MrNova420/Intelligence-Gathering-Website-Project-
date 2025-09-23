# Mock SQLAlchemy for demonstration when SQLAlchemy is not installed
try:
    from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON, Enum, Float, LargeBinary
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship
    from sqlalchemy.sql import func
except ImportError:
    # Mock SQLAlchemy classes for testing
    def Column(*args, **kwargs):
        return None
    
    def Integer():
        return "Integer"
    
    def String(length=None):
        return f"String({length})"
    
    def Text():
        return "Text"
    
    def DateTime(timezone=False):
        return "DateTime"
    
    def Boolean():
        return "Boolean"
    
    def ForeignKey(key):
        return f"ForeignKey({key})"
    
    def Float():
        return "Float"
    
    def JSON():
        return "JSON"
    
    def Enum(*args, **kwargs):
        return "Enum"
    
    def LargeBinary():
        return "LargeBinary"
    
    def declarative_base():
        class MockBase:
            pass
        return MockBase
    
    def relationship(*args, **kwargs):
        return None
    
    class func:
        @staticmethod
        def now():
            return "func.now()"

import enum
from typing import Optional

# Create Base if not imported
try:
    from app.core.database import Base
except ImportError:
    Base = declarative_base()


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
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.FREE)
    queries_this_month = Column(Integer, default=0)
    last_query_reset = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    queries = relationship("Query", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")
    api_keys = relationship("APIKey", back_populates="user")
    payments = relationship("Payment", back_populates="user")


class APIKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    key_hash = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    requests_made = Column(Integer, default=0)
    rate_limit = Column(Integer, default=1000)  # per month
    last_used = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="api_keys")


class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    query_type = Column(Enum(QueryType), nullable=False)
    query_value = Column(String, nullable=False)
    status = Column(Enum(QueryStatus), default=QueryStatus.PENDING)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    priority = Column(Integer, default=1)  # 1=normal, 2=high, 3=urgent
    confidence_threshold = Column(Float, default=0.5)  # Minimum confidence to include results
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True))
    error_message = Column(Text)
    metadata = Column(JSON)  # Store additional query parameters
    
    # Relationships
    user = relationship("User", back_populates="queries")
    scan_results = relationship("ScanResult", back_populates="query", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="query", cascade="all, delete-orphan")


class ScanResult(Base):
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("queries.id"), nullable=False)
    scanner_type = Column(Enum(ScannerType), nullable=False)
    scanner_name = Column(String, nullable=False)  # Specific scanner instance
    status = Column(Enum(QueryStatus), default=QueryStatus.PENDING)
    confidence_score = Column(Float, default=0.0)  # 0.0 to 1.0
    relevance_score = Column(Float, default=0.0)  # How relevant to query
    data = Column(JSON)  # Raw scan data
    processed_data = Column(JSON)  # Normalized/processed data
    entities_found = Column(JSON)  # Extracted entities
    error_message = Column(Text)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    source_url = Column(String)  # URL of the source
    cost_credits = Column(Integer, default=1)  # Credits consumed
    
    # Relationships
    query = relationship("Query", back_populates="scan_results")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("queries.id"), nullable=False)
    report_type = Column(String, nullable=False)  # "preview" or "full"
    status = Column(Enum(QueryStatus), default=QueryStatus.PENDING)
    data = Column(JSON)  # Report content
    summary = Column(Text)  # Executive summary
    total_sources = Column(Integer, default=0)
    confidence_score = Column(Float, default=0.0)
    pdf_path = Column(String)  # Path to generated PDF
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))  # For temporary reports
    download_count = Column(Integer, default=0)
    
    # Relationships
    query = relationship("Query", back_populates="reports")


class Entity(Base):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String, nullable=False)  # person, organization, location, etc.
    name = Column(String, nullable=False)
    canonical_name = Column(String)  # Normalized name
    confidence_score = Column(Float, default=0.0)
    verification_status = Column(String, default="unverified")
    attributes = Column(JSON)  # Store entity attributes
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())
    source_count = Column(Integer, default=1)  # Number of sources confirming
    
    # Relationships
    relationships = relationship("EntityRelationship", foreign_keys="EntityRelationship.entity_id")


class EntityRelationship(Base):
    __tablename__ = "entity_relationships"

    id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    related_entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    relationship_type = Column(String, nullable=False)  # works_at, lives_in, owns, etc.
    confidence_score = Column(Float, default=0.0)
    verified = Column(Boolean, default=False)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    source_info = Column(JSON)  # Information about sources


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_name = Column(Enum(SubscriptionPlan), nullable=False)
    stripe_subscription_id = Column(String, unique=True)
    stripe_customer_id = Column(String)
    status = Column(String, nullable=False)  # active, inactive, cancelled, past_due
    current_period_start = Column(DateTime(timezone=True))
    current_period_end = Column(DateTime(timezone=True))
    trial_end = Column(DateTime(timezone=True))
    cancel_at_period_end = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    cancelled_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Integer, nullable=False)  # Amount in cents
    currency = Column(String, default="usd")
    stripe_payment_intent_id = Column(String, unique=True)
    status = Column(String, nullable=False)
    description = Column(String)
    invoice_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="payments")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String, nullable=False)
    resource_type = Column(String)
    resource_id = Column(String)
    ip_address = Column(String)
    user_agent = Column(String)
    metadata = Column(JSON)
    severity = Column(String, default="info")  # info, warning, error, critical
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ScannerConfig(Base):
    __tablename__ = "scanner_configs"

    id = Column(Integer, primary_key=True, index=True)
    scanner_type = Column(Enum(ScannerType), nullable=False)
    scanner_name = Column(String, nullable=False)
    is_enabled = Column(Boolean, default=True)
    config = Column(JSON)  # Scanner-specific configuration
    rate_limit = Column(Integer, default=100)  # Requests per hour
    priority = Column(Integer, default=1)  # Execution priority
    cost_per_request = Column(Integer, default=1)  # Credits per request
    success_rate = Column(Float, default=0.0)  # Historical success rate
    avg_response_time = Column(Float, default=0.0)  # Average response time
    last_health_check = Column(DateTime(timezone=True))
    health_status = Column(String, default="unknown")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ScannerMetrics(Base):
    __tablename__ = "scanner_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    scanner_name = Column(String, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    requests_made = Column(Integer, default=0)
    successful_requests = Column(Integer, default=0)
    failed_requests = Column(Integer, default=0)
    avg_response_time = Column(Float, default=0.0)
    total_credits_used = Column(Integer, default=0)
    avg_confidence_score = Column(Float, default=0.0)


class DataSource(Base):
    __tablename__ = "data_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    url = Column(String)
    api_endpoint = Column(String)
    source_type = Column(String, nullable=False)  # api, scraper, database
    reliability_score = Column(Float, default=0.5)
    last_successful_access = Column(DateTime(timezone=True))
    total_queries = Column(Integer, default=0)
    successful_queries = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())