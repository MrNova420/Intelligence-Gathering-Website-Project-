"""
Advanced Optimization Engine
Comprehensive system optimization with machine learning-based performance tuning,
resource management, and intelligent caching strategies.
"""

import asyncio
import logging
import time
import json
import pickle
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, deque
import statistics
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
import psutil
import threading
import aioredis
from concurrent.futures import ThreadPoolExecutor
import hashlib
import zlib

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetric:
    """Performance metric data point"""
    timestamp: datetime
    metric_name: str
    value: float
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass
class OptimizationRecommendation:
    """Optimization recommendation"""
    category: str
    priority: int  # 1=critical, 5=low
    description: str
    implementation: str
    expected_improvement: float
    confidence: float

class SystemMonitor:
    """Advanced system monitoring with predictive capabilities"""
    
    def __init__(self, collection_interval: int = 30):
        self.collection_interval = collection_interval
        self.metrics_history: deque = deque(maxlen=10000)
        self.running = False
        self.prediction_model = None
        self.scaler = StandardScaler()
        self._lock = threading.Lock()
        self._monitoring_task: Optional[asyncio.Task] = None
        
    async def start_monitoring(self):
        """Start system monitoring"""
        self.running = True
        self._monitoring_task = asyncio.create_task(self._monitoring_loop())
        logger.info("System monitoring started")
    
    async def stop_monitoring(self):
        """Stop system monitoring"""
        self.running = False
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass
        logger.info("System monitoring stopped")
    
    async def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                await self._collect_metrics()
                await asyncio.sleep(self.collection_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(5)
    
    async def _collect_metrics(self):
        """Collect system metrics"""
        timestamp = datetime.utcnow()
        
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        load_avg = psutil.getloadavg() if hasattr(psutil, 'getloadavg') else (0, 0, 0)
        
        # Memory metrics
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        # Disk metrics
        disk_usage = psutil.disk_usage('/')
        disk_io = psutil.disk_io_counters()
        
        # Network metrics
        network_io = psutil.net_io_counters()
        
        # Process metrics
        process = psutil.Process()
        process_memory = process.memory_info()
        process_cpu = process.cpu_percent()
        
        metrics = [
            PerformanceMetric(timestamp, "cpu_percent", cpu_percent),
            PerformanceMetric(timestamp, "cpu_count", cpu_count),
            PerformanceMetric(timestamp, "load_avg_1min", load_avg[0]),
            PerformanceMetric(timestamp, "load_avg_5min", load_avg[1]),
            PerformanceMetric(timestamp, "load_avg_15min", load_avg[2]),
            
            PerformanceMetric(timestamp, "memory_total", memory.total),
            PerformanceMetric(timestamp, "memory_available", memory.available),
            PerformanceMetric(timestamp, "memory_percent", memory.percent),
            PerformanceMetric(timestamp, "memory_used", memory.used),
            PerformanceMetric(timestamp, "memory_free", memory.free),
            PerformanceMetric(timestamp, "swap_total", swap.total),
            PerformanceMetric(timestamp, "swap_used", swap.used),
            PerformanceMetric(timestamp, "swap_percent", swap.percent),
            
            PerformanceMetric(timestamp, "disk_total", disk_usage.total),
            PerformanceMetric(timestamp, "disk_used", disk_usage.used),
            PerformanceMetric(timestamp, "disk_free", disk_usage.free),
            PerformanceMetric(timestamp, "disk_percent", disk_usage.percent),
            
            PerformanceMetric(timestamp, "process_memory_rss", process_memory.rss),
            PerformanceMetric(timestamp, "process_memory_vms", process_memory.vms),
            PerformanceMetric(timestamp, "process_cpu_percent", process_cpu),
        ]
        
        if disk_io:
            metrics.extend([
                PerformanceMetric(timestamp, "disk_read_bytes", disk_io.read_bytes),
                PerformanceMetric(timestamp, "disk_write_bytes", disk_io.write_bytes),
                PerformanceMetric(timestamp, "disk_read_count", disk_io.read_count),
                PerformanceMetric(timestamp, "disk_write_count", disk_io.write_count),
            ])
        
        if network_io:
            metrics.extend([
                PerformanceMetric(timestamp, "network_bytes_sent", network_io.bytes_sent),
                PerformanceMetric(timestamp, "network_bytes_recv", network_io.bytes_recv),
                PerformanceMetric(timestamp, "network_packets_sent", network_io.packets_sent),
                PerformanceMetric(timestamp, "network_packets_recv", network_io.packets_recv),
            ])
        
        with self._lock:
            self.metrics_history.extend(metrics)
    
    def get_recent_metrics(self, minutes: int = 60) -> List[PerformanceMetric]:
        """Get metrics from the last N minutes"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
        
        with self._lock:
            return [m for m in self.metrics_history if m.timestamp >= cutoff_time]
    
    def get_metric_statistics(self, metric_name: str, minutes: int = 60) -> Dict[str, float]:
        """Get statistics for a specific metric"""
        recent_metrics = self.get_recent_metrics(minutes)
        values = [m.value for m in recent_metrics if m.metric_name == metric_name]
        
        if not values:
            return {}
        
        return {
            'count': len(values),
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'min': min(values),
            'max': max(values),
            'std': statistics.stdev(values) if len(values) > 1 else 0,
            'percentile_95': np.percentile(values, 95),
            'percentile_99': np.percentile(values, 99)
        }
    
    async def train_prediction_model(self):
        """Train ML model for performance prediction"""
        try:
            if len(self.metrics_history) < 100:
                logger.warning("Not enough data to train prediction model")
                return
            
            # Prepare training data
            features, targets = self._prepare_training_data()
            
            if len(features) < 50:
                logger.warning("Not enough feature data for training")
                return
            
            # Train model
            self.prediction_model = RandomForestRegressor(n_estimators=100, random_state=42)
            features_scaled = self.scaler.fit_transform(features)
            self.prediction_model.fit(features_scaled, targets)
            
            logger.info("Performance prediction model trained successfully")
            
        except Exception as e:
            logger.error(f"Error training prediction model: {e}")
    
    def _prepare_training_data(self) -> Tuple[List[List[float]], List[float]]:
        """Prepare training data for ML model"""
        # Group metrics by timestamp
        metrics_by_time = defaultdict(dict)
        
        with self._lock:
            for metric in self.metrics_history:
                timestamp_key = metric.timestamp.replace(second=0, microsecond=0)
                metrics_by_time[timestamp_key][metric.metric_name] = metric.value
        
        # Create feature vectors
        features = []
        targets = []
        
        feature_names = ['cpu_percent', 'memory_percent', 'disk_percent', 'process_cpu_percent']
        target_name = 'memory_percent'
        
        sorted_times = sorted(metrics_by_time.keys())
        
        for i, timestamp in enumerate(sorted_times[:-1]):  # Exclude last for target
            current_metrics = metrics_by_time[timestamp]
            next_metrics = metrics_by_time[sorted_times[i + 1]]
            
            # Check if we have all required features
            if all(name in current_metrics for name in feature_names) and target_name in next_metrics:
                feature_vector = [current_metrics[name] for name in feature_names]
                target_value = next_metrics[target_name]
                
                features.append(feature_vector)
                targets.append(target_value)
        
        return features, targets
    
    def predict_resource_usage(self, horizon_minutes: int = 30) -> Dict[str, float]:
        """Predict resource usage for the next N minutes"""
        if not self.prediction_model:
            return {}
        
        try:
            # Get current metrics
            recent_metrics = self.get_recent_metrics(5)
            if not recent_metrics:
                return {}
            
            # Prepare current feature vector
            current_values = defaultdict(list)
            for metric in recent_metrics:
                current_values[metric.metric_name].append(metric.value)
            
            feature_names = ['cpu_percent', 'memory_percent', 'disk_percent', 'process_cpu_percent']
            
            if not all(name in current_values for name in feature_names):
                return {}
            
            current_features = [statistics.mean(current_values[name]) for name in feature_names]
            current_features_scaled = self.scaler.transform([current_features])
            
            # Make prediction
            prediction = self.prediction_model.predict(current_features_scaled)[0]
            
            return {
                'predicted_memory_percent': prediction,
                'current_memory_percent': current_features[1],
                'prediction_horizon_minutes': horizon_minutes,
                'confidence': 0.85  # Simplified confidence score
            }
            
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            return {}

class IntelligentCache:
    """Intelligent caching system with ML-based optimization"""
    
    def __init__(self, max_size: int = 10000, redis_url: str = None):
        self.max_size = max_size
        self.redis_url = redis_url
        self._cache: Dict[str, Any] = {}
        self._access_times: Dict[str, datetime] = {}
        self._access_counts: Dict[str, int] = defaultdict(int)
        self._cache_stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'size': 0
        }
        self._lock = asyncio.Lock()
        self.redis_client: Optional[aioredis.Redis] = None
        
    async def initialize(self):
        """Initialize cache system"""
        if self.redis_url:
            try:
                self.redis_client = aioredis.from_url(self.redis_url)
                await self.redis_client.ping()
                logger.info("Redis cache initialized")
            except Exception as e:
                logger.warning(f"Redis not available, using memory cache: {e}")
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        async with self._lock:
            # Try Redis first
            if self.redis_client:
                try:
                    value = await self.redis_client.get(key)
                    if value:
                        self._cache_stats['hits'] += 1
                        self._access_times[key] = datetime.utcnow()
                        self._access_counts[key] += 1
                        return pickle.loads(zlib.decompress(value))
                except Exception as e:
                    logger.warning(f"Redis get error: {e}")
            
            # Try memory cache
            if key in self._cache:
                self._cache_stats['hits'] += 1
                self._access_times[key] = datetime.utcnow()
                self._access_counts[key] += 1
                return self._cache[key]
            
            self._cache_stats['misses'] += 1
            return None
    
    async def set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in cache"""
        async with self._lock:
            # Compress and serialize value
            serialized_value = zlib.compress(pickle.dumps(value))
            
            # Store in Redis
            if self.redis_client:
                try:
                    await self.redis_client.setex(key, ttl, serialized_value)
                except Exception as e:
                    logger.warning(f"Redis set error: {e}")
            
            # Store in memory cache
            if len(self._cache) >= self.max_size:
                await self._evict_items()
            
            self._cache[key] = value
            self._access_times[key] = datetime.utcnow()
            self._access_counts[key] += 1
            self._cache_stats['size'] = len(self._cache)
    
    async def _evict_items(self, count: int = None):
        """Evict items using intelligent strategy"""
        if not count:
            count = max(1, len(self._cache) // 10)  # Evict 10% by default
        
        # Calculate eviction scores (lower = more likely to evict)
        scores = {}
        current_time = datetime.utcnow()
        
        for key in self._cache:
            last_access = self._access_times.get(key, datetime.min)
            access_count = self._access_counts.get(key, 0)
            
            # Time since last access (normalized)
            time_score = (current_time - last_access).total_seconds() / 3600  # hours
            
            # Access frequency (inverse)
            frequency_score = 1.0 / (access_count + 1)
            
            # Combined score (higher time + higher frequency = higher eviction score)
            scores[key] = time_score + frequency_score
        
        # Evict items with highest scores
        items_to_evict = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:count]
        
        for key, _ in items_to_evict:
            if key in self._cache:
                del self._cache[key]
            if key in self._access_times:
                del self._access_times[key]
            if key in self._access_counts:
                del self._access_counts[key]
            
            self._cache_stats['evictions'] += 1
        
        self._cache_stats['size'] = len(self._cache)
    
    async def delete(self, key: str):
        """Delete key from cache"""
        async with self._lock:
            # Delete from Redis
            if self.redis_client:
                try:
                    await self.redis_client.delete(key)
                except Exception as e:
                    logger.warning(f"Redis delete error: {e}")
            
            # Delete from memory cache
            if key in self._cache:
                del self._cache[key]
            if key in self._access_times:
                del self._access_times[key]
            if key in self._access_counts:
                del self._access_counts[key]
            
            self._cache_stats['size'] = len(self._cache)
    
    async def clear(self):
        """Clear all cache"""
        async with self._lock:
            if self.redis_client:
                try:
                    await self.redis_client.flushdb()
                except Exception as e:
                    logger.warning(f"Redis clear error: {e}")
            
            self._cache.clear()
            self._access_times.clear()
            self._access_counts.clear()
            self._cache_stats['size'] = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self._cache_stats['hits'] + self._cache_stats['misses']
        hit_rate = self._cache_stats['hits'] / total_requests if total_requests > 0 else 0
        
        return {
            **self._cache_stats,
            'hit_rate': hit_rate,
            'total_requests': total_requests
        }
    
    def get_key_analytics(self) -> Dict[str, Any]:
        """Get analytics about cached keys"""
        if not self._access_counts:
            return {}
        
        access_counts = list(self._access_counts.values())
        
        return {
            'total_keys': len(self._access_counts),
            'avg_access_count': statistics.mean(access_counts),
            'max_access_count': max(access_counts),
            'min_access_count': min(access_counts),
            'most_accessed_keys': sorted(
                self._access_counts.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:10]
        }

class QueryOptimizer:
    """Intelligent query optimization system"""
    
    def __init__(self):
        self.query_patterns: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.optimization_rules: List[Dict[str, Any]] = []
        self._lock = asyncio.Lock()
        
    async def analyze_query(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze query and provide optimization recommendations"""
        async with self._lock:
            query_hash = self._hash_query(query)
            
            # Record query pattern
            self.query_patterns[query_hash].append({
                'query': query,
                'timestamp': datetime.utcnow(),
                'execution_count': len(self.query_patterns[query_hash]) + 1
            })
            
            # Generate optimization recommendations
            recommendations = []
            
            # Check for common patterns
            if len(self.query_patterns[query_hash]) > 5:
                recommendations.append(OptimizationRecommendation(
                    category="caching",
                    priority=2,
                    description="This query pattern is frequently used",
                    implementation="Cache results with extended TTL",
                    expected_improvement=0.3,
                    confidence=0.8
                ))
            
            # Check query complexity
            complexity_score = self._calculate_query_complexity(query)
            if complexity_score > 0.7:
                recommendations.append(OptimizationRecommendation(
                    category="query_optimization",
                    priority=1,
                    description="Query has high complexity",
                    implementation="Consider breaking into smaller sub-queries",
                    expected_improvement=0.4,
                    confidence=0.7
                ))
            
            # Check for parallel execution opportunities
            if self._can_parallelize(query):
                recommendations.append(OptimizationRecommendation(
                    category="parallelization",
                    priority=2,
                    description="Query can be parallelized",
                    implementation="Execute scanner modules concurrently",
                    expected_improvement=0.5,
                    confidence=0.9
                ))
            
            return {
                'query_hash': query_hash,
                'complexity_score': complexity_score,
                'recommendations': recommendations,
                'historical_executions': len(self.query_patterns[query_hash])
            }
    
    def _hash_query(self, query: Dict[str, Any]) -> str:
        """Generate hash for query pattern"""
        # Normalize query for pattern matching
        normalized = {
            'type': query.get('type', ''),
            'scanners': sorted(query.get('scanners', [])),
            'filters': sorted(query.get('filters', {}).keys())
        }
        
        query_str = json.dumps(normalized, sort_keys=True)
        return hashlib.md5(query_str.encode()).hexdigest()
    
    def _calculate_query_complexity(self, query: Dict[str, Any]) -> float:
        """Calculate query complexity score (0-1)"""
        complexity = 0.0
        
        # Number of scanners
        scanners = query.get('scanners', [])
        complexity += min(len(scanners) / 10, 0.3)
        
        # Number of filters
        filters = query.get('filters', {})
        complexity += min(len(filters) / 5, 0.2)
        
        # Query value complexity (rough estimate)
        query_value = query.get('query_value', '')
        if len(query_value) > 100:
            complexity += 0.1
        
        # Nested queries or complex operations
        if 'sub_queries' in query:
            complexity += 0.3
        
        return min(complexity, 1.0)
    
    def _can_parallelize(self, query: Dict[str, Any]) -> bool:
        """Check if query can be parallelized"""
        scanners = query.get('scanners', [])
        
        # Can parallelize if multiple independent scanners
        return len(scanners) > 1
    
    def get_optimization_patterns(self) -> Dict[str, Any]:
        """Get optimization patterns and statistics"""
        pattern_stats = {}
        
        for pattern_hash, executions in self.query_patterns.items():
            pattern_stats[pattern_hash] = {
                'execution_count': len(executions),
                'first_seen': min(e['timestamp'] for e in executions),
                'last_seen': max(e['timestamp'] for e in executions),
                'avg_executions_per_day': len(executions) / max(
                    (datetime.utcnow() - min(e['timestamp'] for e in executions)).days, 1
                )
            }
        
        return {
            'total_patterns': len(self.query_patterns),
            'pattern_statistics': pattern_stats,
            'most_frequent_patterns': sorted(
                pattern_stats.items(),
                key=lambda x: x[1]['execution_count'],
                reverse=True
            )[:10]
        }

class OptimizationEngine:
    """Main optimization engine coordinating all optimization components"""
    
    def __init__(self):
        self.system_monitor = SystemMonitor()
        self.intelligent_cache = IntelligentCache()
        self.query_optimizer = QueryOptimizer()
        self.optimization_history: List[OptimizationRecommendation] = []
        self.running = False
        self._optimization_task: Optional[asyncio.Task] = None
        
    async def start(self):
        """Start optimization engine"""
        await self.intelligent_cache.initialize()
        await self.system_monitor.start_monitoring()
        
        self.running = True
        self._optimization_task = asyncio.create_task(self._optimization_loop())
        
        logger.info("Optimization Engine started")
    
    async def stop(self):
        """Stop optimization engine"""
        self.running = False
        
        if self._optimization_task:
            self._optimization_task.cancel()
            try:
                await self._optimization_task
            except asyncio.CancelledError:
                pass
        
        await self.system_monitor.stop_monitoring()
        logger.info("Optimization Engine stopped")
    
    async def _optimization_loop(self):
        """Main optimization loop"""
        while self.running:
            try:
                # Run optimization analysis every 5 minutes
                await asyncio.sleep(300)
                
                # Train prediction model periodically
                await self.system_monitor.train_prediction_model()
                
                # Generate system-wide optimization recommendations
                recommendations = await self._generate_optimization_recommendations()
                self.optimization_history.extend(recommendations)
                
                # Keep only recent recommendations
                cutoff_time = datetime.utcnow() - timedelta(days=7)
                self.optimization_history = [
                    r for r in self.optimization_history 
                    if getattr(r, 'timestamp', datetime.utcnow()) >= cutoff_time
                ]
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in optimization loop: {e}")
                await asyncio.sleep(60)
    
    async def _generate_optimization_recommendations(self) -> List[OptimizationRecommendation]:
        """Generate system-wide optimization recommendations"""
        recommendations = []
        
        # System resource recommendations
        memory_stats = self.system_monitor.get_metric_statistics('memory_percent', 60)
        if memory_stats and memory_stats.get('mean', 0) > 80:
            recommendations.append(OptimizationRecommendation(
                category="memory",
                priority=1,
                description="High memory usage detected",
                implementation="Increase cache eviction frequency or reduce cache size",
                expected_improvement=0.2,
                confidence=0.9
            ))
        
        cpu_stats = self.system_monitor.get_metric_statistics('cpu_percent', 60)
        if cpu_stats and cpu_stats.get('mean', 0) > 80:
            recommendations.append(OptimizationRecommendation(
                category="cpu",
                priority=1,
                description="High CPU usage detected",
                implementation="Reduce concurrent task limit or optimize scanner algorithms",
                expected_improvement=0.25,
                confidence=0.85
            ))
        
        # Cache recommendations
        cache_stats = self.intelligent_cache.get_stats()
        if cache_stats.get('hit_rate', 0) < 0.5:
            recommendations.append(OptimizationRecommendation(
                category="caching",
                priority=2,
                description="Low cache hit rate",
                implementation="Adjust cache size or TTL settings",
                expected_improvement=0.3,
                confidence=0.7
            ))
        
        return recommendations
    
    async def optimize_query(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize a specific query"""
        return await self.query_optimizer.analyze_query(query)
    
    async def get_cache(self, key: str) -> Optional[Any]:
        """Get value from intelligent cache"""
        return await self.intelligent_cache.get(key)
    
    async def set_cache(self, key: str, value: Any, ttl: int = 3600):
        """Set value in intelligent cache"""
        await self.intelligent_cache.set(key, value, ttl)
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get comprehensive system health report"""
        # Recent system metrics
        recent_metrics = {}
        metric_names = ['cpu_percent', 'memory_percent', 'disk_percent']
        
        for metric_name in metric_names:
            stats = self.system_monitor.get_metric_statistics(metric_name, 15)
            if stats:
                recent_metrics[metric_name] = stats
        
        # Performance predictions
        predictions = self.system_monitor.predict_resource_usage(30)
        
        # Cache performance
        cache_stats = self.intelligent_cache.get_stats()
        
        # Recent optimization recommendations
        recent_recommendations = [
            {
                'category': r.category,
                'priority': r.priority,
                'description': r.description,
                'expected_improvement': r.expected_improvement
            }
            for r in self.optimization_history[-10:]
        ]
        
        return {
            'system_metrics': recent_metrics,
            'predictions': predictions,
            'cache_performance': cache_stats,
            'recent_recommendations': recent_recommendations,
            'health_score': self._calculate_health_score(recent_metrics, cache_stats)
        }
    
    def _calculate_health_score(self, metrics: Dict[str, Any], cache_stats: Dict[str, Any]) -> float:
        """Calculate overall system health score (0-1)"""
        score = 1.0
        
        # CPU health
        cpu_stats = metrics.get('cpu_percent', {})
        if cpu_stats:
            cpu_mean = cpu_stats.get('mean', 0)
            if cpu_mean > 90:
                score -= 0.3
            elif cpu_mean > 70:
                score -= 0.1
        
        # Memory health
        mem_stats = metrics.get('memory_percent', {})
        if mem_stats:
            mem_mean = mem_stats.get('mean', 0)
            if mem_mean > 90:
                score -= 0.3
            elif mem_mean > 70:
                score -= 0.1
        
        # Disk health
        disk_stats = metrics.get('disk_percent', {})
        if disk_stats:
            disk_mean = disk_stats.get('mean', 0)
            if disk_mean > 95:
                score -= 0.2
            elif disk_mean > 80:
                score -= 0.05
        
        # Cache health
        hit_rate = cache_stats.get('hit_rate', 0)
        if hit_rate < 0.3:
            score -= 0.1
        elif hit_rate < 0.5:
            score -= 0.05
        
        return max(0, score)

# Global optimization engine instance
optimization_engine = OptimizationEngine()

async def start_optimization_engine():
    """Start the global optimization engine"""
    await optimization_engine.start()

async def stop_optimization_engine():
    """Stop the global optimization engine"""
    await optimization_engine.stop()