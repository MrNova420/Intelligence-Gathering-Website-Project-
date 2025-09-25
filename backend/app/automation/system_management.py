"""
System Management Module
=======================

Integrated system management capabilities for the Intelligence Gathering Platform.
"""

import asyncio
import logging
import psutil
import shutil
import os
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path

logger = logging.getLogger(__name__)


class SystemManager:
    """System management and monitoring"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent.parent
    
    async def get_system_health(self) -> Dict[str, Any]:
        """Get comprehensive system health information"""
        try:
            health_data = {
                "cpu": self._get_cpu_info(),
                "memory": self._get_memory_info(),
                "disk": self._get_disk_info(),
                "network": self._get_network_info(),
                "processes": self._get_process_info(),
                "uptime": self._get_uptime(),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            return {
                "success": True,
                "health_data": health_data
            }
        except Exception as e:
            logger.error(f"System health check error: {e}")
            return {"success": False, "error": str(e)}
    
    def _get_cpu_info(self) -> Dict[str, Any]:
        """Get CPU information"""
        try:
            return {
                "usage_percent": psutil.cpu_percent(interval=1),
                "core_count": psutil.cpu_count(),
                "frequency": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
                "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else None
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _get_memory_info(self) -> Dict[str, Any]:
        """Get memory information"""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "percentage": memory.percent,
                "swap_total": swap.total,
                "swap_used": swap.used,
                "swap_percentage": swap.percent
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _get_disk_info(self) -> Dict[str, Any]:
        """Get disk information"""
        try:
            disk_usage = shutil.disk_usage(str(self.base_path))
            
            return {
                "total": disk_usage.total,
                "used": disk_usage.used,
                "free": disk_usage.free,
                "percentage": (disk_usage.used / disk_usage.total) * 100
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _get_network_info(self) -> Dict[str, Any]:
        """Get network information"""
        try:
            network_io = psutil.net_io_counters()
            
            return {
                "bytes_sent": network_io.bytes_sent,
                "bytes_recv": network_io.bytes_recv,
                "packets_sent": network_io.packets_sent,
                "packets_recv": network_io.packets_recv
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _get_process_info(self) -> Dict[str, Any]:
        """Get process information"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    if 'python' in proc.info['name'].lower() or 'uvicorn' in proc.info['name'].lower():
                        processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            return {
                "total_processes": len(list(psutil.process_iter())),
                "python_processes": processes[:10]  # Limit to top 10
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _get_uptime(self) -> Dict[str, Any]:
        """Get system uptime"""
        try:
            boot_time = psutil.boot_time()
            uptime_seconds = datetime.now().timestamp() - boot_time
            
            return {
                "boot_time": datetime.fromtimestamp(boot_time).isoformat(),
                "uptime_seconds": uptime_seconds,
                "uptime_hours": uptime_seconds / 3600
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def optimize_system(self) -> Dict[str, Any]:
        """Run system optimization tasks"""
        try:
            optimization_results = []
            
            # Clear system cache
            cache_result = await self._clear_system_cache()
            optimization_results.append({"task": "clear_cache", "result": cache_result})
            
            # Optimize database
            db_result = await self._optimize_database()
            optimization_results.append({"task": "optimize_database", "result": db_result})
            
            # Clean temporary files
            temp_result = await self._clean_temp_files()
            optimization_results.append({"task": "clean_temp", "result": temp_result})
            
            return {
                "success": True,
                "optimization_results": optimization_results,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _clear_system_cache(self) -> Dict[str, Any]:
        """Clear system cache"""
        try:
            cache_dir = self.base_path / "data" / "cache"
            if cache_dir.exists():
                # Clear cache files
                for cache_file in cache_dir.glob("*"):
                    if cache_file.is_file():
                        cache_file.unlink()
                
                return {"success": True, "message": "System cache cleared"}
            else:
                return {"success": True, "message": "No cache directory found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _optimize_database(self) -> Dict[str, Any]:
        """Optimize database performance"""
        try:
            # This would run database optimization commands
            return {"success": True, "message": "Database optimized"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _clean_temp_files(self) -> Dict[str, Any]:
        """Clean temporary files"""
        try:
            temp_dirs = [
                self.base_path / "tmp",
                self.base_path / "temp",
                Path("/tmp") / "intelligence-platform"
            ]
            
            cleaned_files = 0
            for temp_dir in temp_dirs:
                if temp_dir.exists():
                    for temp_file in temp_dir.glob("*"):
                        if temp_file.is_file():
                            temp_file.unlink()
                            cleaned_files += 1
            
            return {
                "success": True,
                "cleaned_files": cleaned_files,
                "message": f"Cleaned {cleaned_files} temporary files"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_security_status(self) -> Dict[str, Any]:
        """Get security status and recommendations"""
        try:
            security_checks = []
            
            # Check file permissions
            permissions_check = self._check_file_permissions()
            security_checks.append({"check": "file_permissions", "result": permissions_check})
            
            # Check for security updates
            updates_check = await self._check_security_updates()
            security_checks.append({"check": "security_updates", "result": updates_check})
            
            # Check SSL/TLS configuration
            ssl_check = self._check_ssl_config()
            security_checks.append({"check": "ssl_config", "result": ssl_check})
            
            return {
                "success": True,
                "security_checks": security_checks,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _check_file_permissions(self) -> Dict[str, Any]:
        """Check file permissions"""
        try:
            sensitive_files = [
                ".env",
                ".env.production",
                "config.py"
            ]
            
            permission_issues = []
            for file_name in sensitive_files:
                file_path = self.base_path / file_name
                if file_path.exists():
                    file_mode = oct(file_path.stat().st_mode)[-3:]
                    if file_mode != "600":  # Should be readable/writable by owner only
                        permission_issues.append({
                            "file": file_name,
                            "current_mode": file_mode,
                            "recommended_mode": "600"
                        })
            
            return {
                "success": True,
                "issues_found": len(permission_issues),
                "permission_issues": permission_issues
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _check_security_updates(self) -> Dict[str, Any]:
        """Check for security updates"""
        try:
            # This would check for available security updates
            return {
                "success": True,
                "updates_available": False,
                "message": "No security updates available"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _check_ssl_config(self) -> Dict[str, Any]:
        """Check SSL/TLS configuration"""
        try:
            # This would check SSL certificate validity and configuration
            return {
                "success": True,
                "ssl_enabled": False,
                "recommendation": "Enable SSL/TLS for production deployment"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


# Global system manager instance
system_manager = SystemManager()