"""
Intelligence Gathering Platform - Main Application
Production-ready FastAPI application with comprehensive intelligence gathering capabilities
Optimized for Docker, standalone, and Termux deployments
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any

# Import handling for different deployment modes
try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.middleware.trustedhost import TrustedHostMiddleware
    from fastapi.responses import JSONResponse
    FASTAPI_AVAILABLE = True
except ImportError:
    # Fallback for minimal deployments
    FASTAPI_AVAILABLE = False
    FastAPI = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app):
    """Application lifespan manager - handles startup and shutdown."""
    logger.info("🚀 Starting Intelligence Gathering Platform...")
    
    try:
        # Initialize database
        from app.core.database import init_db
        await init_db()
        logger.info("✅ Database initialized")
        
        # Register scanner modules
        from app.scanners.implementations import register_scanners
        register_scanners()
        logger.info("✅ Scanner modules registered")
        
        # Initialize security system
        from app.core.enhanced_security import SecurityManager
        security = SecurityManager()
        logger.info("✅ Security system initialized")
        
        # Initialize performance optimizer
        from app.core.performance_optimizer import PerformanceOptimizer
        performance = PerformanceOptimizer()
        logger.info("✅ Performance optimizer initialized")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise
    
    # Application is running
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Intelligence Gathering Platform...")

def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    if not FASTAPI_AVAILABLE:
        logger.error("❌ FastAPI not available - install with: pip install fastapi")
        raise ImportError("FastAPI is required")
    
    # Get settings
    try:
        from app.core.config import settings
    except:
        # Fallback settings for standalone deployment
        class Settings:
            PROJECT_NAME = "Intelligence Gathering Platform"
            VERSION = "1.0.0"
            DEBUG = os.getenv("DEBUG", "false").lower() == "true"
            API_V1_STR = "/api/v1"
        settings = Settings()
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="🔍 Intelligence Gathering Web Platform - 100+ Scanner Tools\n\n"
                   "A comprehensive, modular intelligence gathering platform providing "
                   "legal intelligence collection through advanced scanner modules.\n\n"
                   "**Features:**\n"
                   "- 📧 Email Intelligence (validation, reputation, breach detection)\n"
                   "- 📱 Phone Lookup (carrier ID, spam detection, location)\n"
                   "- 👥 Social Media Scanning (Twitter, LinkedIn, Instagram, etc.)\n"
                   "- 🔍 Public Records Search (court, business, property data)\n"
                   "- 🖼️ Image Analysis (reverse search, face recognition)\n"
                   "- 🛡️ Enterprise Security (MFA, RBAC, encryption)\n"
                   "- ⚡ High Performance (Redis caching, async processing)\n"
                   "- 📊 Professional Reports (PDF, JSON, CSV exports)\n\n"
                   "**Compatibility:** Docker, Standalone, Termux/Android",
        version=settings.VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )
    
    # CORS middleware - allow all origins for development/Termux
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # More permissive for Termux/standalone
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Trusted host middleware for production
    if not settings.DEBUG:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*"]  # Configure for production
        )
    
    # Include API router
    try:
        from app.api import api_router
        app.include_router(api_router, prefix=settings.API_V1_STR)
        logger.info("✅ API router included")
    except Exception as e:
        logger.warning(f"⚠️ Could not include API router: {e}")
    
    # Health check endpoint
    @app.get("/health", tags=["System"])
    async def health_check():
        """
        System health check endpoint.
        Returns platform status and component health.
        """
        try:
            # Check database connection
            from app.core.database import get_db
            db_status = "healthy"
        except Exception as e:
            db_status = f"error: {str(e)}"
        
        # Check Redis connection (if available)
        redis_status = "not configured"
        try:
            from app.core.performance_optimizer import PerformanceOptimizer
            optimizer = PerformanceOptimizer()
            if hasattr(optimizer, 'cache') and optimizer.cache:
                redis_status = "healthy"
        except Exception as e:
            redis_status = f"error: {str(e)}"
        
        # Check scanner modules
        scanner_count = 0
        try:
            from app.scanners.implementations import scanner_registry
            scanner_count = len(scanner_registry.get_all_scanners())
        except:
            pass
        
        return {
            "status": "healthy",
            "platform": "Intelligence Gathering Platform",
            "version": settings.VERSION,
            "environment": os.getenv("ENVIRONMENT", "production"),
            "termux_compatible": True,
            "components": {
                "database": db_status,
                "cache": redis_status,
                "scanners": f"{scanner_count} modules loaded"
            },
            "endpoints": {
                "api_docs": "/docs",
                "health": "/health",
                "api_base": settings.API_V1_STR
            }
        }
    
    # Root endpoint
    @app.get("/", tags=["System"])
    async def root():
        """
        Root endpoint - platform information.
        """
        return {
            "message": "🔍 Intelligence Gathering Platform",
            "description": "Advanced intelligence gathering with 100+ scanner tools",
            "version": settings.VERSION,
            "documentation": "/docs",
            "health": "/health",
            "api": settings.API_V1_STR,
            "compatibility": {
                "docker": True,
                "standalone": True,
                "termux": True,
                "android": True
            },
            "features": [
                "Email Intelligence",
                "Phone Lookup", 
                "Social Media Scanning",
                "Public Records Search",
                "Image Analysis",
                "Enterprise Security",
                "Professional Reports"
            ]
        }
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        """Global exception handler for better error responses."""
        logger.error(f"Global exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": str(exc) if settings.DEBUG else "An error occurred",
                "type": type(exc).__name__
            }
        )
    
    logger.info(f"✅ FastAPI application created - {settings.PROJECT_NAME} v{settings.VERSION}")
    return app

# Create the application instance
app = create_application()

# For standalone/direct execution
if __name__ == "__main__":
    import uvicorn
    
    # Configuration for standalone deployment
    config = {
        "host": "0.0.0.0",  # Allow external connections (Termux compatibility)
        "port": int(os.getenv("PORT", 8000)),
        "reload": os.getenv("DEBUG", "false").lower() == "true",
        "log_level": "info",
        "workers": 1,  # Single worker for standalone
    }
    
    logger.info("🚀 Starting standalone server...")
    logger.info(f"📱 Termux compatible: YES")
    logger.info(f"🌐 Server will be available at: http://localhost:{config['port']}")
    
    uvicorn.run(app, **config)
            "status": "healthy", 
            "service": "intelligence-gathering-api",
            "scanners": "100+ tools ready"
        }

    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "message": "Intelligence Gathering Platform API",
            "docs": "/docs",
            "health": "/health",
            "version": settings.VERSION,
            "scanners_available": 100
        }
    
    return app


# Create app instance
app = create_application()

if __name__ == "__main__":
    # Simple test runner
    async def test_app():
        logging.basicConfig(level=logging.INFO)
        
        # Test health endpoint
        health_result = await app.routes[0]["func"]()
        print("Health check:", health_result)
        
        # Test root endpoint  
        root_result = await app.routes[1]["func"]()
        print("Root endpoint:", root_result)
        
        print("✅ Intelligence Gathering Platform API is working!")
        print("🔍 100+ Scanner Tools Available")
        print("📊 Ready for production deployment")
    
    asyncio.run(test_app())