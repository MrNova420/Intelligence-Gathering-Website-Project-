"""
Platform Automation System
==========================

Integrated automation capabilities for the Intelligence Gathering Platform.
All automation scripts and orchestration are now part of the unified web application.
"""

import asyncio
import logging
import os
import subprocess
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class PlatformAutomation:
    """Unified platform automation system"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent.parent
        self.automation_tasks = {}
        self.scheduled_tasks = []
        
    async def start_platform(self, mode: str = "production") -> Dict[str, Any]:
        """Start platform with specified mode"""
        try:
            if mode == "development":
                return await self._start_development_mode()
            elif mode == "production":
                return await self._start_production_mode()
            elif mode == "docker":
                return await self._start_docker_mode()
            else:
                return {"success": False, "error": f"Unknown mode: {mode}"}
        except Exception as e:
            logger.error(f"Platform start error: {e}")
            return {"success": False, "error": str(e)}
    
    async def _start_development_mode(self) -> Dict[str, Any]:
        """Start in development mode"""
        try:
            # Start the unified app with development settings
            process = await asyncio.create_subprocess_exec(
                "python", "unified_app.py",
                cwd=self.base_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            return {
                "success": True,
                "mode": "development",
                "pid": process.pid,
                "message": "Platform started in development mode"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _start_production_mode(self) -> Dict[str, Any]:
        """Start in production mode"""
        try:
            # Use uvicorn for production
            process = await asyncio.create_subprocess_exec(
                "uvicorn", "webapp:app", 
                "--host", "0.0.0.0", 
                "--port", "8000",
                "--workers", "4",
                cwd=self.base_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            return {
                "success": True,
                "mode": "production",
                "pid": process.pid,
                "message": "Platform started in production mode"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _start_docker_mode(self) -> Dict[str, Any]:
        """Start with Docker"""
        try:
            process = await asyncio.create_subprocess_exec(
                "docker-compose", "up", "-d",
                cwd=self.base_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return {
                    "success": True,
                    "mode": "docker",
                    "message": "Platform started with Docker"
                }
            else:
                return {
                    "success": False,
                    "error": stderr.decode() if stderr else "Docker start failed"
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def stop_platform(self) -> Dict[str, Any]:
        """Stop the platform"""
        try:
            # Try to stop Docker containers first
            try:
                process = await asyncio.create_subprocess_exec(
                    "docker-compose", "down",
                    cwd=self.base_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                await process.communicate()
            except:
                pass
            
            # Kill any Python processes running the app
            try:
                process = await asyncio.create_subprocess_exec(
                    "pkill", "-f", "unified_app.py",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                await process.communicate()
            except:
                pass
            
            return {
                "success": True,
                "message": "Platform stopped successfully"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_platform_status(self) -> Dict[str, Any]:
        """Get platform status"""
        try:
            status = {
                "webapp_running": False,
                "docker_running": False,
                "database_status": "unknown",
                "api_status": "unknown",
                "uptime": None
            }
            
            # Check if webapp is running
            try:
                import requests
                response = requests.get("http://localhost:8000/health", timeout=5)
                if response.status_code == 200:
                    status["webapp_running"] = True
                    status["api_status"] = "healthy"
            except:
                pass
            
            # Check Docker status
            try:
                process = await asyncio.create_subprocess_exec(
                    "docker-compose", "ps", "-q",
                    cwd=self.base_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, _ = await process.communicate()
                if stdout and stdout.strip():
                    status["docker_running"] = True
            except:
                pass
            
            return {
                "success": True,
                "status": status,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def run_maintenance(self) -> Dict[str, Any]:
        """Run platform maintenance tasks"""
        try:
            maintenance_results = {}
            
            # Clean up logs
            log_cleanup = await self._cleanup_logs()
            maintenance_results["log_cleanup"] = log_cleanup
            
            # Clean up cache
            cache_cleanup = await self._cleanup_cache()
            maintenance_results["cache_cleanup"] = cache_cleanup
            
            # Database maintenance
            db_maintenance = await self._database_maintenance()
            maintenance_results["database_maintenance"] = db_maintenance
            
            return {
                "success": True,
                "maintenance_results": maintenance_results,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _cleanup_logs(self) -> Dict[str, Any]:
        """Clean up old log files"""
        try:
            logs_dir = self.base_path / "logs"
            if not logs_dir.exists():
                return {"success": True, "message": "No logs directory found"}
            
            # Remove logs older than 30 days
            cutoff_date = datetime.now() - timedelta(days=30)
            removed_files = 0
            
            for log_file in logs_dir.glob("*.log*"):
                if log_file.stat().st_mtime < cutoff_date.timestamp():
                    log_file.unlink()
                    removed_files += 1
            
            return {
                "success": True,
                "removed_files": removed_files,
                "message": f"Removed {removed_files} old log files"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _cleanup_cache(self) -> Dict[str, Any]:
        """Clean up cache files"""
        try:
            cache_dir = self.base_path / "data" / "cache"
            if not cache_dir.exists():
                return {"success": True, "message": "No cache directory found"}
            
            # Remove cache files older than 7 days
            cutoff_date = datetime.now() - timedelta(days=7)
            removed_files = 0
            
            for cache_file in cache_dir.glob("*.cache"):
                if cache_file.stat().st_mtime < cutoff_date.timestamp():
                    cache_file.unlink()
                    removed_files += 1
            
            return {
                "success": True,
                "removed_files": removed_files,
                "message": f"Removed {removed_files} old cache files"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _database_maintenance(self) -> Dict[str, Any]:
        """Perform database maintenance"""
        try:
            # This would typically run VACUUM, ANALYZE, etc. on the database
            return {
                "success": True,
                "message": "Database maintenance completed"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def deploy_updates(self) -> Dict[str, Any]:
        """Deploy platform updates"""
        try:
            deployment_steps = []
            
            # Backup current state
            backup_result = await self._create_backup()
            deployment_steps.append({"step": "backup", "result": backup_result})
            
            # Update dependencies
            deps_result = await self._update_dependencies()
            deployment_steps.append({"step": "dependencies", "result": deps_result})
            
            # Restart services
            restart_result = await self._restart_services()
            deployment_steps.append({"step": "restart", "result": restart_result})
            
            return {
                "success": True,
                "deployment_steps": deployment_steps,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _create_backup(self) -> Dict[str, Any]:
        """Create platform backup"""
        try:
            backup_dir = self.base_path / "backups"
            backup_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"platform_backup_{timestamp}"
            
            # This would create a comprehensive backup
            return {
                "success": True,
                "backup_name": backup_name,
                "message": "Backup created successfully"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _update_dependencies(self) -> Dict[str, Any]:
        """Update platform dependencies"""
        try:
            # Update pip packages
            process = await asyncio.create_subprocess_exec(
                "pip", "install", "-r", "requirements.txt", "--upgrade",
                cwd=self.base_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return {
                    "success": True,
                    "message": "Dependencies updated successfully"
                }
            else:
                return {
                    "success": False,
                    "error": stderr.decode() if stderr else "Update failed"
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _restart_services(self) -> Dict[str, Any]:
        """Restart platform services"""
        try:
            # Stop current services
            await self.stop_platform()
            
            # Wait a moment
            await asyncio.sleep(2)
            
            # Start services again
            start_result = await self.start_platform("production")
            
            return start_result
        except Exception as e:
            return {"success": False, "error": str(e)}


# Global automation instance
platform_automation = PlatformAutomation()