
# Enhanced Security Configuration
import secrets
import hashlib
import hmac
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class EnhancedSecurityManager:
    def __init__(self):
        self.fernet = None
        self._init_encryption()
    
    def _init_encryption(self):
        """Initialize encryption with enhanced key derivation."""
        # Use environment variable or generate secure key
        key_material = os.environ.get('ENCRYPTION_KEY', self._generate_key())
        key = base64.urlsafe_b64encode(
            PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'intelligence_platform',
                iterations=100000,
            ).derive(key_material.encode())
        )
        self.fernet = Fernet(key)
    
    def _generate_key(self) -> str:
        """Generate a secure encryption key."""
        return secrets.token_urlsafe(32)
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data with AES-256."""
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data."""
        return self.fernet.decrypt(encrypted_data.encode()).decode()
    
    def generate_secure_token(self, length: int = 32) -> str:
        """Generate cryptographically secure token."""
        return secrets.token_urlsafe(length)
    
    def verify_signature(self, data: str, signature: str, secret: str) -> bool:
        """Verify HMAC signature for data integrity."""
        expected = hmac.new(
            secret.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, expected)
    
    def sanitize_input(self, user_input: str) -> str:
        """Sanitize user input to prevent injection attacks."""
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '|', '`']
        sanitized = user_input
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        return sanitized.strip()[:1000]  # Limit length
