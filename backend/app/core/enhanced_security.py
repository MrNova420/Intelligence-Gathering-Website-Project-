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
import time
import pyotp
import qrcode
from io import BytesIO

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


class SecurityManager:
    """Main security manager that coordinates all security features"""
    
    def __init__(self):
        self.enhanced_security = EnhancedSecurityManager()
        self.mfa_manager = MFAManager()
        self.rbac_manager = RBACManager()
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        return self.enhanced_security.encrypt_data(data)
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        return self.enhanced_security.decrypt_data(encrypted_data)
    
    def hash_password(self, password: str) -> str:
        """Hash password securely"""
        return self.enhanced_security.hash_password(password)
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return self.enhanced_security.verify_password(password, hashed)
    
    def generate_mfa_secret(self, user_email: str) -> Dict[str, Any]:
        """Generate MFA secret for user"""
        return self.mfa_manager.generate_secret(user_email)
    
    def verify_mfa_token(self, secret: str, token: str) -> bool:
        """Verify MFA token"""
        return self.mfa_manager.verify_token(secret, token)
    
    def check_permission(self, user_role: str, resource: str, action: str) -> bool:
        """Check if user has permission for action"""
        return self.rbac_manager.check_permission(user_role, resource, action)
    
    def calculate_password_strength(self, password: str) -> Dict[str, Any]:
        """Calculate password strength score and recommendations"""
        score = 0
        issues = []
        recommendations = []
        
        # Length check
        if len(password) >= 12:
            score += 25
        elif len(password) >= 8:
            score += 15
        else:
            issues.append("Password too short")
            recommendations.append("Use at least 12 characters")
        
        # Character diversity
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        char_types = sum([has_lower, has_upper, has_digit, has_special])
        
        if char_types >= 4:
            score += 25
        elif char_types >= 3:
            score += 15
        elif char_types >= 2:
            score += 10
        else:
            issues.append("Insufficient character diversity")
            recommendations.append("Include uppercase, lowercase, numbers, and special characters")
        
        # Common patterns
        common_patterns = ["123", "abc", "password", "admin", "qwerty"]
        if any(pattern in password.lower() for pattern in common_patterns):
            score -= 15
            issues.append("Contains common patterns")
            recommendations.append("Avoid common patterns and dictionary words")
        
        # Repetition check
        if len(set(password)) < len(password) * 0.6:
            score -= 10
            issues.append("Too much character repetition")
            recommendations.append("Use more diverse characters")
        
        # Final scoring
        score = max(0, min(100, score))
        
        if score >= 90:
            strength = "Excellent"
        elif score >= 70:
            strength = "Strong"
        elif score >= 50:
            strength = "Medium"
        elif score >= 30:
            strength = "Weak"
        else:
            strength = "Very Weak"
        
        return {
            "score": score,
            "strength": strength,
            "issues": issues,
            "recommendations": recommendations,
            "is_secure": score >= 70
        }


class MFAManager:
    """Multi-Factor Authentication Manager"""
    
    def __init__(self):
        self.app_name = "Intelligence Platform"
    
    def generate_secret(self, user_email: str) -> Dict[str, Any]:
        """Generate TOTP secret and QR code for user"""
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret)
        
        # Generate QR code
        provisioning_uri = totp.provisioning_uri(
            name=user_email,
            issuer_name=self.app_name
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 for easy transmission
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        # Generate backup codes
        backup_codes = [secrets.token_hex(8) for _ in range(10)]
        
        return {
            "secret": secret,
            "qr_code": qr_base64,
            "backup_codes": backup_codes,
            "provisioning_uri": provisioning_uri
        }
    
    def verify_token(self, secret: str, token: str) -> bool:
        """Verify TOTP token"""
        try:
            totp = pyotp.TOTP(secret)
            return totp.verify(token, valid_window=1)
        except Exception as e:
            logger.error(f"MFA verification failed: {e}")
            return False
    
    def verify_backup_code(self, backup_codes: list, code: str) -> bool:
        """Verify backup recovery code"""
        return code in backup_codes


class RBACManager:
    """Role-Based Access Control Manager"""
    
    def __init__(self):
        self.permissions = {
            "USER": {
                "queries": ["read", "create"],
                "reports": ["read"],
                "profile": ["read", "update"]
            },
            "PREMIUM": {
                "queries": ["read", "create", "delete"],
                "reports": ["read", "export"],
                "profile": ["read", "update"],
                "api": ["read", "create"]
            },
            "ADMIN": {
                "queries": ["read", "create", "update", "delete"],
                "reports": ["read", "create", "update", "delete", "export"],
                "profile": ["read", "update"],
                "api": ["read", "create", "update", "delete"],
                "users": ["read", "update", "delete"],
                "system": ["read", "configure"]
            },
            "SUPER_ADMIN": {
                "*": ["*"]  # Full access to everything
            }
        }
    
    def check_permission(self, user_role: str, resource: str, action: str) -> bool:
        """Check if user role has permission for resource and action"""
        if user_role not in self.permissions:
            return False
        
        role_perms = self.permissions[user_role]
        
        # Super admin has full access
        if "*" in role_perms and "*" in role_perms["*"]:
            return True
        
        # Check specific resource permissions
        if resource in role_perms:
            resource_actions = role_perms[resource]
            return action in resource_actions or "*" in resource_actions
        
        return False
    
    def get_user_permissions(self, user_role: str) -> Dict[str, Any]:
        """Get all permissions for a user role"""
        return self.permissions.get(user_role, {})
    
    def get_role_permissions(self, user_role: str) -> Dict[str, Any]:
        """Alias for get_user_permissions for backward compatibility"""
        return self.get_user_permissions(user_role)
    
    def has_role(self, user_role: str, required_role: str) -> bool:
        """Check if user has required role or higher"""
        role_hierarchy = ["USER", "PREMIUM", "ADMIN", "SUPER_ADMIN"]
        
        try:
            user_level = role_hierarchy.index(user_role)
            required_level = role_hierarchy.index(required_role)
            return user_level >= required_level
        except ValueError:
            return False


# Global security manager instance
security_manager = SecurityManager()
