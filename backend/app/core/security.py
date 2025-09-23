from datetime import datetime, timedelta
from typing import Optional
import hashlib
import secrets
import logging

logger = logging.getLogger(__name__)


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    # Simplified token creation for demo
    token_data = f"{subject}:{datetime.utcnow().isoformat()}"
    return hashlib.sha256(token_data.encode()).hexdigest()[:32]


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    # Simple hash verification for demo
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password


def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_token(token: str) -> Optional[str]:
    """Verify JWT token and return subject."""
    # Simplified token verification for demo
    if len(token) == 32:
        return "demo_user"  # Return demo user for valid-looking tokens
    return None


def create_api_key() -> str:
    """Generate a new API key."""
    return f"igp_{secrets.token_urlsafe(32)}"


def hash_api_key(api_key: str) -> str:
    """Hash an API key for storage."""
    return get_password_hash(api_key)


def verify_api_key(plain_api_key: str, hashed_api_key: str) -> bool:
    """Verify an API key against its hash."""
    return verify_password(plain_api_key, hashed_api_key)