"""
Advanced Orchestration Engine
============================

Enterprise-grade orchestration system for managing complex intelligence operations
with advanced workflow management, resource optimization, and failure recovery.
"""

import asyncio
import logging
import weakref
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable, Set
from enum import Enum
from dataclasses import dataclass, field
from collections import defaultdict
import uuid
import json

logger = logging.getLogger(__name__)


class WorkflowStatus(Enum):
    """Workflow execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class WorkflowTask:
    """Individual task within a workflow."""
    task_id: str
    name: str
    scanner_type: str
    target: str
    priority: TaskPriority = TaskPriority.NORMAL
    dependencies: List[str] = field(default_factory=list)
    retry_count: int = 0
    max_retries: int = 3
    timeout: int = 30
    metadata: Dict[str, Any] = field(default_factory=dict)
    status: WorkflowStatus = WorkflowStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class IntelligenceWorkflow:
    """Complete intelligence gathering workflow."""
    workflow_id: str
    name: str
    description: str
    tasks: List[WorkflowTask] = field(default_factory=list)
    status: WorkflowStatus = WorkflowStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    user_id: Optional[str] = None
    priority: TaskPriority = TaskPriority.NORMAL
    metadata: Dict[str, Any] = field(default_factory=dict)


class ResourceManager:
    """Advanced resource management for optimal performance."""
    
    def __init__(self, max_concurrent_tasks: int = 50):
        self.max_concurrent_tasks = max_concurrent_tasks
        self.active_tasks: Dict[str, WorkflowTask] = {}
        self.resource_usage: Dict[str, float] = defaultdict(float)
        self.priority_queues: Dict[TaskPriority, List[WorkflowTask]] = {
            priority: [] for priority in TaskPriority
        }
        
    async def can_execute_task(self, task: WorkflowTask) -> bool:
        """Check if task can be executed based on resource availability."""
        if len(self.active_tasks) >= self.max_concurrent_tasks:
            return False
            
        # Check scanner-specific resource limits
        scanner_usage = self.resource_usage.get(task.scanner_type, 0)
        max_scanner_concurrent = self._get_scanner_limit(task.scanner_type)
        
        return scanner_usage < max_scanner_concurrent
    
    def _get_scanner_limit(self, scanner_type: str) -> int:
        """Get concurrent execution limit for specific scanner type."""
        limits = {
            "email_validation": 20,
            "phone_lookup": 15,
            "social_media": 10,
            "domain_analysis": 25,
            "default": 10
        }
        return limits.get(scanner_type, limits["default"])
    
    async def acquire_resource(self, task: WorkflowTask):
        """Acquire resources for task execution."""
        self.active_tasks[task.task_id] = task
        self.resource_usage[task.scanner_type] += 1
        
    async def release_resource(self, task: WorkflowTask):
        """Release resources after task completion."""
        self.active_tasks.pop(task.task_id, None)
        self.resource_usage[task.scanner_type] = max(0, 
            self.resource_usage[task.scanner_type] - 1)


class WorkflowScheduler:
    """Advanced workflow scheduling with priority management."""
    
    def __init__(self, resource_manager: ResourceManager):
        self.resource_manager = resource_manager
        self.pending_workflows: List[IntelligenceWorkflow] = []
        self.active_workflows: Dict[str, IntelligenceWorkflow] = {}
        self.completed_workflows: Dict[str, IntelligenceWorkflow] = {}
        
    def add_workflow(self, workflow: IntelligenceWorkflow):
        """Add workflow to scheduling queue."""
        self.pending_workflows.append(workflow)
        self._sort_workflows_by_priority()
        
    def _sort_workflows_by_priority(self):
        """Sort workflows by priority and creation time."""
        self.pending_workflows.sort(
            key=lambda w: (w.priority.value, w.created_at),
            reverse=True
        )
    
    async def get_next_executable_tasks(self) -> List[WorkflowTask]:
        """Get next batch of tasks ready for execution."""
        executable_tasks = []
        
        for workflow in list(self.pending_workflows):
            if workflow.status != WorkflowStatus.PENDING:
                continue
                
            ready_tasks = self._get_ready_tasks(workflow)
            for task in ready_tasks:
                if await self.resource_manager.can_execute_task(task):
                    executable_tasks.append(task)
                    
                    # Move workflow to active if it has tasks starting
                    if workflow.workflow_id not in self.active_workflows:
                        workflow.status = WorkflowStatus.RUNNING
                        workflow.started_at = datetime.utcnow()
                        self.active_workflows[workflow.workflow_id] = workflow
                        self.pending_workflows.remove(workflow)
                        
        return executable_tasks
    
    def _get_ready_tasks(self, workflow: IntelligenceWorkflow) -> List[WorkflowTask]:
        """Get tasks that are ready to execute (dependencies satisfied)."""
        ready_tasks = []
        completed_task_ids = {
            task.task_id for task in workflow.tasks 
            if task.status == WorkflowStatus.COMPLETED
        }
        
        for task in workflow.tasks:
            if task.status != WorkflowStatus.PENDING:
                continue
                
            # Check if all dependencies are completed
            if all(dep_id in completed_task_ids for dep_id in task.dependencies):
                ready_tasks.append(task)
                
        return ready_tasks


class AdvancedOrchestrationEngine:
    """
    Advanced orchestration engine for enterprise intelligence operations.
    
    Features:
    - Workflow management with dependencies
    - Resource optimization and scheduling
    - Failure recovery and retry logic
    - Real-time progress tracking
    - Performance analytics
    """
    
    def __init__(self, max_concurrent_tasks: int = 50):
        self.resource_manager = ResourceManager(max_concurrent_tasks)
        self.scheduler = WorkflowScheduler(self.resource_manager)
        self.scanner_registry: Dict[str, Any] = {}
        self.active_executions: Dict[str, asyncio.Task] = {}
        self.performance_metrics: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.event_handlers: Dict[str, List[Callable]] = defaultdict(list)
        
        # Start background scheduler
        self._scheduler_task = None
        self._running = False
        
    async def start(self):
        """Start the orchestration engine."""
        if not self._running:
            self._running = True
            self._scheduler_task = asyncio.create_task(self._scheduler_loop())
            logger.info("🚀 Advanced Orchestration Engine started")
    
    async def stop(self):
        """Stop the orchestration engine."""
        self._running = False
        if self._scheduler_task:
            self._scheduler_task.cancel()
            try:
                await self._scheduler_task
            except asyncio.CancelledError:
                pass
        logger.info("⏹️ Advanced Orchestration Engine stopped")
    
    def register_scanner(self, scanner_type: str, scanner_class: Any):
        """Register a scanner type with the orchestration engine."""
        self.scanner_registry[scanner_type] = scanner_class
        logger.info(f"📝 Registered scanner: {scanner_type}")
    
    def add_event_handler(self, event_type: str, handler: Callable):
        """Add event handler for workflow events."""
        self.event_handlers[event_type].append(handler)
    
    async def submit_workflow(self, workflow: IntelligenceWorkflow) -> str:
        """Submit a workflow for execution."""
        # Validate workflow
        await self._validate_workflow(workflow)
        
        # Add to scheduler
        self.scheduler.add_workflow(workflow)
        
        # Emit event
        await self._emit_event("workflow_submitted", {
            "workflow_id": workflow.workflow_id,
            "name": workflow.name,
            "task_count": len(workflow.tasks)
        })
        
        logger.info(f"📋 Workflow submitted: {workflow.name} ({workflow.workflow_id})")
        return workflow.workflow_id
    
    async def get_workflow_status(self, workflow_id: str) -> Optional[IntelligenceWorkflow]:
        """Get current status of a workflow."""
        # Check active workflows
        if workflow_id in self.scheduler.active_workflows:
            return self.scheduler.active_workflows[workflow_id]
            
        # Check completed workflows
        if workflow_id in self.scheduler.completed_workflows:
            return self.scheduler.completed_workflows[workflow_id]
            
        # Check pending workflows
        for workflow in self.scheduler.pending_workflows:
            if workflow.workflow_id == workflow_id:
                return workflow
                
        return None
    
    async def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel a running or pending workflow."""
        workflow = await self.get_workflow_status(workflow_id)
        if not workflow:
            return False
            
        # Cancel active tasks
        for task in workflow.tasks:
            if task.task_id in self.active_executions:
                self.active_executions[task.task_id].cancel()
                
        # Update workflow status
        workflow.status = WorkflowStatus.CANCELLED
        workflow.completed_at = datetime.utcnow()
        
        # Move to completed
        if workflow_id in self.scheduler.active_workflows:
            self.scheduler.completed_workflows[workflow_id] = workflow
            del self.scheduler.active_workflows[workflow_id]
        
        await self._emit_event("workflow_cancelled", {
            "workflow_id": workflow_id
        })
        
        logger.info(f"❌ Workflow cancelled: {workflow_id}")
        return True
    
    async def _scheduler_loop(self):
        """Main scheduler loop for task execution."""
        while self._running:
            try:
                # Get next executable tasks
                tasks = await self.scheduler.get_next_executable_tasks()
                
                # Execute tasks
                for task in tasks:
                    await self._execute_task(task)
                
                # Check for completed workflows
                await self._check_completed_workflows()
                
                # Brief pause to prevent busy waiting
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"❌ Scheduler loop error: {str(e)}")
                await asyncio.sleep(1)
    
    async def _execute_task(self, task: WorkflowTask):
        """Execute a single task."""
        try:
            # Acquire resources
            await self.resource_manager.acquire_resource(task)
            
            # Update task status
            task.status = WorkflowStatus.RUNNING
            task.started_at = datetime.utcnow()
            
            # Create execution coroutine
            execution_coro = self._run_task(task)
            execution_task = asyncio.create_task(execution_coro)
            self.active_executions[task.task_id] = execution_task
            
            logger.info(f"▶️ Started task: {task.name} ({task.task_id})")
            
        except Exception as e:
            logger.error(f"❌ Failed to start task {task.task_id}: {str(e)}")
            task.status = WorkflowStatus.FAILED
            task.error = str(e)
            await self.resource_manager.release_resource(task)
    
    async def _run_task(self, task: WorkflowTask):
        """Run the actual task execution."""
        try:
            # Get scanner instance
            scanner_class = self.scanner_registry.get(task.scanner_type)
            if not scanner_class:
                raise ValueError(f"Unknown scanner type: {task.scanner_type}")
                
            scanner = scanner_class()
            
            # Execute with timeout
            start_time = datetime.utcnow()
            try:
                result = await asyncio.wait_for(
                    scanner.scan(task.target, **task.metadata),
                    timeout=task.timeout
                )
                
                # Update task with result
                task.result = result
                task.status = WorkflowStatus.COMPLETED
                task.completed_at = datetime.utcnow()
                
                # Record performance metrics
                execution_time = (task.completed_at - start_time).total_seconds()
                self._record_performance_metric(task, execution_time, True)
                
                logger.info(f"✅ Task completed: {task.name} ({task.task_id})")
                
            except asyncio.TimeoutError:
                raise Exception(f"Task timeout after {task.timeout} seconds")
                
        except Exception as e:
            # Handle task failure
            await self._handle_task_failure(task, str(e))
            
        finally:
            # Clean up resources
            await self.resource_manager.release_resource(task)
            self.active_executions.pop(task.task_id, None)
    
    async def _handle_task_failure(self, task: WorkflowTask, error: str):
        """Handle task failure with retry logic."""
        task.retry_count += 1
        task.error = error
        
        if task.retry_count <= task.max_retries:
            # Retry task
            task.status = WorkflowStatus.PENDING
            logger.warning(f"🔄 Retrying task: {task.name} (attempt {task.retry_count})")
            
            # Add delay before retry
            await asyncio.sleep(min(2 ** task.retry_count, 30))
            
        else:
            # Mark as failed
            task.status = WorkflowStatus.FAILED
            task.completed_at = datetime.utcnow()
            
            # Record performance metrics
            execution_time = (task.completed_at - task.started_at).total_seconds()
            self._record_performance_metric(task, execution_time, False)
            
            logger.error(f"❌ Task failed permanently: {task.name} ({task.task_id})")
    
    async def _check_completed_workflows(self):
        """Check for completed workflows and update their status."""
        for workflow_id, workflow in list(self.scheduler.active_workflows.items()):
            if self._is_workflow_completed(workflow):
                workflow.status = WorkflowStatus.COMPLETED
                workflow.completed_at = datetime.utcnow()
                
                # Move to completed
                self.scheduler.completed_workflows[workflow_id] = workflow
                del self.scheduler.active_workflows[workflow_id]
                
                await self._emit_event("workflow_completed", {
                    "workflow_id": workflow_id,
                    "duration": (workflow.completed_at - workflow.started_at).total_seconds(),
                    "task_count": len(workflow.tasks)
                })
                
                logger.info(f"🎉 Workflow completed: {workflow.name} ({workflow_id})")
    
    def _is_workflow_completed(self, workflow: IntelligenceWorkflow) -> bool:
        """Check if all tasks in workflow are completed or failed."""
        return all(
            task.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED]
            for task in workflow.tasks
        )
    
    async def _validate_workflow(self, workflow: IntelligenceWorkflow):
        """Validate workflow before execution."""
        if not workflow.tasks:
            raise ValueError("Workflow must contain at least one task")
            
        # Check for circular dependencies
        task_ids = {task.task_id for task in workflow.tasks}
        for task in workflow.tasks:
            if not all(dep_id in task_ids for dep_id in task.dependencies):
                raise ValueError(f"Task {task.task_id} has invalid dependencies")
                
        # Check scanner types
        for task in workflow.tasks:
            if task.scanner_type not in self.scanner_registry:
                raise ValueError(f"Unknown scanner type: {task.scanner_type}")
    
    def _record_performance_metric(self, task: WorkflowTask, execution_time: float, success: bool):
        """Record performance metrics for analysis."""
        metric = {
            "timestamp": datetime.utcnow().isoformat(),
            "task_id": task.task_id,
            "scanner_type": task.scanner_type,
            "execution_time": execution_time,
            "success": success,
            "retry_count": task.retry_count
        }
        self.performance_metrics[task.scanner_type].append(metric)
        
        # Keep only recent metrics (last 1000 per scanner type)
        if len(self.performance_metrics[task.scanner_type]) > 1000:
            self.performance_metrics[task.scanner_type] = \
                self.performance_metrics[task.scanner_type][-1000:]
    
    async def _emit_event(self, event_type: str, data: Dict[str, Any]):
        """Emit event to registered handlers."""
        for handler in self.event_handlers[event_type]:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event_type, data)
                else:
                    handler(event_type, data)
            except Exception as e:
                logger.error(f"❌ Event handler error: {str(e)}")
    
    def get_performance_analytics(self) -> Dict[str, Any]:
        """Get performance analytics for all scanner types."""
        analytics = {}
        
        for scanner_type, metrics in self.performance_metrics.items():
            if not metrics:
                continue
                
            recent_metrics = metrics[-100:]  # Last 100 executions
            success_rate = sum(1 for m in recent_metrics if m["success"]) / len(recent_metrics)
            avg_time = sum(m["execution_time"] for m in recent_metrics) / len(recent_metrics)
            
            analytics[scanner_type] = {
                "total_executions": len(metrics),
                "recent_success_rate": success_rate,
                "average_execution_time": avg_time,
                "last_execution": recent_metrics[-1]["timestamp"] if recent_metrics else None
            }
            
        return analytics


# Workflow builder utilities
class WorkflowBuilder:
    """Builder pattern for creating complex workflows."""
    
    def __init__(self, name: str, description: str = ""):
        self.workflow = IntelligenceWorkflow(
            workflow_id=str(uuid.uuid4()),
            name=name,
            description=description
        )
    
    def add_task(self, name: str, scanner_type: str, target: str,
                 dependencies: List[str] = None, priority: TaskPriority = TaskPriority.NORMAL,
                 timeout: int = 30, **metadata) -> 'WorkflowBuilder':
        """Add a task to the workflow."""
        task = WorkflowTask(
            task_id=str(uuid.uuid4()),
            name=name,
            scanner_type=scanner_type,
            target=target,
            dependencies=dependencies or [],
            priority=priority,
            timeout=timeout,
            metadata=metadata
        )
        self.workflow.tasks.append(task)
        return self
    
    def set_priority(self, priority: TaskPriority) -> 'WorkflowBuilder':
        """Set workflow priority."""
        self.workflow.priority = priority
        return self
    
    def build(self) -> IntelligenceWorkflow:
        """Build and return the complete workflow."""
        return self.workflow


# Example usage functions
async def create_comprehensive_intelligence_workflow(target: str) -> IntelligenceWorkflow:
    """Create a comprehensive intelligence gathering workflow."""
    builder = WorkflowBuilder(
        name=f"Comprehensive Intelligence: {target}",
        description="Complete intelligence gathering across all available sources"
    )
    
    # Phase 1: Basic validation
    email_task_id = str(uuid.uuid4())
    builder.add_task(
        name="Email Validation",
        scanner_type="email_validation",
        target=target,
        priority=TaskPriority.HIGH,
        timeout=15
    )
    
    # Phase 2: Extended analysis (depends on email validation)
    phone_task_id = str(uuid.uuid4())
    builder.add_task(
        name="Phone Lookup",
        scanner_type="phone_lookup", 
        target=target,
        dependencies=[email_task_id],
        timeout=20
    )
    
    social_task_id = str(uuid.uuid4())
    builder.add_task(
        name="Social Media Scan",
        scanner_type="social_media",
        target=target,
        dependencies=[email_task_id],
        timeout=30
    )
    
    # Phase 3: Domain analysis (can run in parallel)
    domain_task_id = str(uuid.uuid4())
    if "@" in target:
        domain = target.split("@")[1]
        builder.add_task(
            name="Domain Analysis",
            scanner_type="domain_analysis",
            target=domain,
            timeout=25
        )
    
    return builder.build()