"""
Enterprise Database Models
==========================

AAA-grade database models with:
- Proper relationships and constraints
- Audit trails and soft deletes
- Performance optimization
- Data integrity validation
- Enterprise security features
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from enum import Enum as PyEnum

try:
    from sqlalchemy import (
        Column, String, Integer, DateTime, Boolean, Text, JSON, 
        ForeignKey, Index, UniqueConstraint, CheckConstraint,
        Float, BigInteger, DECIMAL, func
    )
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship, Session
    from sqlalchemy.dialects.postgresql import UUID, JSONB
    from sqlalchemy.ext.hybrid import hybrid_property
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False
    declarative_base = lambda: object
    Column = String = Integer = DateTime = Boolean = Text = JSON = ForeignKey = relationship = None

# Base model with common fields
Base = declarative_base()


class TimestampMixin:
    """Mixin for created/updated timestamps"""
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), 
                       onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class SoftDeleteMixin:
    """Mixin for soft delete functionality"""
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    def soft_delete(self):
        """Mark record as deleted"""
        self.is_deleted = True
        self.deleted_at = datetime.now(timezone.utc)
    
    def restore(self):
        """Restore soft-deleted record"""
        self.is_deleted = False
        self.deleted_at = None


class AuditMixin:
    """Mixin for audit trail"""
    created_by = Column(UUID(as_uuid=True), nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    version = Column(Integer, default=1, nullable=False)


class UserPlanType(PyEnum):
    """User subscription plan types"""
    FREE = "free"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class QueryStatus(PyEnum):
    """Query execution status"""
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class ScannerStatus(PyEnum):
    """Individual scanner status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    RATE_LIMITED = "rate_limited"


class User(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """Enterprise user model with comprehensive features"""
    __tablename__ = "users"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic information
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=True, index=True)
    full_name = Column(String(255), nullable=True)
    
    # Authentication
    password_hash = Column(String(255), nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    email_verification_token = Column(String(255), nullable=True)
    password_reset_token = Column(String(255), nullable=True)
    password_reset_expires = Column(DateTime(timezone=True), nullable=True)
    
    # MFA
    mfa_enabled = Column(Boolean, default=False, nullable=False)
    mfa_secret = Column(String(32), nullable=True)
    backup_codes = Column(JSON, nullable=True)
    
    # Subscription and limits
    plan_type = Column(String(20), default=UserPlanType.FREE.value, nullable=False)
    subscription_id = Column(String(255), nullable=True)  # Stripe subscription ID
    subscription_status = Column(String(50), nullable=True)
    subscription_expires = Column(DateTime(timezone=True), nullable=True)
    
    # Usage tracking
    api_quota_limit = Column(Integer, default=100, nullable=False)
    api_quota_used = Column(Integer, default=0, nullable=False)
    api_quota_reset_date = Column(DateTime(timezone=True), nullable=True)
    credits_balance = Column(Integer, default=10, nullable=False)
    
    # Security and audit
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    last_login_ip = Column(String(45), nullable=True)  # IPv6 compatible
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    account_locked_until = Column(DateTime(timezone=True), nullable=True)
    
    # Preferences
    timezone = Column(String(50), default="UTC", nullable=False)
    language = Column(String(10), default="en", nullable=False)
    notification_preferences = Column(JSON, nullable=True)
    
    # Relationships
    queries = relationship("IntelligenceQuery", back_populates="user", lazy="dynamic")
    reports = relationship("Report", back_populates="user", lazy="dynamic")
    api_keys = relationship("APIKey", back_populates="user", lazy="dynamic")
    audit_logs = relationship("AuditLog", back_populates="user", lazy="dynamic")
    
    # Indexes and constraints
    __table_args__ = (
        Index('idx_user_email_active', 'email', postgresql_where=(~is_deleted)),
        Index('idx_user_plan_active', 'plan_type', postgresql_where=(~is_deleted)),
        Index('idx_user_created', 'created_at'),
        CheckConstraint('api_quota_used >= 0', name='check_api_quota_used_positive'),
        CheckConstraint('credits_balance >= 0', name='check_credits_balance_positive'),
    )
    
    @hybrid_property
    def is_premium(self) -> bool:
        """Check if user has premium plan"""
        return self.plan_type in [UserPlanType.PROFESSIONAL.value, UserPlanType.ENTERPRISE.value]
    
    @hybrid_property
    def is_account_locked(self) -> bool:
        """Check if account is locked"""
        if self.account_locked_until is None:
            return False
        return datetime.now(timezone.utc) < self.account_locked_until
    
    def can_perform_query(self, cost: int = 1) -> bool:
        """Check if user can perform a query based on quota and credits"""
        if self.is_account_locked:
            return False
        return (self.api_quota_used < self.api_quota_limit and 
                self.credits_balance >= cost)
    
    def consume_quota(self, amount: int = 1, cost: int = 1):
        """Consume API quota and credits"""
        self.api_quota_used += amount
        self.credits_balance -= cost
    
    def reset_quota(self):
        """Reset API quota (called periodically)"""
        self.api_quota_used = 0
        self.api_quota_reset_date = datetime.now(timezone.utc)


class IntelligenceQuery(Base, TimestampMixin, SoftDeleteMixin):
    """Intelligence gathering query model"""
    __tablename__ = "intelligence_queries"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # User association
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Query details
    query_type = Column(String(50), nullable=False, index=True)  # email, phone, name, etc.
    target = Column(String(500), nullable=False)
    target_hash = Column(String(64), nullable=False, index=True)  # For deduplication
    
    # Execution details
    status = Column(String(20), default=QueryStatus.PENDING.value, nullable=False, index=True)
    priority = Column(String(20), default="normal", nullable=False)
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    execution_time_seconds = Column(Float, nullable=True)
    
    # Configuration
    scanner_selection = Column(JSON, nullable=True)  # Specific scanners requested
    scan_categories = Column(JSON, nullable=True)   # Scanner categories
    scan_config = Column(JSON, nullable=True)       # Additional scan configuration
    
    # Results summary
    total_scanners = Column(Integer, default=0, nullable=False)
    completed_scanners = Column(Integer, default=0, nullable=False)
    failed_scanners = Column(Integer, default=0, nullable=False)
    success_rate = Column(Float, nullable=True)
    
    # Cost and usage
    estimated_cost = Column(Integer, default=1, nullable=False)
    actual_cost = Column(Integer, nullable=True)
    
    # Error handling
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0, nullable=False)
    max_retries = Column(Integer, default=3, nullable=False)
    
    # Metadata
    metadata = Column(JSON, nullable=True)
    tags = Column(JSON, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="queries")
    scan_results = relationship("ScanResult", back_populates="query", lazy="dynamic")
    reports = relationship("Report", back_populates="query", lazy="dynamic")
    
    # Indexes and constraints
    __table_args__ = (
        Index('idx_query_user_status', 'user_id', 'status'),
        Index('idx_query_type_status', 'query_type', 'status'),
        Index('idx_query_target_hash', 'target_hash'),
        Index('idx_query_created', 'created_at'),
        Index('idx_query_scheduled', 'scheduled_at'),
        UniqueConstraint('user_id', 'target_hash', 'query_type', name='uq_user_target_type'),
    )
    
    @hybrid_property
    def is_completed(self) -> bool:
        """Check if query is completed"""
        return self.status in [QueryStatus.COMPLETED.value, QueryStatus.FAILED.value, 
                              QueryStatus.CANCELLED.value, QueryStatus.TIMEOUT.value]
    
    @hybrid_property
    def progress_percentage(self) -> float:
        """Calculate completion percentage"""
        if self.total_scanners == 0:
            return 0.0
        return (self.completed_scanners + self.failed_scanners) / self.total_scanners * 100
    
    def mark_started(self):
        """Mark query as started"""
        self.status = QueryStatus.RUNNING.value
        self.started_at = datetime.now(timezone.utc)
    
    def mark_completed(self, success: bool = True):
        """Mark query as completed"""
        self.status = QueryStatus.COMPLETED.value if success else QueryStatus.FAILED.value
        self.completed_at = datetime.now(timezone.utc)
        if self.started_at:
            delta = self.completed_at - self.started_at
            self.execution_time_seconds = delta.total_seconds()


class ScanResult(Base, TimestampMixin):
    """Individual scanner result model"""
    __tablename__ = "scan_results"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Query association
    query_id = Column(UUID(as_uuid=True), ForeignKey("intelligence_queries.id"), nullable=False, index=True)
    
    # Scanner details
    scanner_name = Column(String(100), nullable=False, index=True)
    scanner_category = Column(String(50), nullable=False, index=True)
    scanner_version = Column(String(20), nullable=True)
    
    # Execution details
    status = Column(String(20), nullable=False, index=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    execution_time_seconds = Column(Float, nullable=True)
    
    # Results
    data = Column(JSONB, nullable=True)  # PostgreSQL JSONB for better performance
    raw_data = Column(JSONB, nullable=True)  # Unprocessed scanner output
    confidence_score = Column(Float, nullable=True)
    risk_score = Column(Float, nullable=True)
    
    # Error handling
    error_message = Column(Text, nullable=True)
    error_code = Column(String(50), nullable=True)
    retry_count = Column(Integer, default=0, nullable=False)
    
    # Performance metrics
    api_calls_made = Column(Integer, default=0, nullable=False)
    data_points_found = Column(Integer, default=0, nullable=False)
    cost_credits = Column(Integer, default=1, nullable=False)
    
    # Metadata
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    query = relationship("IntelligenceQuery", back_populates="scan_results")
    
    # Indexes and constraints
    __table_args__ = (
        Index('idx_scan_result_query_scanner', 'query_id', 'scanner_name'),
        Index('idx_scan_result_status', 'status'),
        Index('idx_scan_result_category', 'scanner_category'),
        Index('idx_scan_result_created', 'created_at'),
        # GIN index for JSONB data searching
        Index('idx_scan_result_data_gin', 'data', postgresql_using='gin'),
    )
    
    def mark_started(self):
        """Mark scan as started"""
        self.status = ScannerStatus.RUNNING.value
        self.started_at = datetime.now(timezone.utc)
    
    def mark_completed(self, data: Dict[str, Any], confidence: float = None):
        """Mark scan as completed with data"""
        self.status = ScannerStatus.COMPLETED.value
        self.completed_at = datetime.now(timezone.utc)
        self.data = data
        self.confidence_score = confidence
        if self.started_at:
            delta = self.completed_at - self.started_at
            self.execution_time_seconds = delta.total_seconds()
    
    def mark_failed(self, error: str, error_code: str = None):
        """Mark scan as failed"""
        self.status = ScannerStatus.FAILED.value
        self.completed_at = datetime.now(timezone.utc)
        self.error_message = error
        self.error_code = error_code


class Report(Base, TimestampMixin, SoftDeleteMixin):
    """Report generation model"""
    __tablename__ = "reports"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Associations
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    query_id = Column(UUID(as_uuid=True), ForeignKey("intelligence_queries.id"), nullable=False, index=True)
    
    # Report details
    title = Column(String(255), nullable=False)
    report_type = Column(String(50), nullable=False)  # summary, detailed, custom
    format = Column(String(20), nullable=False)  # pdf, html, json, csv
    status = Column(String(20), default="pending", nullable=False, index=True)
    
    # Generation details
    generated_at = Column(DateTime(timezone=True), nullable=True)
    generation_time_seconds = Column(Float, nullable=True)
    file_size_bytes = Column(BigInteger, nullable=True)
    file_path = Column(String(500), nullable=True)
    download_url = Column(String(500), nullable=True)
    
    # Configuration
    include_raw_data = Column(Boolean, default=False, nullable=False)
    custom_sections = Column(JSON, nullable=True)
    template_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Access control
    is_public = Column(Boolean, default=False, nullable=False)
    access_token = Column(String(255), nullable=True)  # For secure sharing
    download_count = Column(Integer, default=0, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Metadata
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="reports")
    query = relationship("IntelligenceQuery", back_populates="reports")
    
    # Indexes and constraints
    __table_args__ = (
        Index('idx_report_user_created', 'user_id', 'created_at'),
        Index('idx_report_query', 'query_id'),
        Index('idx_report_status', 'status'),
        Index('idx_report_format', 'format'),
    )
    
    @hybrid_property
    def is_expired(self) -> bool:
        """Check if report has expired"""
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at
    
    def generate_access_token(self) -> str:
        """Generate secure access token for sharing"""
        self.access_token = str(uuid.uuid4())
        return self.access_token


class APIKey(Base, TimestampMixin, SoftDeleteMixin):
    """API key management model"""
    __tablename__ = "api_keys"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # User association
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Key details
    name = Column(String(100), nullable=False)
    key_hash = Column(String(255), nullable=False, unique=True, index=True)
    key_prefix = Column(String(10), nullable=False)  # For identification
    
    # Permissions and limits
    scopes = Column(JSON, nullable=True)  # Allowed endpoints/actions
    rate_limit_per_minute = Column(Integer, default=60, nullable=False)
    daily_quota = Column(Integer, default=1000, nullable=False)
    
    # Usage tracking
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    last_used_ip = Column(String(45), nullable=True)
    total_requests = Column(BigInteger, default=0, nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="api_keys")
    
    # Indexes and constraints
    __table_args__ = (
        Index('idx_api_key_user_active', 'user_id', 'is_active'),
        Index('idx_api_key_hash', 'key_hash'),
        Index('idx_api_key_last_used', 'last_used_at'),
    )
    
    @hybrid_property
    def is_expired(self) -> bool:
        """Check if API key has expired"""
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at
    
    def record_usage(self, ip_address: str = None):
        """Record API key usage"""
        self.last_used_at = datetime.now(timezone.utc)
        self.last_used_ip = ip_address
        self.total_requests += 1


class AuditLog(Base, TimestampMixin):
    """Comprehensive audit log model"""
    __tablename__ = "audit_logs"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # User association (nullable for system events)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    
    # Event details
    event_type = Column(String(50), nullable=False, index=True)
    event_category = Column(String(50), nullable=False, index=True)
    event_description = Column(Text, nullable=False)
    
    # Context
    resource_type = Column(String(50), nullable=True)
    resource_id = Column(UUID(as_uuid=True), nullable=True)
    action = Column(String(50), nullable=True)
    
    # Request context
    ip_address = Column(String(45), nullable=True, index=True)
    user_agent = Column(Text, nullable=True)
    request_id = Column(String(36), nullable=True, index=True)
    session_id = Column(String(36), nullable=True)
    
    # Additional data
    metadata = Column(JSON, nullable=True)
    severity = Column(String(20), default="info", nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    
    # Indexes and constraints
    __table_args__ = (
        Index('idx_audit_log_event_type', 'event_type'),
        Index('idx_audit_log_user_created', 'user_id', 'created_at'),
        Index('idx_audit_log_ip_created', 'ip_address', 'created_at'),
        Index('idx_audit_log_severity', 'severity'),
        Index('idx_audit_log_created', 'created_at'),
    )


# Database utilities
def create_all_tables(engine):
    """Create all tables"""
    if SQLALCHEMY_AVAILABLE:
        Base.metadata.create_all(bind=engine)


def get_model_by_name(name: str):
    """Get model class by name"""
    models = {
        'User': User,
        'IntelligenceQuery': IntelligenceQuery,
        'ScanResult': ScanResult,
        'Report': Report,
        'APIKey': APIKey,
        'AuditLog': AuditLog
    }
    return models.get(name)