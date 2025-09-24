"""
Advanced Monitoring and Alerting System
Comprehensive monitoring infrastructure with real-time metrics collection,
intelligent alerting, and predictive analytics for system health management.
"""

import asyncio
import logging
import time
import json
from typing import Dict, List, Any, Optional, Callable, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, deque
from enum import Enum
import statistics
import threading
import smtplib
import websockets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import psutil
import aiohttp
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pickle

logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    """Alert severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class MetricType(Enum):
    """Types of metrics"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"

@dataclass
class Metric:
    """Represents a monitoring metric"""
    name: str
    value: float
    timestamp: datetime
    labels: Dict[str, str] = field(default_factory=dict)
    metric_type: MetricType = MetricType.GAUGE

@dataclass
class Alert:
    """Represents a monitoring alert"""
    id: str
    name: str
    severity: AlertSeverity
    message: str
    timestamp: datetime
    metric_name: str
    metric_value: float
    threshold: float
    labels: Dict[str, str] = field(default_factory=dict)
    resolved: bool = False
    resolved_at: Optional[datetime] = None

@dataclass
class AlertRule:
    """Defines conditions for triggering alerts"""
    name: str
    metric_name: str
    condition: str  # "gt", "lt", "eq", "ne"
    threshold: float
    severity: AlertSeverity
    duration: int = 300  # seconds
    labels: Dict[str, str] = field(default_factory=dict)
    enabled: bool = True

class MetricsCollector:
    """Collects and stores metrics from various sources"""
    
    def __init__(self, max_metrics: int = 100000):
        self.max_metrics = max_metrics
        self.metrics: deque = deque(maxlen=max_metrics)
        self.counters: Dict[str, float] = defaultdict(float)
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, List[float]] = defaultdict(list)
        self._lock = threading.Lock()
        self._collection_tasks: Set[asyncio.Task] = set()
        self.running = False
        
    async def start_collection(self):
        """Start metrics collection"""
        self.running = True
        
        # Start system metrics collection
        system_task = asyncio.create_task(self._collect_system_metrics())
        self._collection_tasks.add(system_task)
        
        # Start application metrics collection
        app_task = asyncio.create_task(self._collect_application_metrics())
        self._collection_tasks.add(app_task)
        
        logger.info("Metrics collection started")
    
    async def stop_collection(self):
        """Stop metrics collection"""
        self.running = False
        
        # Cancel all collection tasks
        for task in self._collection_tasks:
            task.cancel()
        
        await asyncio.gather(*self._collection_tasks, return_exceptions=True)
        self._collection_tasks.clear()
        
        logger.info("Metrics collection stopped")
    
    async def _collect_system_metrics(self):
        """Collect system-level metrics"""
        while self.running:
            try:
                timestamp = datetime.utcnow()
                
                # CPU metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                cpu_count = psutil.cpu_count()
                cpu_freq = psutil.cpu_freq()
                
                self.record_metric("system_cpu_percent", cpu_percent, timestamp)
                self.record_metric("system_cpu_count", cpu_count, timestamp)
                if cpu_freq:
                    self.record_metric("system_cpu_frequency_mhz", cpu_freq.current, timestamp)
                
                # Memory metrics
                memory = psutil.virtual_memory()
                swap = psutil.swap_memory()
                
                self.record_metric("system_memory_total_bytes", memory.total, timestamp)
                self.record_metric("system_memory_available_bytes", memory.available, timestamp)
                self.record_metric("system_memory_used_bytes", memory.used, timestamp)
                self.record_metric("system_memory_percent", memory.percent, timestamp)
                self.record_metric("system_swap_total_bytes", swap.total, timestamp)
                self.record_metric("system_swap_used_bytes", swap.used, timestamp)
                self.record_metric("system_swap_percent", swap.percent, timestamp)
                
                # Disk metrics
                disk_usage = psutil.disk_usage('/')
                disk_io = psutil.disk_io_counters()
                
                self.record_metric("system_disk_total_bytes", disk_usage.total, timestamp)
                self.record_metric("system_disk_used_bytes", disk_usage.used, timestamp)
                self.record_metric("system_disk_free_bytes", disk_usage.free, timestamp)
                self.record_metric("system_disk_percent", disk_usage.percent, timestamp)
                
                if disk_io:
                    self.record_metric("system_disk_read_bytes_total", disk_io.read_bytes, timestamp, MetricType.COUNTER)
                    self.record_metric("system_disk_write_bytes_total", disk_io.write_bytes, timestamp, MetricType.COUNTER)
                    self.record_metric("system_disk_read_count_total", disk_io.read_count, timestamp, MetricType.COUNTER)
                    self.record_metric("system_disk_write_count_total", disk_io.write_count, timestamp, MetricType.COUNTER)
                
                # Network metrics
                network_io = psutil.net_io_counters()
                
                if network_io:
                    self.record_metric("system_network_bytes_sent_total", network_io.bytes_sent, timestamp, MetricType.COUNTER)
                    self.record_metric("system_network_bytes_recv_total", network_io.bytes_recv, timestamp, MetricType.COUNTER)
                    self.record_metric("system_network_packets_sent_total", network_io.packets_sent, timestamp, MetricType.COUNTER)
                    self.record_metric("system_network_packets_recv_total", network_io.packets_recv, timestamp, MetricType.COUNTER)
                
                # Process metrics
                process = psutil.Process()
                process_memory = process.memory_info()
                
                self.record_metric("process_memory_rss_bytes", process_memory.rss, timestamp)
                self.record_metric("process_memory_vms_bytes", process_memory.vms, timestamp)
                self.record_metric("process_cpu_percent", process.cpu_percent(), timestamp)
                self.record_metric("process_num_threads", process.num_threads(), timestamp)
                self.record_metric("process_num_fds", process.num_fds(), timestamp)
                
                await asyncio.sleep(30)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error collecting system metrics: {e}")
                await asyncio.sleep(5)
    
    async def _collect_application_metrics(self):
        """Collect application-specific metrics"""
        while self.running:
            try:
                timestamp = datetime.utcnow()
                
                # Scanner metrics (simulated - integrate with actual scanners)
                self.record_metric("scanner_active_tasks", len(getattr(self, '_active_scanners', [])), timestamp)
                self.record_metric("scanner_queue_size", getattr(self, '_scanner_queue_size', 0), timestamp)
                self.record_metric("scanner_success_rate", getattr(self, '_scanner_success_rate', 0.95), timestamp)
                
                # Cache metrics (integrate with actual cache)
                self.record_metric("cache_hit_rate", getattr(self, '_cache_hit_rate', 0.75), timestamp)
                self.record_metric("cache_size", getattr(self, '_cache_size', 1000), timestamp)
                self.record_metric("cache_eviction_rate", getattr(self, '_cache_eviction_rate', 0.1), timestamp)
                
                # Database metrics (simulated)
                self.record_metric("database_connections_active", getattr(self, '_db_connections', 5), timestamp)
                self.record_metric("database_query_duration_seconds", getattr(self, '_db_query_duration', 0.05), timestamp)
                self.record_metric("database_queries_total", getattr(self, '_db_queries_total', 1000), timestamp, MetricType.COUNTER)
                
                # API metrics
                self.record_metric("api_requests_total", getattr(self, '_api_requests_total', 500), timestamp, MetricType.COUNTER)
                self.record_metric("api_response_time_seconds", getattr(self, '_api_response_time', 0.2), timestamp)
                self.record_metric("api_error_rate", getattr(self, '_api_error_rate', 0.05), timestamp)
                
                await asyncio.sleep(60)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error collecting application metrics: {e}")
                await asyncio.sleep(10)
    
    def record_metric(self, name: str, value: float, timestamp: Optional[datetime] = None, 
                     metric_type: MetricType = MetricType.GAUGE, labels: Dict[str, str] = None):
        """Record a metric value"""
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        if labels is None:
            labels = {}
        
        metric = Metric(name=name, value=value, timestamp=timestamp, labels=labels, metric_type=metric_type)
        
        with self._lock:
            self.metrics.append(metric)
            
            # Update metric stores
            if metric_type == MetricType.COUNTER:
                self.counters[name] += value
            elif metric_type == MetricType.GAUGE:
                self.gauges[name] = value
            elif metric_type == MetricType.HISTOGRAM:
                self.histograms[name].append(value)
                # Keep only recent values for histograms
                if len(self.histograms[name]) > 1000:
                    self.histograms[name] = self.histograms[name][-1000:]
    
    def get_metric_values(self, name: str, minutes: int = 60) -> List[float]:
        """Get metric values from the last N minutes"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
        
        with self._lock:
            return [
                m.value for m in self.metrics 
                if m.name == name and m.timestamp >= cutoff_time
            ]
    
    def get_metric_statistics(self, name: str, minutes: int = 60) -> Dict[str, float]:
        """Get statistics for a metric"""
        values = self.get_metric_values(name, minutes)
        
        if not values:
            return {}
        
        return {
            'count': len(values),
            'min': min(values),
            'max': max(values),
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'std': statistics.stdev(values) if len(values) > 1 else 0,
            'percentile_95': np.percentile(values, 95),
            'percentile_99': np.percentile(values, 99)
        }
    
    def get_current_metrics(self) -> Dict[str, float]:
        """Get current metric values"""
        current_metrics = {}
        
        with self._lock:
            # Get latest gauge values
            current_metrics.update(self.gauges)
            
            # Get counter totals
            for name, value in self.counters.items():
                current_metrics[name] = value
            
            # Get histogram summaries
            for name, values in self.histograms.items():
                if values:
                    current_metrics[f"{name}_mean"] = statistics.mean(values)
                    current_metrics[f"{name}_p95"] = np.percentile(values, 95)
        
        return current_metrics

class AlertManager:
    """Manages alert rules and notifications"""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        self.alert_rules: Dict[str, AlertRule] = {}
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_history: deque = deque(maxlen=10000)
        self.notification_channels: List[Callable] = []
        self.running = False
        self._evaluation_task: Optional[asyncio.Task] = None
        self._alert_counter = 0
    
    def add_alert_rule(self, rule: AlertRule):
        """Add an alert rule"""
        self.alert_rules[rule.name] = rule
        logger.info(f"Added alert rule: {rule.name}")
    
    def remove_alert_rule(self, rule_name: str):
        """Remove an alert rule"""
        if rule_name in self.alert_rules:
            del self.alert_rules[rule_name]
            logger.info(f"Removed alert rule: {rule_name}")
    
    def add_notification_channel(self, channel: Callable):
        """Add a notification channel"""
        self.notification_channels.append(channel)
    
    async def start_monitoring(self):
        """Start alert monitoring"""
        self.running = True
        self._evaluation_task = asyncio.create_task(self._evaluation_loop())
        logger.info("Alert monitoring started")
    
    async def stop_monitoring(self):
        """Stop alert monitoring"""
        self.running = False
        
        if self._evaluation_task:
            self._evaluation_task.cancel()
            try:
                await self._evaluation_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Alert monitoring stopped")
    
    async def _evaluation_loop(self):
        """Main alert evaluation loop"""
        while self.running:
            try:
                await self._evaluate_alert_rules()
                await asyncio.sleep(30)  # Evaluate every 30 seconds
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in alert evaluation loop: {e}")
                await asyncio.sleep(5)
    
    async def _evaluate_alert_rules(self):
        """Evaluate all alert rules"""
        current_time = datetime.utcnow()
        
        for rule_name, rule in self.alert_rules.items():
            if not rule.enabled:
                continue
            
            try:
                # Get recent metric values
                values = self.metrics_collector.get_metric_values(rule.metric_name, rule.duration // 60)
                
                if not values:
                    continue
                
                # Get current value (latest)
                current_value = values[-1]
                
                # Evaluate condition
                alert_triggered = self._evaluate_condition(current_value, rule.condition, rule.threshold)
                
                # Check if alert should be fired or resolved
                alert_key = f"{rule_name}_{rule.metric_name}"
                
                if alert_triggered and alert_key not in self.active_alerts:
                    # Fire new alert
                    alert = Alert(
                        id=f"alert_{self._alert_counter}",
                        name=rule.name,
                        severity=rule.severity,
                        message=f"{rule.metric_name} is {current_value} (threshold: {rule.threshold})",
                        timestamp=current_time,
                        metric_name=rule.metric_name,
                        metric_value=current_value,
                        threshold=rule.threshold,
                        labels=rule.labels
                    )
                    
                    self.active_alerts[alert_key] = alert
                    self.alert_history.append(alert)
                    self._alert_counter += 1
                    
                    # Send notifications
                    await self._send_alert_notifications(alert)
                    
                elif not alert_triggered and alert_key in self.active_alerts:
                    # Resolve alert
                    alert = self.active_alerts[alert_key]
                    alert.resolved = True
                    alert.resolved_at = current_time
                    
                    del self.active_alerts[alert_key]
                    
                    # Send resolution notification
                    await self._send_resolution_notifications(alert)
                    
            except Exception as e:
                logger.error(f"Error evaluating alert rule {rule_name}: {e}")
    
    def _evaluate_condition(self, value: float, condition: str, threshold: float) -> bool:
        """Evaluate alert condition"""
        if condition == "gt":
            return value > threshold
        elif condition == "lt":
            return value < threshold
        elif condition == "eq":
            return abs(value - threshold) < 0.001
        elif condition == "ne":
            return abs(value - threshold) >= 0.001
        elif condition == "gte":
            return value >= threshold
        elif condition == "lte":
            return value <= threshold
        else:
            logger.warning(f"Unknown condition: {condition}")
            return False
    
    async def _send_alert_notifications(self, alert: Alert):
        """Send alert notifications to all channels"""
        for channel in self.notification_channels:
            try:
                await self._call_notification_channel(channel, alert, "alert")
            except Exception as e:
                logger.error(f"Error sending alert notification: {e}")
    
    async def _send_resolution_notifications(self, alert: Alert):
        """Send alert resolution notifications"""
        for channel in self.notification_channels:
            try:
                await self._call_notification_channel(channel, alert, "resolution")
            except Exception as e:
                logger.error(f"Error sending resolution notification: {e}")
    
    async def _call_notification_channel(self, channel: Callable, alert: Alert, notification_type: str):
        """Call a notification channel"""
        if asyncio.iscoroutinefunction(channel):
            await channel(alert, notification_type)
        else:
            channel(alert, notification_type)
    
    def get_active_alerts(self) -> List[Alert]:
        """Get all active alerts"""
        return list(self.active_alerts.values())
    
    def get_alert_history(self, hours: int = 24) -> List[Alert]:
        """Get alert history from the last N hours"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        return [alert for alert in self.alert_history if alert.timestamp >= cutoff_time]
    
    def get_alert_statistics(self) -> Dict[str, Any]:
        """Get alert statistics"""
        active_alerts = list(self.active_alerts.values())
        recent_history = self.get_alert_history(24)
        
        severity_counts = defaultdict(int)
        for alert in recent_history:
            severity_counts[alert.severity.value] += 1
        
        return {
            'active_alerts': len(active_alerts),
            'alerts_last_24h': len(recent_history),
            'severity_distribution': dict(severity_counts),
            'most_frequent_alerts': self._get_most_frequent_alerts(recent_history)
        }
    
    def _get_most_frequent_alerts(self, alerts: List[Alert]) -> List[Dict[str, Any]]:
        """Get most frequent alert types"""
        alert_counts = defaultdict(int)
        
        for alert in alerts:
            key = f"{alert.name}:{alert.metric_name}"
            alert_counts[key] += 1
        
        return sorted(
            [{'alert': k, 'count': v} for k, v in alert_counts.items()],
            key=lambda x: x['count'],
            reverse=True
        )[:10]

class AnomalyDetector:
    """ML-based anomaly detection for metrics"""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        self.models: Dict[str, IsolationForest] = {}
        self.scalers: Dict[str, StandardScaler] = {}
        self.training_data: Dict[str, List[float]] = defaultdict(list)
        self.anomaly_threshold = -0.1  # Isolation Forest threshold
        self.min_training_samples = 100
        
    async def train_models(self, metric_names: List[str]):
        """Train anomaly detection models for specified metrics"""
        for metric_name in metric_names:
            try:
                # Get training data
                values = self.metrics_collector.get_metric_values(metric_name, minutes=1440)  # 24 hours
                
                if len(values) < self.min_training_samples:
                    logger.warning(f"Not enough data to train anomaly model for {metric_name}")
                    continue
                
                # Prepare training data
                X = np.array(values).reshape(-1, 1)
                
                # Scale data
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)
                
                # Train model
                model = IsolationForest(contamination=0.1, random_state=42)
                model.fit(X_scaled)
                
                # Store model and scaler
                self.models[metric_name] = model
                self.scalers[metric_name] = scaler
                
                logger.info(f"Trained anomaly detection model for {metric_name}")
                
            except Exception as e:
                logger.error(f"Error training anomaly model for {metric_name}: {e}")
    
    def detect_anomalies(self, metric_name: str, values: List[float]) -> List[bool]:
        """Detect anomalies in metric values"""
        if metric_name not in self.models:
            return [False] * len(values)
        
        try:
            model = self.models[metric_name]
            scaler = self.scalers[metric_name]
            
            # Scale values
            X = np.array(values).reshape(-1, 1)
            X_scaled = scaler.transform(X)
            
            # Predict anomalies
            scores = model.decision_function(X_scaled)
            anomalies = scores < self.anomaly_threshold
            
            return anomalies.tolist()
            
        except Exception as e:
            logger.error(f"Error detecting anomalies for {metric_name}: {e}")
            return [False] * len(values)
    
    def get_anomaly_score(self, metric_name: str, value: float) -> float:
        """Get anomaly score for a single value"""
        if metric_name not in self.models:
            return 0.0
        
        try:
            model = self.models[metric_name]
            scaler = self.scalers[metric_name]
            
            # Scale value
            X = np.array([[value]])
            X_scaled = scaler.transform(X)
            
            # Get anomaly score
            score = model.decision_function(X_scaled)[0]
            
            return score
            
        except Exception as e:
            logger.error(f"Error getting anomaly score for {metric_name}: {e}")
            return 0.0

# Notification channels
async def email_notification_channel(alert: Alert, notification_type: str):
    """Email notification channel"""
    # Implement email sending logic
    logger.info(f"Email notification: {notification_type} - {alert.name}")

async def webhook_notification_channel(alert: Alert, notification_type: str):
    """Webhook notification channel"""
    # Implement webhook sending logic
    logger.info(f"Webhook notification: {notification_type} - {alert.name}")

async def slack_notification_channel(alert: Alert, notification_type: str):
    """Slack notification channel"""
    # Implement Slack API integration
    logger.info(f"Slack notification: {notification_type} - {alert.name}")

class DashboardMetrics:
    """Provides metrics for monitoring dashboards"""
    
    def __init__(self, metrics_collector: MetricsCollector, alert_manager: AlertManager):
        self.metrics_collector = metrics_collector
        self.alert_manager = alert_manager
    
    def get_system_overview(self) -> Dict[str, Any]:
        """Get system overview metrics"""
        current_metrics = self.metrics_collector.get_current_metrics()
        active_alerts = self.alert_manager.get_active_alerts()
        
        return {
            'system_health': {
                'cpu_percent': current_metrics.get('system_cpu_percent', 0),
                'memory_percent': current_metrics.get('system_memory_percent', 0),
                'disk_percent': current_metrics.get('system_disk_percent', 0),
            },
            'application_health': {
                'scanner_success_rate': current_metrics.get('scanner_success_rate', 0),
                'cache_hit_rate': current_metrics.get('cache_hit_rate', 0),
                'api_error_rate': current_metrics.get('api_error_rate', 0),
            },
            'alerts': {
                'active_count': len(active_alerts),
                'critical_count': len([a for a in active_alerts if a.severity == AlertSeverity.CRITICAL]),
                'high_count': len([a for a in active_alerts if a.severity == AlertSeverity.HIGH]),
            },
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def get_performance_metrics(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance metrics for the last N hours"""
        metric_names = [
            'system_cpu_percent',
            'system_memory_percent',
            'api_response_time_seconds',
            'scanner_success_rate'
        ]
        
        metrics_data = {}
        for metric_name in metric_names:
            stats = self.metrics_collector.get_metric_statistics(metric_name, hours * 60)
            if stats:
                metrics_data[metric_name] = stats
        
        return {
            'metrics': metrics_data,
            'period_hours': hours,
            'timestamp': datetime.utcnow().isoformat()
        }

class MonitoringSystem:
    """Main monitoring system coordinating all components"""
    
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.alert_manager = AlertManager(self.metrics_collector)
        self.anomaly_detector = AnomalyDetector(self.metrics_collector)
        self.dashboard_metrics = DashboardMetrics(self.metrics_collector, self.alert_manager)
        self.running = False
        
    async def start(self):
        """Start monitoring system"""
        await self.metrics_collector.start_collection()
        await self.alert_manager.start_monitoring()
        
        # Setup default alert rules
        self._setup_default_alert_rules()
        
        # Setup notification channels
        self._setup_notification_channels()
        
        self.running = True
        logger.info("Monitoring system started")
    
    async def stop(self):
        """Stop monitoring system"""
        self.running = False
        
        await self.alert_manager.stop_monitoring()
        await self.metrics_collector.stop_collection()
        
        logger.info("Monitoring system stopped")
    
    def _setup_default_alert_rules(self):
        """Setup default alert rules"""
        rules = [
            AlertRule(
                name="High CPU Usage",
                metric_name="system_cpu_percent",
                condition="gt",
                threshold=80.0,
                severity=AlertSeverity.HIGH,
                duration=300
            ),
            AlertRule(
                name="Critical CPU Usage",
                metric_name="system_cpu_percent",
                condition="gt",
                threshold=95.0,
                severity=AlertSeverity.CRITICAL,
                duration=60
            ),
            AlertRule(
                name="High Memory Usage",
                metric_name="system_memory_percent",
                condition="gt",
                threshold=85.0,
                severity=AlertSeverity.HIGH,
                duration=300
            ),
            AlertRule(
                name="Critical Memory Usage",
                metric_name="system_memory_percent",
                condition="gt",
                threshold=95.0,
                severity=AlertSeverity.CRITICAL,
                duration=60
            ),
            AlertRule(
                name="High Disk Usage",
                metric_name="system_disk_percent",
                condition="gt",
                threshold=90.0,
                severity=AlertSeverity.MEDIUM,
                duration=600
            ),
            AlertRule(
                name="Low Scanner Success Rate",
                metric_name="scanner_success_rate",
                condition="lt",
                threshold=0.8,
                severity=AlertSeverity.HIGH,
                duration=600
            ),
            AlertRule(
                name="High API Error Rate",
                metric_name="api_error_rate",
                condition="gt",
                threshold=0.1,
                severity=AlertSeverity.MEDIUM,
                duration=300
            )
        ]
        
        for rule in rules:
            self.alert_manager.add_alert_rule(rule)
    
    def _setup_notification_channels(self):
        """Setup notification channels"""
        # Add default notification channels
        self.alert_manager.add_notification_channel(email_notification_channel)
        self.alert_manager.add_notification_channel(webhook_notification_channel)
        self.alert_manager.add_notification_channel(slack_notification_channel)
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get comprehensive system health report"""
        return self.dashboard_metrics.get_system_overview()
    
    def get_performance_report(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance report"""
        return self.dashboard_metrics.get_performance_metrics(hours)
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Get alert summary"""
        return self.alert_manager.get_alert_statistics()

# Global monitoring system instance
monitoring_system = MonitoringSystem()

async def start_monitoring():
    """Start the global monitoring system"""
    await monitoring_system.start()

async def stop_monitoring():
    """Stop the global monitoring system"""
    await monitoring_system.stop()