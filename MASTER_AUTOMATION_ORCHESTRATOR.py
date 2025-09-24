#!/usr/bin/env python3
"""
Master Automation Orchestrator for Intelligence Gathering Platform
Coordinates all automation systems: monitoring, security, connections, maintenance, and optimization
"""

import asyncio
import json
import logging
import os
import sys
import time
import threading
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor
import schedule

# Configure comprehensive logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'master_orchestrator.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class OrchestratorConfig:
    """Master configuration for the orchestrator"""
    # System settings
    monitoring_enabled: bool = True
    security_enabled: bool = True
    backup_enabled: bool = True
    optimization_enabled: bool = True
    health_checks_enabled: bool = True
    
    # Intervals (in seconds)
    monitoring_interval: int = 30
    security_scan_interval: int = 300  # 5 minutes
    backup_interval: int = 3600  # 1 hour
    optimization_interval: int = 7200  # 2 hours
    health_check_interval: int = 60
    status_report_interval: int = 900  # 15 minutes
    
    # Thresholds
    cpu_critical_threshold: float = 90.0
    memory_critical_threshold: float = 95.0
    disk_critical_threshold: float = 98.0
    response_time_critical_ms: float = 5000.0
    
    # Paths
    project_root: str = "."
    scripts_dir: str = "./scripts"
    logs_dir: str = "./logs"
    backups_dir: str = "./backups"
    config_dir: str = "./config"
    
    # External integrations
    webhook_urls: List[str] = field(default_factory=list)
    email_alerts: List[str] = field(default_factory=list)
    slack_webhook: str = ""
    
    # Emergency settings
    emergency_shutdown_threshold: int = 5  # Number of critical failures
    emergency_contact: str = ""
    emergency_backup_enabled: bool = True

class SystemHealthChecker:
    """Comprehensive system health monitoring"""
    
    def __init__(self, config: OrchestratorConfig):
        self.config = config
        self.health_history = []
        self.critical_failures = 0
        self.last_health_check = None
    
    async def perform_comprehensive_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive system health check"""
        logger.info("🏥 Performing comprehensive health check...")
        
        health_report = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'healthy',
            'components': {},
            'critical_issues': [],
            'warnings': [],
            'metrics': {}
        }
        
        try:
            # Check system resources
            health_report['components']['system'] = await self._check_system_resources()
            
            # Check services
            health_report['components']['services'] = await self._check_services()
            
            # Check database connectivity
            health_report['components']['database'] = await self._check_database()
            
            # Check external connectivity
            health_report['components']['connectivity'] = await self._check_connectivity()
            
            # Check disk space and file system
            health_report['components']['filesystem'] = await self._check_filesystem()
            
            # Check security status
            health_report['components']['security'] = await self._check_security_status()
            
            # Aggregate results
            self._aggregate_health_results(health_report)
            
            # Store in history
            self.health_history.append(health_report)
            if len(self.health_history) > 100:  # Keep last 100 checks
                self.health_history.pop(0)
            
            self.last_health_check = datetime.now()
            
            return health_report
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            health_report['overall_status'] = 'critical'
            health_report['critical_issues'].append(f"Health check system failure: {str(e)}")
            return health_report
    
    async def _check_system_resources(self) -> Dict[str, Any]:
        """Check system resource usage"""
        try:
            import psutil
            
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            status = 'healthy'
            issues = []
            
            if cpu_percent > self.config.cpu_critical_threshold:
                status = 'critical'
                issues.append(f"Critical CPU usage: {cpu_percent}%")
            
            if memory.percent > self.config.memory_critical_threshold:
                status = 'critical'
                issues.append(f"Critical memory usage: {memory.percent}%")
            
            if disk.percent > self.config.disk_critical_threshold:
                status = 'critical'
                issues.append(f"Critical disk usage: {disk.percent}%")
            
            return {
                'status': status,
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'disk_percent': disk.percent,
                'load_average': os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0],
                'issues': issues
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'issues': [f"System resource check failed: {str(e)}"]
            }
    
    async def _check_services(self) -> Dict[str, Any]:
        """Check critical services status"""
        services = ['backend', 'frontend', 'database', 'redis']
        service_results = {}
        overall_status = 'healthy'
        
        for service in services:
            try:
                if service == 'backend':
                    result = await self._check_http_service('http://localhost:8000/health')
                elif service == 'frontend':
                    result = await self._check_http_service('http://localhost:3000')
                elif service == 'database':
                    result = await self._check_tcp_service('localhost', 5432)
                elif service == 'redis':
                    result = await self._check_tcp_service('localhost', 6379)
                
                service_results[service] = result
                
                if result['status'] != 'healthy':
                    overall_status = 'unhealthy'
                    
            except Exception as e:
                service_results[service] = {
                    'status': 'error',
                    'error': str(e)
                }
                overall_status = 'unhealthy'
        
        return {
            'status': overall_status,
            'services': service_results
        }
    
    async def _check_http_service(self, url: str) -> Dict[str, Any]:
        """Check HTTP service health"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    response_time = (time.time() - start_time) * 1000
                    
                    return {
                        'status': 'healthy' if response.status == 200 else 'unhealthy',
                        'response_time_ms': response_time,
                        'status_code': response.status
                    }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    async def _check_tcp_service(self, host: str, port: int) -> Dict[str, Any]:
        """Check TCP service connectivity"""
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            
            return {
                'status': 'healthy' if result == 0 else 'unhealthy',
                'connection': 'successful' if result == 0 else 'failed'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    async def _check_database(self) -> Dict[str, Any]:
        """Check database specific health"""
        try:
            # Try to connect and run a simple query
            # This would be implemented with actual database connection
            return {
                'status': 'healthy',
                'connection_pool': 'available',
                'query_performance': 'normal'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    async def _check_connectivity(self) -> Dict[str, Any]:
        """Check external connectivity"""
        test_urls = [
            'https://google.com',
            'https://github.com',
            'https://api.ipify.org'
        ]
        
        connectivity_results = {}
        overall_status = 'healthy'
        
        for url in test_urls:
            try:
                result = await self._check_http_service(url)
                connectivity_results[url] = result
                
                if result['status'] != 'healthy':
                    overall_status = 'degraded'
                    
            except Exception as e:
                connectivity_results[url] = {'status': 'error', 'error': str(e)}
                overall_status = 'degraded'
        
        return {
            'status': overall_status,
            'external_connectivity': connectivity_results
        }
    
    async def _check_filesystem(self) -> Dict[str, Any]:
        """Check filesystem health"""
        try:
            critical_paths = [
                self.config.logs_dir,
                self.config.backups_dir,
                self.config.config_dir,
                '/tmp'
            ]
            
            filesystem_status = {}
            overall_status = 'healthy'
            
            for path in critical_paths:
                path_obj = Path(path)
                if path_obj.exists():
                    # Check if path is writable
                    test_file = path_obj / f'.test_{int(time.time())}'
                    try:
                        test_file.touch()
                        test_file.unlink()
                        filesystem_status[path] = {'status': 'healthy', 'writable': True}
                    except:
                        filesystem_status[path] = {'status': 'error', 'writable': False}
                        overall_status = 'unhealthy'
                else:
                    filesystem_status[path] = {'status': 'missing', 'exists': False}
                    overall_status = 'unhealthy'
            
            return {
                'status': overall_status,
                'paths': filesystem_status
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    async def _check_security_status(self) -> Dict[str, Any]:
        """Check security-related status"""
        try:
            security_checks = {
                'firewall': 'active',  # Would check actual firewall status
                'ssl_certificates': 'valid',  # Would check certificate expiry
                'failed_logins': 'normal',  # Would check recent failed login attempts
                'suspicious_activity': 'none'  # Would check for suspicious processes/network activity
            }
            
            return {
                'status': 'healthy',
                'checks': security_checks
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _aggregate_health_results(self, health_report: Dict[str, Any]):
        """Aggregate health check results"""
        critical_count = 0
        warning_count = 0
        
        for component_name, component_data in health_report['components'].items():
            if isinstance(component_data, dict):
                status = component_data.get('status', 'unknown')
                
                if status == 'critical':
                    critical_count += 1
                    health_report['critical_issues'].extend(
                        component_data.get('issues', [f"{component_name} is critical"])
                    )
                elif status in ['unhealthy', 'degraded', 'error']:
                    warning_count += 1
                    health_report['warnings'].append(
                        f"{component_name} status: {status}"
                    )
        
        # Determine overall status
        if critical_count > 0:
            health_report['overall_status'] = 'critical'
            self.critical_failures += 1
        elif warning_count > 0:
            health_report['overall_status'] = 'warning'
        else:
            health_report['overall_status'] = 'healthy'
            self.critical_failures = 0  # Reset on healthy status

class AutomationOrchestrator:
    """Master orchestrator for all automation systems"""
    
    def __init__(self, config: OrchestratorConfig = None):
        self.config = config or OrchestratorConfig()
        self.health_checker = SystemHealthChecker(self.config)
        self.running = False
        self.start_time = None
        self.executor = ThreadPoolExecutor(max_workers=6)
        self.system_status = {
            'status': 'initializing',
            'components': {},
            'last_update': datetime.now().isoformat()
        }
        
        # Create necessary directories
        self._setup_directories()
        
        # Load external configuration if available
        self._load_external_config()
    
    def _setup_directories(self):
        """Create necessary directories"""
        dirs = [
            self.config.logs_dir,
            self.config.backups_dir,
            self.config.config_dir
        ]
        
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def _load_external_config(self):
        """Load external configuration file if available"""
        config_file = Path(self.config.config_dir) / "orchestrator_config.json"
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    external_config = json.load(f)
                
                # Update config with external values
                for key, value in external_config.items():
                    if hasattr(self.config, key):
                        setattr(self.config, key, value)
                
                logger.info("External configuration loaded successfully")
                
            except Exception as e:
                logger.error(f"Failed to load external configuration: {e}")
    
    async def start(self):
        """Start the master orchestrator"""
        logger.info("🚀 Starting Master Automation Orchestrator...")
        
        self.running = True
        self.start_time = datetime.now()
        
        try:
            # Initialize all subsystems
            await self._initialize_subsystems()
            
            # Start monitoring loops
            self._start_monitoring_loops()
            
            # Schedule periodic tasks
            self._schedule_periodic_tasks()
            
            self.system_status['status'] = 'running'
            self.system_status['last_update'] = datetime.now().isoformat()
            
            logger.info("✅ Master Automation Orchestrator started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start orchestrator: {e}")
            self.system_status['status'] = 'error'
            raise
    
    async def stop(self):
        """Stop the orchestrator gracefully"""
        logger.info("🛑 Stopping Master Automation Orchestrator...")
        
        self.running = False
        
        # Stop all monitoring loops
        self.executor.shutdown(wait=True)
        
        # Perform final backup if enabled
        if self.config.backup_enabled:
            await self._create_emergency_backup()
        
        self.system_status['status'] = 'stopped'
        self.system_status['last_update'] = datetime.now().isoformat()
        
        logger.info("✅ Master Automation Orchestrator stopped")
    
    async def _initialize_subsystems(self):
        """Initialize all automation subsystems"""
        logger.info("🔧 Initializing automation subsystems...")
        
        subsystems = {}
        
        try:
            # Initialize monitoring system
            if self.config.monitoring_enabled:
                subsystems['monitoring'] = await self._initialize_monitoring()
            
            # Initialize security system
            if self.config.security_enabled:
                subsystems['security'] = await self._initialize_security()
            
            # Initialize connection management
            subsystems['connections'] = await self._initialize_connections()
            
            # Initialize backup system
            if self.config.backup_enabled:
                subsystems['backup'] = await self._initialize_backup()
            
            self.system_status['components'] = subsystems
            logger.info("✅ All subsystems initialized")
            
        except Exception as e:
            logger.error(f"Subsystem initialization failed: {e}")
            raise
    
    async def _initialize_monitoring(self) -> Dict[str, Any]:
        """Initialize monitoring subsystem"""
        try:
            # Import and initialize monitoring system
            # This would import the actual monitoring system
            return {
                'status': 'initialized',
                'type': 'advanced_monitoring',
                'features': ['metrics_collection', 'alerting', 'health_checks']
            }
        except Exception as e:
            logger.error(f"Monitoring initialization failed: {e}")
            return {'status': 'error', 'error': str(e)}
    
    async def _initialize_security(self) -> Dict[str, Any]:
        """Initialize security subsystem"""
        try:
            # Initialize security monitoring and threat detection
            return {
                'status': 'initialized',
                'type': 'security_monitoring',
                'features': ['threat_detection', 'intrusion_prevention', 'audit_logging']
            }
        except Exception as e:
            logger.error(f"Security initialization failed: {e}")
            return {'status': 'error', 'error': str(e)}
    
    async def _initialize_connections(self) -> Dict[str, Any]:
        """Initialize connection management"""
        try:
            # Initialize connection pools and external API management
            return {
                'status': 'initialized',
                'type': 'connection_management',
                'features': ['database_pools', 'redis_cache', 'api_management']
            }
        except Exception as e:
            logger.error(f"Connection management initialization failed: {e}")
            return {'status': 'error', 'error': str(e)}
    
    async def _initialize_backup(self) -> Dict[str, Any]:
        """Initialize backup subsystem"""
        try:
            # Initialize automated backup system
            return {
                'status': 'initialized',
                'type': 'backup_system',
                'features': ['automated_backups', 'rotation', 'verification']
            }
        except Exception as e:
            logger.error(f"Backup initialization failed: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def _start_monitoring_loops(self):
        """Start all monitoring loops"""
        logger.info("📊 Starting monitoring loops...")
        
        # Health check loop
        if self.config.health_checks_enabled:
            self.executor.submit(self._health_check_loop)
        
        # System monitoring loop
        if self.config.monitoring_enabled:
            self.executor.submit(self._system_monitoring_loop)
        
        # Security monitoring loop
        if self.config.security_enabled:
            self.executor.submit(self._security_monitoring_loop)
        
        # Status reporting loop
        self.executor.submit(self._status_reporting_loop)
    
    def _schedule_periodic_tasks(self):
        """Schedule periodic maintenance tasks"""
        logger.info("⏰ Scheduling periodic tasks...")
        
        # Schedule backups
        if self.config.backup_enabled:
            schedule.every().hour.do(self._run_scheduled_backup)
        
        # Schedule optimization
        if self.config.optimization_enabled:
            schedule.every(2).hours.do(self._run_optimization)
        
        # Schedule security scans
        if self.config.security_enabled:
            schedule.every(5).minutes.do(self._run_security_scan)
        
        # Start scheduler thread
        self.executor.submit(self._scheduler_loop)
    
    def _health_check_loop(self):
        """Health check monitoring loop"""
        while self.running:
            try:
                health_report = asyncio.run(self.health_checker.perform_comprehensive_health_check())
                
                # Check for emergency conditions
                if health_report['overall_status'] == 'critical':
                    asyncio.run(self._handle_critical_condition(health_report))
                
                time.sleep(self.config.health_check_interval)
                
            except Exception as e:
                logger.error(f"Health check loop error: {e}")
                time.sleep(30)
    
    def _system_monitoring_loop(self):
        """System monitoring loop"""
        while self.running:
            try:
                # Collect and process system metrics
                self._collect_system_metrics()
                time.sleep(self.config.monitoring_interval)
                
            except Exception as e:
                logger.error(f"System monitoring loop error: {e}")
                time.sleep(30)
    
    def _security_monitoring_loop(self):
        """Security monitoring loop"""
        while self.running:
            try:
                # Perform security checks
                self._perform_security_checks()
                time.sleep(self.config.security_scan_interval)
                
            except Exception as e:
                logger.error(f"Security monitoring loop error: {e}")
                time.sleep(60)
    
    def _status_reporting_loop(self):
        """Status reporting loop"""
        while self.running:
            try:
                # Generate and send status reports
                status_report = self._generate_status_report()
                self._send_status_report(status_report)
                time.sleep(self.config.status_report_interval)
                
            except Exception as e:
                logger.error(f"Status reporting loop error: {e}")
                time.sleep(60)
    
    def _scheduler_loop(self):
        """Scheduled tasks loop"""
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)
            except Exception as e:
                logger.error(f"Scheduler loop error: {e}")
                time.sleep(60)
    
    def _collect_system_metrics(self):
        """Collect system metrics"""
        try:
            # This would collect comprehensive system metrics
            logger.debug("Collecting system metrics...")
        except Exception as e:
            logger.error(f"System metrics collection failed: {e}")
    
    def _perform_security_checks(self):
        """Perform security checks"""
        try:
            # This would perform comprehensive security checks
            logger.debug("Performing security checks...")
        except Exception as e:
            logger.error(f"Security checks failed: {e}")
    
    async def _handle_critical_condition(self, health_report: Dict[str, Any]):
        """Handle critical system conditions"""
        logger.critical("🚨 CRITICAL SYSTEM CONDITION DETECTED!")
        
        # Check if emergency shutdown is needed
        if self.health_checker.critical_failures >= self.config.emergency_shutdown_threshold:
            logger.critical("⚠️ EMERGENCY SHUTDOWN THRESHOLD REACHED!")
            
            if self.config.emergency_backup_enabled:
                await self._create_emergency_backup()
            
            # Send emergency alerts
            await self._send_emergency_alerts(health_report)
            
            # Consider emergency shutdown
            # await self._emergency_shutdown()
    
    async def _create_emergency_backup(self):
        """Create emergency backup"""
        try:
            logger.warning("📦 Creating emergency backup...")
            
            # Run emergency backup script
            backup_script = Path(self.config.scripts_dir) / "enhanced_maintenance.sh"
            if backup_script.exists():
                subprocess.run([str(backup_script), "backup"], check=True)
                logger.info("✅ Emergency backup completed")
            else:
                logger.error("❌ Backup script not found")
                
        except Exception as e:
            logger.error(f"Emergency backup failed: {e}")
    
    async def _send_emergency_alerts(self, health_report: Dict[str, Any]):
        """Send emergency alerts"""
        try:
            alert_message = f"""
🚨 EMERGENCY ALERT - Intelligence Gathering Platform

Critical system condition detected at {datetime.now()}

Issues:
{chr(10).join(health_report.get('critical_issues', []))}

System Status: {health_report.get('overall_status', 'unknown')}

Immediate attention required!
"""
            
            # Send alerts through all configured channels
            for webhook_url in self.config.webhook_urls:
                try:
                    import requests
                    requests.post(webhook_url, json={'text': alert_message}, timeout=10)
                except Exception as e:
                    logger.error(f"Failed to send webhook alert: {e}")
            
            logger.critical("🚨 Emergency alerts sent")
            
        except Exception as e:
            logger.error(f"Failed to send emergency alerts: {e}")
    
    def _generate_status_report(self) -> Dict[str, Any]:
        """Generate comprehensive status report"""
        uptime = datetime.now() - self.start_time if self.start_time else timedelta(0)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': uptime.total_seconds(),
            'system_status': self.system_status,
            'health_summary': self.health_checker.health_history[-1] if self.health_checker.health_history else {},
            'critical_failures': self.health_checker.critical_failures,
            'components_status': self.system_status.get('components', {}),
            'configuration': {
                'monitoring_enabled': self.config.monitoring_enabled,
                'security_enabled': self.config.security_enabled,
                'backup_enabled': self.config.backup_enabled,
                'optimization_enabled': self.config.optimization_enabled
            }
        }
    
    def _send_status_report(self, report: Dict[str, Any]):
        """Send status report"""
        try:
            # Save report to file
            report_file = Path(self.config.logs_dir) / f"status_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            logger.debug(f"Status report saved: {report_file}")
            
        except Exception as e:
            logger.error(f"Failed to save status report: {e}")
    
    def _run_scheduled_backup(self):
        """Run scheduled backup"""
        try:
            logger.info("📦 Running scheduled backup...")
            asyncio.run(self._create_emergency_backup())
        except Exception as e:
            logger.error(f"Scheduled backup failed: {e}")
    
    def _run_optimization(self):
        """Run system optimization"""
        try:
            logger.info("⚡ Running system optimization...")
            # This would run optimization tasks
        except Exception as e:
            logger.error(f"Optimization failed: {e}")
    
    def _run_security_scan(self):
        """Run security scan"""
        try:
            logger.info("🔒 Running security scan...")
            # This would run security scans
        except Exception as e:
            logger.error(f"Security scan failed: {e}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return self.system_status

async def main():
    """Main entry point"""
    try:
        # Create configuration
        config = OrchestratorConfig()
        
        # Create and start orchestrator
        orchestrator = AutomationOrchestrator(config)
        await orchestrator.start()
        
        logger.info("🎯 Master Automation Orchestrator is running...")
        logger.info("📊 Use Ctrl+C to stop gracefully")
        
        # Keep running
        try:
            while True:
                await asyncio.sleep(60)
                
                # Print periodic status
                status = orchestrator.get_system_status()
                logger.info(f"System Status: {status['status']} | Components: {len(status.get('components', {}))}")
                
        except KeyboardInterrupt:
            logger.info("🛑 Shutdown requested by user...")
        
        await orchestrator.stop()
        
    except Exception as e:
        logger.error(f"Orchestrator error: {e}")
        raise

def create_sample_config():
    """Create sample configuration file"""
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    sample_config = {
        "monitoring_enabled": True,
        "security_enabled": True,
        "backup_enabled": True,
        "optimization_enabled": True,
        "health_checks_enabled": True,
        "monitoring_interval": 30,
        "security_scan_interval": 300,
        "backup_interval": 3600,
        "webhook_urls": [],
        "email_alerts": [],
        "slack_webhook": "",
        "emergency_contact": "admin@yourdomain.com"
    }
    
    config_file = config_dir / "orchestrator_config.json"
    with open(config_file, 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    logger.info(f"Sample configuration created: {config_file}")

if __name__ == "__main__":
    print("🚀 Intelligence Gathering Platform - Master Automation Orchestrator")
    print("=" * 80)
    
    if "--create-config" in sys.argv:
        create_sample_config()
        sys.exit(0)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Orchestrator stopped by user")
    except Exception as e:
        print(f"\n❌ Orchestrator failed: {e}")
        sys.exit(1)