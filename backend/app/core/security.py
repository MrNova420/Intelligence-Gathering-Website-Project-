from datetime import datetime, timedelta
from typing import Optional
import hashlib
import secrets
import logging
import bcrypt
import jwt
from cryptography.fernet import Fernet
import base64
import os

from app.core.config import settings

logger = logging.getLogger(__name__)

# Initialize encryption
def generate_encryption_key() -> bytes:
    """Generate a new encryption key."""
    return Fernet.generate_key()

def get_encryption_key() -> bytes:
    """Get encryption key from environment or generate new one."""
    key = os.environ.get('ENCRYPTION_KEY')
    if not key:
        # In production, this should be stored securely
        key = base64.urlsafe_b64encode(b"your-32-byte-secret-key-change-this!")
    return key

# Initialize Fernet cipher
cipher_suite = Fernet(get_encryption_key())

def encrypt_data(data: str) -> str:
    """Encrypt sensitive data using AES-256."""
    try:
        encrypted_data = cipher_suite.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()
    except Exception as e:
        logger.error(f"Encryption error: {e}")
        raise

def decrypt_data(encrypted_data: str) -> str:
    """Decrypt sensitive data."""
    try:
        decoded_data = base64.urlsafe_b64decode(encrypted_data)
        decrypted_data = cipher_suite.decrypt(decoded_data)
        return decrypted_data.decode()
    except Exception as e:
        logger.error(f"Decryption error: {e}")
        raise

def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token with proper security."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "iat": datetime.utcnow(),
        "jti": secrets.token_urlsafe(16)  # JWT ID for token revocation
    }
    
    try:
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    except Exception as e:
        logger.error(f"JWT encoding error: {e}")
        raise

def verify_token(token: str) -> Optional[str]:
    """Verify JWT token and return subject."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired")
        return None
    except jwt.JWTError as e:
        logger.warning(f"JWT verification error: {e}")
        return None

def get_password_hash(password: str) -> str:
    """Generate secure password hash using bcrypt."""
    try:
        # Generate salt and hash password
        salt = bcrypt.gensalt(rounds=12)  # High cost factor for security
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    except Exception as e:
        logger.error(f"Password hashing error: {e}")
        raise

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against bcrypt hash."""
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False

def create_api_key() -> str:
    """Generate a secure API key."""
    # Use cryptographically secure random generation
    key_bytes = secrets.token_bytes(32)
    api_key = f"igp_{base64.urlsafe_b64encode(key_bytes).decode().rstrip('=')}"
    return api_key

def hash_api_key(api_key: str) -> str:
    """Hash an API key for secure storage."""
    return get_password_hash(api_key)

def verify_api_key(plain_api_key: str, hashed_api_key: str) -> bool:
    """Verify an API key against its hash."""
    return verify_password(plain_api_key, hashed_api_key)

def generate_secure_filename(filename: str) -> str:
    """Generate a secure filename to prevent directory traversal."""
    # Remove any path components and dangerous characters
    safe_filename = os.path.basename(filename)
    safe_filename = "".join(c for c in safe_filename if c.isalnum() or c in "._-")
    
    # Add timestamp and random component for uniqueness
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    random_suffix = secrets.token_urlsafe(8)
    
    name, ext = os.path.splitext(safe_filename)
    return f"{timestamp}_{random_suffix}_{name}{ext}"

def sanitize_input(input_data: str, max_length: int = 1000) -> str:
    """Sanitize user input to prevent injection attacks."""
    if not input_data:
        return ""
    
    # Limit length
    if len(input_data) > max_length:
        input_data = input_data[:max_length]
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', '\x00', '\r', '\n']
    for char in dangerous_chars:
        input_data = input_data.replace(char, '')
    
    return input_data.strip()

def validate_email(email: str) -> bool:
    """Validate email format."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone number format."""
    import re
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    # Check if it's a valid length (7-15 digits)
    return 7 <= len(digits_only) <= 15

def rate_limit_key(user_id: str, endpoint: str) -> str:
    """Generate rate limiting key."""
    return f"rate_limit:{user_id}:{endpoint}"

def audit_log_entry(user_id: Optional[int], action: str, resource: str, 
                   details: Optional[dict] = None, ip_address: Optional[str] = None) -> dict:
    """Create audit log entry."""
    return {
        "user_id": user_id,
        "action": action,
        "resource": resource,
        "details": details or {},
        "ip_address": ip_address,
        "timestamp": datetime.utcnow().isoformat(),
        "severity": "info"
    }