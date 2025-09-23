"""
Database Optimization and Performance Enhancements
==================================================

Optimized database operations with connection pooling, caching, and performance tuning.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Text, Float, Boolean
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool
import redis
import json
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

Base = declarative_base()

class OptimizedDatabaseManager:
    """Optimized database manager with connection pooling and caching"""
    
    def __init__(self, database_url: str, redis_url: str = "redis://localhost:6379"):
        self.database_url = database_url
        self.redis_url = redis_url
        self.engine = None
        self.SessionLocal = None
        self.redis_client = None
        self._setup_database()
        self._setup_cache()
    
    def _setup_database(self):
        """Setup database with optimized connection pooling"""
        try:
            self.engine = create_engine(
                self.database_url,
                poolclass=QueuePool,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False
            )
            
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            logger.info("Database connection pool initialized")
            
        except Exception as e:
            logger.error(f"Database setup failed: {e}")
            # Fallback to SQLite for development
            self.engine = create_engine("sqlite:///./intelligence_platform.db")
            self.SessionLocal = sessionmaker(bind=self.engine)
    
    def _setup_cache(self):
        """Setup Redis cache for performance optimization"""
        try:
            self.redis_client = redis.from_url(
                self.redis_url,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                health_check_interval=30
            )
            
            # Test connection
            self.redis_client.ping()
            logger.info("Redis cache initialized")
            
        except Exception as e:
            logger.warning(f"Redis cache setup failed: {e}")
            self.redis_client = None
    
    def get_session(self) -> Session:
        """Get database session with proper error handling"""
        try:
            return self.SessionLocal()
        except Exception as e:
            logger.error(f"Failed to create database session: {e}")
            raise
    
    async def cache_set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in cache with TTL"""
        if not self.redis_client:
            return
        
        try:
            serialized_value = json.dumps(value, default=str)
            self.redis_client.setex(key, ttl, serialized_value)
        except Exception as e:
            logger.warning(f"Cache set failed for key {key}: {e}")
    
    async def cache_get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.redis_client:
            return None
        
        try:
            cached_value = self.redis_client.get(key)
            if cached_value:
                return json.loads(cached_value)
            return None
        except Exception as e:
            logger.warning(f"Cache get failed for key {key}: {e}")
            return None
    
    async def cache_delete(self, key: str):
        """Delete value from cache"""
        if not self.redis_client:
            return
        
        try:
            self.redis_client.delete(key)
        except Exception as e:
            logger.warning(f"Cache delete failed for key {key}: {e}")
    
    def create_tables(self):
        """Create all database tables"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Table creation failed: {e}")
    
    async def health_check(self) -> Dict[str, bool]:
        """Perform health check on database and cache"""
        health_status = {
            "database": False,
            "cache": False
        }
        
        # Database health check
        try:
            with self.get_session() as session:
                session.execute("SELECT 1")
                health_status["database"] = True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
        
        # Cache health check
        if self.redis_client:
            try:
                self.redis_client.ping()
                health_status["cache"] = True
            except Exception as e:
                logger.error(f"Cache health check failed: {e}")
        
        return health_status

# Optimized database models with proper indexing
class OptimizedUser(Base):
    """Optimized User model with indexing"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    is_premium = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    last_login = Column(DateTime, index=True)

class OptimizedQuery(Base):
    """Optimized Query model with indexing"""
    __tablename__ = "queries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    query_type = Column(String(50), index=True, nullable=False)
    query_value = Column(String(500), nullable=False)
    status = Column(String(20), index=True, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, index=True)
    processing_time = Column(Float)

class OptimizedScanResult(Base):
    """Optimized ScanResult model with indexing"""
    __tablename__ = "scan_results"
    
    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, index=True, nullable=False)
    scanner_name = Column(String(100), index=True, nullable=False)
    scanner_type = Column(String(50), index=True, nullable=False)
    result_data = Column(Text, nullable=False)
    confidence_score = Column(Float, index=True, default=0.0)
    processing_time = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class OptimizedReport(Base):
    """Optimized Report model with indexing"""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, index=True, nullable=False)
    user_id = Column(Integer, index=True, nullable=False)
    report_type = Column(String(20), index=True, nullable=False)  # preview/full
    report_data = Column(Text, nullable=False)
    is_paid = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    accessed_at = Column(DateTime, index=True)

# Global database manager instance
db_manager = OptimizedDatabaseManager(
    database_url="postgresql://user:password@localhost/intelligence_platform",
    redis_url="redis://localhost:6379"
)
