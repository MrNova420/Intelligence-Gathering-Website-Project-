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

try:
    from backend.app.core.config import settings
except ImportError:
    # Mock settings for standalone testing
    class MockSettings:
        SECRET_KEY = "your-secret-key-change-in-production"
        ALGORITHM = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES = 30
    settings = MockSettings()

logger = logging.getLogger(__name__)

# Initialize encryption
def generate_encryption_key() -> bytes:
    """Generate a new encryption key."""
    return Fernet.generate_key()

def get_encryption_key() -> bytes:
    """Get encryption key from environment or generate new one."""
    key = os.environ.get('ENCRYPTION_KEY')
    if not key:
        # Generate a proper 32-byte key for production
        key = base64.urlsafe_b64encode(b"intelligence_platform_key_32bit!")
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

def hash_password(password: str) -> str:
    """Hash a password using BCrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

def generate_api_key() -> str:
    """Generate a secure API key."""
    return secrets.token_urlsafe(32)

def sanitize_input(input_data: str) -> str:
    """Sanitize user input to prevent XSS and injection attacks."""
    if not input_data:
        return ""
    
    # Basic sanitization - remove potentially dangerous characters
    dangerous_chars = ["<", ">", "\"", "'", "&", "script", "javascript"]
    sanitized = input_data
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, "")
    
    return sanitized.strip()

# Security middleware functions
def get_client_ip(request) -> str:
    """Extract client IP address from request."""
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host

# Rate limiting (Redis-based in production)
rate_limit_store = {}

def check_rate_limit(identifier: str, limit: int = 100, window: int = 3600) -> bool:
    """Check if request is within rate limits."""
    current_time = datetime.utcnow().timestamp()
    
    if identifier not in rate_limit_store:
        rate_limit_store[identifier] = []
    
    # Clean old entries
    rate_limit_store[identifier] = [
        timestamp for timestamp in rate_limit_store[identifier] 
        if current_time - timestamp < window
    ]
    
    # Check limit
    if len(rate_limit_store[identifier]) >= limit:
        return False
    
    # Add current request
    rate_limit_store[identifier].append(current_time)
    return True

# Audit logging
def log_security_event(event_type: str, user_id: str = None, ip_address: str = None, details: dict = None):
    """Log security events for audit purposes."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "user_id": user_id,
        "ip_address": ip_address,
        "details": details or {}
    }
    
    logger.info(f"Security Event: {log_entry}")
    # In production, this would be stored in a secure audit log

def mask_sensitive_data(data: str, mask_char: str = "*", visible_chars: int = 4) -> str:
    """Mask sensitive data for logging/display."""
    if not data or len(data) <= visible_chars:
        return mask_char * len(data) if data else ""
    
    return data[:visible_chars] + mask_char * (len(data) - visible_chars)

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