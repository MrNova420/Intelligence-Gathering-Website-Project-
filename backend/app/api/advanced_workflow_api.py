"""
Advanced Workflow API
====================

Enterprise-grade API endpoints for workflow management, orchestration,
and advanced intelligence operations with comprehensive monitoring.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
import uuid

from ..core.advanced_orchestration import (
    AdvancedOrchestrationEngine,
    IntelligenceWorkflow,
    WorkflowTask,
    WorkflowStatus,
    TaskPriority,
    WorkflowBuilder,
    create_comprehensive_intelligence_workflow
)
from ..services.enterprise_analytics_service import (
    EnterpriseAnalyticsService,
    AnalyticsEvent,
    track_user_activity
)

logger = logging.getLogger(__name__)

# Global instances (would be dependency injected in production)
orchestration_engine = AdvancedOrchestrationEngine()
analytics_service = EnterpriseAnalyticsService()

router = APIRouter(prefix="/api/v1/workflows", tags=["Advanced Workflows"])


# Pydantic models for API
class WorkflowTaskRequest(BaseModel):
    """Request model for creating a workflow task."""
    name: str = Field(..., description="Task name")
    scanner_type: str = Field(..., description="Scanner type to use")
    target: str = Field(..., description="Target for scanning")
    dependencies: List[str] = Field(default_factory=list, description="Task dependencies")
    priority: str = Field(default="normal", description="Task priority (low, normal, high, critical)")
    timeout: int = Field(default=30, description="Task timeout in seconds")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional task metadata")
    
    @validator('priority')
    def validate_priority(cls, v):
        valid_priorities = ["low", "normal", "high", "critical"]
        if v.lower() not in valid_priorities:
            raise ValueError(f"Priority must be one of: {valid_priorities}")
        return v.lower()


class WorkflowRequest(BaseModel):
    """Request model for creating a workflow."""
    name: str = Field(..., description="Workflow name")
    description: str = Field(default="", description="Workflow description")
    tasks: List[WorkflowTaskRequest] = Field(..., description="List of tasks")
    priority: str = Field(default="normal", description="Workflow priority")
    
    @validator('priority')
    def validate_priority(cls, v):
        valid_priorities = ["low", "normal", "high", "critical"]
        if v.lower() not in valid_priorities:
            raise ValueError(f"Priority must be one of: {valid_priorities}")
        return v.lower()


class WorkflowResponse(BaseModel):
    """Response model for workflow operations."""
    workflow_id: str
    name: str
    description: str
    status: str
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    task_count: int
    progress: Dict[str, Any]


class WorkflowTaskResponse(BaseModel):
    """Response model for workflow tasks."""
    task_id: str
    name: str
    scanner_type: str
    target: str
    status: str
    priority: str
    dependencies: List[str]
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    execution_time: Optional[float] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class WorkflowListResponse(BaseModel):
    """Response model for workflow list."""
    workflows: List[WorkflowResponse]
    total: int
    page: int
    per_page: int


class PerformanceAnalyticsResponse(BaseModel):
    """Response model for performance analytics."""
    analytics: Dict[str, Any]
    insights: List[Dict[str, Any]]
    recommendations: List[str]


# Dependency functions
async def get_current_user() -> Dict[str, Any]:
    """Get current user (simplified for demo)."""
    return {
        "user_id": "demo_user_123",
        "username": "demo_user",
        "plan": "professional",
        "session_id": f"session_{uuid.uuid4()}"
    }


async def track_api_activity(
    user: Dict[str, Any],
    endpoint: str,
    method: str,
    success: bool = True,
    additional_properties: Dict[str, Any] = None
):
    """Track API activity for analytics."""
    properties = {
        "endpoint": endpoint,
        "method": method,
        "success": success
    }
    if additional_properties:
        properties.update(additional_properties)
    
    await track_user_activity(
        analytics_service,
        user["user_id"],
        user.get("session_id"),
        f"api_{method.lower()}_{endpoint.replace('/', '_')}",
        properties
    )


# API Endpoints
@router.on_event("startup")
async def startup_orchestration():
    """Start the orchestration engine on API startup."""
    await orchestration_engine.start()
    logger.info("🚀 Advanced Workflow API initialized")


@router.on_event("shutdown")
async def shutdown_orchestration():
    """Stop the orchestration engine on API shutdown."""
    await orchestration_engine.stop()
    logger.info("⏹️ Advanced Workflow API shut down")


@router.post("/", response_model=WorkflowResponse, status_code=201)
async def create_workflow(
    request: WorkflowRequest,
    background_tasks: BackgroundTasks,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Create and submit a new intelligence gathering workflow.
    
    This endpoint creates a complex workflow with multiple tasks,
    dependencies, and advanced scheduling capabilities.
    """
    try:
        # Convert priority string to enum
        priority_map = {
            "low": TaskPriority.LOW,
            "normal": TaskPriority.NORMAL,
            "high": TaskPriority.HIGH,
            "critical": TaskPriority.CRITICAL
        }
        
        # Create workflow
        workflow = IntelligenceWorkflow(
            workflow_id=str(uuid.uuid4()),
            name=request.name,
            description=request.description,
            user_id=user["user_id"],
            priority=priority_map[request.priority]
        )
        
        # Create tasks
        for task_req in request.tasks:
            task = WorkflowTask(
                task_id=str(uuid.uuid4()),
                name=task_req.name,
                scanner_type=task_req.scanner_type,
                target=task_req.target,
                dependencies=task_req.dependencies,
                priority=priority_map[task_req.priority],
                timeout=task_req.timeout,
                metadata=task_req.metadata
            )
            workflow.tasks.append(task)
        
        # Submit to orchestration engine
        workflow_id = await orchestration_engine.submit_workflow(workflow)
        
        # Track activity
        background_tasks.add_task(
            track_api_activity,
            user,
            "/workflows",
            "POST",
            True,
            {"workflow_id": workflow_id, "task_count": len(workflow.tasks)}
        )
        
        # Return response
        return WorkflowResponse(
            workflow_id=workflow_id,
            name=workflow.name,
            description=workflow.description,
            status=workflow.status.value,
            created_at=workflow.created_at,
            started_at=workflow.started_at,
            completed_at=workflow.completed_at,
            task_count=len(workflow.tasks),
            progress={"completed": 0, "total": len(workflow.tasks), "percentage": 0.0}
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to create workflow: {str(e)}")
        background_tasks.add_task(
            track_api_activity,
            user,
            "/workflows",
            "POST",
            False,
            {"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=f"Failed to create workflow: {str(e)}")


@router.get("/", response_model=WorkflowListResponse)
async def list_workflows(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by status"),
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    List workflows for the current user with pagination and filtering.
    """
    try:
        # Get all workflows (in production, this would filter by user_id)
        all_workflows = []
        
        # Add pending workflows
        for workflow in orchestration_engine.scheduler.pending_workflows:
            if workflow.user_id == user["user_id"]:
                all_workflows.append(workflow)
        
        # Add active workflows
        for workflow in orchestration_engine.scheduler.active_workflows.values():
            if workflow.user_id == user["user_id"]:
                all_workflows.append(workflow)
        
        # Add completed workflows
        for workflow in orchestration_engine.scheduler.completed_workflows.values():
            if workflow.user_id == user["user_id"]:
                all_workflows.append(workflow)
        
        # Filter by status if provided
        if status:
            all_workflows = [w for w in all_workflows if w.status.value == status.lower()]
        
        # Sort by creation time (newest first)
        all_workflows.sort(key=lambda w: w.created_at, reverse=True)
        
        # Paginate
        total = len(all_workflows)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_workflows = all_workflows[start_idx:end_idx]
        
        # Convert to response format
        workflow_responses = []
        for workflow in paginated_workflows:
            completed_tasks = sum(1 for task in workflow.tasks if task.status == WorkflowStatus.COMPLETED)
            total_tasks = len(workflow.tasks)
            progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            
            workflow_responses.append(WorkflowResponse(
                workflow_id=workflow.workflow_id,
                name=workflow.name,
                description=workflow.description,
                status=workflow.status.value,
                created_at=workflow.created_at,
                started_at=workflow.started_at,
                completed_at=workflow.completed_at,
                task_count=total_tasks,
                progress={
                    "completed": completed_tasks,
                    "total": total_tasks,
                    "percentage": progress_percentage
                }
            ))
        
        return WorkflowListResponse(
            workflows=workflow_responses,
            total=total,
            page=page,
            per_page=per_page
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to list workflows: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list workflows: {str(e)}")


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(
    workflow_id: str,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get detailed information about a specific workflow.
    """
    try:
        workflow = await orchestration_engine.get_workflow_status(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        # Check user ownership
        if workflow.user_id != user["user_id"]:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Calculate progress
        completed_tasks = sum(1 for task in workflow.tasks if task.status == WorkflowStatus.COMPLETED)
        failed_tasks = sum(1 for task in workflow.tasks if task.status == WorkflowStatus.FAILED)
        running_tasks = sum(1 for task in workflow.tasks if task.status == WorkflowStatus.RUNNING)
        total_tasks = len(workflow.tasks)
        
        progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return WorkflowResponse(
            workflow_id=workflow.workflow_id,
            name=workflow.name,
            description=workflow.description,
            status=workflow.status.value,
            created_at=workflow.created_at,
            started_at=workflow.started_at,
            completed_at=workflow.completed_at,
            task_count=total_tasks,
            progress={
                "completed": completed_tasks,
                "failed": failed_tasks,
                "running": running_tasks,
                "pending": total_tasks - completed_tasks - failed_tasks - running_tasks,
                "total": total_tasks,
                "percentage": progress_percentage
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get workflow {workflow_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get workflow: {str(e)}")


@router.get("/{workflow_id}/tasks", response_model=List[WorkflowTaskResponse])
async def get_workflow_tasks(
    workflow_id: str,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get detailed information about all tasks in a workflow.
    """
    try:
        workflow = await orchestration_engine.get_workflow_status(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        # Check user ownership
        if workflow.user_id != user["user_id"]:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Convert tasks to response format
        task_responses = []
        for task in workflow.tasks:
            execution_time = None
            if task.started_at and task.completed_at:
                execution_time = (task.completed_at - task.started_at).total_seconds()
            
            task_responses.append(WorkflowTaskResponse(
                task_id=task.task_id,
                name=task.name,
                scanner_type=task.scanner_type,
                target=task.target,
                status=task.status.value,
                priority=task.priority.name.lower(),
                dependencies=task.dependencies,
                started_at=task.started_at,
                completed_at=task.completed_at,
                execution_time=execution_time,
                result=task.result,
                error=task.error
            ))
        
        return task_responses
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get workflow tasks {workflow_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get workflow tasks: {str(e)}")


@router.post("/{workflow_id}/cancel")
async def cancel_workflow(
    workflow_id: str,
    background_tasks: BackgroundTasks,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Cancel a running or pending workflow.
    """
    try:
        workflow = await orchestration_engine.get_workflow_status(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        # Check user ownership
        if workflow.user_id != user["user_id"]:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Cancel workflow
        success = await orchestration_engine.cancel_workflow(workflow_id)
        if not success:
            raise HTTPException(status_code=400, detail="Unable to cancel workflow")
        
        # Track activity
        background_tasks.add_task(
            track_api_activity,
            user,
            f"/workflows/{workflow_id}/cancel",
            "POST",
            True,
            {"workflow_id": workflow_id}
        )
        
        return JSONResponse(
            status_code=200,
            content={"message": "Workflow cancelled successfully", "workflow_id": workflow_id}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to cancel workflow {workflow_id}: {str(e)}")
        background_tasks.add_task(
            track_api_activity,
            user,
            f"/workflows/{workflow_id}/cancel",
            "POST",
            False,
            {"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=f"Failed to cancel workflow: {str(e)}")


@router.post("/quick-intelligence/{target}")
async def create_quick_intelligence_workflow(
    target: str,
    background_tasks: BackgroundTasks,
    priority: str = Query("normal", description="Workflow priority"),
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Create a pre-configured comprehensive intelligence gathering workflow for a target.
    
    This is a convenience endpoint that creates a full intelligence gathering
    workflow with all available scanners and proper dependencies.
    """
    try:
        # Create comprehensive workflow
        workflow = await create_comprehensive_intelligence_workflow(target)
        workflow.user_id = user["user_id"]
        
        # Set priority
        priority_map = {
            "low": TaskPriority.LOW,
            "normal": TaskPriority.NORMAL,
            "high": TaskPriority.HIGH,
            "critical": TaskPriority.CRITICAL
        }
        workflow.priority = priority_map.get(priority.lower(), TaskPriority.NORMAL)
        
        # Submit workflow
        workflow_id = await orchestration_engine.submit_workflow(workflow)
        
        # Track activity
        background_tasks.add_task(
            track_api_activity,
            user,
            f"/workflows/quick-intelligence/{target}",
            "POST",
            True,
            {"workflow_id": workflow_id, "target": target, "task_count": len(workflow.tasks)}
        )
        
        return WorkflowResponse(
            workflow_id=workflow_id,
            name=workflow.name,
            description=workflow.description,
            status=workflow.status.value,
            created_at=workflow.created_at,
            started_at=workflow.started_at,
            completed_at=workflow.completed_at,
            task_count=len(workflow.tasks),
            progress={"completed": 0, "total": len(workflow.tasks), "percentage": 0.0}
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to create quick intelligence workflow: {str(e)}")
        background_tasks.add_task(
            track_api_activity,
            user,
            f"/workflows/quick-intelligence/{target}",
            "POST",
            False,
            {"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=f"Failed to create workflow: {str(e)}")


@router.get("/analytics/performance", response_model=PerformanceAnalyticsResponse)
async def get_performance_analytics(
    timeframe: str = Query("week", description="Analytics timeframe (hour, day, week, month)")
):
    """
    Get comprehensive performance analytics for workflow execution.
    
    Provides insights into scanner performance, execution times,
    success rates, and recommendations for optimization.
    """
    try:
        # Get performance analytics from orchestration engine
        performance_data = orchestration_engine.get_performance_analytics()
        
        # Generate insights and recommendations
        insights = []
        recommendations = []
        
        for scanner_type, metrics in performance_data.items():
            if metrics["recent_success_rate"] < 0.8:
                insights.append({
                    "type": "performance_issue",
                    "scanner": scanner_type,
                    "success_rate": metrics["recent_success_rate"],
                    "severity": "high" if metrics["recent_success_rate"] < 0.6 else "medium"
                })
                recommendations.append(f"Review {scanner_type} scanner configuration and error handling")
            
            if metrics["average_execution_time"] > 10.0:
                insights.append({
                    "type": "slow_execution",
                    "scanner": scanner_type,
                    "avg_time": metrics["average_execution_time"],
                    "severity": "medium"
                })
                recommendations.append(f"Optimize {scanner_type} scanner for better performance")
        
        # Add general recommendations
        if not recommendations:
            recommendations.append("System performance is optimal")
        
        return PerformanceAnalyticsResponse(
            analytics=performance_data,
            insights=insights,
            recommendations=recommendations
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to get performance analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")


@router.get("/status/system")
async def get_system_status():
    """
    Get overall system status and health metrics.
    """
    try:
        # Get real-time dashboard data
        dashboard_data = await analytics_service.get_real_time_dashboard_data()
        
        # Get orchestration metrics
        performance_analytics = orchestration_engine.get_performance_analytics()
        
        # Calculate system health score
        health_score = 100.0
        issues = []
        
        # Check error rate
        if dashboard_data["current_error_rate"] > 0.1:
            health_score -= 20
            issues.append("High error rate detected")
        
        # Check response time
        if dashboard_data["current_avg_response_time"] > 5.0:
            health_score -= 15
            issues.append("Slow response times")
        
        # Check scanner performance
        for scanner_type, metrics in performance_analytics.items():
            if metrics.get("recent_success_rate", 1.0) < 0.8:
                health_score -= 10
                issues.append(f"{scanner_type} scanner underperforming")
        
        system_status = "healthy"
        if health_score < 70:
            system_status = "critical"
        elif health_score < 85:
            system_status = "warning"
        
        return {
            "status": system_status,
            "health_score": max(0, health_score),
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": {
                "active_sessions": dashboard_data["active_sessions"],
                "error_rate": dashboard_data["current_error_rate"],
                "avg_response_time": dashboard_data["current_avg_response_time"],
                "events_last_hour": dashboard_data["events_last_hour"]
            },
            "scanner_performance": performance_analytics,
            "issues": issues
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get system status: {str(e)}")
        return {
            "status": "error",
            "health_score": 0,
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }