"""
Advanced Intelligence Orchestrator
Comprehensive orchestration engine for managing all intelligence gathering operations
with advanced workflow management, load balancing, and optimization capabilities.
"""

import asyncio
import logging
import time
from typing import Dict, List, Any, Optional, Set, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import threading
from datetime import datetime, timedelta
import uuid
import aioredis
import psutil
from collections import defaultdict, deque
import heapq
import statistics

logger = logging.getLogger(__name__)

class TaskPriority(Enum):
    """Task priority levels for intelligent scheduling"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKGROUND = 5

class WorkflowStatus(Enum):
    """Workflow execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"

@dataclass
class Task:
    """Represents a single intelligence gathering task"""
    id: str
    scanner_type: str
    query: str
    priority: TaskPriority
    created_at: datetime
    estimated_duration: float
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    retry_count: int = 0
    max_retries: int = 3
    timeout: float = 300.0
    
class WorkflowNode:
    """Node in the workflow execution graph"""
    
    def __init__(self, task: Task):
        self.task = task
        self.status = WorkflowStatus.PENDING
        self.result: Optional[Dict[str, Any]] = None
        self.error: Optional[Exception] = None
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.dependencies: Set[str] = set(task.dependencies)
        self.dependents: Set[str] = set()
        
    @property
    def duration(self) -> Optional[float]:
        """Calculate task execution duration"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
    
    @property
    def is_ready(self) -> bool:
        """Check if task is ready for execution"""
        return self.status == WorkflowStatus.PENDING and len(self.dependencies) == 0

class ResourceManager:
    """Manages system resources and load balancing"""
    
    def __init__(self, max_concurrent_tasks: int = 10):
        self.max_concurrent_tasks = max_concurrent_tasks
        self.active_tasks: Set[str] = set()
        self.resource_locks: Dict[str, asyncio.Lock] = {}
        self.performance_history: deque = deque(maxlen=1000)
        self._lock = asyncio.Lock()
        
    async def acquire_resources(self, task: Task) -> bool:
        """Acquire resources for task execution"""
        async with self._lock:
            if len(self.active_tasks) >= self.max_concurrent_tasks:
                return False
                
            # Check system resources
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory_percent = psutil.virtual_memory().percent
            
            if cpu_percent > 90 or memory_percent > 90:
                logger.warning(f"System resources high: CPU {cpu_percent}%, Memory {memory_percent}%")
                return False
                
            self.active_tasks.add(task.id)
            return True
    
    async def release_resources(self, task_id: str):
        """Release resources after task completion"""
        async with self._lock:
            self.active_tasks.discard(task_id)
    
    def record_performance(self, task_id: str, duration: float, success: bool):
        """Record task performance metrics"""
        self.performance_history.append({
            'task_id': task_id,
            'duration': duration,
            'success': success,
            'timestamp': datetime.utcnow()
        })
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        if not self.performance_history:
            return {}
            
        durations = [h['duration'] for h in self.performance_history]
        success_rate = sum(1 for h in self.performance_history if h['success']) / len(self.performance_history)
        
        return {
            'total_tasks': len(self.performance_history),
            'success_rate': success_rate,
            'avg_duration': statistics.mean(durations),
            'min_duration': min(durations),
            'max_duration': max(durations),
            'median_duration': statistics.median(durations)
        }

class WorkflowEngine:
    """Advanced workflow execution engine with dependency management"""
    
    def __init__(self):
        self.workflows: Dict[str, Dict[str, WorkflowNode]] = {}
        self.task_queue: List[Tuple[TaskPriority, str, str]] = []  # priority, workflow_id, task_id
        self.completed_workflows: Dict[str, Dict[str, Any]] = {}
        self._lock = asyncio.Lock()
        
    async def create_workflow(self, workflow_id: str, tasks: List[Task]) -> bool:
        """Create a new workflow with dependency graph"""
        async with self._lock:
            if workflow_id in self.workflows:
                return False
                
            # Build dependency graph
            nodes = {task.id: WorkflowNode(task) for task in tasks}
            
            # Set up dependency relationships
            for task in tasks:
                node = nodes[task.id]
                for dep_id in task.dependencies:
                    if dep_id in nodes:
                        nodes[dep_id].dependents.add(task.id)
                    else:
                        logger.warning(f"Dependency {dep_id} not found for task {task.id}")
            
            self.workflows[workflow_id] = nodes
            
            # Queue ready tasks
            for task_id, node in nodes.items():
                if node.is_ready:
                    heapq.heappush(self.task_queue, (node.task.priority, workflow_id, task_id))
            
            return True
    
    async def get_next_task(self) -> Optional[Tuple[str, Task]]:
        """Get the next task to execute based on priority"""
        async with self._lock:
            while self.task_queue:
                priority, workflow_id, task_id = heapq.heappop(self.task_queue)
                
                if workflow_id in self.workflows and task_id in self.workflows[workflow_id]:
                    node = self.workflows[workflow_id][task_id]
                    if node.is_ready:
                        node.status = WorkflowStatus.RUNNING
                        node.start_time = datetime.utcnow()
                        return workflow_id, node.task
                        
            return None
    
    async def complete_task(self, workflow_id: str, task_id: str, result: Dict[str, Any], error: Optional[Exception] = None):
        """Mark task as completed and update workflow state"""
        async with self._lock:
            if workflow_id not in self.workflows or task_id not in self.workflows[workflow_id]:
                return
                
            node = self.workflows[workflow_id][task_id]
            node.end_time = datetime.utcnow()
            node.result = result
            node.error = error
            node.status = WorkflowStatus.COMPLETED if error is None else WorkflowStatus.FAILED
            
            # Update dependent tasks
            if error is None:
                for dependent_id in node.dependents:
                    if dependent_id in self.workflows[workflow_id]:
                        dependent_node = self.workflows[workflow_id][dependent_id]
                        dependent_node.dependencies.discard(task_id)
                        
                        # Queue dependent task if ready
                        if dependent_node.is_ready:
                            heapq.heappush(self.task_queue, (dependent_node.task.priority, workflow_id, dependent_id))
            
            # Check if workflow is complete
            await self._check_workflow_completion(workflow_id)
    
    async def _check_workflow_completion(self, workflow_id: str):
        """Check if workflow is complete and move to completed workflows"""
        if workflow_id not in self.workflows:
            return
            
        nodes = self.workflows[workflow_id]
        all_completed = all(node.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED] for node in nodes.values())
        
        if all_completed:
            # Move to completed workflows
            workflow_result = {
                'workflow_id': workflow_id,
                'completed_at': datetime.utcnow(),
                'tasks': {
                    task_id: {
                        'status': node.status.value,
                        'duration': node.duration,
                        'result': node.result,
                        'error': str(node.error) if node.error else None
                    }
                    for task_id, node in nodes.items()
                }
            }
            
            self.completed_workflows[workflow_id] = workflow_result
            del self.workflows[workflow_id]
            
            logger.info(f"Workflow {workflow_id} completed")

class IntelligenceOrchestrator:
    """Advanced orchestrator for intelligence gathering operations"""
    
    def __init__(self, max_concurrent_tasks: int = 10):
        self.resource_manager = ResourceManager(max_concurrent_tasks)
        self.workflow_engine = WorkflowEngine()
        self.executor = ThreadPoolExecutor(max_workers=max_concurrent_tasks)
        self.running = False
        self.metrics: Dict[str, Any] = defaultdict(int)
        self._background_task: Optional[asyncio.Task] = None
        
    async def start(self):
        """Start the orchestrator"""
        self.running = True
        self._background_task = asyncio.create_task(self._orchestration_loop())
        logger.info("Intelligence Orchestrator started")
    
    async def stop(self):
        """Stop the orchestrator"""
        self.running = False
        if self._background_task:
            self._background_task.cancel()
            try:
                await self._background_task
            except asyncio.CancelledError:
                pass
        self.executor.shutdown(wait=True)
        logger.info("Intelligence Orchestrator stopped")
    
    async def submit_workflow(self, tasks: List[Dict[str, Any]]) -> str:
        """Submit a workflow for execution"""
        workflow_id = str(uuid.uuid4())
        
        # Convert task dictionaries to Task objects
        task_objects = []
        for task_data in tasks:
            task = Task(
                id=task_data.get('id', str(uuid.uuid4())),
                scanner_type=task_data['scanner_type'],
                query=task_data['query'],
                priority=TaskPriority(task_data.get('priority', TaskPriority.MEDIUM.value)),
                created_at=datetime.utcnow(),
                estimated_duration=task_data.get('estimated_duration', 60.0),
                dependencies=task_data.get('dependencies', []),
                metadata=task_data.get('metadata', {}),
                timeout=task_data.get('timeout', 300.0)
            )
            task_objects.append(task)
        
        success = await self.workflow_engine.create_workflow(workflow_id, task_objects)
        if success:
            self.metrics['workflows_submitted'] += 1
            logger.info(f"Workflow {workflow_id} submitted with {len(task_objects)} tasks")
            return workflow_id
        else:
            raise ValueError(f"Failed to create workflow {workflow_id}")
    
    async def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a workflow"""
        # Check active workflows
        if workflow_id in self.workflow_engine.workflows:
            nodes = self.workflow_engine.workflows[workflow_id]
            return {
                'workflow_id': workflow_id,
                'status': 'running',
                'tasks': {
                    task_id: {
                        'status': node.status.value,
                        'progress': self._calculate_task_progress(node)
                    }
                    for task_id, node in nodes.items()
                }
            }
        
        # Check completed workflows
        if workflow_id in self.workflow_engine.completed_workflows:
            return self.workflow_engine.completed_workflows[workflow_id]
        
        return None
    
    def _calculate_task_progress(self, node: WorkflowNode) -> float:
        """Calculate task progress based on status and elapsed time"""
        if node.status == WorkflowStatus.COMPLETED:
            return 1.0
        elif node.status == WorkflowStatus.FAILED:
            return 0.0
        elif node.status == WorkflowStatus.RUNNING and node.start_time:
            elapsed = (datetime.utcnow() - node.start_time).total_seconds()
            progress = min(elapsed / node.task.estimated_duration, 0.95)
            return progress
        else:
            return 0.0
    
    async def _orchestration_loop(self):
        """Main orchestration loop"""
        while self.running:
            try:
                # Get next task
                next_task = await self.workflow_engine.get_next_task()
                if next_task is None:
                    await asyncio.sleep(1)
                    continue
                
                workflow_id, task = next_task
                
                # Acquire resources
                if not await self.resource_manager.acquire_resources(task):
                    # Put task back in queue
                    await self.workflow_engine.task_queue.put((task.priority, workflow_id, task.id))
                    await asyncio.sleep(1)
                    continue
                
                # Execute task
                asyncio.create_task(self._execute_task(workflow_id, task))
                
            except Exception as e:
                logger.error(f"Error in orchestration loop: {e}")
                await asyncio.sleep(1)
    
    async def _execute_task(self, workflow_id: str, task: Task):
        """Execute a single task"""
        try:
            start_time = time.time()
            
            # Simulate task execution (replace with actual scanner execution)
            result = await self._simulate_scanner_execution(task)
            
            duration = time.time() - start_time
            
            # Record performance
            self.resource_manager.record_performance(task.id, duration, True)
            self.metrics['tasks_completed'] += 1
            
            # Complete task
            await self.workflow_engine.complete_task(workflow_id, task.id, result)
            
        except Exception as e:
            duration = time.time() - start_time if 'start_time' in locals() else 0
            
            # Record performance
            self.resource_manager.record_performance(task.id, duration, False)
            self.metrics['tasks_failed'] += 1
            
            # Handle task failure
            await self.workflow_engine.complete_task(workflow_id, task.id, {}, e)
            
            logger.error(f"Task {task.id} failed: {e}")
        
        finally:
            # Release resources
            await self.resource_manager.release_resources(task.id)
    
    async def _simulate_scanner_execution(self, task: Task) -> Dict[str, Any]:
        """Simulate scanner execution (replace with actual scanner integration)"""
        await asyncio.sleep(1)  # Simulate processing time
        
        return {
            'scanner_type': task.scanner_type,
            'query': task.query,
            'results': [
                {
                    'source': f"{task.scanner_type}_source",
                    'data': f"Mock data for {task.query}",
                    'confidence': 0.85,
                    'timestamp': datetime.utcnow().isoformat()
                }
            ],
            'metadata': task.metadata
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get orchestrator metrics"""
        performance_stats = self.resource_manager.get_performance_stats()
        
        return {
            'orchestrator_metrics': dict(self.metrics),
            'performance_stats': performance_stats,
            'active_tasks': len(self.resource_manager.active_tasks),
            'active_workflows': len(self.workflow_engine.workflows),
            'completed_workflows': len(self.workflow_engine.completed_workflows)
        }

class IntelligenceScheduler:
    """Advanced scheduler for periodic and scheduled intelligence operations"""
    
    def __init__(self, orchestrator: IntelligenceOrchestrator):
        self.orchestrator = orchestrator
        self.scheduled_workflows: Dict[str, Dict[str, Any]] = {}
        self.cron_jobs: Dict[str, asyncio.Task] = {}
        self.running = False
        
    async def start(self):
        """Start the scheduler"""
        self.running = True
        logger.info("Intelligence Scheduler started")
    
    async def stop(self):
        """Stop the scheduler"""
        self.running = False
        
        # Cancel all cron jobs
        for job_id, task in self.cron_jobs.items():
            task.cancel()
        
        await asyncio.gather(*self.cron_jobs.values(), return_exceptions=True)
        self.cron_jobs.clear()
        logger.info("Intelligence Scheduler stopped")
    
    async def schedule_workflow(self, schedule_id: str, workflow_config: Dict[str, Any], 
                              schedule_type: str = "once", schedule_data: Dict[str, Any] = None):
        """Schedule a workflow for execution"""
        schedule_data = schedule_data or {}
        
        self.scheduled_workflows[schedule_id] = {
            'workflow_config': workflow_config,
            'schedule_type': schedule_type,
            'schedule_data': schedule_data,
            'created_at': datetime.utcnow(),
            'last_executed': None,
            'execution_count': 0
        }
        
        if schedule_type == "interval":
            # Schedule recurring workflow
            interval_seconds = schedule_data.get('interval_seconds', 3600)
            task = asyncio.create_task(self._run_interval_workflow(schedule_id, interval_seconds))
            self.cron_jobs[schedule_id] = task
        
        elif schedule_type == "cron":
            # Schedule cron-like workflow
            task = asyncio.create_task(self._run_cron_workflow(schedule_id, schedule_data))
            self.cron_jobs[schedule_id] = task
        
        elif schedule_type == "once":
            # Schedule one-time workflow
            execute_at = schedule_data.get('execute_at')
            if execute_at:
                task = asyncio.create_task(self._run_once_workflow(schedule_id, execute_at))
                self.cron_jobs[schedule_id] = task
        
        logger.info(f"Scheduled workflow {schedule_id} with type {schedule_type}")
    
    async def _run_interval_workflow(self, schedule_id: str, interval_seconds: int):
        """Run workflow at regular intervals"""
        while self.running and schedule_id in self.scheduled_workflows:
            try:
                await self._execute_scheduled_workflow(schedule_id)
                await asyncio.sleep(interval_seconds)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in interval workflow {schedule_id}: {e}")
                await asyncio.sleep(60)  # Wait before retrying
    
    async def _run_cron_workflow(self, schedule_id: str, schedule_data: Dict[str, Any]):
        """Run workflow based on cron-like schedule"""
        # Simplified cron implementation - extend as needed
        hour = schedule_data.get('hour', 0)
        minute = schedule_data.get('minute', 0)
        
        while self.running and schedule_id in self.scheduled_workflows:
            try:
                now = datetime.now()
                next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                if next_run <= now:
                    next_run += timedelta(days=1)
                
                sleep_seconds = (next_run - now).total_seconds()
                await asyncio.sleep(sleep_seconds)
                
                if self.running:
                    await self._execute_scheduled_workflow(schedule_id)
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in cron workflow {schedule_id}: {e}")
                await asyncio.sleep(3600)  # Wait an hour before retrying
    
    async def _run_once_workflow(self, schedule_id: str, execute_at: datetime):
        """Run workflow once at specified time"""
        try:
            now = datetime.utcnow()
            if execute_at > now:
                sleep_seconds = (execute_at - now).total_seconds()
                await asyncio.sleep(sleep_seconds)
            
            await self._execute_scheduled_workflow(schedule_id)
            
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Error in once workflow {schedule_id}: {e}")
        finally:
            # Clean up one-time workflow
            if schedule_id in self.cron_jobs:
                del self.cron_jobs[schedule_id]
            if schedule_id in self.scheduled_workflows:
                del self.scheduled_workflows[schedule_id]
    
    async def _execute_scheduled_workflow(self, schedule_id: str):
        """Execute a scheduled workflow"""
        if schedule_id not in self.scheduled_workflows:
            return
        
        workflow_info = self.scheduled_workflows[schedule_id]
        workflow_config = workflow_info['workflow_config']
        
        try:
            workflow_id = await self.orchestrator.submit_workflow(workflow_config['tasks'])
            
            # Update execution info
            workflow_info['last_executed'] = datetime.utcnow()
            workflow_info['execution_count'] += 1
            workflow_info['last_workflow_id'] = workflow_id
            
            logger.info(f"Executed scheduled workflow {schedule_id} as {workflow_id}")
            
        except Exception as e:
            logger.error(f"Failed to execute scheduled workflow {schedule_id}: {e}")
    
    def get_scheduled_workflows(self) -> Dict[str, Dict[str, Any]]:
        """Get all scheduled workflows"""
        return dict(self.scheduled_workflows)

# Global orchestrator instance
intelligence_orchestrator = IntelligenceOrchestrator()
intelligence_scheduler = IntelligenceScheduler(intelligence_orchestrator)

async def start_orchestration_services():
    """Start all orchestration services"""
    await intelligence_orchestrator.start()
    await intelligence_scheduler.start()

async def stop_orchestration_services():
    """Stop all orchestration services"""
    await intelligence_scheduler.stop()
    await intelligence_orchestrator.stop()