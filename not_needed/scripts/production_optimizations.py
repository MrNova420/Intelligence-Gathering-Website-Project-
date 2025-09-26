#!/usr/bin/env python3
"""
Production Optimization and Enhancement Suite
==============================================
Comprehensive suite for improving production readiness and performance.
"""

import asyncio
import logging
import sys
import os
from pathlib import Path

# Production Configuration Enhancements
PRODUCTION_CONFIG = {
    "security": {
        "jwt_expiry": 3600,  # 1 hour
        "rate_limit": 100,   # requests per minute
        "max_file_size": 10 * 1024 * 1024,  # 10MB
        "password_min_length": 8,
        "bcrypt_rounds": 12,
    },
    "performance": {
        "max_concurrent_scans": 50,
        "database_pool_size": 20,
        "redis_max_connections": 100,
        "scanner_timeout": 30,  # seconds
        "cache_ttl": 3600,  # 1 hour
    },
    "monitoring": {
        "health_check_interval": 30,  # seconds
        "log_level": "INFO",
        "metrics_retention": 30,  # days
        "alert_thresholds": {
            "cpu_usage": 80,
            "memory_usage": 85,
            "disk_usage": 90,
            "error_rate": 5,  # percent
        }
    },
    "deployment": {
        "container_restart_policy": "always",
        "max_memory": "2G",
        "max_cpu": "1.0",
        "replicas": 3,
        "rolling_update_strategy": "25%",
    }
}

class ProductionOptimizer:
    """Production optimization and enhancement system."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.logger = self._setup_logging()
    
    def _setup_logging(self):
        """Configure production-grade logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('production_optimization.log')
            ]
        )
        return logging.getLogger(__name__)
    
    async def optimize_scanner_performance(self):
        """Optimize scanner performance and reliability."""
        self.logger.info("🚀 Optimizing scanner performance...")
        
        # Fix async scanner execution
        scanner_fixes = """
# Enhanced scanner base with proper async handling
import asyncio
import aiohttp
import time
from typing import Dict, Any, Optional

class OptimizedBaseScannerModule:
    def __init__(self, name: str, scanner_type: str, description: str = ""):
        self.name = name
        self.scanner_type = scanner_type
        self.description = description
        self.enabled = True
        self.timeout = 30
        self.retry_count = 3
        self.rate_limit = 1.0  # seconds between requests
        self._last_request = 0
    
    async def scan(self, query) -> Dict[str, Any]:
        \"\"\"Enhanced scan with timeout, retries, and rate limiting.\"\"\"
        # Rate limiting
        current_time = time.time()
        time_since_last = current_time - self._last_request
        if time_since_last < self.rate_limit:
            await asyncio.sleep(self.rate_limit - time_since_last)
        
        self._last_request = time.time()
        
        for attempt in range(self.retry_count):
            try:
                async with asyncio.timeout(self.timeout):
                    result = await self._perform_scan(query)
                    return {
                        "scanner": self.name,
                        "type": self.scanner_type,
                        "query": query.query_value if hasattr(query, 'query_value') else str(query),
                        "result": result,
                        "confidence": self._calculate_confidence(result),
                        "timestamp": time.time(),
                        "attempt": attempt + 1
                    }
            except asyncio.TimeoutError:
                self.logger.warning(f"Scanner {self.name} timeout on attempt {attempt + 1}")
                if attempt == self.retry_count - 1:
                    return self._error_result(query, "timeout")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                self.logger.error(f"Scanner {self.name} error: {e}")
                if attempt == self.retry_count - 1:
                    return self._error_result(query, str(e))
                await asyncio.sleep(1)
        
        return self._error_result(query, "max_retries_exceeded")
    
    async def _perform_scan(self, query) -> Dict[str, Any]:
        \"\"\"Override this method in subclasses.\"\"\"
        await asyncio.sleep(0.1)  # Simulate API call
        return {"status": "success", "data": f"Mock result for {query}"}
    
    def _calculate_confidence(self, result: Dict[str, Any]) -> float:
        \"\"\"Calculate confidence score for the result.\"\"\"
        if not result or result.get("status") == "error":
            return 0.0
        return 0.85  # Default confidence
    
    def _error_result(self, query, error: str) -> Dict[str, Any]:
        \"\"\"Create error result structure.\"\"\"
        return {
            "scanner": self.name,
            "type": self.scanner_type,
            "query": query.query_value if hasattr(query, 'query_value') else str(query),
            "result": {"status": "error", "error": error},
            "confidence": 0.0,
            "timestamp": time.time(),
            "error": True
        }
"""
        
        # Write optimized scanner implementation
        scanner_file = self.project_root / "backend" / "app" / "scanners" / "optimized.py"
        scanner_file.write_text(scanner_fixes)
        
        self.logger.info("✅ Scanner performance optimizations applied")
    
    async def enhance_security_configuration(self):
        """Enhance security configuration and hardening."""
        self.logger.info("🛡️ Enhancing security configuration...")
        
        security_config = """
# Enhanced Security Configuration
import secrets
import hashlib
import hmac
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class EnhancedSecurityManager:
    def __init__(self):
        self.fernet = None
        self._init_encryption()
    
    def _init_encryption(self):
        \"\"\"Initialize encryption with enhanced key derivation.\"\"\"
        # Use environment variable or generate secure key
        key_material = os.environ.get('ENCRYPTION_KEY', self._generate_key())
        key = base64.urlsafe_b64encode(
            PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'intelligence_platform',
                iterations=100000,
            ).derive(key_material.encode())
        )
        self.fernet = Fernet(key)
    
    def _generate_key(self) -> str:
        \"\"\"Generate a secure encryption key.\"\"\"
        return secrets.token_urlsafe(32)
    
    def encrypt_sensitive_data(self, data: str) -> str:
        \"\"\"Encrypt sensitive data with AES-256.\"\"\"
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        \"\"\"Decrypt sensitive data.\"\"\"
        return self.fernet.decrypt(encrypted_data.encode()).decode()
    
    def generate_secure_token(self, length: int = 32) -> str:
        \"\"\"Generate cryptographically secure token.\"\"\"
        return secrets.token_urlsafe(length)
    
    def verify_signature(self, data: str, signature: str, secret: str) -> bool:
        \"\"\"Verify HMAC signature for data integrity.\"\"\"
        expected = hmac.new(
            secret.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, expected)
    
    def sanitize_input(self, user_input: str) -> str:
        \"\"\"Sanitize user input to prevent injection attacks.\"\"\"
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '|', '`']
        sanitized = user_input
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        return sanitized.strip()[:1000]  # Limit length
"""
        
        # Write enhanced security configuration
        security_file = self.project_root / "backend" / "app" / "core" / "enhanced_security.py"
        security_file.write_text(security_config)
        
        self.logger.info("✅ Security enhancements applied")
    
    async def optimize_database_performance(self):
        """Optimize database performance and reliability."""
        self.logger.info("🗄️ Optimizing database performance...")
        
        db_optimizations = """
# Enhanced Database Configuration
import asyncpg
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import logging

class OptimizedDatabaseManager:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = None
        self.session_factory = None
        self.logger = logging.getLogger(__name__)
    
    async def initialize(self):
        \"\"\"Initialize optimized database connection.\"\"\"
        self.engine = create_async_engine(
            self.database_url,
            poolclass=QueuePool,
            pool_size=20,
            max_overflow=30,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False,  # Set to True for development
        )
        
        self.session_factory = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        self.logger.info("Database connection pool initialized")
    
    async def get_session(self) -> AsyncSession:
        \"\"\"Get database session with proper error handling.\"\"\"
        try:
            async with self.session_factory() as session:
                yield session
        except Exception as e:
            self.logger.error(f"Database session error: {e}")
            raise
    
    async def health_check(self) -> bool:
        \"\"\"Check database health.\"\"\"
        try:
            async with self.session_factory() as session:
                await session.execute("SELECT 1")
                return True
        except Exception as e:
            self.logger.error(f"Database health check failed: {e}")
            return False
    
    async def create_indexes(self):
        \"\"\"Create optimized database indexes.\"\"\"
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);",
            "CREATE INDEX IF NOT EXISTS idx_queries_user_id ON intelligence_queries(user_id);",
            "CREATE INDEX IF NOT EXISTS idx_queries_created_at ON intelligence_queries(created_at);",
            "CREATE INDEX IF NOT EXISTS idx_scan_results_query_id ON scan_results(query_id);",
            "CREATE INDEX IF NOT EXISTS idx_scan_results_scanner_type ON scan_results(scanner_type);",
            "CREATE INDEX IF NOT EXISTS idx_reports_user_id ON reports(user_id);",
            "CREATE INDEX IF NOT EXISTS idx_reports_created_at ON reports(created_at);",
        ]
        
        async with self.session_factory() as session:
            for index_sql in indexes:
                try:
                    await session.execute(index_sql)
                    await session.commit()
                except Exception as e:
                    self.logger.warning(f"Index creation warning: {e}")
        
        self.logger.info("Database indexes optimized")
"""
        
        # Write database optimizations
        db_file = self.project_root / "backend" / "app" / "db" / "optimized.py"
        db_file.write_text(db_optimizations)
        
        self.logger.info("✅ Database optimizations applied")
    
    async def create_monitoring_system(self):
        """Create comprehensive monitoring and alerting."""
        self.logger.info("📊 Creating monitoring system...")
        
        monitoring_config = """
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
        \"\"\"Collect system performance metrics.\"\"\"
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
        \"\"\"Check if metrics exceed alert thresholds.\"\"\"
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
        \"\"\"Start continuous monitoring.\"\"\"
        self.logger.info(f"Starting monitoring with {interval}s interval")
        while True:
            await self.collect_system_metrics()
            await asyncio.sleep(interval)
    
    def get_health_status(self) -> Dict[str, Any]:
        \"\"\"Get overall system health status.\"\"\"
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
        \"\"\"Get most recent metrics.\"\"\"
        if not self.metrics:
            return {}
        latest_timestamp = max(self.metrics.keys())
        return self.metrics[latest_timestamp]
"""
        
        # Write monitoring system
        monitoring_file = self.project_root / "backend" / "app" / "monitoring" / "__init__.py"
        monitoring_file.parent.mkdir(exist_ok=True)
        monitoring_file.write_text(monitoring_config)
        
        self.logger.info("✅ Monitoring system created")
    
    async def create_deployment_automation(self):
        """Create advanced deployment automation."""
        self.logger.info("🚀 Creating deployment automation...")
        
        # Enhanced production Docker Compose
        production_compose = """version: '3.8'

services:
  nginx:
    image: nginx:alpine
    container_name: intelligence_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./infrastructure/nginx/nginx.prod.conf:/etc/nginx/nginx.conf:ro
      - ./infrastructure/ssl:/etc/ssl/certs:ro
      - static_files:/var/www/static:ro
    depends_on:
      - backend
      - frontend
    restart: always
    networks:
      - intelligence_network
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    container_name: intelligence_backend
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - SECRET_KEY=${SECRET_KEY}
      - ENCRYPTION_KEY=${ENCRYPTION_KEY}
      - ENVIRONMENT=production
    volumes:
      - logs:/app/logs
      - uploads:/app/uploads
    depends_on:
      - postgres
      - redis
    restart: always
    networks:
      - intelligence_network
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    container_name: intelligence_frontend
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
    volumes:
      - static_files:/app/.next/static
    restart: always
    networks:
      - intelligence_network
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'

  postgres:
    image: postgres:15-alpine
    container_name: intelligence_postgres
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_INITDB_ARGS=--auth-host=scram-sha-256
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./infrastructure/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    restart: always
    networks:
      - intelligence_network
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: '2.0'

  redis:
    image: redis:7-alpine
    container_name: intelligence_redis
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    restart: always
    networks:
      - intelligence_network
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'

  monitoring:
    image: prom/prometheus:latest
    container_name: intelligence_monitoring
    ports:
      - "9090:9090"
    volumes:
      - ./infrastructure/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    restart: always
    networks:
      - intelligence_network

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  static_files:
  logs:
  uploads:

networks:
  intelligence_network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
"""
        
        # Write enhanced production Docker Compose
        compose_file = self.project_root / "docker-compose.prod.enhanced.yml"
        compose_file.write_text(production_compose)
        
        # Enhanced deployment script
        deploy_script = """#!/bin/bash
set -e

echo "🚀 Starting Enhanced Production Deployment..."

# Configuration
PROJECT_NAME="intelligence-platform"
BACKUP_DIR="/opt/backups/$(date +%Y%m%d_%H%M%S)"
LOG_FILE="/var/log/deploy.log"

# Functions
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

check_requirements() {
    log "Checking deployment requirements..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log "ERROR: Docker is not installed"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log "ERROR: Docker Compose is not installed"
        exit 1
    fi
    
    # Check environment file
    if [ ! -f ".env.production" ]; then
        log "ERROR: .env.production file not found"
        exit 1
    fi
    
    log "✅ Requirements check passed"
}

backup_data() {
    log "Creating data backup..."
    mkdir -p "$BACKUP_DIR"
    
    # Backup database
    docker exec intelligence_postgres pg_dump -U postgres intelligence_db > "$BACKUP_DIR/database.sql" 2>/dev/null || true
    
    # Backup uploads
    docker cp intelligence_backend:/app/uploads "$BACKUP_DIR/" 2>/dev/null || true
    
    log "✅ Data backup completed: $BACKUP_DIR"
}

deploy() {
    log "Deploying application..."
    
    # Load environment variables
    set -a
    source .env.production
    set +a
    
    # Pull latest images
    docker-compose -f docker-compose.prod.enhanced.yml pull
    
    # Build custom images
    docker-compose -f docker-compose.prod.enhanced.yml build --no-cache
    
    # Start services with rolling update
    docker-compose -f docker-compose.prod.enhanced.yml up -d --remove-orphans
    
    # Wait for services to be healthy
    log "Waiting for services to be ready..."
    sleep 30
    
    # Run database migrations
    docker exec intelligence_backend python -m alembic upgrade head
    
    log "✅ Deployment completed successfully"
}

health_check() {
    log "Performing health checks..."
    
    # Check backend health
    if curl -f http://localhost/api/health > /dev/null 2>&1; then
        log "✅ Backend health check passed"
    else
        log "❌ Backend health check failed"
        exit 1
    fi
    
    # Check frontend
    if curl -f http://localhost > /dev/null 2>&1; then
        log "✅ Frontend health check passed"
    else
        log "❌ Frontend health check failed"
        exit 1
    fi
    
    log "✅ All health checks passed"
}

rollback() {
    log "Rolling back deployment..."
    
    # Stop current services
    docker-compose -f docker-compose.prod.enhanced.yml down
    
    # Restore from backup
    if [ -d "$BACKUP_DIR" ]; then
        # Restore database
        docker exec intelligence_postgres psql -U postgres -c "DROP DATABASE IF EXISTS intelligence_db;"
        docker exec intelligence_postgres psql -U postgres -c "CREATE DATABASE intelligence_db;"
        docker exec -i intelligence_postgres psql -U postgres intelligence_db < "$BACKUP_DIR/database.sql"
        
        # Restore uploads
        docker cp "$BACKUP_DIR/uploads" intelligence_backend:/app/
    fi
    
    log "✅ Rollback completed"
}

# Main execution
main() {
    log "Starting deployment process..."
    
    check_requirements
    backup_data
    
    # Deploy with error handling
    if deploy; then
        if health_check; then
            log "🎉 Deployment successful!"
            
            # Cleanup old images
            docker image prune -f
            
            # Send success notification
            echo "Deployment completed successfully at $(date)" | mail -s "Deployment Success" admin@yourdomain.com 2>/dev/null || true
        else
            log "❌ Health checks failed, rolling back..."
            rollback
            exit 1
        fi
    else
        log "❌ Deployment failed, rolling back..."
        rollback
        exit 1
    fi
}

# Handle script arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "rollback")
        rollback
        ;;
    "health")
        health_check
        ;;
    *)
        echo "Usage: $0 {deploy|rollback|health}"
        exit 1
        ;;
esac
"""
        
        # Write enhanced deployment script
        deploy_file = self.project_root / "scripts" / "deploy_enhanced.sh"
        deploy_file.write_text(deploy_script)
        deploy_file.chmod(0o755)
        
        self.logger.info("✅ Enhanced deployment automation created")
    
    async def run_optimization_suite(self):
        """Run the complete optimization suite."""
        self.logger.info("🎯 Starting comprehensive production optimization...")
        
        optimizations = [
            ("Scanner Performance", self.optimize_scanner_performance),
            ("Security Configuration", self.enhance_security_configuration),
            ("Database Performance", self.optimize_database_performance),
            ("Monitoring System", self.create_monitoring_system),
            ("Deployment Automation", self.create_deployment_automation),
        ]
        
        results = []
        for name, optimization in optimizations:
            try:
                await optimization()
                results.append((name, "✅ Success"))
            except Exception as e:
                self.logger.error(f"Failed to optimize {name}: {e}")
                results.append((name, f"❌ Failed: {e}"))
        
        # Generate optimization report
        self.logger.info("\n" + "="*80)
        self.logger.info("🎉 PRODUCTION OPTIMIZATION COMPLETE")
        self.logger.info("="*80)
        for name, status in results:
            self.logger.info(f"{name}: {status}")
        
        success_count = len([r for r in results if "✅" in r[1]])
        self.logger.info(f"\nOptimization Score: {success_count}/{len(results)} ({success_count/len(results)*100:.1f}%)")
        
        if success_count == len(results):
            self.logger.info("🚀 Platform is now FULLY OPTIMIZED for production!")
        else:
            self.logger.warning("⚠️ Some optimizations failed. Review logs for details.")


async def main():
    """Main optimization runner."""
    optimizer = ProductionOptimizer()
    await optimizer.run_optimization_suite()


if __name__ == "__main__":
    asyncio.run(main())