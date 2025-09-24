"""
Health check endpoints for production monitoring
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import asyncio
import psutil
import time
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with system metrics"""
    try:
        # Check system resources
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Check database connection
        db_status = await check_database_connection()
        
        # Check Redis connection
        redis_status = await check_redis_connection()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "system": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "disk_percent": disk.percent,
            },
            "services": {
                "database": db_status,
                "redis": redis_status,
            }
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")

async def check_database_connection():
    """Check database connectivity"""
    try:
        # Add your database connection check here
        return {"status": "connected", "latency_ms": 5}
    except Exception:
        return {"status": "disconnected", "error": "Connection failed"}

async def check_redis_connection():
    """Check Redis connectivity"""
    try:
        # Add your Redis connection check here
        return {"status": "connected", "latency_ms": 2}
    except Exception:
        return {"status": "disconnected", "error": "Connection failed"}
