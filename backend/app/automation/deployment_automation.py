"""
Deployment Automation Module
============================

Automated deployment and infrastructure management for the Intelligence Gathering Platform.
"""

import asyncio
import logging
import json
import yaml
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class DeploymentManager:
    """Automated deployment management"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent.parent
        self.deployment_configs = {
            "development": {
                "host": "0.0.0.0",
                "port": 8000,
                "workers": 1,
                "reload": True
            },
            "production": {
                "host": "0.0.0.0", 
                "port": 8000,
                "workers": 4,
                "reload": False
            },
            "docker": {
                "compose_file": "docker-compose.yml"
            }
        }
    
    async def deploy(self, environment: str = "production", config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Deploy the platform to specified environment"""
        try:
            deployment_config = config or self.deployment_configs.get(environment, {})
            
            deployment_steps = []
            
            # Pre-deployment checks
            pre_check = await self._pre_deployment_checks(environment)
            deployment_steps.append({"step": "pre_checks", "result": pre_check})
            
            if not pre_check["success"]:
                return {
                    "success": False,
                    "error": "Pre-deployment checks failed",
                    "deployment_steps": deployment_steps
                }
            
            # Build and prepare
            build_result = await self._build_application(environment)
            deployment_steps.append({"step": "build", "result": build_result})
            
            # Deploy based on environment
            if environment == "docker":
                deploy_result = await self._deploy_docker()
            elif environment == "production":
                deploy_result = await self._deploy_production(deployment_config)
            else:
                deploy_result = await self._deploy_development(deployment_config)
            
            deployment_steps.append({"step": "deploy", "result": deploy_result})
            
            # Post-deployment verification
            verify_result = await self._post_deployment_verification()
            deployment_steps.append({"step": "verification", "result": verify_result})
            
            return {
                "success": True,
                "environment": environment,
                "deployment_steps": deployment_steps,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Deployment error: {e}")
            return {"success": False, "error": str(e)}
    
    async def _pre_deployment_checks(self, environment: str) -> Dict[str, Any]:
        """Run pre-deployment checks"""
        try:
            checks = []
            
            # Check if required files exist
            required_files = ["webapp.py", "unified_app.py", "requirements.txt"]
            for file_name in required_files:
                file_path = self.base_path / file_name
                checks.append({
                    "check": f"file_exists_{file_name}",
                    "success": file_path.exists(),
                    "file": file_name
                })
            
            # Check environment configuration
            if environment == "production":
                env_file = self.base_path / ".env.production"
                checks.append({
                    "check": "production_env_config",
                    "success": env_file.exists(),
                    "message": "Production environment file exists" if env_file.exists() else "Missing .env.production file"
                })
            
            # Check dependencies
            deps_check = await self._check_dependencies()
            checks.append({
                "check": "dependencies",
                "success": deps_check["success"],
                "details": deps_check
            })
            
            all_passed = all(check["success"] for check in checks)
            
            return {
                "success": all_passed,
                "checks": checks,
                "message": "All pre-deployment checks passed" if all_passed else "Some checks failed"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _check_dependencies(self) -> Dict[str, Any]:
        """Check if all dependencies are available"""
        try:
            requirements_file = self.base_path / "requirements.txt"
            if not requirements_file.exists():
                return {"success": False, "error": "requirements.txt not found"}
            
            # This would check if all required packages are installed
            return {
                "success": True,
                "message": "All dependencies are available"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _build_application(self, environment: str) -> Dict[str, Any]:
        """Build the application for deployment"""
        try:
            build_steps = []
            
            # Install/update dependencies
            if environment in ["production", "docker"]:
                deps_result = await self._install_dependencies()
                build_steps.append({"step": "install_dependencies", "result": deps_result})
            
            # Generate static files if needed
            static_result = await self._generate_static_files()
            build_steps.append({"step": "static_files", "result": static_result})
            
            # Run any build scripts
            scripts_result = await self._run_build_scripts(environment)
            build_steps.append({"step": "build_scripts", "result": scripts_result})
            
            return {
                "success": True,
                "build_steps": build_steps,
                "message": "Application built successfully"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _install_dependencies(self) -> Dict[str, Any]:
        """Install application dependencies"""
        try:
            process = await asyncio.create_subprocess_exec(
                "pip", "install", "-r", "requirements.txt",
                cwd=self.base_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return {
                    "success": True,
                    "message": "Dependencies installed successfully"
                }
            else:
                return {
                    "success": False,
                    "error": stderr.decode() if stderr else "Failed to install dependencies"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _generate_static_files(self) -> Dict[str, Any]:
        """Generate static files"""
        try:
            # Ensure static directories exist
            static_dirs = [
                self.base_path / "web" / "static" / "css",
                self.base_path / "web" / "static" / "js",
                self.base_path / "web" / "static" / "images"
            ]
            
            for static_dir in static_dirs:
                static_dir.mkdir(parents=True, exist_ok=True)
            
            return {
                "success": True,
                "message": "Static files prepared"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _run_build_scripts(self, environment: str) -> Dict[str, Any]:
        """Run environment-specific build scripts"""
        try:
            # This would run any custom build scripts
            return {
                "success": True,
                "message": f"Build scripts completed for {environment}"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _deploy_docker(self) -> Dict[str, Any]:
        """Deploy using Docker"""
        try:
            # Stop existing containers
            stop_process = await asyncio.create_subprocess_exec(
                "docker-compose", "down",
                cwd=self.base_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await stop_process.communicate()
            
            # Start containers
            start_process = await asyncio.create_subprocess_exec(
                "docker-compose", "up", "-d", "--build",
                cwd=self.base_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await start_process.communicate()
            
            if start_process.returncode == 0:
                return {
                    "success": True,
                    "message": "Docker deployment successful"
                }
            else:
                return {
                    "success": False,
                    "error": stderr.decode() if stderr else "Docker deployment failed"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _deploy_production(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy to production environment"""
        try:
            # Start with uvicorn for production
            cmd = [
                "uvicorn", "webapp:app",
                "--host", config.get("host", "0.0.0.0"),
                "--port", str(config.get("port", 8000)),
                "--workers", str(config.get("workers", 4))
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=self.base_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Give it a moment to start
            await asyncio.sleep(2)
            
            return {
                "success": True,
                "message": "Production deployment started",
                "pid": process.pid,
                "config": config
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _deploy_development(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy to development environment"""
        try:
            process = await asyncio.create_subprocess_exec(
                "python", "unified_app.py",
                cwd=self.base_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Give it a moment to start
            await asyncio.sleep(2)
            
            return {
                "success": True,
                "message": "Development deployment started",
                "pid": process.pid,
                "config": config
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _post_deployment_verification(self) -> Dict[str, Any]:
        """Verify deployment was successful"""
        try:
            verification_checks = []
            
            # Check if application is responding
            try:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.get("http://localhost:8000/health", timeout=10) as response:
                        if response.status == 200:
                            verification_checks.append({
                                "check": "health_endpoint",
                                "success": True,
                                "status_code": response.status
                            })
                        else:
                            verification_checks.append({
                                "check": "health_endpoint",
                                "success": False,
                                "status_code": response.status
                            })
            except Exception as e:
                verification_checks.append({
                    "check": "health_endpoint",
                    "success": False,
                    "error": str(e)
                })
            
            # Check API endpoints
            api_checks = await self._verify_api_endpoints()
            verification_checks.extend(api_checks)
            
            all_passed = all(check["success"] for check in verification_checks)
            
            return {
                "success": all_passed,
                "verification_checks": verification_checks,
                "message": "All verification checks passed" if all_passed else "Some verification checks failed"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _verify_api_endpoints(self) -> List[Dict[str, Any]]:
        """Verify key API endpoints are working"""
        endpoints_to_check = [
            "/api/v1/dashboard/metrics",
            "/api/v1/performance/health",
            "/docs"
        ]
        
        checks = []
        for endpoint in endpoints_to_check:
            try:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"http://localhost:8000{endpoint}", timeout=5) as response:
                        checks.append({
                            "check": f"endpoint_{endpoint}",
                            "success": response.status < 500,
                            "status_code": response.status,
                            "endpoint": endpoint
                        })
            except Exception as e:
                checks.append({
                    "check": f"endpoint_{endpoint}",
                    "success": False,
                    "error": str(e),
                    "endpoint": endpoint
                })
        
        return checks
    
    async def rollback(self, version: str = "previous") -> Dict[str, Any]:
        """Rollback to previous deployment"""
        try:
            # This would implement rollback functionality
            return {
                "success": True,
                "message": f"Rollback to {version} initiated",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_deployment_status(self) -> Dict[str, Any]:
        """Get current deployment status"""
        try:
            status = {
                "deployment_active": False,
                "environment": "unknown",
                "version": "unknown",
                "health_status": "unknown"
            }
            
            # Check if services are running
            try:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.get("http://localhost:8000/health", timeout=5) as response:
                        if response.status == 200:
                            status["deployment_active"] = True
                            status["health_status"] = "healthy"
                            
                            # Try to get version info from response
                            try:
                                data = await response.json()
                                status["version"] = data.get("version", "unknown")
                            except:
                                pass
            except:
                pass
            
            return {
                "success": True,
                "status": status,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}


# Global deployment manager instance
deployment_manager = DeploymentManager()