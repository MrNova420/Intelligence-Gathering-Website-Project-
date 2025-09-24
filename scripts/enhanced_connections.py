#!/usr/bin/env python3
"""
Enhanced Connection Management System
Manages database connections, API connections, and external service integrations
"""

import asyncio
import logging
import json
import time
import ssl
import socket
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor
import threading
import queue
from pathlib import Path
import aiohttp
import asyncpg
import redis
import sqlite3

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ConnectionConfig:
    """Configuration for connection management"""
    # Database settings
    database_url: str = "postgresql://localhost:5432/intelligence_db"
    database_pool_min: int = 5
    database_pool_max: int = 20
    database_timeout: int = 30
    
    # Redis settings
    redis_url: str = "redis://localhost:6379/0"
    redis_pool_max: int = 10
    redis_timeout: int = 5
    
    # HTTP settings
    http_timeout: int = 30
    http_max_connections: int = 100
    http_max_connections_per_host: int = 30
    
    # Connection health check settings
    health_check_interval: int = 60
    max_retries: int = 3
    retry_delay: int = 5
    
    # External API configurations
    external_apis: Dict[str, Dict[str, Any]] = field(default_factory=dict)

class ConnectionPool:
    """Base connection pool class"""
    
    def __init__(self, name: str, config: ConnectionConfig):
        self.name = name
        self.config = config
        self.active_connections = 0
        self.total_connections = 0
        self.failed_connections = 0
        self.last_health_check = None
        self.is_healthy = True
        self._lock = threading.Lock()
    
    async def get_connection(self):
        """Get a connection from the pool"""
        raise NotImplementedError
    
    async def release_connection(self, connection):
        """Release a connection back to the pool"""
        raise NotImplementedError
    
    async def health_check(self) -> bool:
        """Perform health check on the connection pool"""
        raise NotImplementedError
    
    def get_stats(self) -> Dict[str, Any]:
        """Get connection pool statistics"""
        with self._lock:
            return {
                'name': self.name,
                'active_connections': self.active_connections,
                'total_connections': self.total_connections,
                'failed_connections': self.failed_connections,
                'is_healthy': self.is_healthy,
                'last_health_check': self.last_health_check.isoformat() if self.last_health_check else None
            }

class DatabaseConnectionPool(ConnectionPool):
    """PostgreSQL database connection pool"""
    
    def __init__(self, config: ConnectionConfig):
        super().__init__("database", config)
        self.pool = None
        self._initialized = False
    
    async def initialize(self):
        """Initialize the database connection pool"""
        try:
            self.pool = await asyncpg.create_pool(
                self.config.database_url,
                min_size=self.config.database_pool_min,
                max_size=self.config.database_pool_max,
                command_timeout=self.config.database_timeout
            )
            self._initialized = True
            logger.info(f"Database connection pool initialized with {self.config.database_pool_max} max connections")
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            self.is_healthy = False
            raise
    
    async def get_connection(self):
        """Get a database connection"""
        if not self._initialized:
            await self.initialize()
        
        try:
            with self._lock:
                self.active_connections += 1
            
            connection = await self.pool.acquire()
            return connection
        except Exception as e:
            with self._lock:
                self.failed_connections += 1
            logger.error(f"Failed to get database connection: {e}")
            raise
    
    async def release_connection(self, connection):
        """Release a database connection"""
        try:
            await self.pool.release(connection)
            with self._lock:
                self.active_connections -= 1
        except Exception as e:
            logger.error(f"Failed to release database connection: {e}")
    
    async def health_check(self) -> bool:
        """Check database connection health"""
        try:
            async with self.pool.acquire() as connection:
                await connection.execute("SELECT 1")
            self.is_healthy = True
            self.last_health_check = datetime.now()
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            self.is_healthy = False
            return False
    
    async def close(self):
        """Close the database connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")

class RedisConnectionPool(ConnectionPool):
    """Redis connection pool"""
    
    def __init__(self, config: ConnectionConfig):
        super().__init__("redis", config)
        self.pool = None
        self._initialized = False
    
    async def initialize(self):
        """Initialize the Redis connection pool"""
        try:
            self.pool = redis.ConnectionPool.from_url(
                self.config.redis_url,
                max_connections=self.config.redis_pool_max,
                socket_timeout=self.config.redis_timeout
            )
            self._initialized = True
            logger.info(f"Redis connection pool initialized with {self.config.redis_pool_max} max connections")
        except Exception as e:
            logger.error(f"Failed to initialize Redis pool: {e}")
            self.is_healthy = False
            raise
    
    async def get_connection(self):
        """Get a Redis connection"""
        if not self._initialized:
            await self.initialize()
        
        try:
            with self._lock:
                self.active_connections += 1
            
            client = redis.Redis(connection_pool=self.pool)
            return client
        except Exception as e:
            with self._lock:
                self.failed_connections += 1
            logger.error(f"Failed to get Redis connection: {e}")
            raise
    
    async def release_connection(self, connection):
        """Release a Redis connection"""
        try:
            connection.close()
            with self._lock:
                self.active_connections -= 1
        except Exception as e:
            logger.error(f"Failed to release Redis connection: {e}")
    
    async def health_check(self) -> bool:
        """Check Redis connection health"""
        try:
            client = redis.Redis(connection_pool=self.pool)
            await client.ping()
            self.is_healthy = True
            self.last_health_check = datetime.now()
            return True
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            self.is_healthy = False
            return False
    
    async def close(self):
        """Close the Redis connection pool"""
        if self.pool:
            self.pool.disconnect()
            logger.info("Redis connection pool closed")

class HTTPConnectionPool(ConnectionPool):
    """HTTP connection pool for external API calls"""
    
    def __init__(self, config: ConnectionConfig):
        super().__init__("http", config)
        self.session = None
        self._initialized = False
    
    async def initialize(self):
        """Initialize HTTP session"""
        try:
            timeout = aiohttp.ClientTimeout(total=self.config.http_timeout)
            connector = aiohttp.TCPConnector(
                limit=self.config.http_max_connections,
                limit_per_host=self.config.http_max_connections_per_host,
                ttl_dns_cache=300,
                use_dns_cache=True
            )
            
            self.session = aiohttp.ClientSession(
                timeout=timeout,
                connector=connector
            )
            self._initialized = True
            logger.info("HTTP connection pool initialized")
        except Exception as e:
            logger.error(f"Failed to initialize HTTP pool: {e}")
            self.is_healthy = False
            raise
    
    async def get_connection(self):
        """Get HTTP session"""
        if not self._initialized:
            await self.initialize()
        
        with self._lock:
            self.active_connections += 1
        
        return self.session
    
    async def release_connection(self, connection):
        """Release HTTP connection (no-op for session-based)"""
        with self._lock:
            self.active_connections -= 1
    
    async def health_check(self) -> bool:
        """Check HTTP connection health"""
        try:
            async with self.session.get('https://httpbin.org/status/200') as response:
                if response.status == 200:
                    self.is_healthy = True
                    self.last_health_check = datetime.now()
                    return True
                else:
                    raise Exception(f"HTTP health check returned status {response.status}")
        except Exception as e:
            logger.error(f"HTTP health check failed: {e}")
            self.is_healthy = False
            return False
    
    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
            logger.info("HTTP connection pool closed")

class ExternalAPIManager:
    """Manages connections to external APIs"""
    
    def __init__(self, config: ConnectionConfig, http_pool: HTTPConnectionPool):
        self.config = config
        self.http_pool = http_pool
        self.api_stats = {}
        self._lock = threading.Lock()
    
    async def call_api(self, api_name: str, endpoint: str, method: str = 'GET', 
                      data: Dict = None, headers: Dict = None) -> Dict[str, Any]:
        """Make an API call to external service"""
        
        if api_name not in self.config.external_apis:
            raise ValueError(f"API {api_name} not configured")
        
        api_config = self.config.external_apis[api_name]
        base_url = api_config.get('base_url', '')
        api_key = api_config.get('api_key', '')
        
        # Build headers
        request_headers = {'User-Agent': 'Intelligence-Platform/1.0'}
        if headers:
            request_headers.update(headers)
        
        if api_key:
            auth_header = api_config.get('auth_header', 'Authorization')
            auth_type = api_config.get('auth_type', 'Bearer')
            request_headers[auth_header] = f"{auth_type} {api_key}"
        
        # Build URL
        url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            session = await self.http_pool.get_connection()
            
            start_time = time.time()
            
            async with session.request(
                method=method.upper(),
                url=url,
                json=data if method.upper() in ['POST', 'PUT', 'PATCH'] else None,
                params=data if method.upper() == 'GET' else None,
                headers=request_headers
            ) as response:
                
                response_time = time.time() - start_time
                
                # Update API statistics
                with self._lock:
                    if api_name not in self.api_stats:
                        self.api_stats[api_name] = {
                            'total_calls': 0,
                            'successful_calls': 0,
                            'failed_calls': 0,
                            'avg_response_time': 0,
                            'last_call': None
                        }
                    
                    stats = self.api_stats[api_name]
                    stats['total_calls'] += 1
                    stats['last_call'] = datetime.now().isoformat()
                    
                    if response.status < 400:
                        stats['successful_calls'] += 1
                    else:
                        stats['failed_calls'] += 1
                    
                    # Update average response time
                    total_successful = stats['successful_calls']
                    if total_successful > 0:
                        stats['avg_response_time'] = (
                            (stats['avg_response_time'] * (total_successful - 1) + response_time) 
                            / total_successful
                        )
                
                await self.http_pool.release_connection(session)
                
                if response.status >= 400:
                    error_text = await response.text()
                    raise Exception(f"API call failed with status {response.status}: {error_text}")
                
                try:
                    result = await response.json()
                except:
                    result = await response.text()
                
                return {
                    'status_code': response.status,
                    'data': result,
                    'response_time': response_time,
                    'headers': dict(response.headers)
                }
        
        except Exception as e:
            await self.http_pool.release_connection(session)
            logger.error(f"API call to {api_name} failed: {e}")
            raise
    
    def get_api_stats(self) -> Dict[str, Any]:
        """Get API call statistics"""
        with self._lock:
            return dict(self.api_stats)

class ConnectionManager:
    """Main connection manager orchestrating all connection pools"""
    
    def __init__(self, config: ConnectionConfig = None):
        self.config = config or ConnectionConfig()
        self.pools = {}
        self.api_manager = None
        self.running = False
        self.executor = ThreadPoolExecutor(max_workers=2)
    
    async def initialize(self):
        """Initialize all connection pools"""
        logger.info("🔗 Initializing Connection Manager...")
        
        try:
            # Initialize database pool
            db_pool = DatabaseConnectionPool(self.config)
            await db_pool.initialize()
            self.pools['database'] = db_pool
            
            # Initialize Redis pool
            redis_pool = RedisConnectionPool(self.config)
            await redis_pool.initialize()
            self.pools['redis'] = redis_pool
            
            # Initialize HTTP pool
            http_pool = HTTPConnectionPool(self.config)
            await http_pool.initialize()
            self.pools['http'] = http_pool
            
            # Initialize API manager
            self.api_manager = ExternalAPIManager(self.config, http_pool)
            
            logger.info("✅ All connection pools initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize connection pools: {e}")
            raise
    
    async def start_health_monitoring(self):
        """Start health monitoring for all pools"""
        self.running = True
        self.executor.submit(self._health_check_loop)
        logger.info("🏥 Connection health monitoring started")
    
    async def stop(self):
        """Stop connection manager and close all pools"""
        logger.info("🛑 Stopping Connection Manager...")
        
        self.running = False
        self.executor.shutdown(wait=True)
        
        # Close all pools
        for name, pool in self.pools.items():
            try:
                await pool.close()
                logger.info(f"Closed {name} connection pool")
            except Exception as e:
                logger.error(f"Error closing {name} pool: {e}")
        
        logger.info("✅ Connection Manager stopped")
    
    def _health_check_loop(self):
        """Health check loop for all connection pools"""
        while self.running:
            try:
                asyncio.run(self._perform_health_checks())
                time.sleep(self.config.health_check_interval)
            except Exception as e:
                logger.error(f"Health check loop error: {e}")
                time.sleep(30)
    
    async def _perform_health_checks(self):
        """Perform health checks on all pools"""
        for name, pool in self.pools.items():
            try:
                is_healthy = await pool.health_check()
                if not is_healthy:
                    logger.warning(f"Health check failed for {name} pool")
                else:
                    logger.debug(f"Health check passed for {name} pool")
            except Exception as e:
                logger.error(f"Health check error for {name} pool: {e}")
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get statistics for all connection pools"""
        stats = {
            'pools': {},
            'api_stats': {},
            'overall_health': True
        }
        
        for name, pool in self.pools.items():
            pool_stats = pool.get_stats()
            stats['pools'][name] = pool_stats
            
            if not pool_stats['is_healthy']:
                stats['overall_health'] = False
        
        if self.api_manager:
            stats['api_stats'] = self.api_manager.get_api_stats()
        
        return stats
    
    async def get_database_connection(self):
        """Get database connection"""
        return await self.pools['database'].get_connection()
    
    async def release_database_connection(self, connection):
        """Release database connection"""
        await self.pools['database'].release_connection(connection)
    
    async def get_redis_connection(self):
        """Get Redis connection"""
        return await self.pools['redis'].get_connection()
    
    async def release_redis_connection(self, connection):
        """Release Redis connection"""
        await self.pools['redis'].release_connection(connection)
    
    async def make_api_call(self, api_name: str, endpoint: str, **kwargs):
        """Make external API call"""
        return await self.api_manager.call_api(api_name, endpoint, **kwargs)

# Global connection manager instance
_connection_manager = None

async def get_connection_manager() -> ConnectionManager:
    """Get global connection manager instance"""
    global _connection_manager
    if _connection_manager is None:
        _connection_manager = ConnectionManager()
        await _connection_manager.initialize()
        await _connection_manager.start_health_monitoring()
    return _connection_manager

async def main():
    """Main entry point for testing"""
    try:
        # Create configuration
        config = ConnectionConfig()
        
        # Add some example external APIs
        config.external_apis = {
            'example_api': {
                'base_url': 'https://jsonplaceholder.typicode.com',
                'api_key': '',
                'auth_header': 'Authorization',
                'auth_type': 'Bearer'
            }
        }
        
        # Initialize connection manager
        manager = ConnectionManager(config)
        await manager.initialize()
        await manager.start_health_monitoring()
        
        # Test connections
        logger.info("Testing connections...")
        
        # Test API call
        try:
            result = await manager.make_api_call('example_api', 'posts/1')
            logger.info(f"API call successful: {result['status_code']}")
        except Exception as e:
            logger.error(f"API call failed: {e}")
        
        # Show stats
        stats = manager.get_connection_stats()
        logger.info(f"Connection stats: {json.dumps(stats, indent=2)}")
        
        # Keep running
        logger.info("Connection manager running. Press Ctrl+C to stop.")
        try:
            while True:
                await asyncio.sleep(60)
        except KeyboardInterrupt:
            logger.info("Shutdown requested...")
        
        await manager.stop()
        
    except Exception as e:
        logger.error(f"Connection manager error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())