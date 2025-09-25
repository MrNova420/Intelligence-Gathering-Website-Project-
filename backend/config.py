#!/usr/bin/env python3
"""
Intelligence Gathering Platform - Unified Configuration
Centralized configuration for the complete web platform
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional

class PlatformConfig:
    """Unified configuration for the Intelligence Gathering Platform"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.load_configuration()
    
    def load_configuration(self):
        """Load configuration from environment and defaults"""
        
        # Platform Information
        self.PLATFORM_NAME = "Intelligence Gathering Platform"
        self.PLATFORM_VERSION = "2.0.0"
        self.PLATFORM_DESCRIPTION = "🔍 Unified Intelligence Gathering Website"
        
        # Server Configuration
        self.HOST = os.getenv("HOST", "0.0.0.0")
        self.PORT = int(os.getenv("PORT", 8000))
        self.DEBUG = os.getenv("DEBUG", "false").lower() == "true"
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
        
        # Security
        self.SECRET_KEY = os.getenv("SECRET_KEY", "intelligence-platform-secret-key-change-in-production")
        self.SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", 3600))  # 1 hour
        
        # Database Configuration
        self.DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{self.project_root}/data/platform.db")
        self.DATABASE_ECHO = self.DEBUG
        
        # File Storage
        self.DATA_DIR = self.project_root / "data"
        self.SCANS_DIR = self.DATA_DIR / "scans"
        self.REPORTS_DIR = self.DATA_DIR / "reports" 
        self.BACKUPS_DIR = self.DATA_DIR / "backups"
        self.LOGS_DIR = self.project_root / "logs"
        
        # Web Interface
        self.WEB_DIR = self.project_root / "web"
        self.TEMPLATES_DIR = self.WEB_DIR / "templates"
        self.STATIC_DIR = self.WEB_DIR / "static"
        
        # API Configuration
        self.API_PREFIX = "/api/v1"
        self.API_DOCS_URL = "/docs"
        self.API_REDOC_URL = "/redoc"
        
        # Scanning Configuration
        self.MAX_CONCURRENT_SCANS = int(os.getenv("MAX_CONCURRENT_SCANS", 5))
        self.SCAN_TIMEOUT = int(os.getenv("SCAN_TIMEOUT", 300))  # 5 minutes
        self.DEFAULT_SCAN_OPTIONS = {
            "deep_scan": False,
            "include_social": True,
            "timeout": self.SCAN_TIMEOUT
        }
        
        # Performance and Monitoring
        self.ENABLE_MONITORING = os.getenv("ENABLE_MONITORING", "true").lower() == "true"
        self.METRICS_RETENTION_HOURS = int(os.getenv("METRICS_RETENTION_HOURS", 24))
        self.PERFORMANCE_ALERTS = {
            "cpu_threshold": 80.0,
            "memory_threshold": 85.0,
            "response_time_threshold": 2.0
        }
        
        # Error Tracking
        self.ENABLE_ERROR_TRACKING = os.getenv("ENABLE_ERROR_TRACKING", "true").lower() == "true"
        self.ERROR_RETENTION_DAYS = int(os.getenv("ERROR_RETENTION_DAYS", 30))
        
        # Backup Configuration
        self.ENABLE_AUTO_BACKUP = os.getenv("ENABLE_AUTO_BACKUP", "true").lower() == "true"
        self.BACKUP_INTERVAL_HOURS = int(os.getenv("BACKUP_INTERVAL_HOURS", 24))
        self.BACKUP_RETENTION_DAYS = int(os.getenv("BACKUP_RETENTION_DAYS", 30))
        
        # Platform Features
        self.FEATURES = {
            "web_interface": True,
            "api_access": True,
            "real_time_scanning": True,
            "performance_monitoring": self.ENABLE_MONITORING,
            "error_tracking": self.ENABLE_ERROR_TRACKING,
            "auto_backup": self.ENABLE_AUTO_BACKUP,
            "plugin_system": True,
            "user_onboarding": True
        }
        
        # Termux/Android Specific
        self.IS_TERMUX = "com.termux" in os.environ.get("PREFIX", "")
        if self.IS_TERMUX:
            self.HOST = "127.0.0.1"  # Localhost only for Termux
            self.DEBUG = True  # Enable debug mode in Termux
        
        # Ensure directories exist
        self.create_directories()
    
    def create_directories(self):
        """Create necessary directories"""
        directories = [
            self.DATA_DIR,
            self.SCANS_DIR,
            self.REPORTS_DIR,
            self.BACKUPS_DIR,
            self.LOGS_DIR,
            self.WEB_DIR,
            self.TEMPLATES_DIR,
            self.STATIC_DIR,
            self.STATIC_DIR / "css",
            self.STATIC_DIR / "js",
            self.STATIC_DIR / "images"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration"""
        return {
            "url": self.DATABASE_URL,
            "echo": self.DATABASE_ECHO,
            "connect_args": {"check_same_thread": False} if "sqlite" in self.DATABASE_URL else {}
        }
    
    def get_server_config(self) -> Dict[str, Any]:
        """Get server configuration"""
        return {
            "host": self.HOST,
            "port": self.PORT,
            "debug": self.DEBUG,
            "reload": self.DEBUG,
            "log_level": "debug" if self.DEBUG else "info"
        }
    
    def get_cors_config(self) -> Dict[str, Any]:
        """Get CORS configuration"""
        if self.DEBUG or self.IS_TERMUX:
            # Permissive CORS for development and Termux
            return {
                "allow_origins": ["*"],
                "allow_credentials": True,
                "allow_methods": ["*"],
                "allow_headers": ["*"]
            }
        else:
            # Restrictive CORS for production
            return {
                "allow_origins": ["https://yourdomain.com"],
                "allow_credentials": True,
                "allow_methods": ["GET", "POST", "PUT", "DELETE"],
                "allow_headers": ["*"]
            }
    
    def get_feature_status(self) -> Dict[str, bool]:
        """Get current feature status"""
        return self.FEATURES.copy()
    
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.DEBUG or self.ENVIRONMENT == "development"
    
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return not self.DEBUG and self.ENVIRONMENT == "production"
    
    def get_platform_info(self) -> Dict[str, Any]:
        """Get platform information"""
        return {
            "name": self.PLATFORM_NAME,
            "version": self.PLATFORM_VERSION,
            "description": self.PLATFORM_DESCRIPTION,
            "environment": self.ENVIRONMENT,
            "debug": self.DEBUG,
            "termux": self.IS_TERMUX,
            "features": self.get_feature_status(),
            "api_docs": self.API_DOCS_URL,
            "health_check": "/health"
        }
    
    def update_setting(self, key: str, value: Any):
        """Update a configuration setting"""
        if hasattr(self, key):
            setattr(self, key, value)
            return True
        return False
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all configuration settings (excluding sensitive data)"""
        settings = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_') and 'SECRET' not in key.upper() and 'PASSWORD' not in key.upper():
                if isinstance(value, Path):
                    settings[key] = str(value)
                else:
                    settings[key] = value
        return settings

# Global configuration instance
config = PlatformConfig()

# Convenience functions
def get_config() -> PlatformConfig:
    """Get the global configuration instance"""
    return config

def get_database_url() -> str:
    """Get database URL"""
    return config.DATABASE_URL

def get_server_config() -> Dict[str, Any]:
    """Get server configuration"""
    return config.get_server_config()

def is_debug() -> bool:
    """Check if debug mode is enabled"""
    return config.DEBUG

def is_termux() -> bool:
    """Check if running on Termux"""
    return config.IS_TERMUX

if __name__ == "__main__":
    # Configuration test and display
    print("🔧 Intelligence Gathering Platform Configuration")
    print("=" * 50)
    
    print(f"Platform: {config.PLATFORM_NAME} v{config.PLATFORM_VERSION}")
    print(f"Environment: {config.ENVIRONMENT}")
    print(f"Debug Mode: {config.DEBUG}")
    print(f"Termux Mode: {config.IS_TERMUX}")
    print(f"Host: {config.HOST}:{config.PORT}")
    print(f"Database: {config.DATABASE_URL}")
    print(f"Data Directory: {config.DATA_DIR}")
    
    print("\n🎯 Features Enabled:")
    for feature, enabled in config.get_feature_status().items():
        status = "✅" if enabled else "❌"
        print(f"  {status} {feature.replace('_', ' ').title()}")
    
    print("\n📁 Directory Structure:")
    directories = [
        ("Data", config.DATA_DIR),
        ("Scans", config.SCANS_DIR),
        ("Reports", config.REPORTS_DIR),
        ("Backups", config.BACKUPS_DIR),
        ("Logs", config.LOGS_DIR),
        ("Web", config.WEB_DIR),
        ("Templates", config.TEMPLATES_DIR),
        ("Static", config.STATIC_DIR)
    ]
    
    for name, path in directories:
        exists = "✅" if path.exists() else "❌"
        print(f"  {exists} {name}: {path}")
    
    print("=" * 50)