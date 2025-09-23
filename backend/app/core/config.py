import secrets
from typing import List, Optional


class Settings:
    """Application settings."""
    
    # Project Info
    PROJECT_NAME: str = "Intelligence Gathering Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://localhost:3000",
        "http://localhost:8080",
    ]
    
    # Allowed hosts
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "*"]
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "intelligence_db"
    POSTGRES_PORT: int = 5432
    
    # API Keys for external services (100+ integrations)
    CLEARBIT_API_KEY: Optional[str] = None
    HUNTER_API_KEY: Optional[str] = None
    TWITTER_BEARER_TOKEN: Optional[str] = None
    LINKEDIN_CLIENT_ID: Optional[str] = None
    FACEBOOK_ACCESS_TOKEN: Optional[str] = None
    INSTAGRAM_ACCESS_TOKEN: Optional[str] = None
    TRUECALLER_API_KEY: Optional[str] = None
    WHITEPAGES_API_KEY: Optional[str] = None
    GOOGLE_CUSTOM_SEARCH_API_KEY: Optional[str] = None
    BING_SEARCH_API_KEY: Optional[str] = None
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 3600  # 1 hour
    
    # Logging
    LOG_LEVEL: str = "INFO"


settings = Settings()