#!/usr/bin/env python3
"""
Advanced Performance Monitoring and Metrics System
Provides comprehensive monitoring, alerting, and metrics collection
"""

import time
import psutil
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import json
import threading
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetric:
    """Individual performance metric data point"""
    timestamp: datetime
    metric_name: str
    value: float
    tags: Dict[str, str]
    unit: str = ""

@dataclass
class SystemMetrics:
    """System resource metrics"""
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    disk_usage_percent: float
    disk_free_gb: float
    load_average_1m: float
    load_average_5m: float
    load_average_15m: float
    network_bytes_sent: int
    network_bytes_recv: int
    active_connections: int
    timestamp: datetime

@dataclass
class ApplicationMetrics:
    """Application-specific metrics"""
    requests_per_minute: float
    average_response_time: float
    error_rate: float
    active_users: int
    database_connections: int
    cache_hit_rate: float
    queue_size: int
    timestamp: datetime

class MetricsCollector:
    """Collects and stores performance metrics"""
    
    def __init__(self, max_history: int = 1440):  # 24 hours of minute-by-minute data
        self.max_history = max_history
        self.metrics_history: deque = deque(maxlen=max_history)
        self.system_metrics_history: deque = deque(maxlen=max_history)
        self.app_metrics_history: deque = deque(maxlen=max_history)
        
        # Real-time counters
        self.request_counter: int = 0
        self.error_counter: int = 0
        self.response_times: deque = deque(maxlen=1000)
        self.active_connections: int = 0
        
        # Threading lock for thread-safe operations
        self.lock = threading.Lock()
        
        # Auto-collection settings
        self.collection_interval = 60  # seconds
        self.auto_collect = True
        self._collection_thread: Optional[threading.Thread] = None
        
        logger.info("📊 Performance Metrics Collector initialized")
    
    def start_auto_collection(self):
        """Start automatic metrics collection"""
        if self._collection_thread is None or not self._collection_thread.is_alive():
            self.auto_collect = True
            self._collection_thread = threading.Thread(target=self._collect_loop, daemon=True)
            self._collection_thread.start()
            logger.info("🔄 Started automatic metrics collection")
    
    def stop_auto_collection(self):
        """Stop automatic metrics collection"""
        self.auto_collect = False
        if self._collection_thread:
            self._collection_thread.join(timeout=5)
        logger.info("⏹️ Stopped automatic metrics collection")
    
    def _collect_loop(self):
        """Background thread for automatic metrics collection"""
        while self.auto_collect:
            try:
                self.collect_system_metrics()
                self.collect_application_metrics()
                time.sleep(self.collection_interval)
            except Exception as e:
                logger.error(f"Error in metrics collection loop: {e}")
                time.sleep(10)  # Wait before retrying
    
    def collect_system_metrics(self) -> SystemMetrics:
        """Collect system resource metrics"""
        try:
            # CPU and Memory
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            # Disk usage
            disk = psutil.disk_usage('/')
            
            # Load average (Unix-like systems)
            try:
                load_avg = psutil.getloadavg()
                load_1m, load_5m, load_15m = load_avg
            except (AttributeError, OSError):
                # Windows doesn't have load average
                load_1m = load_5m = load_15m = cpu_percent / 100.0
            
            # Network I/O
            try:
                network = psutil.net_io_counters()
                bytes_sent = network.bytes_sent
                bytes_recv = network.bytes_recv
            except (AttributeError, OSError):
                bytes_sent = bytes_recv = 0
            
            metrics = SystemMetrics(
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_used_mb=memory.used / (1024 * 1024),
                memory_available_mb=memory.available / (1024 * 1024),
                disk_usage_percent=disk.percent,
                disk_free_gb=disk.free / (1024 * 1024 * 1024),
                load_average_1m=load_1m,
                load_average_5m=load_5m,
                load_average_15m=load_15m,
                network_bytes_sent=bytes_sent,
                network_bytes_recv=bytes_recv,
                active_connections=self.active_connections,
                timestamp=datetime.now()
            )
            
            with self.lock:
                self.system_metrics_history.append(metrics)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            return SystemMetrics(
                cpu_percent=0, memory_percent=0, memory_used_mb=0,
                memory_available_mb=0, disk_usage_percent=0, disk_free_gb=0,
                load_average_1m=0, load_average_5m=0, load_average_15m=0,
                network_bytes_sent=0, network_bytes_recv=0,
                active_connections=0, timestamp=datetime.now()
            )
    
    def collect_application_metrics(self) -> ApplicationMetrics:
        """Collect application-specific metrics"""
        try:
            with self.lock:
                # Calculate requests per minute
                now = datetime.now()
                one_minute_ago = now - timedelta(minutes=1)
                
                # Response time calculation
                avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
                
                # Error rate calculation
                total_requests = self.request_counter if self.request_counter > 0 else 1
                error_rate = (self.error_counter / total_requests) * 100
                
                metrics = ApplicationMetrics(
                    requests_per_minute=self.request_counter,  # Simplified for now
                    average_response_time=avg_response_time,
                    error_rate=error_rate,
                    active_users=0,  # Would need session tracking
                    database_connections=0,  # Would need DB connection pool info
                    cache_hit_rate=0,  # Would need cache metrics
                    queue_size=0,  # Would need queue monitoring
                    timestamp=now
                )
                
                self.app_metrics_history.append(metrics)
                
                # Reset counters for next collection period
                self.request_counter = 0
                self.error_counter = 0
                
                return metrics
                
        except Exception as e:
            logger.error(f"Error collecting application metrics: {e}")
            return ApplicationMetrics(
                requests_per_minute=0, average_response_time=0, error_rate=0,
                active_users=0, database_connections=0, cache_hit_rate=0,
                queue_size=0, timestamp=datetime.now()
            )
    
    def record_request(self, response_time: float):
        """Record a request with its response time"""
        with self.lock:
            self.request_counter += 1
            self.response_times.append(response_time)
    
    def record_error(self):
        """Record an error occurrence"""
        with self.lock:
            self.error_counter += 1
    
    def increment_connections(self):
        """Increment active connections counter"""
        with self.lock:
            self.active_connections += 1
    
    def decrement_connections(self):
        """Decrement active connections counter"""
        with self.lock:
            self.active_connections = max(0, self.active_connections - 1)
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics summary"""
        system_metrics = self.collect_system_metrics()
        app_metrics = self.collect_application_metrics()
        
        return {
            "system": asdict(system_metrics),
            "application": asdict(app_metrics),
            "collection_time": datetime.now().isoformat()
        }
    
    def get_metrics_history(self, hours: int = 1) -> Dict[str, List[Dict]]:
        """Get metrics history for specified number of hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        with self.lock:
            system_history = [
                asdict(m) for m in self.system_metrics_history 
                if m.timestamp >= cutoff_time
            ]
            app_history = [
                asdict(m) for m in self.app_metrics_history 
                if m.timestamp >= cutoff_time
            ]
        
        return {
            "system_metrics": system_history,
            "application_metrics": app_history,
            "period_hours": hours
        }
    
    def save_metrics_to_file(self, filepath: str):
        """Save current metrics to JSON file"""
        try:
            metrics_data = {
                "export_time": datetime.now().isoformat(),
                "system_metrics": [asdict(m) for m in self.system_metrics_history],
                "application_metrics": [asdict(m) for m in self.app_metrics_history]
            }
            
            with open(filepath, 'w') as f:
                json.dump(metrics_data, f, indent=2, default=str)
            
            logger.info(f"📁 Metrics saved to {filepath}")
            
        except Exception as e:
            logger.error(f"Error saving metrics to file: {e}")

class PerformanceAlerting:
    """Performance alerting system"""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        self.alerts_config = {
            "cpu_threshold": 80.0,
            "memory_threshold": 85.0,
            "disk_threshold": 90.0,
            "response_time_threshold": 2.0,
            "error_rate_threshold": 5.0
        }
        self.alert_history: List[Dict] = []
        logger.info("🚨 Performance Alerting system initialized")
    
    def check_alerts(self) -> List[Dict[str, Any]]:
        """Check current metrics against alert thresholds"""
        alerts = []
        
        try:
            current_metrics = self.metrics_collector.get_current_metrics()
            system = current_metrics["system"]
            app = current_metrics["application"]
            
            # CPU Alert
            if system["cpu_percent"] > self.alerts_config["cpu_threshold"]:
                alerts.append({
                    "type": "HIGH_CPU",
                    "severity": "WARNING",
                    "message": f"CPU usage is {system['cpu_percent']:.1f}% (threshold: {self.alerts_config['cpu_threshold']}%)",
                    "value": system["cpu_percent"],
                    "threshold": self.alerts_config["cpu_threshold"],
                    "timestamp": datetime.now().isoformat()
                })
            
            # Memory Alert
            if system["memory_percent"] > self.alerts_config["memory_threshold"]:
                alerts.append({
                    "type": "HIGH_MEMORY",
                    "severity": "WARNING",
                    "message": f"Memory usage is {system['memory_percent']:.1f}% (threshold: {self.alerts_config['memory_threshold']}%)",
                    "value": system["memory_percent"],
                    "threshold": self.alerts_config["memory_threshold"],
                    "timestamp": datetime.now().isoformat()
                })
            
            # Disk Alert
            if system["disk_usage_percent"] > self.alerts_config["disk_threshold"]:
                alerts.append({
                    "type": "HIGH_DISK_USAGE",
                    "severity": "CRITICAL",
                    "message": f"Disk usage is {system['disk_usage_percent']:.1f}% (threshold: {self.alerts_config['disk_threshold']}%)",
                    "value": system["disk_usage_percent"],
                    "threshold": self.alerts_config["disk_threshold"],
                    "timestamp": datetime.now().isoformat()
                })
            
            # Response Time Alert
            if app["average_response_time"] > self.alerts_config["response_time_threshold"]:
                alerts.append({
                    "type": "SLOW_RESPONSE",
                    "severity": "WARNING",
                    "message": f"Average response time is {app['average_response_time']:.2f}s (threshold: {self.alerts_config['response_time_threshold']}s)",
                    "value": app["average_response_time"],
                    "threshold": self.alerts_config["response_time_threshold"],
                    "timestamp": datetime.now().isoformat()
                })
            
            # Error Rate Alert
            if app["error_rate"] > self.alerts_config["error_rate_threshold"]:
                alerts.append({
                    "type": "HIGH_ERROR_RATE",
                    "severity": "CRITICAL",
                    "message": f"Error rate is {app['error_rate']:.1f}% (threshold: {self.alerts_config['error_rate_threshold']}%)",
                    "value": app["error_rate"],
                    "threshold": self.alerts_config["error_rate_threshold"],
                    "timestamp": datetime.now().isoformat()
                })
            
            # Store alerts in history
            for alert in alerts:
                self.alert_history.append(alert)
                logger.warning(f"🚨 ALERT: {alert['message']}")
            
            # Keep only last 100 alerts
            self.alert_history = self.alert_history[-100:]
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error checking alerts: {e}")
            return []

# Global metrics collector instance
metrics_collector = MetricsCollector()
performance_alerting = PerformanceAlerting(metrics_collector)

def get_performance_summary() -> Dict[str, Any]:
    """Get comprehensive performance summary"""
    try:
        current_metrics = metrics_collector.get_current_metrics()
        alerts = performance_alerting.check_alerts()
        
        return {
            "status": "healthy" if not alerts else "warning",
            "metrics": current_metrics,
            "active_alerts": alerts,
            "alert_count": len(alerts),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting performance summary: {e}")
        return {
            "status": "error",
            "error": str(e),
            "last_updated": datetime.now().isoformat()
        }

if __name__ == "__main__":
    # Test metrics collection
    collector = MetricsCollector()
    print("🧪 Testing metrics collection...")
    
    # Collect some metrics
    sys_metrics = collector.collect_system_metrics()
    app_metrics = collector.collect_application_metrics()
    
    print(f"System metrics: {asdict(sys_metrics)}")
    print(f"Application metrics: {asdict(app_metrics)}")
    
    # Test alerting
    alerting = PerformanceAlerting(collector)
    alerts = alerting.check_alerts()
    print(f"Current alerts: {alerts}")
    
    print("✅ Metrics system test completed!")