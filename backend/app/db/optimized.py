
# Enhanced Database Configuration
import asyncpg
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import logging

class OptimizedDatabaseManager:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = None
        self.session_factory = None
        self.logger = logging.getLogger(__name__)
    
    async def initialize(self):
        """Initialize optimized database connection."""
        self.engine = create_async_engine(
            self.database_url,
            poolclass=QueuePool,
            pool_size=20,
            max_overflow=30,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False,  # Set to True for development
        )
        
        self.session_factory = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        self.logger.info("Database connection pool initialized")
    
    async def get_session(self) -> AsyncSession:
        """Get database session with proper error handling."""
        try:
            async with self.session_factory() as session:
                yield session
        except Exception as e:
            self.logger.error(f"Database session error: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check database health."""
        try:
            async with self.session_factory() as session:
                await session.execute("SELECT 1")
                return True
        except Exception as e:
            self.logger.error(f"Database health check failed: {e}")
            return False
    
    async def create_indexes(self):
        """Create optimized database indexes."""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);",
            "CREATE INDEX IF NOT EXISTS idx_queries_user_id ON intelligence_queries(user_id);",
            "CREATE INDEX IF NOT EXISTS idx_queries_created_at ON intelligence_queries(created_at);",
            "CREATE INDEX IF NOT EXISTS idx_scan_results_query_id ON scan_results(query_id);",
            "CREATE INDEX IF NOT EXISTS idx_scan_results_scanner_type ON scan_results(scanner_type);",
            "CREATE INDEX IF NOT EXISTS idx_reports_user_id ON reports(user_id);",
            "CREATE INDEX IF NOT EXISTS idx_reports_created_at ON reports(created_at);",
        ]
        
        async with self.session_factory() as session:
            for index_sql in indexes:
                try:
                    await session.execute(index_sql)
                    await session.commit()
                except Exception as e:
                    self.logger.warning(f"Index creation warning: {e}")
        
        self.logger.info("Database indexes optimized")
