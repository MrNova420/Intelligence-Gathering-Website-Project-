#!/usr/bin/env python3
"""
Advanced Monitoring System for Intelligence Gathering Platform
Comprehensive monitoring with real-time alerts, metrics collection, and automated responses
"""

import json
import logging
import os
import time
import psutil
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor
import threading
import queue
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class MonitoringConfig:
    """Configuration for monitoring system"""
    monitoring_interval: int = 30
    health_check_interval: int = 15
    cpu_warning_threshold: float = 70.0
    memory_warning_threshold: float = 75.0
    disk_warning_threshold: float = 80.0
    
    services: List[Dict[str, Any]] = field(default_factory=lambda: [
        {"name": "backend", "type": "http", "url": "http://localhost:8000/health", "timeout": 10},
        {"name": "frontend", "type": "http", "url": "http://localhost:3000", "timeout": 10}
    ])

class AdvancedMonitoringSystem:
    """Main monitoring system"""
    
    def __init__(self, config: MonitoringConfig = None):
        self.config = config or MonitoringConfig()
        self.running = False
        self.executor = ThreadPoolExecutor(max_workers=2)
        
    def start(self):
        """Start monitoring"""
        logger.info("🚀 Starting Advanced Monitoring System...")
        self.running = True
        self.executor.submit(self._monitoring_loop)
        
    def stop(self):
        """Stop monitoring"""
        self.running = False
        self.executor.shutdown(wait=True)
        
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                metrics = self.get_system_metrics()
                self._check_thresholds(metrics)
                time.sleep(self.config.monitoring_interval)
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                time.sleep(30)
    
    def get_system_metrics(self):
        """Get system metrics"""
        try:
            return {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage('/').percent,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting metrics: {e}")
            return {}
    
    def _check_thresholds(self, metrics):
        """Check metric thresholds"""
        if not metrics:
            return
            
        cpu = metrics.get('cpu_percent', 0)
        if cpu > self.config.cpu_warning_threshold:
            logger.warning(f"High CPU usage: {cpu}%")
            
        memory = metrics.get('memory_percent', 0)
        if memory > self.config.memory_warning_threshold:
            logger.warning(f"High memory usage: {memory}%")
            
        disk = metrics.get('disk_percent', 0)
        if disk > self.config.disk_warning_threshold:
            logger.warning(f"High disk usage: {disk}%")

def main():
    """Main entry point"""
    monitoring = AdvancedMonitoringSystem()
    try:
        monitoring.start()
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        monitoring.stop()

if __name__ == "__main__":
    main()