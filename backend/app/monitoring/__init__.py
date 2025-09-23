
# Production Monitoring System
import asyncio
import psutil
import time
import logging
import json
from typing import Dict, Any
from datetime import datetime, timedelta

class ProductionMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.metrics = {}
        self.alerts = []
        self.thresholds = {
            "cpu_usage": 80,
            "memory_usage": 85,
            "disk_usage": 90,
            "response_time": 5.0,
            "error_rate": 5.0
        }
    
    async def collect_system_metrics(self) -> Dict[str, Any]:
        """Collect system performance metrics."""
        try:
            metrics = {
                "timestamp": datetime.utcnow().isoformat(),
                "cpu_usage": psutil.cpu_percent(interval=1),
                "memory_usage": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent,
                "network_io": dict(psutil.net_io_counters()._asdict()),
                "process_count": len(psutil.pids()),
                "load_average": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else [0, 0, 0]
            }
            
            self.metrics[time.time()] = metrics
            await self._check_thresholds(metrics)
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error collecting metrics: {e}")
            return {}
    
    async def _check_thresholds(self, metrics: Dict[str, Any]):
        """Check if metrics exceed alert thresholds."""
        for metric, value in metrics.items():
            if metric in self.thresholds and isinstance(value, (int, float)):
                if value > self.thresholds[metric]:
                    alert = {
                        "timestamp": datetime.utcnow().isoformat(),
                        "metric": metric,
                        "value": value,
                        "threshold": self.thresholds[metric],
                        "severity": "high" if value > self.thresholds[metric] * 1.2 else "medium"
                    }
                    self.alerts.append(alert)
                    self.logger.warning(f"ALERT: {metric} = {value}% (threshold: {self.thresholds[metric]}%)")
    
    async def start_monitoring(self, interval: int = 30):
        """Start continuous monitoring."""
        self.logger.info(f"Starting monitoring with {interval}s interval")
        while True:
            await self.collect_system_metrics()
            await asyncio.sleep(interval)
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get overall system health status."""
        recent_metrics = self._get_recent_metrics()
        if not recent_metrics:
            return {"status": "unknown", "reason": "no_metrics"}
        
        # Check if any critical thresholds are exceeded
        critical_issues = []
        for metric in ["cpu_usage", "memory_usage", "disk_usage"]:
            if metric in recent_metrics and recent_metrics[metric] > self.thresholds[metric]:
                critical_issues.append(f"{metric}: {recent_metrics[metric]}%")
        
        if critical_issues:
            return {
                "status": "unhealthy",
                "issues": critical_issues,
                "metrics": recent_metrics
            }
        
        return {
            "status": "healthy",
            "metrics": recent_metrics
        }
    
    def _get_recent_metrics(self) -> Dict[str, Any]:
        """Get most recent metrics."""
        if not self.metrics:
            return {}
        latest_timestamp = max(self.metrics.keys())
        return self.metrics[latest_timestamp]
