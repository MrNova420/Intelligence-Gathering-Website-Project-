"""
Comprehensive System Monitoring
==============================

Real-time monitoring, health checks, and performance metrics for the intelligence platform.
"""

import asyncio
import psutil
import time
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
import json
import aiohttp
from pathlib import Path

logger = logging.getLogger(__name__)

class SystemMonitor:
    """Comprehensive system monitoring with health checks and metrics"""
    
    def __init__(self):
        self.start_time = time.time()
        self.metrics_history = []
        self.alerts = []
        self.health_checks = {}
    
    async def get_system_metrics(self) -> Dict[str, Any]:
        """Get comprehensive system metrics"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Memory metrics
            memory = psutil.virtual_memory()
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            
            # Network metrics
            network = psutil.net_io_counters()
            
            # Process metrics
            process = psutil.Process()
            
            metrics = {
                "timestamp": datetime.utcnow().isoformat(),
                "uptime": time.time() - self.start_time,
                "cpu": {
                    "percent": cpu_percent,
                    "count": cpu_count,
                    "load_avg": list(psutil.getloadavg()) if hasattr(psutil, 'getloadavg') else []
                },
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "used": memory.used,
                    "percent": memory.percent
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "percent": disk.used / disk.total * 100
                },
                "network": {
                    "bytes_sent": network.bytes_sent,
                    "bytes_recv": network.bytes_recv,
                    "packets_sent": network.packets_sent,
                    "packets_recv": network.packets_recv
                },
                "process": {
                    "pid": process.pid,
                    "memory_percent": process.memory_percent(),
                    "cpu_percent": process.cpu_percent(),
                    "num_threads": process.num_threads(),
                    "create_time": process.create_time()
                }
            }
            
            # Store metrics history (keep last 100 entries)
            self.metrics_history.append(metrics)
            if len(self.metrics_history) > 100:
                self.metrics_history.pop(0)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to get system metrics: {e}")
            return {"error": str(e), "timestamp": datetime.utcnow().isoformat()}
    
    async def check_database_health(self) -> Dict[str, Any]:
        """Check database connectivity and performance"""
        try:
            from backend.app.db.optimized import db_manager
            
            start_time = time.time()
            health = await db_manager.health_check()
            response_time = time.time() - start_time
            
            result = {
                "status": "healthy" if health.get("database") else "unhealthy",
                "response_time": response_time,
                "details": health,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.health_checks["database"] = result
            return result
            
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            result = {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
            self.health_checks["database"] = result
            return result
    
    async def check_cache_health(self) -> Dict[str, Any]:
        """Check cache (Redis) connectivity and performance"""
        try:
            from backend.app.db.optimized import db_manager
            
            if not db_manager.redis_client:
                return {
                    "status": "unavailable",
                    "message": "Redis not configured",
                    "timestamp": datetime.utcnow().isoformat()
                }
            
            start_time = time.time()
            db_manager.redis_client.ping()
            response_time = time.time() - start_time
            
            # Get Redis info
            info = db_manager.redis_client.info()
            
            result = {
                "status": "healthy",
                "response_time": response_time,
                "connected_clients": info.get("connected_clients", 0),
                "used_memory": info.get("used_memory", 0),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.health_checks["cache"] = result
            return result
            
        except Exception as e:
            logger.error(f"Cache health check failed: {e}")
            result = {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
            self.health_checks["cache"] = result
            return result
    
    async def check_scanner_health(self) -> Dict[str, Any]:
        """Check scanner services health"""
        try:
            from backend.app.scanners.optimized import scanner_orchestrator
            
            # Mock query for health check
            test_query = {"query_value": "health@check.com"}
            
            start_time = time.time()
            # Run a lightweight health check scan
            result = await scanner_orchestrator.run_comprehensive_scan(
                test_query, 
                scanner_types=["email"]
            )
            response_time = time.time() - start_time
            
            health_result = {
                "status": "healthy" if result.get("summary", {}).get("success_rate", 0) > 0 else "degraded",
                "response_time": response_time,
                "scanners_available": len(scanner_orchestrator.scanners),
                "last_test": datetime.utcnow().isoformat()
            }
            
            self.health_checks["scanners"] = health_result
            return health_result
            
        except Exception as e:
            logger.error(f"Scanner health check failed: {e}")
            result = {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
            self.health_checks["scanners"] = result
            return result
    
    async def get_comprehensive_health(self) -> Dict[str, Any]:
        """Get comprehensive health status of all services"""
        health_checks = await asyncio.gather(
            self.check_database_health(),
            self.check_cache_health(),
            self.check_scanner_health(),
            return_exceptions=True
        )
        
        database_health, cache_health, scanner_health = health_checks
        
        # Calculate overall health
        healthy_services = 0
        total_services = 3
        
        if isinstance(database_health, dict) and database_health.get("status") == "healthy":
            healthy_services += 1
        
        if isinstance(cache_health, dict) and cache_health.get("status") in ["healthy", "unavailable"]:
            healthy_services += 1
        
        if isinstance(scanner_health, dict) and scanner_health.get("status") == "healthy":
            healthy_services += 1
        
        overall_status = "healthy" if healthy_services == total_services else "degraded" if healthy_services > 0 else "unhealthy"
        
        return {
            "overall_status": overall_status,
            "service_health": healthy_services / total_services,
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "database": database_health,
                "cache": cache_health,
                "scanners": scanner_health
            },
            "system_metrics": await self.get_system_metrics()
        }
    
    def check_alerts(self, metrics: Dict[str, Any]):
        """Check for system alerts based on metrics"""
        alerts = []
        
        # CPU usage alert
        cpu_percent = metrics.get("cpu", {}).get("percent", 0)
        if cpu_percent > 80:
            alerts.append({
                "level": "warning" if cpu_percent < 90 else "critical",
                "message": f"High CPU usage: {cpu_percent}%",
                "timestamp": datetime.utcnow().isoformat()
            })
        
        # Memory usage alert
        memory_percent = metrics.get("memory", {}).get("percent", 0)
        if memory_percent > 80:
            alerts.append({
                "level": "warning" if memory_percent < 90 else "critical",
                "message": f"High memory usage: {memory_percent}%",
                "timestamp": datetime.utcnow().isoformat()
            })
        
        # Disk usage alert
        disk_percent = metrics.get("disk", {}).get("percent", 0)
        if disk_percent > 80:
            alerts.append({
                "level": "warning" if disk_percent < 90 else "critical",
                "message": f"High disk usage: {disk_percent}%",
                "timestamp": datetime.utcnow().isoformat()
            })
        
        self.alerts.extend(alerts)
        
        # Keep only recent alerts (last 24 hours)
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        self.alerts = [
            alert for alert in self.alerts 
            if datetime.fromisoformat(alert["timestamp"]) > cutoff_time
        ]
        
        return alerts
    
    async def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary and trends"""
        if len(self.metrics_history) < 2:
            return {"message": "Insufficient data for performance summary"}
        
        recent_metrics = self.metrics_history[-10:]  # Last 10 measurements
        
        # Calculate averages
        avg_cpu = sum(m.get("cpu", {}).get("percent", 0) for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m.get("memory", {}).get("percent", 0) for m in recent_metrics) / len(recent_metrics)
        avg_disk = sum(m.get("disk", {}).get("percent", 0) for m in recent_metrics) / len(recent_metrics)
        
        return {
            "performance_summary": {
                "avg_cpu_percent": round(avg_cpu, 2),
                "avg_memory_percent": round(avg_memory, 2),
                "avg_disk_percent": round(avg_disk, 2),
                "uptime_hours": round((time.time() - self.start_time) / 3600, 2),
                "measurements_taken": len(self.metrics_history)
            },
            "current_alerts": len(self.alerts),
            "health_status": self.health_checks,
            "timestamp": datetime.utcnow().isoformat()
        }

# Global monitor instance
system_monitor = SystemMonitor()
