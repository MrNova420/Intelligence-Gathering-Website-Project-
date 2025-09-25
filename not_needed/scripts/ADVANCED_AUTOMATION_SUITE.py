#!/usr/bin/env python3
"""
Intelligence Gathering Platform - Advanced Automation Suite
Comprehensive automation system for scripts, monitoring, security, and connections
"""

import os
import sys
import asyncio
import json
import logging
import subprocess
import time
import psutil
import requests
import smtplib
import ssl
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from concurrent.futures import ThreadPoolExecutor
import threading
import queue
import socket
import sqlite3

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation_suite.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class AutomationConfig:
    """Configuration for automation suite"""
    monitoring_interval: int = 60  # seconds
    health_check_interval: int = 30
    backup_interval: int = 3600  # 1 hour
    log_retention_days: int = 30
    alert_email: str = ""
    smtp_server: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    webhook_url: str = ""
    max_cpu_threshold: float = 80.0
    max_memory_threshold: float = 85.0
    max_disk_threshold: float = 90.0
    min_free_disk_gb: float = 5.0

class AdvancedMonitoringSystem:
    """Advanced monitoring with real-time metrics and intelligent alerting"""
    
    def __init__(self, config: AutomationConfig):
        self.config = config
        self.metrics_db = sqlite3.connect('metrics.db', check_same_thread=False)
        self.alert_queue = queue.Queue()
        self.running = False
        self.executor = ThreadPoolExecutor(max_workers=4)
        self._setup_database()
    
    def _setup_database(self):
        """Initialize metrics database"""
        cursor = self.metrics_db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                metric_type TEXT,
                metric_name TEXT,
                value REAL,
                tags TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                severity TEXT,
                message TEXT,
                resolved BOOLEAN DEFAULT FALSE
            )
        ''')
        self.metrics_db.commit()
    
    def record_metric(self, metric_type: str, name: str, value: float, tags: Dict = None):
        """Record a metric to the database"""
        cursor = self.metrics_db.cursor()
        tags_json = json.dumps(tags or {})
        cursor.execute(
            'INSERT INTO metrics (metric_type, metric_name, value, tags) VALUES (?, ?, ?, ?)',
            (metric_type, name, value, tags_json)
        )
        self.metrics_db.commit()
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive system metrics"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'cpu': {
                'percent': psutil.cpu_percent(interval=1),
                'count': psutil.cpu_count(),
                'load_avg': os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]
            },
            'memory': {
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available,
                'percent': psutil.virtual_memory().percent,
                'used': psutil.virtual_memory().used
            },
            'disk': {
                'total': psutil.disk_usage('/').total,
                'used': psutil.disk_usage('/').used,
                'free': psutil.disk_usage('/').free,
                'percent': psutil.disk_usage('/').percent
            },
            'network': {
                'bytes_sent': psutil.net_io_counters().bytes_sent,
                'bytes_recv': psutil.net_io_counters().bytes_recv,
                'packets_sent': psutil.net_io_counters().packets_sent,
                'packets_recv': psutil.net_io_counters().packets_recv
            },
            'processes': {
                'count': len(psutil.pids()),
                'running': len([p for p in psutil.process_iter() if p.status() == 'running'])
            }
        }
        
        # Record metrics
        self.record_metric('system', 'cpu_percent', metrics['cpu']['percent'])
        self.record_metric('system', 'memory_percent', metrics['memory']['percent'])
        self.record_metric('system', 'disk_percent', metrics['disk']['percent'])
        
        return metrics
    
    def check_service_health(self, services: List[Dict]) -> Dict[str, Any]:
        """Check health of configured services"""
        health_status = {
            'timestamp': datetime.now().isoformat(),
            'services': {},
            'overall_status': 'healthy'
        }
        
        for service in services:
            name = service['name']
            health_status['services'][name] = self._check_single_service(service)
            
            if health_status['services'][name]['status'] != 'healthy':
                health_status['overall_status'] = 'unhealthy'
        
        return health_status
    
    def _check_single_service(self, service: Dict) -> Dict[str, Any]:
        """Check health of a single service"""
        try:
            if service['type'] == 'http':
                response = requests.get(
                    service['url'], 
                    timeout=service.get('timeout', 10),
                    verify=service.get('verify_ssl', True)
                )
                return {
                    'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                    'response_time': response.elapsed.total_seconds(),
                    'status_code': response.status_code
                }
            elif service['type'] == 'tcp':
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(service.get('timeout', 10))
                result = sock.connect_ex((service['host'], service['port']))
                sock.close()
                return {
                    'status': 'healthy' if result == 0 else 'unhealthy',
                    'connection': 'successful' if result == 0 else 'failed'
                }
            elif service['type'] == 'process':
                processes = [p.name() for p in psutil.process_iter()]
                return {
                    'status': 'healthy' if service['process_name'] in processes else 'unhealthy',
                    'running': service['process_name'] in processes
                }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def generate_alert(self, severity: str, message: str, service: str = None):
        """Generate an alert"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'severity': severity,
            'message': message,
            'service': service
        }
        
        # Store alert in database
        cursor = self.metrics_db.cursor()
        cursor.execute(
            'INSERT INTO alerts (severity, message) VALUES (?, ?)',
            (severity, message)
        )
        self.metrics_db.commit()
        
        # Queue alert for notification
        self.alert_queue.put(alert)
        logger.warning(f"Alert generated: {severity} - {message}")
    
    def start_monitoring(self):
        """Start the monitoring system"""
        self.running = True
        self.executor.submit(self._monitoring_loop)
        self.executor.submit(self._alert_processor)
        logger.info("Advanced monitoring system started")
    
    def stop_monitoring(self):
        """Stop the monitoring system"""
        self.running = False
        self.executor.shutdown(wait=True)
        self.metrics_db.close()
        logger.info("Advanced monitoring system stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        services = [
            {'name': 'backend', 'type': 'http', 'url': 'http://localhost:8000/health'},
            {'name': 'frontend', 'type': 'http', 'url': 'http://localhost:3000'},
            {'name': 'database', 'type': 'tcp', 'host': 'localhost', 'port': 5432},
            {'name': 'redis', 'type': 'tcp', 'host': 'localhost', 'port': 6379}
        ]
        
        while self.running:
            try:
                # Collect system metrics
                metrics = self.get_system_metrics()
                
                # Check thresholds
                if metrics['cpu']['percent'] > self.config.max_cpu_threshold:
                    self.generate_alert('warning', f"High CPU usage: {metrics['cpu']['percent']}%")
                
                if metrics['memory']['percent'] > self.config.max_memory_threshold:
                    self.generate_alert('warning', f"High memory usage: {metrics['memory']['percent']}%")
                
                if metrics['disk']['percent'] > self.config.max_disk_threshold:
                    self.generate_alert('critical', f"High disk usage: {metrics['disk']['percent']}%")
                
                # Check service health
                health = self.check_service_health(services)
                if health['overall_status'] != 'healthy':
                    self.generate_alert('error', "One or more services are unhealthy")
                
                time.sleep(self.config.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
                time.sleep(30)  # Short delay on error
    
    def _alert_processor(self):
        """Process alerts and send notifications"""
        while self.running:
            try:
                alert = self.alert_queue.get(timeout=5)
                self._send_alert_notification(alert)
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Alert processing error: {e}")
    
    def _send_alert_notification(self, alert: Dict):
        """Send alert notification via email and webhook"""
        try:
            # Email notification
            if self.config.alert_email and self.config.smtp_server:
                self._send_email_alert(alert)
            
            # Webhook notification
            if self.config.webhook_url:
                self._send_webhook_alert(alert)
                
        except Exception as e:
            logger.error(f"Failed to send alert notification: {e}")
    
    def _send_email_alert(self, alert: Dict):
        """Send email alert notification"""
        msg = MimeMultipart()
        msg['From'] = self.config.smtp_user
        msg['To'] = self.config.alert_email
        msg['Subject'] = f"[{alert['severity'].upper()}] Intelligence Platform Alert"
        
        body = f"""
        Alert Details:
        - Severity: {alert['severity']}
        - Message: {alert['message']}
        - Timestamp: {alert['timestamp']}
        - Service: {alert.get('service', 'System')}
        
        Please check the system immediately.
        """
        
        msg.attach(MimeText(body, 'plain'))
        
        context = ssl.create_default_context()
        with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port) as server:
            server.starttls(context=context)
            server.login(self.config.smtp_user, self.config.smtp_password)
            server.send_message(msg)
    
    def _send_webhook_alert(self, alert: Dict):
        """Send webhook alert notification"""
        requests.post(self.config.webhook_url, json=alert, timeout=10)

class EnhancedSecuritySystem:
    """Enhanced security system with automated threat detection"""
    
    def __init__(self):
        self.security_events = []
        self.blocked_ips = set()
        self.login_attempts = {}
        self.running = False
    
    def start_security_monitoring(self):
        """Start security monitoring"""
        self.running = True
        threading.Thread(target=self._security_monitor_loop, daemon=True).start()
        logger.info("Enhanced security monitoring started")
    
    def stop_security_monitoring(self):
        """Stop security monitoring"""
        self.running = False
        logger.info("Enhanced security monitoring stopped")
    
    def _security_monitor_loop(self):
        """Main security monitoring loop"""
        while self.running:
            try:
                self._check_failed_logins()
                self._monitor_system_access()
                self._check_suspicious_processes()
                time.sleep(30)  # Security check every 30 seconds
            except Exception as e:
                logger.error(f"Security monitoring error: {e}")
                time.sleep(60)
    
    def _check_failed_logins(self):
        """Monitor failed login attempts"""
        # This would typically read from log files
        # Placeholder for actual implementation
        pass
    
    def _monitor_system_access(self):
        """Monitor system access patterns"""
        # Monitor network connections, file access, etc.
        connections = psutil.net_connections()
        suspicious_ports = [22, 23, 3389, 445]  # SSH, Telnet, RDP, SMB
        
        for conn in connections:
            if conn.laddr and conn.laddr.port in suspicious_ports:
                if conn.status == 'ESTABLISHED':
                    logger.warning(f"Suspicious connection on port {conn.laddr.port}")
    
    def _check_suspicious_processes(self):
        """Check for suspicious processes"""
        suspicious_names = ['nc', 'netcat', 'nmap', 'sqlmap', 'metasploit']
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if any(sus in proc.info['name'].lower() for sus in suspicious_names):
                    logger.warning(f"Suspicious process detected: {proc.info['name']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    
    def log_security_event(self, event_type: str, description: str, ip_address: str = None):
        """Log a security event"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'description': description,
            'ip_address': ip_address
        }
        self.security_events.append(event)
        logger.warning(f"Security event: {event_type} - {description}")
    
    def block_ip(self, ip_address: str, reason: str):
        """Block an IP address"""
        self.blocked_ips.add(ip_address)
        self.log_security_event('ip_blocked', f"IP {ip_address} blocked: {reason}", ip_address)
        
        # Add iptables rule (Linux only)
        try:
            subprocess.run(['iptables', '-A', 'INPUT', '-s', ip_address, '-j', 'DROP'], 
                         check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to block IP {ip_address}: {e}")

class ConnectionPoolManager:
    """Enhanced connection pool management"""
    
    def __init__(self):
        self.pools = {}
        self.health_checks = {}
    
    def create_database_pool(self, name: str, config: Dict):
        """Create a database connection pool"""
        # This would create actual database connection pools
        self.pools[name] = {
            'type': 'database',
            'config': config,
            'connections': [],
            'max_connections': config.get('max_connections', 10),
            'active_connections': 0
        }
        logger.info(f"Database pool '{name}' created")
    
    def create_redis_pool(self, name: str, config: Dict):
        """Create a Redis connection pool"""
        self.pools[name] = {
            'type': 'redis',
            'config': config,
            'connections': [],
            'max_connections': config.get('max_connections', 5),
            'active_connections': 0
        }
        logger.info(f"Redis pool '{name}' created")
    
    def get_connection(self, pool_name: str):
        """Get a connection from the pool"""
        # Placeholder for actual connection pool implementation
        if pool_name in self.pools:
            return f"Connection from {pool_name}"
        return None
    
    def health_check_pools(self):
        """Perform health checks on all connection pools"""
        healthy_pools = 0
        total_pools = len(self.pools)
        
        for name, pool in self.pools.items():
            if self._check_pool_health(name, pool):
                healthy_pools += 1
        
        return {
            'healthy_pools': healthy_pools,
            'total_pools': total_pools,
            'health_percentage': (healthy_pools / total_pools * 100) if total_pools > 0 else 100
        }
    
    def _check_pool_health(self, name: str, pool: Dict) -> bool:
        """Check health of a specific connection pool"""
        # Placeholder for actual health check logic
        return True

class AutomatedBackupSystem:
    """Automated backup system with rotation and verification"""
    
    def __init__(self, config: AutomationConfig):
        self.config = config
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_database_backup(self) -> str:
        """Create database backup"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"db_backup_{timestamp}.sql"
        
        try:
            # PostgreSQL backup
            cmd = [
                'docker', 'exec', 'intelligence_db',
                'pg_dump', '-U', 'intelligence_user', 'intelligence_db'
            ]
            
            with open(backup_file, 'w') as f:
                subprocess.run(cmd, stdout=f, check=True)
            
            logger.info(f"Database backup created: {backup_file}")
            return str(backup_file)
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Database backup failed: {e}")
            return None
    
    def create_files_backup(self) -> str:
        """Create application files backup"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"files_backup_{timestamp}.tar.gz"
        
        try:
            cmd = [
                'tar', '-czf', str(backup_file),
                '--exclude=node_modules',
                '--exclude=.git',
                '--exclude=__pycache__',
                '--exclude=*.log',
                '.'
            ]
            
            subprocess.run(cmd, check=True)
            logger.info(f"Files backup created: {backup_file}")
            return str(backup_file)
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Files backup failed: {e}")
            return None
    
    def rotate_backups(self, keep_days: int = None):
        """Rotate old backups"""
        keep_days = keep_days or self.config.log_retention_days
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        
        removed = 0
        for backup_file in self.backup_dir.glob("*backup_*.{sql,tar.gz}"):
            if backup_file.stat().st_mtime < cutoff_date.timestamp():
                backup_file.unlink()
                removed += 1
        
        logger.info(f"Removed {removed} old backup files")
    
    def verify_backup(self, backup_file: str) -> bool:
        """Verify backup integrity"""
        try:
            backup_path = Path(backup_file)
            if not backup_path.exists():
                return False
            
            # Basic verification - check file size and readability
            if backup_path.stat().st_size == 0:
                return False
            
            # For SQL files, check basic structure
            if backup_path.suffix == '.sql':
                with open(backup_path, 'r') as f:
                    content = f.read(1000)  # Read first 1KB
                    if 'PostgreSQL database dump' not in content:
                        return False
            
            return True
            
        except Exception as e:
            logger.error(f"Backup verification failed: {e}")
            return False

class AdvancedAutomationSuite:
    """Main automation suite orchestrator"""
    
    def __init__(self):
        self.config = AutomationConfig()
        self.monitoring = AdvancedMonitoringSystem(self.config)
        self.security = EnhancedSecuritySystem()
        self.connections = ConnectionPoolManager()
        self.backup = AutomatedBackupSystem(self.config)
        self.running = False
        
        # Load configuration from file if exists
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file"""
        config_file = Path("automation_config.json")
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config_data = json.load(f)
                    for key, value in config_data.items():
                        if hasattr(self.config, key):
                            setattr(self.config, key, value)
                logger.info("Configuration loaded from automation_config.json")
            except Exception as e:
                logger.error(f"Failed to load configuration: {e}")
    
    def save_config(self):
        """Save current configuration to file"""
        config_data = {
            'monitoring_interval': self.config.monitoring_interval,
            'health_check_interval': self.config.health_check_interval,
            'backup_interval': self.config.backup_interval,
            'log_retention_days': self.config.log_retention_days,
            'alert_email': self.config.alert_email,
            'max_cpu_threshold': self.config.max_cpu_threshold,
            'max_memory_threshold': self.config.max_memory_threshold,
            'max_disk_threshold': self.config.max_disk_threshold
        }
        
        with open("automation_config.json", 'w') as f:
            json.dump(config_data, f, indent=2)
        
        logger.info("Configuration saved to automation_config.json")
    
    def start_all_systems(self):
        """Start all automation systems"""
        logger.info("🚀 Starting Advanced Automation Suite...")
        
        self.running = True
        self.monitoring.start_monitoring()
        self.security.start_security_monitoring()
        
        # Initialize connection pools
        self.connections.create_database_pool('main', {
            'host': 'localhost',
            'port': 5432,
            'database': 'intelligence_db',
            'max_connections': 10
        })
        
        self.connections.create_redis_pool('cache', {
            'host': 'localhost',
            'port': 6379,
            'max_connections': 5
        })
        
        # Start automated backup scheduler
        threading.Thread(target=self._backup_scheduler, daemon=True).start()
        
        logger.info("✅ Advanced Automation Suite started successfully!")
    
    def stop_all_systems(self):
        """Stop all automation systems"""
        logger.info("🛑 Stopping Advanced Automation Suite...")
        
        self.running = False
        self.monitoring.stop_monitoring()
        self.security.stop_security_monitoring()
        
        logger.info("✅ Advanced Automation Suite stopped successfully!")
    
    def _backup_scheduler(self):
        """Automated backup scheduler"""
        while self.running:
            try:
                # Create database backup
                db_backup = self.backup.create_database_backup()
                if db_backup and self.backup.verify_backup(db_backup):
                    logger.info("✅ Database backup completed and verified")
                else:
                    logger.error("❌ Database backup failed or verification failed")
                
                # Create files backup
                files_backup = self.backup.create_files_backup()
                if files_backup and self.backup.verify_backup(files_backup):
                    logger.info("✅ Files backup completed and verified")
                else:
                    logger.error("❌ Files backup failed or verification failed")
                
                # Rotate old backups
                self.backup.rotate_backups()
                
                # Wait for next backup cycle
                time.sleep(self.config.backup_interval)
                
            except Exception as e:
                logger.error(f"Backup scheduler error: {e}")
                time.sleep(300)  # Wait 5 minutes on error
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            'timestamp': datetime.now().isoformat(),
            'automation_suite': {
                'running': self.running,
                'uptime': time.time() - getattr(self, 'start_time', time.time())
            },
            'monitoring': self.monitoring.get_system_metrics(),
            'security': {
                'events_count': len(self.security.security_events),
                'blocked_ips': len(self.security.blocked_ips)
            },
            'connections': self.connections.health_check_pools(),
            'backups': {
                'backup_dir': str(self.backup.backup_dir),
                'backup_count': len(list(self.backup.backup_dir.glob("*backup_*")))
            }
        }
    
    def generate_status_report(self) -> str:
        """Generate comprehensive status report"""
        status = self.get_system_status()
        
        report = f"""
🚀 INTELLIGENCE GATHERING PLATFORM - AUTOMATION STATUS REPORT
============================================================
Generated: {status['timestamp']}

🔧 AUTOMATION SUITE STATUS:
- Running: {'✅ Yes' if status['automation_suite']['running'] else '❌ No'}
- Uptime: {status['automation_suite']['uptime']:.2f} seconds

📊 SYSTEM MONITORING:
- CPU Usage: {status['monitoring']['cpu']['percent']:.1f}%
- Memory Usage: {status['monitoring']['memory']['percent']:.1f}%
- Disk Usage: {status['monitoring']['disk']['percent']:.1f}%
- Active Processes: {status['monitoring']['processes']['count']}

🔒 SECURITY STATUS:
- Security Events: {status['security']['events_count']}
- Blocked IPs: {status['security']['blocked_ips']}

🔗 CONNECTION POOLS:
- Healthy Pools: {status['connections']['healthy_pools']}/{status['connections']['total_pools']}
- Health Percentage: {status['connections']['health_percentage']:.1f}%

💾 BACKUP STATUS:
- Total Backups: {status['backups']['backup_count']}
- Backup Directory: {status['backups']['backup_dir']}

============================================================
        """
        
        return report.strip()

def main():
    """Main entry point for the automation suite"""
    suite = AdvancedAutomationSuite()
    
    try:
        print("🚀 Intelligence Gathering Platform - Advanced Automation Suite")
        print("=" * 70)
        
        # Start all systems
        suite.start_all_systems()
        suite.start_time = time.time()
        
        # Keep running and provide status updates
        while True:
            time.sleep(300)  # Status update every 5 minutes
            print(suite.generate_status_report())
            
    except KeyboardInterrupt:
        print("\n⏹️ Shutdown requested...")
        suite.stop_all_systems()
        print("✅ Advanced Automation Suite stopped")
    
    except Exception as e:
        logger.error(f"Automation suite error: {e}")
        suite.stop_all_systems()
        sys.exit(1)

if __name__ == "__main__":
    main()