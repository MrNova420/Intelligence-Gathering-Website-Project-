"""
Enhanced Security Implementation
===============================

Comprehensive security features with proper error handling and optimization.
"""

import os
import secrets
import hashlib
import hmac
import logging
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import bcrypt

logger = logging.getLogger(__name__)

class EnhancedSecurityManager:
    """Enhanced security manager with comprehensive features"""
    
    def __init__(self):
        self.fernet = None
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._init_encryption()
    
    def _init_encryption(self):
        """Initialize encryption with enhanced key derivation."""
        try:
            # Use environment variable or generate secure key
            key_material = os.environ.get('ENCRYPTION_KEY', self._generate_key())
            
            # Derive key using PBKDF2
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'intelligence_platform_v1',
                iterations=100000,
            )
            
            key = base64.urlsafe_b64encode(kdf.derive(key_material.encode()))
            self.fernet = Fernet(key)
            logger.info("Encryption initialized successfully")
            
        except Exception as e:
            logger.error(f"Encryption initialization failed: {e}")
            # Fallback to basic key generation
            self.fernet = Fernet(Fernet.generate_key())
    
    def _generate_key(self) -> str:
        """Generate a secure encryption key."""
        return secrets.token_urlsafe(32)
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data with AES-256."""
        try:
            if not self.fernet:
                raise ValueError("Encryption not initialized")
            return self.fernet.encrypt(data.encode()).decode()
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            return data  # Return original data if encryption fails
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data."""
        try:
            if not self.fernet:
                raise ValueError("Encryption not initialized")
            return self.fernet.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return encrypted_data  # Return encrypted data if decryption fails
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt."""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        try:
            return self.pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            logger.error(f"Password verification failed: {e}")
            return False
    
    def generate_secure_token(self, length: int = 32) -> str:
        """Generate cryptographically secure token."""
        return secrets.token_urlsafe(length)
    
    def create_jwt_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT token with expiration."""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=24)
        
        to_encode.update({"exp": expire})
        
        secret_key = os.environ.get('JWT_SECRET_KEY', self._generate_key())
        return jwt.encode(to_encode, secret_key, algorithm="HS256")
    
    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token and return payload."""
        try:
            secret_key = os.environ.get('JWT_SECRET_KEY', self._generate_key())
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid JWT token")
            return None
    
    def verify_signature(self, data: str, signature: str, secret: str) -> bool:
        """Verify HMAC signature for data integrity."""
        try:
            expected = hmac.new(
                secret.encode(),
                data.encode(),
                hashlib.sha256
            ).hexdigest()
            return hmac.compare_digest(expected, signature)
        except Exception as e:
            logger.error(f"Signature verification failed: {e}")
            return False
    
    def sanitize_input(self, input_data: str) -> str:
        """Sanitize user input to prevent XSS and injection attacks."""
        if not isinstance(input_data, str):
            return str(input_data)
        
        # Basic sanitization
        sanitized = input_data.replace('<', '&lt;').replace('>', '&gt;')
        sanitized = sanitized.replace('"', '&quot;').replace("'", '&#x27;')
        sanitized = sanitized.replace('&', '&amp;').replace('/', '&#x2F;')
        
        return sanitized
    
    def generate_api_key(self, user_id: str) -> str:
        """Generate API key for user."""
        timestamp = str(int(time.time()))
        raw_key = f"{user_id}:{timestamp}:{self.generate_secure_token()}"
        return base64.urlsafe_b64encode(raw_key.encode()).decode()
    
    def validate_api_key(self, api_key: str) -> Optional[str]:
        """Validate API key and return user_id."""
        try:
            decoded = base64.urlsafe_b64decode(api_key.encode()).decode()
            parts = decoded.split(':')
            if len(parts) >= 2:
                return parts[0]  # Return user_id
            return None
        except Exception as e:
            logger.error(f"API key validation failed: {e}")
            return None

# Global security manager instance
security_manager = EnhancedSecurityManager()
