#!/usr/bin/env python3
"""
Advanced Error Tracking and Logging System
Provides comprehensive error monitoring, tracking, and alerting
"""

import logging
import traceback
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
from pathlib import Path
import threading
import uuid
from enum import Enum

class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    """Error categories for classification"""
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    VALIDATION = "validation"
    DATABASE = "database"
    NETWORK = "network"
    SYSTEM = "system"
    APPLICATION = "application"
    SECURITY = "security"
    PERFORMANCE = "performance"
    UNKNOWN = "unknown"

@dataclass
class ErrorEvent:
    """Individual error event data structure"""
    id: str
    timestamp: datetime
    severity: ErrorSeverity
    category: ErrorCategory
    message: str
    exception_type: str
    traceback: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    url: Optional[str] = None
    method: Optional[str] = None
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    additional_context: Dict[str, Any] = None
    resolved: bool = False
    resolution_notes: Optional[str] = None

class ErrorTracker:
    """Main error tracking and monitoring system"""
    
    def __init__(self, max_errors: int = 10000, log_dir: str = "logs"):
        self.max_errors = max_errors
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Error storage
        self.errors: deque = deque(maxlen=max_errors)
        self.error_counts = defaultdict(int)
        self.error_patterns = defaultdict(list)
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Configure logging
        self._setup_logging()
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("🔍 Error Tracking System initialized")
    
    def _setup_logging(self):
        """Configure structured logging"""
        # Create formatters for different log levels
        error_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        )
        
        # Error log file
        error_handler = logging.FileHandler(
            self.log_dir / "errors.log", 
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(error_formatter)
        
        # Application log file
        app_handler = logging.FileHandler(
            self.log_dir / "application.log", 
            encoding='utf-8'
        )
        app_handler.setLevel(logging.INFO)
        app_handler.setFormatter(error_formatter)
        
        # Console handler for development
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(error_formatter)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(error_handler)
        root_logger.addHandler(app_handler)
        root_logger.addHandler(console_handler)
    
    def track_error(
        self, 
        exception: Union[Exception, str],
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        request_id: Optional[str] = None,
        url: Optional[str] = None,
        method: Optional[str] = None,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Track a new error event"""
        
        try:
            # Generate unique error ID
            error_id = str(uuid.uuid4())
            
            # Extract error information
            if isinstance(exception, Exception):
                message = str(exception)
                exception_type = type(exception).__name__
                traceback_str = traceback.format_exc()
            else:
                message = str(exception)
                exception_type = "GenericError"
                traceback_str = ""
            
            # Create error event
            error_event = ErrorEvent(
                id=error_id,
                timestamp=datetime.now(),
                severity=severity,
                category=category,
                message=message,
                exception_type=exception_type,
                traceback=traceback_str,
                user_id=user_id,
                session_id=session_id,
                request_id=request_id,
                url=url,
                method=method,
                user_agent=user_agent,
                ip_address=ip_address,
                additional_context=additional_context or {}
            )
            
            # Store error
            with self.lock:
                self.errors.append(error_event)
                self.error_counts[category.value] += 1
                self.error_patterns[exception_type].append(error_event)
            
            # Log error
            self._log_error(error_event)
            
            # Check for critical errors that need immediate attention
            if severity == ErrorSeverity.CRITICAL:
                self._handle_critical_error(error_event)
            
            return error_id
            
        except Exception as e:
            # Fallback error logging
            logging.error(f"Error in error tracking system: {e}")
            return "error-tracking-failed"
    
    def _log_error(self, error_event: ErrorEvent):
        """Log error event with appropriate level"""
        logger = logging.getLogger(__name__)
        
        log_message = (
            f"[{error_event.id}] {error_event.severity.value.upper()} - "
            f"{error_event.category.value}: {error_event.message}"
        )
        
        # Add context if available
        context_parts = []
        if error_event.user_id:
            context_parts.append(f"user:{error_event.user_id}")
        if error_event.url:
            context_parts.append(f"url:{error_event.url}")
        if error_event.method:
            context_parts.append(f"method:{error_event.method}")
        
        if context_parts:
            log_message += f" [{', '.join(context_parts)}]"
        
        # Log based on severity
        if error_event.severity == ErrorSeverity.CRITICAL:
            logger.critical(log_message)
        elif error_event.severity == ErrorSeverity.HIGH:
            logger.error(log_message)
        elif error_event.severity == ErrorSeverity.MEDIUM:
            logger.warning(log_message)
        else:
            logger.info(log_message)
        
        # Log traceback for exceptions
        if error_event.traceback:
            logger.debug(f"Traceback for {error_event.id}:\n{error_event.traceback}")
    
    def _handle_critical_error(self, error_event: ErrorEvent):
        """Handle critical errors that need immediate attention"""
        try:
            # Save critical error to separate file
            critical_log_path = self.log_dir / "critical_errors.log"
            
            with open(critical_log_path, 'a', encoding='utf-8') as f:
                error_data = {
                    "timestamp": error_event.timestamp.isoformat(),
                    "id": error_event.id,
                    "message": error_event.message,
                    "exception_type": error_event.exception_type,
                    "traceback": error_event.traceback,
                    "context": {
                        "user_id": error_event.user_id,
                        "url": error_event.url,
                        "method": error_event.method,
                        "ip_address": error_event.ip_address
                    }
                }
                f.write(json.dumps(error_data) + "\n")
            
            # TODO: Add alerting mechanisms (email, Slack, etc.)
            
        except Exception as e:
            logging.error(f"Failed to handle critical error: {e}")
    
    def get_error_by_id(self, error_id: str) -> Optional[ErrorEvent]:
        """Get specific error by ID"""
        with self.lock:
            for error in self.errors:
                if error.id == error_id:
                    return error
        return None
    
    def get_recent_errors(self, hours: int = 24, severity: Optional[ErrorSeverity] = None) -> List[ErrorEvent]:
        """Get recent errors within specified timeframe"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        with self.lock:
            recent_errors = [
                error for error in self.errors 
                if error.timestamp >= cutoff_time
            ]
            
            if severity:
                recent_errors = [
                    error for error in recent_errors 
                    if error.severity == severity
                ]
        
        return recent_errors
    
    def get_error_statistics(self, hours: int = 24) -> Dict[str, Any]:
        """Get error statistics for specified time period"""
        recent_errors = self.get_recent_errors(hours)
        
        stats = {
            "total_errors": len(recent_errors),
            "by_severity": defaultdict(int),
            "by_category": defaultdict(int),
            "by_exception_type": defaultdict(int),
            "top_errors": [],
            "error_trend": [],
            "time_period_hours": hours
        }
        
        # Count by severity, category, and exception type
        for error in recent_errors:
            stats["by_severity"][error.severity.value] += 1
            stats["by_category"][error.category.value] += 1
            stats["by_exception_type"][error.exception_type] += 1
        
        # Get top error types
        sorted_exceptions = sorted(
            stats["by_exception_type"].items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        stats["top_errors"] = sorted_exceptions[:10]
        
        # Calculate hourly error trend
        hourly_counts = defaultdict(int)
        for error in recent_errors:
            hour_key = error.timestamp.strftime("%Y-%m-%d %H:00")
            hourly_counts[hour_key] += 1
        
        stats["error_trend"] = [
            {"hour": hour, "count": count} 
            for hour, count in sorted(hourly_counts.items())
        ]
        
        return stats
    
    def resolve_error(self, error_id: str, resolution_notes: str) -> bool:
        """Mark an error as resolved"""
        with self.lock:
            for error in self.errors:
                if error.id == error_id:
                    error.resolved = True
                    error.resolution_notes = resolution_notes
                    self.logger.info(f"✅ Error {error_id} marked as resolved: {resolution_notes}")
                    return True
        return False
    
    def export_errors(self, filepath: str, hours: int = 24):
        """Export recent errors to JSON file"""
        try:
            recent_errors = self.get_recent_errors(hours)
            
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "time_period_hours": hours,
                "total_errors": len(recent_errors),
                "errors": [
                    {
                        **asdict(error),
                        "timestamp": error.timestamp.isoformat(),
                        "severity": error.severity.value,
                        "category": error.category.value
                    }
                    for error in recent_errors
                ]
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"📁 Exported {len(recent_errors)} errors to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Failed to export errors: {e}")
    
    def clear_old_errors(self, days: int = 30):
        """Clear errors older than specified days"""
        cutoff_time = datetime.now() - timedelta(days=days)
        
        with self.lock:
            original_count = len(self.errors)
            
            # Filter out old errors
            self.errors = deque(
                [error for error in self.errors if error.timestamp >= cutoff_time],
                maxlen=self.max_errors
            )
            
            cleared_count = original_count - len(self.errors)
            
            if cleared_count > 0:
                self.logger.info(f"🗑️ Cleared {cleared_count} old errors (older than {days} days)")

class ErrorTrackingMiddleware:
    """Middleware for automatic error tracking in web applications"""
    
    def __init__(self, error_tracker: ErrorTracker):
        self.error_tracker = error_tracker
    
    def track_request_error(
        self,
        exception: Exception,
        request_info: Dict[str, Any]
    ) -> str:
        """Track error from web request with context"""
        
        # Determine error category based on exception type
        category = self._classify_exception(exception)
        
        # Determine severity
        severity = self._determine_severity(exception, category)
        
        return self.error_tracker.track_error(
            exception=exception,
            severity=severity,
            category=category,
            url=request_info.get("url"),
            method=request_info.get("method"),
            user_agent=request_info.get("user_agent"),
            ip_address=request_info.get("ip_address"),
            user_id=request_info.get("user_id"),
            session_id=request_info.get("session_id"),
            request_id=request_info.get("request_id"),
            additional_context=request_info
        )
    
    def _classify_exception(self, exception: Exception) -> ErrorCategory:
        """Classify exception into appropriate category"""
        exception_name = type(exception).__name__
        
        # Database errors
        if any(db_error in exception_name.lower() for db_error in 
               ["database", "sql", "connection", "integrity", "constraint"]):
            return ErrorCategory.DATABASE
        
        # Network errors
        if any(net_error in exception_name.lower() for net_error in 
               ["connection", "timeout", "network", "socket", "http"]):
            return ErrorCategory.NETWORK
        
        # Validation errors
        if any(val_error in exception_name.lower() for val_error in 
               ["validation", "value", "type", "attribute"]):
            return ErrorCategory.VALIDATION
        
        # Authentication errors
        if any(auth_error in exception_name.lower() for auth_error in 
               ["auth", "credential", "token", "permission"]):
            return ErrorCategory.AUTHENTICATION
        
        # System errors
        if any(sys_error in exception_name.lower() for sys_error in 
               ["system", "os", "file", "permission", "memory"]):
            return ErrorCategory.SYSTEM
        
        return ErrorCategory.APPLICATION
    
    def _determine_severity(self, exception: Exception, category: ErrorCategory) -> ErrorSeverity:
        """Determine error severity based on exception and category"""
        exception_name = type(exception).__name__
        
        # Critical errors
        if any(critical in exception_name.lower() for critical in 
               ["critical", "fatal", "outofmemory", "systemerror"]):
            return ErrorSeverity.CRITICAL
        
        # High severity errors
        if category in [ErrorCategory.SECURITY, ErrorCategory.DATABASE]:
            return ErrorSeverity.HIGH
        
        if any(high in exception_name.lower() for high in 
               ["permission", "unauthorized", "forbidden"]):
            return ErrorSeverity.HIGH
        
        # Low severity errors
        if category == ErrorCategory.VALIDATION:
            return ErrorSeverity.LOW
        
        return ErrorSeverity.MEDIUM

# Global error tracker instance
error_tracker = ErrorTracker()
error_middleware = ErrorTrackingMiddleware(error_tracker)

def track_error(exception: Union[Exception, str], **kwargs) -> str:
    """Convenience function to track errors"""
    return error_tracker.track_error(exception, **kwargs)

if __name__ == "__main__":
    # Test error tracking system
    print("🧪 Testing Error Tracking System...")
    
    tracker = ErrorTracker()
    
    # Test tracking different types of errors
    try:
        raise ValueError("Test validation error")
    except ValueError as e:
        error_id = tracker.track_error(
            e, 
            severity=ErrorSeverity.LOW,
            category=ErrorCategory.VALIDATION,
            user_id="test-user",
            url="/api/test"
        )
        print(f"Tracked error: {error_id}")
    
    # Test getting statistics
    stats = tracker.get_error_statistics()
    print(f"Error statistics: {stats}")
    
    print("✅ Error tracking system test completed!")