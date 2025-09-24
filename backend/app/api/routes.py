"""
Main API Routes
===============

Core API endpoints for the intelligence gathering platform as promised in PRs.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uuid

from ..scanners.implementations import get_all_scanners
# from ..core.aggregation_engine import aggregation_engine
# from ..core.report_generator import report_generator
# from ..core.enhanced_security import security_manager

logger = logging.getLogger(__name__)

# Create main router
api_router = APIRouter(prefix="/api/v1", tags=["intelligence-platform"])


# Pydantic models
class ScanRequest(BaseModel):
    query_type: str = Field(..., description="Type of query (email, phone, name, username, image)")
    query_value: str = Field(..., description="Value to scan")
    scanners: Optional[List[str]] = Field(default=None, description="Specific scanners to use")
    user_plan: str = Field(default="free", description="User subscription plan")


class ScanResponse(BaseModel):
    scan_id: str
    status: str
    query_type: str
    query_value: str
    scanners_used: List[str]
    results: Dict[str, Any]
    confidence_score: float
    execution_time: float
    timestamp: str


class ReportRequest(BaseModel):
    scan_id: str
    report_type: str = Field(default="preview", description="preview or full")
    format: str = Field(default="json", description="json, html, pdf, csv")


@api_router.get("/scanners")
async def list_scanners():
    """List all available scanner modules"""
    try:
        scanners = get_all_scanners()
        scanner_info = []
        
        for scanner in scanners:
            scanner_info.append({
                "name": getattr(scanner, 'name', 'unknown'),
                "type": getattr(scanner, 'scanner_type', 'unknown'),
                "description": getattr(scanner, 'description', ''),
                "enabled": getattr(scanner, 'enabled', True)
            })
        
        return {
            "total_scanners": len(scanner_info),
            "scanners": scanner_info,
            "categories": {
                "email": len([s for s in scanner_info if 'email' in s['type']]),
                "phone": len([s for s in scanner_info if 'phone' in s['type']]),
                "social": len([s for s in scanner_info if 'social' in s['type']]),
                "public_records": len([s for s in scanner_info if 'public' in s['type']]),
                "api": len([s for s in scanner_info if s['type'] == 'api']),
                "other": len([s for s in scanner_info if s['type'] not in ['email', 'phone', 'social', 'public', 'api']])
            }
        }
    except Exception as e:
        logger.error(f"Error listing scanners: {e}")
        raise HTTPException(status_code=500, detail="Failed to list scanners")


@api_router.post("/scan", response_model=ScanResponse)
async def perform_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    """Perform intelligence gathering scan"""
    try:
        scan_id = str(uuid.uuid4())
        start_time = datetime.utcnow()
        
        # Get available scanners
        all_scanners = get_all_scanners()
        
        # Filter scanners based on query type and user selection
        applicable_scanners = []
        for scanner in all_scanners:
            scanner_name = getattr(scanner, 'name', 'unknown')
            scanner_type = getattr(scanner, 'scanner_type', 'unknown')
            
            # Check if scanner is applicable to query type
            if request.query_type == "email" and "email" in scanner_type:
                applicable_scanners.append(scanner)
            elif request.query_type == "phone" and "phone" in scanner_type:
                applicable_scanners.append(scanner)
            elif request.query_type == "name" and "social" in scanner_type:
                applicable_scanners.append(scanner)
            elif request.query_type == "username" and ("social" in scanner_type or "api" in scanner_type):
                applicable_scanners.append(scanner)
            elif request.scanners and scanner_name in request.scanners:
                applicable_scanners.append(scanner)
        
        # Limit scanners based on user plan
        plan_limits = {"free": 5, "professional": 25, "enterprise": 50}
        max_scanners = plan_limits.get(request.user_plan, 5)
        applicable_scanners = applicable_scanners[:max_scanners]
        
        # Execute scans
        scan_results = {}
        for scanner in applicable_scanners:
            try:
                # Create mock query object
                class MockQuery:
                    def __init__(self, query_type, query_value):
                        self.query_type = query_type
                        self.query_value = query_value
                        self.id = scan_id
                
                mock_query = MockQuery(request.query_type, request.query_value)
                
                # Execute scanner
                result = await scanner.scan(mock_query)
                scanner_name = getattr(scanner, 'name', 'unknown')
                scan_results[scanner_name] = result
                
            except Exception as scanner_error:
                logger.warning(f"Scanner {getattr(scanner, 'name', 'unknown')} failed: {scanner_error}")
                scan_results[getattr(scanner, 'name', 'unknown')] = {
                    "error": str(scanner_error),
                    "status": "failed"
                }
        
        # Calculate execution time and confidence
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        confidence_score = calculate_confidence(scan_results)
        
        # Store scan for report generation
        scan_data = {
            "scan_id": scan_id,
            "query_type": request.query_type,
            "query_value": request.query_value,
            "results": scan_results,
            "confidence_score": confidence_score,
            "execution_time": execution_time,
            "timestamp": start_time.isoformat(),
            "user_plan": request.user_plan
        }
        
        # TODO: Store in database for persistence
        
        return ScanResponse(
            scan_id=scan_id,
            status="completed",
            query_type=request.query_type,
            query_value=request.query_value,
            scanners_used=[getattr(s, 'name', 'unknown') for s in applicable_scanners],
            results=scan_results,
            confidence_score=confidence_score,
            execution_time=execution_time,
            timestamp=start_time.isoformat()
        )
        
    except Exception as e:
        logger.error(f"Scan failed: {e}")
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")


@api_router.post("/report")
async def generate_report(request: ReportRequest):
    """Generate intelligence report"""
    try:
        # TODO: Retrieve scan data from database
        # For now, return mock report structure
        
        if request.report_type == "preview":
            # Free preview - limited data
            return {
                "scan_id": request.scan_id,
                "report_type": "preview",
                "format": request.format,
                "data": {
                    "summary": "Limited preview data available",
                    "sources_found": 3,
                    "confidence": "medium",
                    "upgrade_required": True,
                    "upgrade_url": "/api/v1/subscription/upgrade"
                },
                "generated_at": datetime.utcnow().isoformat()
            }
        else:
            # Full report - requires subscription
            return {
                "scan_id": request.scan_id,
                "report_type": "full",
                "format": request.format,
                "data": {
                    "summary": "Comprehensive intelligence report",
                    "detailed_results": {},  # Would contain full scan results
                    "analytics": {},  # Advanced analytics
                    "visualizations": {},  # Charts and graphs
                    "export_links": {
                        "pdf": f"/api/v1/report/{request.scan_id}/export/pdf",
                        "csv": f"/api/v1/report/{request.scan_id}/export/csv"
                    }
                },
                "generated_at": datetime.utcnow().isoformat()
            }
            
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate report")


@api_router.get("/subscription/features")
async def get_subscription_features():
    """Get subscription features and pricing"""
    return {
        "plans": {
            "free": {
                "price": 0,
                "max_scans_per_day": 5,
                "max_scanners_per_scan": 5,
                "report_types": ["preview"],
                "export_formats": ["json"],
                "features": ["Basic scanning", "Limited preview reports"]
            },
            "professional": {
                "price": 29.99,
                "max_scans_per_day": 100,
                "max_scanners_per_scan": 25,
                "report_types": ["preview", "full"],
                "export_formats": ["json", "html", "csv"],
                "features": ["Full scanning", "Complete reports", "Export capabilities", "Email support"]
            },
            "enterprise": {
                "price": 99.99,
                "max_scans_per_day": 1000,
                "max_scanners_per_scan": 50,
                "report_types": ["preview", "full", "detailed"],
                "export_formats": ["json", "html", "csv", "pdf"],
                "features": ["Unlimited scanning", "Advanced analytics", "API access", "Priority support"]
            }
        }
    }


@api_router.get("/stats")
async def get_platform_stats():
    """Get platform statistics"""
    scanners = get_all_scanners()
    return {
        "total_scanners": len(scanners),
        "platform_version": "1.0.0",
        "uptime": "running",
        "status": "operational",
        "features": {
            "real_time_scanning": True,
            "subscription_tiers": 3,
            "export_formats": 4,
            "security_encryption": "AES-256"
        }
    }


def calculate_confidence(scan_results: Dict[str, Any]) -> float:
    """Calculate overall confidence score from scan results"""
    if not scan_results:
        return 0.0
    
    successful_scans = [r for r in scan_results.values() if not isinstance(r, dict) or r.get("status") != "failed"]
    if not successful_scans:
        return 0.0
    
    # Simple confidence calculation
    success_rate = len(successful_scans) / len(scan_results)
    return round(success_rate * 0.8 + 0.2, 2)  # Base confidence + success rate