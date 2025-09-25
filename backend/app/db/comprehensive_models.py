"""
Comprehensive Database Models for Enterprise Intelligence Platform
Merged from all existing versions and enhanced with ultimate features
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, JSON, ForeignKey, Index, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid

Base = declarative_base()

class UltimateUser(Base):
    """Ultimate user model with comprehensive enterprise features"""
    __tablename__ = "ultimate_users"
    
    # Core fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Enterprise user classification
    role = Column(String(50), nullable=False, default="FREE")  # FREE, PREMIUM, ADMIN, SUPER_ADMIN, FIELD_OPERATIVE, MISSION_CONTROL
    clearance_level = Column(Integer, default=1)  # 1-10 security clearance
    agent_classification = Column(String(100), default="civilian")  # civilian, operative, analyst, commander
    
    # Profile information
    first_name = Column(String(100))
    last_name = Column(String(100))
    organization = Column(String(200))
    department = Column(String(100))
    job_title = Column(String(100))
    
    # Subscription and billing
    subscription_plan = Column(String(50), default="reconnaissance")  # reconnaissance, tactical, strategic, classified, black_ops, quantum
    subscription_status = Column(String(20), default="active")
    subscription_expires = Column(DateTime)
    credits_available = Column(Integer, default=0)
    
    # Security and tracking
    last_login = Column(DateTime)
    login_attempts = Column(Integer, default=0)
    account_locked = Column(Boolean, default=False)
    mfa_enabled = Column(Boolean, default=False)
    mfa_secret = Column(String(32))
    
    # Advanced features
    api_key = Column(String(64), unique=True)
    rate_limit_tier = Column(String(20), default="standard")
    preferences = Column(JSONB, default={})
    user_metadata = Column(JSONB, default={})
    
    # Audit fields
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey('ultimate_users.id'))
    
    # Relationships
    operations = relationship("UltimateOperation", back_populates="agent")
    transactions = relationship("UltimateTransaction", back_populates="user")
    reports = relationship("UltimateIntelligenceReport", back_populates="requested_by_user")
    audit_logs = relationship("UltimateAuditLog", back_populates="user")

class UltimateOperation(Base):
    """Ultimate intelligence operation model with comprehensive tracking"""
    __tablename__ = "ultimate_operations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    operation_code = Column(String(50), unique=True, nullable=False)  # AUTO-GENERATED: INTEL-20240101-001
    
    # Operation details
    agent_id = Column(UUID(as_uuid=True), ForeignKey('ultimate_users.id'), nullable=False)
    operation_type = Column(String(50), nullable=False)  # email_intel, phone_intel, social_intel, etc.
    target_type = Column(String(50), nullable=False)  # phone, email, username, image, domain, blockchain, etc.
    target_value = Column(String(500), nullable=False)
    
    # Classification and priority
    classification_level = Column(String(30), default="unclassified")  # unclassified, confidential, secret, top_secret
    priority = Column(String(20), default="routine")  # routine, priority, immediate, flash
    urgency_score = Column(Integer, default=1)  # 1-10
    
    # Operation status
    status = Column(String(30), default="initiated")  # initiated, processing, analyzing, completed, failed
    progress_percentage = Column(Float, default=0.0)
    estimated_completion = Column(DateTime)
    
    # Results and intelligence
    data_sources_scanned = Column(Integer, default=0)
    intelligence_points_gathered = Column(Integer, default=0)
    confidence_score = Column(Float, default=0.0)  # 0-100%
    risk_assessment = Column(String(20), default="low")  # low, medium, high, critical
    
    # Advanced analytics
    correlation_matches = Column(Integer, default=0)
    pattern_detections = Column(Integer, default=0)
    behavioral_indicators = Column(JSONB, default={})
    geospatial_data = Column(JSONB, default={})
    temporal_analysis = Column(JSONB, default={})
    
    # Monetization
    tier_accessed = Column(String(20), default="free")  # free, basic, advanced, enterprise
    premium_unlocked = Column(Boolean, default=False)
    unlock_price = Column(Float)
    unlock_timestamp = Column(DateTime)
    
    # Results storage
    preview_results = Column(JSONB, default={})  # Free tier results
    full_results = Column(JSONB, default={})     # Premium results
    raw_data = Column(JSONB, default={})         # Raw intelligence data
    processed_intelligence = Column(JSONB, default={})  # AI-processed insights
    
    # Audit and tracking
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    agent = relationship("UltimateUser", back_populates="operations")
    reports = relationship("UltimateIntelligenceReport", back_populates="operation")
    transactions = relationship("UltimateTransaction", back_populates="operation")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_operation_agent_status', 'agent_id', 'status'),
        Index('idx_operation_type_date', 'operation_type', 'created_at'),
        Index('idx_operation_target', 'target_type', 'target_value'),
    )

class UltimateIntelligenceReport(Base):
    """Ultimate intelligence report with AI-enhanced analysis"""
    __tablename__ = "ultimate_intelligence_reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_number = Column(String(50), unique=True, nullable=False)  # RPT-20240101-001
    
    # Report metadata
    operation_id = Column(UUID(as_uuid=True), ForeignKey('ultimate_operations.id'), nullable=False)
    requested_by = Column(UUID(as_uuid=True), ForeignKey('ultimate_users.id'), nullable=False)
    report_type = Column(String(50), nullable=False)  # comprehensive, summary, threat_assessment
    classification = Column(String(30), default="unclassified")
    
    # Content and analysis
    executive_summary = Column(Text)
    detailed_findings = Column(JSONB, default={})
    intelligence_assessment = Column(JSONB, default={})
    threat_analysis = Column(JSONB, default={})
    recommendations = Column(JSONB, default={})
    
    # AI-enhanced features
    ai_insights = Column(JSONB, default={})
    predictive_analysis = Column(JSONB, default={})
    correlation_graph = Column(JSONB, default={})
    behavioral_profile = Column(JSONB, default={})
    risk_matrix = Column(JSONB, default={})
    
    # Visual analytics
    charts_data = Column(JSONB, default={})
    graphs_config = Column(JSONB, default={})
    maps_data = Column(JSONB, default={})
    timeline_data = Column(JSONB, default={})
    
    # Quality metrics
    confidence_score = Column(Float, default=0.0)
    reliability_rating = Column(String(20), default="unknown")
    data_freshness = Column(String(20), default="current")
    source_diversity = Column(Integer, default=0)
    
    # Delivery and access
    delivery_format = Column(String(20), default="json")  # json, pdf, csv, xml
    access_level = Column(String(20), default="standard")
    download_count = Column(Integer, default=0)
    last_accessed = Column(DateTime)
    
    # Audit
    generated_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    
    # Relationships
    operation = relationship("UltimateOperation", back_populates="reports")
    requested_by_user = relationship("UltimateUser", back_populates="reports")

class UltimateTransaction(Base):
    """Ultimate transaction model for comprehensive monetization"""
    __tablename__ = "ultimate_transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_id = Column(String(100), unique=True, nullable=False)
    
    # Transaction details
    user_id = Column(UUID(as_uuid=True), ForeignKey('ultimate_users.id'), nullable=False)
    operation_id = Column(UUID(as_uuid=True), ForeignKey('ultimate_operations.id'))
    
    # Payment information
    payment_type = Column(String(30), nullable=False)  # subscription, one_time, credits, upgrade
    payment_method = Column(String(30))  # stripe, paypal, crypto, credits
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    
    # Product details
    product_type = Column(String(50))  # basic_report, advanced_report, subscription_tactical, etc.
    product_tier = Column(String(30))  # free, basic, advanced, enterprise
    credits_purchased = Column(Integer, default=0)
    
    # Transaction status
    status = Column(String(20), default="pending")  # pending, completed, failed, refunded
    payment_processor_id = Column(String(100))
    payment_intent_id = Column(String(100))
    
    # Metadata
    transaction_metadata = Column(JSONB, default={})
    discount_applied = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    user = relationship("UltimateUser", back_populates="transactions")
    operation = relationship("UltimateOperation", back_populates="transactions")

class UltimateDataSourceRegistry(Base):
    """Registry of all 500+ intelligence data sources"""
    __tablename__ = "ultimate_data_sources"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(String(100), unique=True, nullable=False)
    
    # Source details
    name = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)  # email, phone, social, blockchain, etc.
    subcategory = Column(String(50))
    provider = Column(String(100))
    
    # Configuration
    endpoint_url = Column(String(500))
    api_key_required = Column(Boolean, default=False)
    rate_limit = Column(Integer, default=100)  # requests per minute
    cost_per_query = Column(Float, default=0.0)
    
    # Capabilities
    supported_queries = Column(JSONB, default={})
    data_types = Column(JSONB, default={})
    geographic_coverage = Column(JSONB, default={})
    
    # Quality metrics
    reliability_score = Column(Float, default=0.0)  # 0-100%
    accuracy_rating = Column(String(20), default="unknown")
    data_freshness = Column(String(20), default="unknown")
    update_frequency = Column(String(50))
    
    # Status and monitoring
    status = Column(String(20), default="active")  # active, inactive, maintenance, deprecated
    health_score = Column(Float, default=100.0)
    last_health_check = Column(DateTime)
    avg_response_time = Column(Float, default=0.0)  # milliseconds
    
    # Access control
    access_tier = Column(String(20), default="free")  # free, premium, enterprise
    clearance_required = Column(Integer, default=1)
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UltimateAIModelRegistry(Base):
    """Registry for AI models and correlation engines"""
    __tablename__ = "ultimate_ai_models"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id = Column(String(100), unique=True, nullable=False)
    
    # Model details
    name = Column(String(200), nullable=False)
    version = Column(String(20), nullable=False)
    model_type = Column(String(50))  # classification, correlation, prediction, nlp
    algorithm = Column(String(50))
    
    # Capabilities
    input_types = Column(JSONB, default={})
    output_types = Column(JSONB, default={})
    supported_operations = Column(JSONB, default={})
    
    # Performance metrics
    accuracy_score = Column(Float, default=0.0)
    precision = Column(Float, default=0.0)
    recall = Column(Float, default=0.0)
    f1_score = Column(Float, default=0.0)
    
    # Deployment info
    status = Column(String(20), default="active")
    endpoint_url = Column(String(500))
    compute_requirements = Column(JSONB, default={})
    
    # Usage tracking
    total_predictions = Column(Integer, default=0)
    avg_processing_time = Column(Float, default=0.0)
    
    # Audit
    deployed_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UltimateAuditLog(Base):
    """Comprehensive audit logging for compliance and security"""
    __tablename__ = "ultimate_audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Event details
    user_id = Column(UUID(as_uuid=True), ForeignKey('ultimate_users.id'))
    event_type = Column(String(100), nullable=False)  # login, search, purchase, admin_action
    event_category = Column(String(50))  # authentication, intelligence, financial, administrative
    
    # Event data
    resource_type = Column(String(50))  # user, operation, report, system
    resource_id = Column(String(100))
    action = Column(String(100), nullable=False)  # create, read, update, delete, execute
    
    # Context
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    session_id = Column(String(100))
    
    # Results
    status = Column(String(20))  # success, failure, warning
    error_code = Column(String(50))
    error_message = Column(Text)
    
    # Metadata
    audit_metadata = Column(JSONB, default={})
    security_classification = Column(String(30), default="unclassified")
    
    # Compliance
    gdpr_relevant = Column(Boolean, default=False)
    pci_relevant = Column(Boolean, default=False)
    sox_relevant = Column(Boolean, default=False)
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("UltimateUser", back_populates="audit_logs")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_audit_user_timestamp', 'user_id', 'timestamp'),
        Index('idx_audit_event_type', 'event_type', 'timestamp'),
        Index('idx_audit_resource', 'resource_type', 'resource_id'),
    )

class UltimateSystemMetrics(Base):
    """System metrics and performance monitoring"""
    __tablename__ = "ultimate_system_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Metric details
    metric_type = Column(String(50), nullable=False)  # performance, usage, revenue, security
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String(20))
    
    # Context
    component = Column(String(50))  # api, database, scanner, ai_engine
    instance_id = Column(String(100))
    
    # Aggregation
    aggregation_period = Column(String(20))  # minute, hour, day, week, month
    
    # Metadata
    metrics_metadata = Column(JSONB, default={})
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_metrics_type_time', 'metric_type', 'timestamp'),
        Index('idx_metrics_name_time', 'metric_name', 'timestamp'),
        Index('idx_metrics_component', 'component', 'timestamp'),
    )

# Create all tables
def create_tables(engine):
    """Create all database tables"""
    Base.metadata.create_all(engine)

# Export all models
__all__ = [
    'UltimateUser',
    'UltimateOperation', 
    'UltimateIntelligenceReport',
    'UltimateTransaction',
    'UltimateDataSourceRegistry',
    'UltimateAIModelRegistry',
    'UltimateAuditLog',
    'UltimateSystemMetrics',
    'Base',
    'create_tables'
]