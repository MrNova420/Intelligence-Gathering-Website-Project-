"""
Enterprise Configuration Management
==================================

Advanced configuration system with environment-specific settings,
validation, and security features for enterprise deployment.
"""

import os
import logging
from typing import Optional, List, Dict, Any, Union
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum

try:
    from pydantic import BaseSettings, validator, Field
    from pydantic_settings import BaseSettings as PydanticSettings
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    BaseSettings = object
    PydanticSettings = object

logger = logging.getLogger(__name__)


class Environment(str, Enum):
    """Deployment environment types"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """Logging levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class DatabaseConfig:
    """Database configuration"""
    host: str = "localhost"
    port: int = 5432
    username: str = "postgres"
    password: str = "password"
    database: str = "intelligence_db"
    pool_size: int = 20
    max_overflow: int = 30
    pool_timeout: int = 30
    pool_recycle: int = 3600
    echo: bool = False
    
    @property
    def url(self) -> str:
        """Generate database URL"""
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class RedisConfig:
    """Redis configuration"""
    host: str = "localhost"
    port: int = 6379
    password: Optional[str] = None
    db: int = 0
    max_connections: int = 100
    socket_timeout: int = 30
    socket_connect_timeout: int = 30
    socket_keepalive: bool = True
    socket_keepalive_options: Dict[str, int] = field(default_factory=dict)
    
    @property
    def url(self) -> str:
        """Generate Redis URL"""
        auth = f":{self.password}@" if self.password else ""
        return f"redis://{auth}{self.host}:{self.port}/{self.db}"


@dataclass
class SecurityConfig:
    """Security configuration"""
    secret_key: str = field(default_factory=lambda: os.urandom(32).hex())
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7  # 7 days
    bcrypt_rounds: int = 12
    max_password_attempts: int = 5
    lockout_duration_minutes: int = 30
    session_timeout_minutes: int = 120
    require_mfa: bool = False
    allowed_hosts: List[str] = field(default_factory=lambda: ["*"])
    cors_origins: List[str] = field(default_factory=lambda: ["*"])
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600  # 1 hour


@dataclass
class APIConfig:
    """API configuration"""
    title: str = "Intelligence Gathering Platform"
    description: str = "Enterprise-grade intelligence gathering platform"
    version: str = "2.0.0"
    api_prefix: str = "/api/v1"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"
    max_request_size: int = 10 * 1024 * 1024  # 10MB
    request_timeout: int = 300  # 5 minutes


@dataclass
class MonitoringConfig:
    """Monitoring and observability configuration"""
    enable_metrics: bool = True
    enable_tracing: bool = True
    enable_health_checks: bool = True
    health_check_interval: int = 30
    metrics_port: int = 9090
    log_level: LogLevel = LogLevel.INFO
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
    access_log: bool = True
    error_log: bool = True
    performance_log: bool = True


class EnterpriseSettings:
    """Enterprise configuration management with validation and environment-specific settings"""
    
    def __init__(self, env_file: Optional[str] = None):
        self.env_file = env_file or ".env"
        self.environment = Environment(os.getenv("ENVIRONMENT", Environment.DEVELOPMENT))
        
        # Load environment variables
        self._load_env_file()
        
        # Initialize configurations
        self.database = self._init_database_config()
        self.redis = self._init_redis_config()
        self.security = self._init_security_config()
        self.api = self._init_api_config()
        self.monitoring = self._init_monitoring_config()
        
        # Validate configuration
        self._validate_config()
    
    def _load_env_file(self):
        """Load environment variables from file"""
        env_path = Path(self.env_file)
        if env_path.exists():
            try:
                from dotenv import load_dotenv
                load_dotenv(env_path)
                logger.info(f"✅ Loaded environment from {env_path}")
            except ImportError:
                logger.warning("python-dotenv not available, skipping .env file loading")
        else:
            logger.info(f"No .env file found at {env_path}")
    
    def _init_database_config(self) -> DatabaseConfig:
        """Initialize database configuration"""
        return DatabaseConfig(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            username=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "password"),
            database=os.getenv("DB_NAME", "intelligence_db"),
            pool_size=int(os.getenv("DB_POOL_SIZE", "20")),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "30")),
            echo=os.getenv("DB_ECHO", "false").lower() == "true"
        )
    
    def _init_redis_config(self) -> RedisConfig:
        """Initialize Redis configuration"""
        return RedisConfig(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            password=os.getenv("REDIS_PASSWORD"),
            db=int(os.getenv("REDIS_DB", "0")),
            max_connections=int(os.getenv("REDIS_MAX_CONNECTIONS", "100"))
        )
    
    def _init_security_config(self) -> SecurityConfig:
        """Initialize security configuration"""
        return SecurityConfig(
            secret_key=os.getenv("SECRET_KEY", os.urandom(32).hex()),
            jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
            jwt_expire_minutes=int(os.getenv("JWT_EXPIRE_MINUTES", str(60 * 24 * 7))),
            bcrypt_rounds=int(os.getenv("BCRYPT_ROUNDS", "12")),
            require_mfa=os.getenv("REQUIRE_MFA", "false").lower() == "true",
            allowed_hosts=os.getenv("ALLOWED_HOSTS", "*").split(","),
            cors_origins=os.getenv("CORS_ORIGINS", "*").split(","),
            rate_limit_requests=int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
        )
    
    def _init_api_config(self) -> APIConfig:
        """Initialize API configuration"""
        return APIConfig(
            title=os.getenv("API_TITLE", "Intelligence Gathering Platform"),
            version=os.getenv("API_VERSION", "2.0.0"),
            api_prefix=os.getenv("API_PREFIX", "/api/v1"),
            max_request_size=int(os.getenv("MAX_REQUEST_SIZE", str(10 * 1024 * 1024)))
        )
    
    def _init_monitoring_config(self) -> MonitoringConfig:
        """Initialize monitoring configuration"""
        return MonitoringConfig(
            enable_metrics=os.getenv("ENABLE_METRICS", "true").lower() == "true",
            enable_tracing=os.getenv("ENABLE_TRACING", "true").lower() == "true",
            log_level=LogLevel(os.getenv("LOG_LEVEL", LogLevel.INFO)),
            health_check_interval=int(os.getenv("HEALTH_CHECK_INTERVAL", "30"))
        )
    
    def _validate_config(self):
        """Validate configuration settings"""
        errors = []
        
        # Database validation
        if not self.database.host:
            errors.append("Database host is required")
        if self.database.port <= 0 or self.database.port > 65535:
            errors.append("Database port must be between 1 and 65535")
        
        # Security validation
        if len(self.security.secret_key) < 32:
            errors.append("Secret key must be at least 32 characters long")
        if self.security.jwt_expire_minutes <= 0:
            errors.append("JWT expiration must be positive")
        
        # API validation
        if not self.api.title:
            errors.append("API title is required")
        if not self.api.version:
            errors.append("API version is required")
        
        if errors:
            raise ValueError(f"Configuration validation failed: {', '.join(errors)}")
        
        logger.info("✅ Configuration validation passed")
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.environment == Environment.DEVELOPMENT
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment == Environment.PRODUCTION
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing environment"""
        return self.environment == Environment.TESTING
    
    def get_database_url(self, async_driver: bool = False) -> str:
        """Get database URL with optional async driver"""
        if async_driver:
            return self.database.url.replace("postgresql://", "postgresql+asyncpg://")
        return self.database.url
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary (excluding sensitive data)"""
        return {
            "environment": self.environment.value,
            "database": {
                "host": self.database.host,
                "port": self.database.port,
                "database": self.database.database,
                "pool_size": self.database.pool_size
            },
            "redis": {
                "host": self.redis.host,
                "port": self.redis.port,
                "db": self.redis.db
            },
            "api": {
                "title": self.api.title,
                "version": self.api.version,
                "api_prefix": self.api.api_prefix
            },
            "security": {
                "jwt_algorithm": self.security.jwt_algorithm,
                "require_mfa": self.security.require_mfa,
                "rate_limit_requests": self.security.rate_limit_requests
            },
            "monitoring": {
                "enable_metrics": self.monitoring.enable_metrics,
                "enable_tracing": self.monitoring.enable_tracing,
                "log_level": self.monitoring.log_level.value
            }
        }


# Global settings instance
settings = EnterpriseSettings()

# Convenience functions for backward compatibility
def get_settings() -> EnterpriseSettings:
    """Get global settings instance"""
    return settings

def reload_settings(env_file: Optional[str] = None) -> EnterpriseSettings:
    """Reload settings with optional new env file"""
    global settings
    settings = EnterpriseSettings(env_file)
    return settings