"""
Enterprise Monitoring and Alerting System
=========================================

Advanced monitoring capabilities for production environments:
- Real-time performance monitoring
- Intelligent alerting and notifications
- Health check automation
- Resource usage tracking
- SLA monitoring and reporting
- Anomaly detection
"""

import asyncio
import logging
import time
import psutil
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import statistics
import threading
from collections import defaultdict, deque

logger = logging.getLogger(__name__)


class AlertSeverity(str, Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class MetricType(str, Enum):
    """Types of metrics"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"


@dataclass
class Metric:
    """Individual metric data point"""
    name: str
    value: float
    metric_type: MetricType
    timestamp: datetime = field(default_factory=datetime.utcnow)
    labels: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Alert:
    """Alert notification"""
    alert_id: str
    severity: AlertSeverity
    title: str
    message: str
    source: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthCheck:
    """Health check definition"""
    name: str
    check_function: Callable
    interval_seconds: int = 60
    timeout_seconds: int = 30
    critical: bool = False
    last_run: Optional[datetime] = None
    last_status: bool = True
    consecutive_failures: int = 0


class MetricsCollector:
    """Collects and stores application metrics"""
    
    def __init__(self, max_datapoints: int = 10000):
        self.metrics = defaultdict(lambda: deque(maxlen=max_datapoints))
        self.counters = defaultdict(float)
        self.gauges = defaultdict(float)
        self.timers = defaultdict(list)
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._lock = threading.Lock()
    
    def record_metric(self, metric: Metric):
        """Record a metric data point"""
        with self._lock:
            self.metrics[metric.name].append(metric)
            
            if metric.metric_type == MetricType.COUNTER:
                self.counters[metric.name] += metric.value
            elif metric.metric_type == MetricType.GAUGE:
                self.gauges[metric.name] = metric.value
            elif metric.metric_type == MetricType.TIMER:
                self.timers[metric.name].append(metric.value)
                # Keep only last 1000 timer values
                if len(self.timers[metric.name]) > 1000:
                    self.timers[metric.name] = self.timers[metric.name][-1000:]
    
    def increment_counter(self, name: str, value: float = 1.0, labels: Dict[str, str] = None):
        """Increment a counter metric"""
        metric = Metric(
            name=name,
            value=value,
            metric_type=MetricType.COUNTER,
            labels=labels or {}
        )
        self.record_metric(metric)
    
    def set_gauge(self, name: str, value: float, labels: Dict[str, str] = None):
        """Set a gauge metric value"""
        metric = Metric(
            name=name,
            value=value,
            metric_type=MetricType.GAUGE,
            labels=labels or {}
        )
        self.record_metric(metric)
    
    def record_timer(self, name: str, duration: float, labels: Dict[str, str] = None):
        """Record a timer metric"""
        metric = Metric(
            name=name,
            value=duration,
            metric_type=MetricType.TIMER,
            labels=labels or {}
        )
        self.record_metric(metric)
    
    def get_counter_value(self, name: str) -> float:
        """Get current counter value"""
        return self.counters.get(name, 0.0)
    
    def get_gauge_value(self, name: str) -> float:
        """Get current gauge value"""
        return self.gauges.get(name, 0.0)
    
    def get_timer_stats(self, name: str) -> Dict[str, float]:
        """Get timer statistics"""
        values = self.timers.get(name, [])
        if not values:
            return {"count": 0, "mean": 0, "median": 0, "p95": 0, "p99": 0}
        
        sorted_values = sorted(values)
        count = len(sorted_values)
        
        return {
            "count": count,
            "mean": statistics.mean(sorted_values),
            "median": statistics.median(sorted_values),
            "p95": sorted_values[int(count * 0.95)] if count > 0 else 0,
            "p99": sorted_values[int(count * 0.99)] if count > 0 else 0,
            "min": min(sorted_values),
            "max": max(sorted_values)
        }
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics"""
        summary = {
            "counters": dict(self.counters),
            "gauges": dict(self.gauges),
            "timers": {}
        }
        
        for name in self.timers:
            summary["timers"][name] = self.get_timer_stats(name)
        
        return summary


class SystemMonitor:
    """Monitors system resources and performance"""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics = metrics_collector
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._monitoring = False
        self._monitor_task = None
    
    async def start_monitoring(self, interval_seconds: int = 30):
        """Start system monitoring"""
        if self._monitoring:
            return
        
        self._monitoring = True
        self._monitor_task = asyncio.create_task(self._monitor_loop(interval_seconds))
        self.logger.info("System monitoring started")
    
    async def stop_monitoring(self):
        """Stop system monitoring"""
        self._monitoring = False
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
        self.logger.info("System monitoring stopped")
    
    async def _monitor_loop(self, interval_seconds: int):
        """Main monitoring loop"""
        while self._monitoring:
            try:
                await self._collect_system_metrics()
                await asyncio.sleep(interval_seconds)
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(interval_seconds)
    
    async def _collect_system_metrics(self):
        """Collect system metrics"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            self.metrics.set_gauge("system.cpu.percent", cpu_percent)
            
            # Memory metrics
            memory = psutil.virtual_memory()
            self.metrics.set_gauge("system.memory.percent", memory.percent)
            self.metrics.set_gauge("system.memory.available_mb", memory.available / 1024 / 1024)
            self.metrics.set_gauge("system.memory.used_mb", memory.used / 1024 / 1024)
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            self.metrics.set_gauge("system.disk.percent", disk.percent)
            self.metrics.set_gauge("system.disk.free_gb", disk.free / 1024 / 1024 / 1024)
            
            # Network metrics
            network = psutil.net_io_counters()
            self.metrics.set_gauge("system.network.bytes_sent", network.bytes_sent)
            self.metrics.set_gauge("system.network.bytes_recv", network.bytes_recv)
            
            # Process metrics
            process = psutil.Process()
            process_memory = process.memory_info()
            self.metrics.set_gauge("process.memory.rss_mb", process_memory.rss / 1024 / 1024)
            self.metrics.set_gauge("process.memory.vms_mb", process_memory.vms / 1024 / 1024)
            self.metrics.set_gauge("process.cpu.percent", process.cpu_percent())
            
            # File descriptor count (Unix only)
            try:
                self.metrics.set_gauge("process.file_descriptors", process.num_fds())
            except AttributeError:
                pass  # Windows doesn't have num_fds
            
        except Exception as e:
            self.logger.error(f"Error collecting system metrics: {e}")


class AlertManager:
    """Manages alerts and notifications"""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics = metrics_collector
        self.alerts = {}
        self.alert_rules = []
        self.notification_handlers = []
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._alert_check_task = None
        self._checking_alerts = False
    
    def add_alert_rule(
        self, 
        name: str, 
        metric_name: str, 
        condition: str, 
        threshold: float,
        severity: AlertSeverity = AlertSeverity.WARNING,
        description: str = ""
    ):
        """Add an alert rule"""
        rule = {
            "name": name,
            "metric_name": metric_name,
            "condition": condition,  # "gt", "lt", "eq", "gte", "lte"
            "threshold": threshold,
            "severity": severity,
            "description": description,
            "last_triggered": None,
            "cooldown_seconds": 300  # 5 minutes
        }
        self.alert_rules.append(rule)
        self.logger.info(f"Added alert rule: {name}")
    
    def add_notification_handler(self, handler: Callable[[Alert], None]):
        """Add a notification handler"""
        self.notification_handlers.append(handler)
    
    async def start_alert_checking(self, interval_seconds: int = 60):
        """Start checking alert rules"""
        if self._checking_alerts:
            return
        
        self._checking_alerts = True
        self._alert_check_task = asyncio.create_task(self._alert_check_loop(interval_seconds))
        self.logger.info("Alert checking started")
    
    async def stop_alert_checking(self):
        """Stop checking alert rules"""
        self._checking_alerts = False
        if self._alert_check_task:
            self._alert_check_task.cancel()
            try:
                await self._alert_check_task
            except asyncio.CancelledError:
                pass
        self.logger.info("Alert checking stopped")
    
    async def _alert_check_loop(self, interval_seconds: int):
        """Main alert checking loop"""
        while self._checking_alerts:
            try:
                await self._check_alert_rules()
                await asyncio.sleep(interval_seconds)
            except Exception as e:
                self.logger.error(f"Error in alert checking loop: {e}")
                await asyncio.sleep(interval_seconds)
    
    async def _check_alert_rules(self):
        """Check all alert rules"""
        for rule in self.alert_rules:
            try:
                await self._check_single_rule(rule)
            except Exception as e:
                self.logger.error(f"Error checking rule {rule['name']}: {e}")
    
    async def _check_single_rule(self, rule: Dict[str, Any]):
        """Check a single alert rule"""
        metric_name = rule["metric_name"]
        condition = rule["condition"]
        threshold = rule["threshold"]
        
        # Get current metric value
        current_value = None
        if metric_name in self.metrics.gauges:
            current_value = self.metrics.gauges[metric_name]
        elif metric_name in self.metrics.counters:
            current_value = self.metrics.counters[metric_name]
        
        if current_value is None:
            return
        
        # Check condition
        triggered = False
        if condition == "gt" and current_value > threshold:
            triggered = True
        elif condition == "lt" and current_value < threshold:
            triggered = True
        elif condition == "gte" and current_value >= threshold:
            triggered = True
        elif condition == "lte" and current_value <= threshold:
            triggered = True
        elif condition == "eq" and current_value == threshold:
            triggered = True
        
        # Handle alert
        if triggered:
            await self._trigger_alert(rule, current_value)
        else:
            await self._resolve_alert(rule["name"])
    
    async def _trigger_alert(self, rule: Dict[str, Any], current_value: float):
        """Trigger an alert"""
        alert_name = rule["name"]
        
        # Check cooldown
        if rule["last_triggered"]:
            time_since_last = (datetime.utcnow() - rule["last_triggered"]).total_seconds()
            if time_since_last < rule["cooldown_seconds"]:
                return
        
        # Create alert
        alert = Alert(
            alert_id=f"alert_{alert_name}_{int(time.time())}",
            severity=rule["severity"],
            title=f"Alert: {alert_name}",
            message=f"{rule['description']} (Current: {current_value}, Threshold: {rule['threshold']})",
            source="alert_manager",
            metadata={
                "rule_name": alert_name,
                "metric_name": rule["metric_name"],
                "current_value": current_value,
                "threshold": rule["threshold"],
                "condition": rule["condition"]
            }
        )
        
        self.alerts[alert_name] = alert
        rule["last_triggered"] = datetime.utcnow()
        
        # Send notifications
        for handler in self.notification_handlers:
            try:
                await asyncio.create_task(self._call_handler(handler, alert))
            except Exception as e:
                self.logger.error(f"Error calling notification handler: {e}")
        
        self.logger.warning(f"Alert triggered: {alert.title}")
    
    async def _resolve_alert(self, alert_name: str):
        """Resolve an alert"""
        if alert_name in self.alerts and not self.alerts[alert_name].resolved:
            alert = self.alerts[alert_name]
            alert.resolved = True
            alert.resolved_at = datetime.utcnow()
            
            # Create resolution notification
            resolution_alert = Alert(
                alert_id=f"resolved_{alert.alert_id}",
                severity=AlertSeverity.INFO,
                title=f"Alert Resolved: {alert_name}",
                message=f"Alert '{alert_name}' has been resolved",
                source="alert_manager",
                metadata={"original_alert_id": alert.alert_id}
            )
            
            # Send resolution notifications
            for handler in self.notification_handlers:
                try:
                    await asyncio.create_task(self._call_handler(handler, resolution_alert))
                except Exception as e:
                    self.logger.error(f"Error calling notification handler for resolution: {e}")
            
            self.logger.info(f"Alert resolved: {alert_name}")
    
    async def _call_handler(self, handler: Callable, alert: Alert):
        """Call a notification handler (async or sync)"""
        if asyncio.iscoroutinefunction(handler):
            await handler(alert)
        else:
            handler(alert)
    
    def get_active_alerts(self) -> List[Alert]:
        """Get all active alerts"""
        return [alert for alert in self.alerts.values() if not alert.resolved]
    
    def get_alert_history(self, hours: int = 24) -> List[Alert]:
        """Get alert history for the specified time period"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        return [
            alert for alert in self.alerts.values() 
            if alert.timestamp >= cutoff_time
        ]


class HealthCheckManager:
    """Manages health checks for various system components"""
    
    def __init__(self, alert_manager: AlertManager):
        self.alert_manager = alert_manager
        self.health_checks = {}
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._running_checks = False
        self._check_tasks = {}
    
    def register_health_check(self, health_check: HealthCheck):
        """Register a health check"""
        self.health_checks[health_check.name] = health_check
        self.logger.info(f"Registered health check: {health_check.name}")
    
    async def start_health_checks(self):
        """Start all health checks"""
        if self._running_checks:
            return
        
        self._running_checks = True
        
        for name, check in self.health_checks.items():
            task = asyncio.create_task(self._run_health_check_loop(check))
            self._check_tasks[name] = task
        
        self.logger.info(f"Started {len(self.health_checks)} health checks")
    
    async def stop_health_checks(self):
        """Stop all health checks"""
        self._running_checks = False
        
        for task in self._check_tasks.values():
            task.cancel()
        
        await asyncio.gather(*self._check_tasks.values(), return_exceptions=True)
        self._check_tasks.clear()
        
        self.logger.info("Stopped all health checks")
    
    async def _run_health_check_loop(self, check: HealthCheck):
        """Run a single health check in a loop"""
        while self._running_checks:
            try:
                await self._execute_health_check(check)
                await asyncio.sleep(check.interval_seconds)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in health check loop for {check.name}: {e}")
                await asyncio.sleep(check.interval_seconds)
    
    async def _execute_health_check(self, check: HealthCheck):
        """Execute a single health check"""
        try:
            # Run the check with timeout
            if asyncio.iscoroutinefunction(check.check_function):
                result = await asyncio.wait_for(
                    check.check_function(), 
                    timeout=check.timeout_seconds
                )
            else:
                result = await asyncio.wait_for(
                    asyncio.create_task(asyncio.to_thread(check.check_function)),
                    timeout=check.timeout_seconds
                )
            
            success = bool(result)
            check.last_run = datetime.utcnow()
            
            if success:
                if not check.last_status:
                    # Health check recovered
                    self.logger.info(f"Health check {check.name} recovered")
                check.last_status = True
                check.consecutive_failures = 0
            else:
                check.last_status = False
                check.consecutive_failures += 1
                
                # Trigger alert for critical health checks
                if check.critical and check.consecutive_failures >= 3:
                    await self._trigger_health_alert(check, "Health check failed 3 consecutive times")
        
        except asyncio.TimeoutError:
            check.last_status = False
            check.consecutive_failures += 1
            check.last_run = datetime.utcnow()
            
            if check.critical:
                await self._trigger_health_alert(check, "Health check timed out")
            
            self.logger.warning(f"Health check {check.name} timed out")
        
        except Exception as e:
            check.last_status = False
            check.consecutive_failures += 1
            check.last_run = datetime.utcnow()
            
            if check.critical:
                await self._trigger_health_alert(check, f"Health check error: {str(e)}")
            
            self.logger.error(f"Health check {check.name} failed: {e}")
    
    async def _trigger_health_alert(self, check: HealthCheck, message: str):
        """Trigger an alert for a failed health check"""
        alert = Alert(
            alert_id=f"health_{check.name}_{int(time.time())}",
            severity=AlertSeverity.CRITICAL if check.critical else AlertSeverity.WARNING,
            title=f"Health Check Failed: {check.name}",
            message=message,
            source="health_check_manager",
            metadata={
                "check_name": check.name,
                "consecutive_failures": check.consecutive_failures,
                "critical": check.critical
            }
        )
        
        # Add to alert manager's alerts for tracking
        self.alert_manager.alerts[f"health_{check.name}"] = alert
        
        # Send notifications
        for handler in self.alert_manager.notification_handlers:
            try:
                await self.alert_manager._call_handler(handler, alert)
            except Exception as e:
                self.logger.error(f"Error calling notification handler: {e}")
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get overall health status"""
        total_checks = len(self.health_checks)
        passing_checks = len([
            check for check in self.health_checks.values() 
            if check.last_status
        ])
        
        critical_checks = [
            check for check in self.health_checks.values() 
            if check.critical and not check.last_status
        ]
        
        overall_status = "healthy"
        if critical_checks:
            overall_status = "critical"
        elif passing_checks < total_checks:
            overall_status = "degraded"
        
        return {
            "overall_status": overall_status,
            "total_checks": total_checks,
            "passing_checks": passing_checks,
            "failing_checks": total_checks - passing_checks,
            "critical_failures": len(critical_checks),
            "checks": {
                name: {
                    "status": "passing" if check.last_status else "failing",
                    "last_run": check.last_run.isoformat() if check.last_run else None,
                    "consecutive_failures": check.consecutive_failures,
                    "critical": check.critical
                }
                for name, check in self.health_checks.items()
            }
        }


class EnterpriseMonitoringSystem:
    """Main enterprise monitoring system"""
    
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.system_monitor = SystemMonitor(self.metrics_collector)
        self.alert_manager = AlertManager(self.metrics_collector)
        self.health_check_manager = HealthCheckManager(self.alert_manager)
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Set up default alert rules
        self._setup_default_alerts()
        
        # Set up default health checks
        self._setup_default_health_checks()
    
    def _setup_default_alerts(self):
        """Set up default alert rules"""
        # System resource alerts
        self.alert_manager.add_alert_rule(
            "high_cpu_usage",
            "system.cpu.percent",
            "gt",
            80.0,
            AlertSeverity.WARNING,
            "CPU usage is above 80%"
        )
        
        self.alert_manager.add_alert_rule(
            "high_memory_usage",
            "system.memory.percent",
            "gt",
            85.0,
            AlertSeverity.WARNING,
            "Memory usage is above 85%"
        )
        
        self.alert_manager.add_alert_rule(
            "low_disk_space",
            "system.disk.percent",
            "gt",
            90.0,
            AlertSeverity.CRITICAL,
            "Disk usage is above 90%"
        )
        
        # Application-specific alerts
        self.alert_manager.add_alert_rule(
            "high_error_rate",
            "app.errors.rate",
            "gt",
            0.05,
            AlertSeverity.ERROR,
            "Error rate is above 5%"
        )
    
    def _setup_default_health_checks(self):
        """Set up default health checks"""
        
        # Database health check
        async def check_database():
            # This would check actual database connectivity
            return True
        
        db_check = HealthCheck(
            name="database",
            check_function=check_database,
            interval_seconds=60,
            timeout_seconds=10,
            critical=True
        )
        self.health_check_manager.register_health_check(db_check)
        
        # Redis health check
        async def check_redis():
            # This would check actual Redis connectivity
            return True
        
        redis_check = HealthCheck(
            name="redis",
            check_function=check_redis,
            interval_seconds=60,
            timeout_seconds=5,
            critical=False
        )
        self.health_check_manager.register_health_check(redis_check)
    
    async def start_monitoring(self):
        """Start all monitoring components"""
        try:
            await self.system_monitor.start_monitoring()
            await self.alert_manager.start_alert_checking()
            await self.health_check_manager.start_health_checks()
            
            self.logger.info("Enterprise monitoring system started successfully")
        except Exception as e:
            self.logger.error(f"Failed to start monitoring system: {e}")
            raise
    
    async def stop_monitoring(self):
        """Stop all monitoring components"""
        try:
            await self.system_monitor.stop_monitoring()
            await self.alert_manager.stop_alert_checking()
            await self.health_check_manager.stop_health_checks()
            
            self.logger.info("Enterprise monitoring system stopped")
        except Exception as e:
            self.logger.error(f"Error stopping monitoring system: {e}")
    
    def get_monitoring_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive monitoring dashboard data"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": self.metrics_collector.get_metrics_summary(),
            "alerts": {
                "active": [
                    {
                        "id": alert.alert_id,
                        "severity": alert.severity.value,
                        "title": alert.title,
                        "message": alert.message,
                        "timestamp": alert.timestamp.isoformat()
                    }
                    for alert in self.alert_manager.get_active_alerts()
                ],
                "recent": [
                    {
                        "id": alert.alert_id,
                        "severity": alert.severity.value,
                        "title": alert.title,
                        "resolved": alert.resolved,
                        "timestamp": alert.timestamp.isoformat()
                    }
                    for alert in self.alert_manager.get_alert_history(hours=24)
                ]
            },
            "health": self.health_check_manager.get_health_status(),
            "system": {
                "uptime_seconds": time.time() - self.metrics_collector.gauges.get("system.start_time", time.time()),
                "cpu_percent": self.metrics_collector.gauges.get("system.cpu.percent", 0),
                "memory_percent": self.metrics_collector.gauges.get("system.memory.percent", 0),
                "disk_percent": self.metrics_collector.gauges.get("system.disk.percent", 0)
            }
        }


# Global monitoring instance
monitoring_system = EnterpriseMonitoringSystem()


# Convenience functions
def get_metrics_collector() -> MetricsCollector:
    """Get the global metrics collector"""
    return monitoring_system.metrics_collector


def get_alert_manager() -> AlertManager:
    """Get the global alert manager"""
    return monitoring_system.alert_manager


def get_health_check_manager() -> HealthCheckManager:
    """Get the global health check manager"""
    return monitoring_system.health_check_manager


# Decorators for easy metric collection
def monitor_execution_time(metric_name: str):
    """Decorator to monitor function execution time"""
    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            async def async_wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    return result
                finally:
                    execution_time = time.time() - start_time
                    monitoring_system.metrics_collector.record_timer(
                        metric_name, execution_time
                    )
            return async_wrapper
        else:
            def sync_wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    execution_time = time.time() - start_time
                    monitoring_system.metrics_collector.record_timer(
                        metric_name, execution_time
                    )
            return sync_wrapper
    return decorator


def count_calls(metric_name: str):
    """Decorator to count function calls"""
    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            async def async_wrapper(*args, **kwargs):
                monitoring_system.metrics_collector.increment_counter(metric_name)
                return await func(*args, **kwargs)
            return async_wrapper
        else:
            def sync_wrapper(*args, **kwargs):
                monitoring_system.metrics_collector.increment_counter(metric_name)
                return func(*args, **kwargs)
            return sync_wrapper
    return decorator