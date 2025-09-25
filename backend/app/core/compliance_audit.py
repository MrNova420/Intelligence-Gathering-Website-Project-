"""
Advanced Compliance and Audit System
====================================

Enterprise-grade compliance monitoring and audit logging system providing:
- GDPR, CCPA, HIPAA compliance monitoring
- Comprehensive audit logging with tamper protection
- Automated compliance reporting
- Data retention and privacy controls
- Security incident tracking and response
- User consent and preference management
"""

import asyncio
import logging
import json
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict, field
from enum import Enum
import uuid
import time
from collections import defaultdict
import sqlite3
import os

logger = logging.getLogger(__name__)

# Compliance Standards
class ComplianceStandard(str, Enum):
    GDPR = "gdpr"
    CCPA = "ccpa"
    HIPAA = "hipaa"
    SOC2 = "soc2"
    ISO27001 = "iso27001"
    PCI_DSS = "pci_dss"

# Event Types for Audit Logging
class AuditEventType(str, Enum):
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    DATA_ACCESS = "data_access"
    DATA_MODIFICATION = "data_modification"
    DATA_DELETION = "data_deletion"
    DATA_EXPORT = "data_export"
    SCAN_INITIATED = "scan_initiated"
    SCAN_COMPLETED = "scan_completed"
    REPORT_GENERATED = "report_generated"
    ADMIN_ACTION = "admin_action"
    SECURITY_INCIDENT = "security_incident"
    PRIVACY_REQUEST = "privacy_request"
    CONSENT_GIVEN = "consent_given"
    CONSENT_WITHDRAWN = "consent_withdrawn"

# Risk Levels
class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# Privacy Rights under GDPR/CCPA
class PrivacyRight(str, Enum):
    ACCESS = "access"
    RECTIFICATION = "rectification"
    ERASURE = "erasure"
    PORTABILITY = "portability"
    RESTRICTION = "restriction"
    OBJECTION = "objection"
    OPT_OUT = "opt_out"


@dataclass
class AuditLogEntry:
    """Comprehensive audit log entry with integrity protection"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    event_type: AuditEventType = AuditEventType.DATA_ACCESS
    user_id: Optional[str] = None
    user_ip: Optional[str] = None
    user_agent: Optional[str] = None
    resource: Optional[str] = None
    action: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    risk_level: RiskLevel = RiskLevel.LOW
    compliance_relevant: List[ComplianceStandard] = field(default_factory=list)
    hash_signature: Optional[str] = None
    
    def calculate_hash(self, secret_key: str) -> str:
        """Calculate tamper-proof hash for audit log integrity"""
        data = f"{self.id}{self.timestamp.isoformat()}{self.event_type}{self.user_id}{self.action}"
        return hmac.new(secret_key.encode(), data.encode(), hashlib.sha256).hexdigest()
    
    def sign(self, secret_key: str):
        """Sign the audit log entry"""
        self.hash_signature = self.calculate_hash(secret_key)
    
    def verify(self, secret_key: str) -> bool:
        """Verify audit log integrity"""
        if not self.hash_signature:
            return False
        return self.hash_signature == self.calculate_hash(secret_key)


@dataclass
class ComplianceRule:
    """Compliance rule definition"""
    id: str
    standard: ComplianceStandard
    rule_code: str
    description: str
    risk_level: RiskLevel
    automated_check: bool = True
    remediation_steps: List[str] = field(default_factory=list)


@dataclass
class PrivacyRequest:
    """Privacy rights request tracking"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ""
    user_email: str = ""
    request_type: PrivacyRight = PrivacyRight.ACCESS
    status: str = "pending"  # pending, processing, completed, rejected
    submitted_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    details: Dict[str, Any] = field(default_factory=dict)
    verification_token: str = field(default_factory=lambda: secrets.token_urlsafe(32))


@dataclass
class UserConsent:
    """User consent tracking for privacy compliance"""
    user_id: str
    consent_type: str  # data_processing, marketing, analytics, etc.
    granted: bool
    timestamp: datetime = field(default_factory=datetime.utcnow)
    consent_text: str = ""
    ip_address: Optional[str] = None
    version: str = "1.0"


class ComplianceAuditSystem:
    """Advanced compliance and audit system"""
    
    def __init__(self):
        self.audit_secret = os.getenv("AUDIT_SECRET_KEY", secrets.token_urlsafe(32))
        self.db_path = "data/compliance_audit.db"
        
        # Initialize compliance rules
        self.compliance_rules = self._initialize_compliance_rules()
        self.privacy_requests = {}
        self.user_consents = defaultdict(dict)
        
        # Initialize database
        self._initialize_database()
        
        # Performance tracking
        self._audit_buffer = []
        self._buffer_size = 100
        
        logger.info("🔒 Compliance and Audit System initialized")
    
    def _initialize_database(self):
        """Initialize SQLite database for audit logs"""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Audit logs table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS audit_logs (
                        id TEXT PRIMARY KEY,
                        timestamp TEXT NOT NULL,
                        event_type TEXT NOT NULL,
                        user_id TEXT,
                        user_ip TEXT,
                        user_agent TEXT,
                        resource TEXT,
                        action TEXT NOT NULL,
                        details TEXT,
                        risk_level TEXT NOT NULL,
                        compliance_relevant TEXT,
                        hash_signature TEXT NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Privacy requests table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS privacy_requests (
                        id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        user_email TEXT NOT NULL,
                        request_type TEXT NOT NULL,
                        status TEXT NOT NULL,
                        submitted_at TEXT NOT NULL,
                        completed_at TEXT,
                        details TEXT,
                        verification_token TEXT NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # User consents table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_consents (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        consent_type TEXT NOT NULL,
                        granted BOOLEAN NOT NULL,
                        timestamp TEXT NOT NULL,
                        consent_text TEXT,
                        ip_address TEXT,
                        version TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create indexes for performance
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_logs(user_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_event_type ON audit_logs(event_type)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_privacy_user ON privacy_requests(user_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_consent_user ON user_consents(user_id)")
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
    
    def _initialize_compliance_rules(self) -> List[ComplianceRule]:
        """Initialize compliance rules for different standards"""
        return [
            # GDPR Rules
            ComplianceRule(
                id="gdpr_data_minimization",
                standard=ComplianceStandard.GDPR,
                rule_code="GDPR-5.1(c)",
                description="Data must be adequate, relevant and limited to what is necessary",
                risk_level=RiskLevel.HIGH,
                remediation_steps=[
                    "Review data collection practices",
                    "Eliminate unnecessary data fields",
                    "Implement data retention policies"
                ]
            ),
            ComplianceRule(
                id="gdpr_consent_required",
                standard=ComplianceStandard.GDPR,
                rule_code="GDPR-6.1(a)",
                description="Processing requires valid consent from data subject",
                risk_level=RiskLevel.CRITICAL,
                remediation_steps=[
                    "Obtain explicit consent",
                    "Document consent mechanism",
                    "Provide easy withdrawal option"
                ]
            ),
            ComplianceRule(
                id="gdpr_breach_notification",
                standard=ComplianceStandard.GDPR,
                rule_code="GDPR-33",
                description="Data breach must be reported within 72 hours",
                risk_level=RiskLevel.CRITICAL,
                remediation_steps=[
                    "Implement breach detection",
                    "Create notification procedures",
                    "Train incident response team"
                ]
            ),
            
            # CCPA Rules
            ComplianceRule(
                id="ccpa_disclosure_required",
                standard=ComplianceStandard.CCPA,
                rule_code="CCPA-1798.100(b)",
                description="Business must disclose categories of personal information collected",
                risk_level=RiskLevel.MEDIUM,
                remediation_steps=[
                    "Create privacy policy disclosure",
                    "List all data categories",
                    "Update disclosure annually"
                ]
            ),
            ComplianceRule(
                id="ccpa_opt_out_right",
                standard=ComplianceStandard.CCPA,
                rule_code="CCPA-1798.120",
                description="Consumers have right to opt-out of sale of personal information",
                risk_level=RiskLevel.HIGH,
                remediation_steps=[
                    "Implement 'Do Not Sell' link",
                    "Create opt-out mechanism",
                    "Honor opt-out requests"
                ]
            ),
            
            # SOC 2 Rules
            ComplianceRule(
                id="soc2_access_control",
                standard=ComplianceStandard.SOC2,
                rule_code="CC6.1",
                description="Access to data and systems requires authentication",
                risk_level=RiskLevel.HIGH,
                remediation_steps=[
                    "Implement strong authentication",
                    "Enable multi-factor authentication",
                    "Regular access reviews"
                ]
            )
        ]
    
    async def log_audit_event(self, event: AuditLogEntry, context: Optional[Dict[str, Any]] = None):
        """Log audit event with compliance checking"""
        try:
            # Add context if provided
            if context:
                event.details.update(context)
            
            # Determine compliance relevance
            event.compliance_relevant = self._determine_compliance_relevance(event)
            
            # Sign the audit entry
            event.sign(self.audit_secret)
            
            # Add to buffer
            self._audit_buffer.append(event)
            
            # Flush buffer if full
            if len(self._audit_buffer) >= self._buffer_size:
                await self._flush_audit_buffer()
            
            # Check for high-risk events
            if event.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                await self._handle_high_risk_event(event)
            
            logger.debug(f"Audit event logged: {event.event_type} for user {event.user_id}")
            
        except Exception as e:
            logger.error(f"Audit logging error: {e}")
    
    async def _flush_audit_buffer(self):
        """Flush audit buffer to database"""
        if not self._audit_buffer:
            return
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for entry in self._audit_buffer:
                    cursor.execute("""
                        INSERT INTO audit_logs 
                        (id, timestamp, event_type, user_id, user_ip, user_agent, resource, 
                         action, details, risk_level, compliance_relevant, hash_signature)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        entry.id,
                        entry.timestamp.isoformat(),
                        entry.event_type.value,
                        entry.user_id,
                        entry.user_ip,
                        entry.user_agent,
                        entry.resource,
                        entry.action,
                        json.dumps(entry.details),
                        entry.risk_level.value,
                        json.dumps([s.value for s in entry.compliance_relevant]),
                        entry.hash_signature
                    ))
                
                conn.commit()
                self._audit_buffer.clear()
                
        except Exception as e:
            logger.error(f"Audit buffer flush error: {e}")
    
    def _determine_compliance_relevance(self, event: AuditLogEntry) -> List[ComplianceStandard]:
        """Determine which compliance standards are relevant for this event"""
        relevant = []
        
        # GDPR relevance
        if event.event_type in [AuditEventType.DATA_ACCESS, AuditEventType.DATA_MODIFICATION, 
                               AuditEventType.DATA_DELETION, AuditEventType.DATA_EXPORT,
                               AuditEventType.CONSENT_GIVEN, AuditEventType.CONSENT_WITHDRAWN]:
            relevant.append(ComplianceStandard.GDPR)
        
        # CCPA relevance
        if event.event_type in [AuditEventType.DATA_ACCESS, AuditEventType.DATA_EXPORT,
                               AuditEventType.PRIVACY_REQUEST]:
            relevant.append(ComplianceStandard.CCPA)
        
        # SOC 2 relevance
        if event.event_type in [AuditEventType.USER_LOGIN, AuditEventType.ADMIN_ACTION,
                               AuditEventType.SECURITY_INCIDENT]:
            relevant.append(ComplianceStandard.SOC2)
        
        return relevant
    
    async def _handle_high_risk_event(self, event: AuditLogEntry):
        """Handle high-risk audit events with immediate processing"""
        try:
            # Immediate database write for high-risk events
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO audit_logs 
                    (id, timestamp, event_type, user_id, user_ip, user_agent, resource, 
                     action, details, risk_level, compliance_relevant, hash_signature)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    event.id,
                    event.timestamp.isoformat(),
                    event.event_type.value,
                    event.user_id,
                    event.user_ip,
                    event.user_agent,
                    event.resource,
                    event.action,
                    json.dumps(event.details),
                    event.risk_level.value,
                    json.dumps([s.value for s in event.compliance_relevant]),
                    event.hash_signature
                ))
                conn.commit()
            
            # Alert handling (would integrate with monitoring system)
            logger.warning(f"High-risk audit event: {event.event_type} - {event.action}")
            
        except Exception as e:
            logger.error(f"High-risk event handling error: {e}")
    
    async def create_privacy_request(self, user_id: str, user_email: str, 
                                   request_type: PrivacyRight, details: Dict[str, Any] = None) -> str:
        """Create a privacy rights request"""
        try:
            request = PrivacyRequest(
                user_id=user_id,
                user_email=user_email,
                request_type=request_type,
                details=details or {}
            )
            
            # Store in database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO privacy_requests 
                    (id, user_id, user_email, request_type, status, submitted_at, details, verification_token)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    request.id,
                    request.user_id,
                    request.user_email,
                    request.request_type.value,
                    request.status,
                    request.submitted_at.isoformat(),
                    json.dumps(request.details),
                    request.verification_token
                ))
                conn.commit()
            
            # Log the privacy request
            await self.log_audit_event(AuditLogEntry(
                event_type=AuditEventType.PRIVACY_REQUEST,
                user_id=user_id,
                action=f"Privacy request created: {request_type.value}",
                details={"request_id": request.id},
                risk_level=RiskLevel.MEDIUM
            ))
            
            self.privacy_requests[request.id] = request
            logger.info(f"Privacy request created: {request.id} for user {user_id}")
            
            return request.id
            
        except Exception as e:
            logger.error(f"Privacy request creation error: {e}")
            raise
    
    async def record_user_consent(self, user_id: str, consent_type: str, granted: bool, 
                                 consent_text: str = "", ip_address: str = None, version: str = "1.0"):
        """Record user consent for compliance tracking"""
        try:
            consent = UserConsent(
                user_id=user_id,
                consent_type=consent_type,
                granted=granted,
                consent_text=consent_text,
                ip_address=ip_address,
                version=version
            )
            
            # Store in database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO user_consents 
                    (user_id, consent_type, granted, timestamp, consent_text, ip_address, version)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    consent.user_id,
                    consent.consent_type,
                    consent.granted,
                    consent.timestamp.isoformat(),
                    consent.consent_text,
                    consent.ip_address,
                    consent.version
                ))
                conn.commit()
            
            # Update memory store
            self.user_consents[user_id][consent_type] = consent
            
            # Log consent event
            await self.log_audit_event(AuditLogEntry(
                event_type=AuditEventType.CONSENT_GIVEN if granted else AuditEventType.CONSENT_WITHDRAWN,
                user_id=user_id,
                action=f"Consent {'granted' if granted else 'withdrawn'} for {consent_type}",
                details={"consent_type": consent_type, "version": version},
                risk_level=RiskLevel.LOW
            ))
            
            logger.info(f"User consent recorded: {user_id} - {consent_type}: {granted}")
            
        except Exception as e:
            logger.error(f"Consent recording error: {e}")
    
    async def generate_compliance_report(self, standard: ComplianceStandard, 
                                       start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Generate comprehensive compliance report"""
        try:
            report = {
                "standard": standard.value,
                "period": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat()
                },
                "generated_at": datetime.utcnow().isoformat(),
                "summary": {},
                "audit_events": [],
                "privacy_requests": [],
                "consent_records": [],
                "compliance_violations": [],
                "recommendations": []
            }
            
            # Get relevant audit events
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Audit events
                cursor.execute("""
                    SELECT * FROM audit_logs 
                    WHERE timestamp BETWEEN ? AND ? 
                    AND compliance_relevant LIKE ?
                    ORDER BY timestamp DESC
                """, (start_date.isoformat(), end_date.isoformat(), f'%{standard.value}%'))
                
                audit_events = cursor.fetchall()
                report["audit_events"] = [dict(zip([col[0] for col in cursor.description], row)) 
                                        for row in audit_events]
                
                # Privacy requests
                cursor.execute("""
                    SELECT * FROM privacy_requests 
                    WHERE submitted_at BETWEEN ? AND ?
                    ORDER BY submitted_at DESC
                """, (start_date.isoformat(), end_date.isoformat()))
                
                privacy_requests = cursor.fetchall()
                report["privacy_requests"] = [dict(zip([col[0] for col in cursor.description], row)) 
                                            for row in privacy_requests]
                
                # Consent records
                cursor.execute("""
                    SELECT * FROM user_consents 
                    WHERE timestamp BETWEEN ? AND ?
                    ORDER BY timestamp DESC
                """, (start_date.isoformat(), end_date.isoformat()))
                
                consent_records = cursor.fetchall()
                report["consent_records"] = [dict(zip([col[0] for col in cursor.description], row)) 
                                           for row in consent_records]
            
            # Generate summary statistics
            report["summary"] = {
                "total_audit_events": len(report["audit_events"]),
                "high_risk_events": len([e for e in report["audit_events"] if e["risk_level"] in ["high", "critical"]]),
                "privacy_requests": len(report["privacy_requests"]),
                "consent_granted": len([c for c in report["consent_records"] if c["granted"]]),
                "consent_withdrawn": len([c for c in report["consent_records"] if not c["granted"]])
            }
            
            # Check for compliance violations
            report["compliance_violations"] = await self._check_compliance_violations(
                standard, report["audit_events"], report["privacy_requests"]
            )
            
            # Generate recommendations
            report["recommendations"] = self._generate_compliance_recommendations(
                standard, report["summary"], report["compliance_violations"]
            )
            
            logger.info(f"Compliance report generated for {standard.value}: {len(report['audit_events'])} events")
            return report
            
        except Exception as e:
            logger.error(f"Compliance report generation error: {e}")
            return {"error": str(e)}
    
    async def _check_compliance_violations(self, standard: ComplianceStandard, 
                                         audit_events: List[Dict], privacy_requests: List[Dict]) -> List[Dict]:
        """Check for compliance violations based on audit data"""
        violations = []
        
        try:
            if standard == ComplianceStandard.GDPR:
                # Check for privacy request response times
                for request in privacy_requests:
                    submitted = datetime.fromisoformat(request["submitted_at"])
                    if request["status"] == "pending" and (datetime.utcnow() - submitted).days > 30:
                        violations.append({
                            "rule": "GDPR-12",
                            "description": "Privacy request not responded to within 30 days",
                            "severity": "high",
                            "details": {"request_id": request["id"], "days_pending": (datetime.utcnow() - submitted).days}
                        })
                
                # Check for data breach notification timing
                breach_events = [e for e in audit_events if e["event_type"] == "security_incident"]
                for breach in breach_events:
                    event_time = datetime.fromisoformat(breach["timestamp"])
                    # Check if reported within 72 hours (simplified check)
                    if (datetime.utcnow() - event_time).total_seconds() > 72 * 3600:
                        violations.append({
                            "rule": "GDPR-33",
                            "description": "Data breach not reported within 72 hours",
                            "severity": "critical",
                            "details": {"event_id": breach["id"]}
                        })
            
            elif standard == ComplianceStandard.SOC2:
                # Check for failed login attempts
                failed_logins = [e for e in audit_events if e["event_type"] == "user_login" and "failed" in e.get("details", "")]
                if len(failed_logins) > 100:  # Threshold for concern
                    violations.append({
                        "rule": "CC6.1",
                        "description": "Excessive failed login attempts detected",
                        "severity": "medium",
                        "details": {"failed_attempts": len(failed_logins)}
                    })
            
        except Exception as e:
            logger.error(f"Compliance violation check error: {e}")
        
        return violations
    
    def _generate_compliance_recommendations(self, standard: ComplianceStandard, 
                                           summary: Dict, violations: List[Dict]) -> List[Dict]:
        """Generate compliance recommendations based on analysis"""
        recommendations = []
        
        try:
            # General recommendations based on violations
            for violation in violations:
                if violation["severity"] == "critical":
                    recommendations.append({
                        "priority": "high",
                        "category": "violation_remediation",
                        "title": f"Address {violation['rule']} violation",
                        "description": violation["description"],
                        "actions": ["Immediate investigation required", "Implement corrective measures", "Document remediation"]
                    })
            
            # Standard-specific recommendations
            if standard == ComplianceStandard.GDPR:
                if summary["privacy_requests"] > 0:
                    recommendations.append({
                        "priority": "medium",
                        "category": "process_improvement",
                        "title": "Automate privacy request processing",
                        "description": "Consider implementing automated data extraction for privacy requests",
                        "actions": ["Develop data export automation", "Create user self-service portal", "Implement request tracking"]
                    })
                
                if summary["consent_withdrawn"] > summary["consent_granted"] * 0.1:  # >10% withdrawal rate
                    recommendations.append({
                        "priority": "medium",
                        "category": "user_experience",
                        "title": "Review consent mechanisms",
                        "description": "High consent withdrawal rate may indicate UX issues",
                        "actions": ["Review consent language", "Simplify consent process", "Provide granular controls"]
                    })
            
        except Exception as e:
            logger.error(f"Recommendation generation error: {e}")
        
        return recommendations
    
    async def get_user_data_summary(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive summary of user data for privacy compliance"""
        try:
            summary = {
                "user_id": user_id,
                "generated_at": datetime.utcnow().isoformat(),
                "data_categories": [],
                "processing_activities": [],
                "consent_status": {},
                "privacy_requests": [],
                "data_retention": {}
            }
            
            # Get user's audit events
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Privacy requests
                cursor.execute("SELECT * FROM privacy_requests WHERE user_id = ?", (user_id,))
                requests = cursor.fetchall()
                summary["privacy_requests"] = [dict(zip([col[0] for col in cursor.description], row)) 
                                             for row in requests]
                
                # Consent records
                cursor.execute("SELECT * FROM user_consents WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
                consents = cursor.fetchall()
                
                # Build consent status
                for consent_row in consents:
                    consent_type = consent_row[2]  # consent_type column
                    if consent_type not in summary["consent_status"]:
                        summary["consent_status"][consent_type] = {
                            "current_status": consent_row[3],  # granted column
                            "last_updated": consent_row[4],    # timestamp column
                            "version": consent_row[7]          # version column
                        }
            
            logger.info(f"User data summary generated for {user_id}")
            return summary
            
        except Exception as e:
            logger.error(f"User data summary error: {e}")
            return {"error": str(e)}
    
    async def cleanup_expired_data(self):
        """Clean up expired audit logs and data according to retention policies"""
        try:
            # Default retention periods (can be configured)
            retention_periods = {
                "audit_logs": 2555,  # 7 years for financial/legal compliance
                "privacy_requests": 1095,  # 3 years
                "user_consents": 2555  # 7 years
            }
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                deleted_counts = {}
                
                for table, days in retention_periods.items():
                    cutoff_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
                    
                    if table == "audit_logs":
                        cursor.execute("DELETE FROM audit_logs WHERE timestamp < ?", (cutoff_date,))
                    elif table == "privacy_requests":
                        cursor.execute("DELETE FROM privacy_requests WHERE submitted_at < ?", (cutoff_date,))
                    elif table == "user_consents":
                        cursor.execute("DELETE FROM user_consents WHERE timestamp < ?", (cutoff_date,))
                    
                    deleted_counts[table] = cursor.rowcount
                
                conn.commit()
                
            logger.info(f"Data cleanup completed: {deleted_counts}")
            return deleted_counts
            
        except Exception as e:
            logger.error(f"Data cleanup error: {e}")
            return {"error": str(e)}


# Global compliance system instance
compliance_audit_system = ComplianceAuditSystem()

# Convenience functions for easy integration
async def log_user_action(user_id: str, action: str, resource: str = None, 
                         details: Dict[str, Any] = None, risk_level: RiskLevel = RiskLevel.LOW,
                         request_context: Dict[str, Any] = None):
    """Log user action for audit trail"""
    event = AuditLogEntry(
        event_type=AuditEventType.DATA_ACCESS,
        user_id=user_id,
        action=action,
        resource=resource,
        details=details or {},
        risk_level=risk_level,
        user_ip=request_context.get("ip") if request_context else None,
        user_agent=request_context.get("user_agent") if request_context else None
    )
    
    await compliance_audit_system.log_audit_event(event, request_context)

async def create_privacy_request(user_id: str, email: str, request_type: str, details: Dict = None):
    """Create privacy rights request"""
    privacy_right = PrivacyRight(request_type)
    return await compliance_audit_system.create_privacy_request(user_id, email, privacy_right, details)

async def record_consent(user_id: str, consent_type: str, granted: bool, 
                        consent_text: str = "", ip_address: str = None):
    """Record user consent"""
    await compliance_audit_system.record_user_consent(
        user_id, consent_type, granted, consent_text, ip_address
    )

async def generate_gdpr_report(start_date: datetime, end_date: datetime):
    """Generate GDPR compliance report"""
    return await compliance_audit_system.generate_compliance_report(
        ComplianceStandard.GDPR, start_date, end_date
    )