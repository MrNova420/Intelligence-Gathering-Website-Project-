#!/usr/bin/env python3
"""
Standalone Runner for Intelligence Gathering Platform
Optimized for Termux, Android, and standalone deployments
"""

import os
import sys
import asyncio
import uvicorn
import logging
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_environment():
    """Setup environment variables for standalone deployment"""
    
    # Database - Use SQLite for standalone deployment
    os.environ.setdefault('DATABASE_URL', 'sqlite:///./intelligence_platform.db')
    
    # Redis - Use in-memory fallback if Redis not available
    os.environ.setdefault('REDIS_URL', 'redis://localhost:6379/0')
    os.environ.setdefault('USE_REDIS_FALLBACK', 'true')
    
    # Security
    os.environ.setdefault('SECRET_KEY', 'standalone-development-key-change-in-production')
    os.environ.setdefault('ALGORITHM', 'HS256')
    os.environ.setdefault('ACCESS_TOKEN_EXPIRE_MINUTES', '30')
    
    # Development settings
    os.environ.setdefault('DEBUG', 'true')
    os.environ.setdefault('ENVIRONMENT', 'standalone')
    
    # API Keys (can be added by user)
    os.environ.setdefault('CLEARBIT_API_KEY', '')
    os.environ.setdefault('HUNTER_API_KEY', '')
    os.environ.setdefault('STRIPE_SECRET_KEY', '')
    
    logger.info("Environment configured for standalone deployment")

def check_dependencies():
    """Check if required dependencies are available"""
    missing_deps = []
    
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import pydantic
        import dns  # dnspython imports as dns
        import phonenumbers
        logger.info("✅ Core dependencies found")
    except ImportError as e:
        missing_deps.append(str(e))
    
    if missing_deps:
        logger.error("❌ Missing dependencies:")
        for dep in missing_deps:
            logger.error(f"   {dep}")
        logger.error("Run: pip install -r requirements.txt")
        return False
    
    return True

def initialize_database():
    """Initialize SQLite database for standalone deployment"""
    try:
        from app.db.database import engine, Base
        from app.db import models
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        return False

def check_redis_availability():
    """Check if Redis is available, set fallback if not"""
    try:
        import redis
        r = redis.Redis.from_url(os.environ.get('REDIS_URL', 'redis://localhost:6379/0'))
        r.ping()
        logger.info("✅ Redis connection successful")
        return True
    except Exception as e:
        logger.warning(f"⚠️ Redis not available, using in-memory fallback: {e}")
        os.environ['USE_REDIS_FALLBACK'] = 'true'
        return False

def run_validation_tests():
    """Run basic validation tests"""
    try:
        logger.info("🧪 Running validation tests...")
        
        # Import and run basic tests
        from app.core.aggregation_engine import DataAggregationEngine
        from app.core.enhanced_security import SecurityManager
        from app.scanners.email_scanners import EmailValidator
        
        # Test aggregation engine
        aggregator = DataAggregationEngine()
        test_result = aggregator.normalize_email("test+alias@gmail.com")
        assert test_result == "test@gmail.com", "Email normalization failed"
        
        # Test security manager
        security = SecurityManager()
        assert security.calculate_password_strength("password123") > 0, "Password strength calculation failed"
        
        # Test email scanner
        email_scanner = EmailValidator()
        assert email_scanner.validate_email_format("test@example.com"), "Email validation failed"
        
        logger.info("✅ All validation tests passed")
        return True
    except Exception as e:
        logger.error(f"❌ Validation tests failed: {e}")
        return False

def print_startup_info():
    """Print startup information and access points"""
    logger.info("🚀 Intelligence Gathering Platform - Standalone Mode")
    logger.info("=" * 60)
    logger.info("📱 Termux Compatible: YES")
    logger.info("🖥️  Cross-Platform: YES") 
    logger.info("🔧 Database: SQLite (standalone)")
    logger.info("💾 Cache: In-memory fallback")
    logger.info("🌐 Access Points:")
    logger.info("   • API Server: http://localhost:8000")
    logger.info("   • API Docs: http://localhost:8000/docs")
    logger.info("   • Health Check: http://localhost:8000/health")
    logger.info("   • Admin: http://localhost:8000/admin")
    logger.info("=" * 60)
    logger.info("📋 To test the platform:")
    logger.info("   python backend/run_validation.py")
    logger.info("📋 To stop the server:")
    logger.info("   Press Ctrl+C")
    logger.info("=" * 60)

async def main():
    """Main function to start the standalone server"""
    
    logger.info("🚀 Starting Intelligence Gathering Platform (Standalone)")
    
    # Setup environment
    setup_environment()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Redis availability
    check_redis_availability()
    
    # Initialize database
    if not initialize_database():
        sys.exit(1)
    
    # Run validation tests
    if not run_validation_tests():
        logger.warning("⚠️ Some validation tests failed, but continuing...")
    
    # Print startup information
    print_startup_info()
    
    try:
        # Import the FastAPI app
        from app.main import app
        
        # Run the server
        config = uvicorn.Config(
            app=app,
            host="0.0.0.0",  # Allow external connections (Termux compatibility)
            port=8000,
            log_level="info",
            reload=False,  # Disable reload for stability
            workers=1,  # Single worker for standalone
        )
        
        server = uvicorn.Server(config)
        await server.serve()
        
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Goodbye!")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)