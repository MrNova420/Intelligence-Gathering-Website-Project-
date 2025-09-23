from typing import Dict, Any, List, Optional
from datetime import datetime
import enum


# Mock Enums
class QueryType(str, enum.Enum):
    NAME = "name"
    EMAIL = "email"
    PHONE = "phone"
    USERNAME = "username"
    IMAGE = "image"


class QueryStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ScannerType(str, enum.Enum):
    API = "api"
    SOCIAL_MEDIA = "social_media"
    PUBLIC_RECORDS = "public_records"
    EMAIL_VERIFICATION = "email_verification"
    PHONE_LOOKUP = "phone_lookup"
    IMAGE_MEDIA = "image_media"


class UserRole(str, enum.Enum):
    USER = "user"
    PREMIUM = "premium"
    ADMIN = "admin"


# Mock Pydantic schemas
class BaseModel:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def dict(self, exclude_unset=False):
        result = {}
        for key, value in self.__dict__.items():
            if not exclude_unset or value is not None:
                result[key] = value
        return result


class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    full_name: Optional[str] = None


class QueryCreate(BaseModel):
    query_type: QueryType
    query_value: str
    metadata: Optional[Dict[str, Any]] = None


class QueryUpdate(BaseModel):
    status: Optional[QueryStatus] = None
    error_message: Optional[str] = None


class ReportCreate(BaseModel):
    query_id: int
    report_type: str


class SearchFilters(BaseModel):
    query_type: Optional[QueryType] = None
    status: Optional[QueryStatus] = None
    page: int = 1
    page_size: int = 10


class MessageResponse(BaseModel):
    message: str


class DashboardStats(BaseModel):
    total_queries: int
    active_queries: int
    completed_queries: int
    total_users: int
    active_subscriptions: int


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"