"""
Enhanced API Endpoints
======================

Advanced API endpoints for the intelligence platform with:
- Real-time analytics
- ML-powered insights
- Advanced search capabilities
- Performance monitoring
- Data quality assessment
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends, Query as QueryParam, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field
import json
import uuid

from ..core.advanced_analytics import (
    data_quality_analyzer, behavioral_analyzer, 
    risk_engine, predictive_analytics
)
from ..core.ml_intelligence import (
    source_prioritizer, pattern_recognizer,
    confidence_predictor, anomaly_detector
)
from ..core.performance_optimizer import performance_monitor, cache_manager

logger = logging.getLogger(__name__)

# Create router
enhanced_router = APIRouter(prefix="/api/v2", tags=["enhanced-intelligence"])


# Pydantic models for request/response
class AnalyticsRequest(BaseModel):
    query_id: Optional[int] = None
    data: Dict[str, Any]
    include_predictions: bool = True
    include_patterns: bool = True
    include_anomalies: bool = True


class QualityAssessmentResponse(BaseModel):
    overall_score: float
    completeness: float
    consistency: float
    accuracy: float
    timeliness: float
    uniqueness: float
    validity: float
    recommendations: List[str]


class PatternAnalysisResponse(BaseModel):
    patterns: Dict[str, Any]
    overall_confidence: float
    high_confidence_patterns: List[str]


class RiskAssessmentResponse(BaseModel):
    overall_risk_score: float
    risk_level: str
    individual_risks: Dict[str, float]
    recommendations: List[str]


class EnhancedSearchRequest(BaseModel):
    query: str
    filters: Dict[str, Any] = Field(default_factory=dict)
    sort_by: str = "relevance"
    limit: int = Field(default=50, le=1000)
    include_ml_insights: bool = True
    source_priorities: Optional[List[str]] = None


@enhanced_router.post("/analytics/comprehensive", response_model=Dict[str, Any])
async def comprehensive_analytics(request: AnalyticsRequest, background_tasks: BackgroundTasks):
    """
    Perform comprehensive analytics on intelligence data
    """
    try:
        results = {}
        
        # Data Quality Assessment
        quality_metrics = data_quality_analyzer.analyze_data_quality(request.data)
        results['data_quality'] = quality_metrics
        
        # Pattern Recognition
        if request.include_patterns:
            pattern_analysis = pattern_recognizer.recognize_patterns(request.data)
            results['patterns'] = pattern_analysis
        
        # Risk Assessment
        risk_assessment = risk_engine.assess_risk(request.data)
        results['risk_assessment'] = risk_assessment
        
        # ML-powered Confidence Prediction
        confidence_prediction = confidence_predictor.predict_confidence(request.data)
        results['confidence_prediction'] = confidence_prediction
        
        # Anomaly Detection
        if request.include_anomalies:
            anomaly_analysis = anomaly_detector.detect_anomalies(request.data)
            results['anomaly_detection'] = anomaly_analysis
        
        # Background task for performance monitoring
        background_tasks.add_task(
            performance_monitor.log_api_call, 
            "comprehensive_analytics", 
            len(json.dumps(request.data))
        )
        
        return {
            "success": True,
            "analytics": results,
            "metadata": {
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "analysis_id": str(uuid.uuid4()),
                "components_analyzed": list(results.keys())
            }
        }
        
    except Exception as e:
        logger.error(f"Error in comprehensive analytics: {e}")
        raise HTTPException(status_code=500, detail=f"Analytics processing failed: {str(e)}")


@enhanced_router.get("/analytics/quality/{query_id}")
async def get_data_quality_assessment(query_id: int):
    """
    Get detailed data quality assessment for a specific query
    """
    try:
        # This would typically fetch data from database using query_id
        # For now, we'll use mock data
        mock_data = {
            "emails": ["user@example.com", "john.doe@company.com"],
            "phones": ["+1-555-123-4567", "(555) 987-6543"],
            "social_profiles": {"twitter": "@johndoe", "linkedin": "john-doe"},
            "verification_status": {"email": "verified", "phone": "pending"},
            "last_updated": "2024-01-15T10:30:00Z",
            "source_count": 3
        }
        
        quality_metrics = data_quality_analyzer.analyze_data_quality(mock_data)
        
        # Generate actionable recommendations
        recommendations = []
        if quality_metrics['completeness'] < 0.7:
            recommendations.append("Gather additional data sources to improve completeness")
        if quality_metrics['consistency'] < 0.8:
            recommendations.append("Review and standardize data formats")
        if quality_metrics['timeliness'] < 0.6:
            recommendations.append("Update data from recent sources")
        
        return QualityAssessmentResponse(
            overall_score=quality_metrics['overall_score'],
            completeness=quality_metrics['completeness'],
            consistency=quality_metrics['consistency'],
            accuracy=quality_metrics['accuracy'],
            timeliness=quality_metrics['timeliness'],
            uniqueness=quality_metrics['uniqueness'],
            validity=quality_metrics['validity'],
            recommendations=recommendations
        )
        
    except Exception as e:
        logger.error(f"Error in quality assessment: {e}")
        raise HTTPException(status_code=500, detail=f"Quality assessment failed: {str(e)}")


@enhanced_router.post("/analytics/patterns")
async def analyze_patterns(request: AnalyticsRequest):
    """
    Perform advanced pattern analysis on data
    """
    try:
        pattern_analysis = pattern_recognizer.recognize_patterns(request.data)
        
        return PatternAnalysisResponse(
            patterns=pattern_analysis['patterns'],
            overall_confidence=pattern_analysis['overall_confidence'],
            high_confidence_patterns=pattern_analysis['high_confidence_patterns']
        )
        
    except Exception as e:
        logger.error(f"Error in pattern analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Pattern analysis failed: {str(e)}")


@enhanced_router.post("/analytics/risk-assessment")
async def assess_risk(request: AnalyticsRequest):
    """
    Perform comprehensive risk assessment
    """
    try:
        risk_assessment = risk_engine.assess_risk(request.data)
        
        return RiskAssessmentResponse(
            overall_risk_score=risk_assessment['overall_risk_score'],
            risk_level=risk_assessment['risk_level'],
            individual_risks=risk_assessment['individual_risks'],
            recommendations=risk_assessment['recommendations']
        )
        
    except Exception as e:
        logger.error(f"Error in risk assessment: {e}")
        raise HTTPException(status_code=500, detail=f"Risk assessment failed: {str(e)}")


@enhanced_router.get("/analytics/behavioral/{query_id}")
async def analyze_behavioral_patterns(query_id: int, days_back: int = QueryParam(30, ge=1, le=365)):
    """
    Analyze behavioral patterns from historical data
    """
    try:
        # Mock historical data - in real implementation, fetch from database
        historical_data = [
            {
                "timestamp": (datetime.utcnow() - timedelta(days=i)).isoformat(),
                "query_type": "email_search",
                "confidence_score": 0.8 + (i % 3) * 0.1,
                "sources": ["source1", "source2", "source3"][:i%3+1]
            }
            for i in range(min(days_back, 30))
        ]
        
        behavioral_analysis = behavioral_analyzer.analyze_patterns(historical_data)
        
        return {
            "success": True,
            "behavioral_patterns": behavioral_analysis,
            "analysis_period": f"{days_back} days",
            "data_points": len(historical_data)
        }
        
    except Exception as e:
        logger.error(f"Error in behavioral analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Behavioral analysis failed: {str(e)}")


@enhanced_router.get("/analytics/predictions/{query_id}")
async def get_predictive_insights(query_id: int):
    """
    Get predictive analytics insights
    """
    try:
        # Mock historical data for prediction
        historical_data = [
            {
                "timestamp": (datetime.utcnow() - timedelta(days=i*7)).isoformat(),
                "data_quality_score": 0.7 + (i % 4) * 0.05,
                "confidence_score": 0.75 + (i % 3) * 0.08
            }
            for i in range(8)  # 8 weeks of data
        ]
        
        predictions = predictive_analytics.predict_data_quality_evolution(historical_data)
        
        return {
            "success": True,
            "predictions": predictions,
            "forecast_horizon": "3 periods ahead",
            "model_confidence": predictions.get('confidence', 0.5)
        }
        
    except Exception as e:
        logger.error(f"Error in predictive analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Predictive analysis failed: {str(e)}")


@enhanced_router.post("/search/enhanced")
async def enhanced_search(request: EnhancedSearchRequest, background_tasks: BackgroundTasks):
    """
    Enhanced search with ML-powered ranking and insights
    """
    try:
        # Mock search results - in real implementation, this would query your data sources
        base_results = [
            {
                "id": i,
                "query": request.query,
                "title": f"Result {i}",
                "confidence": 0.8 + (i % 3) * 0.05,
                "sources": ["source1", "source2"][:i%2+1],
                "data": {
                    "email": f"user{i}@example.com",
                    "name": f"User {i}",
                    "location": "New York, NY" if i % 2 == 0 else "Los Angeles, CA"
                }
            }
            for i in range(min(request.limit, 20))
        ]
        
        enhanced_results = []
        
        for result in base_results:
            enhanced_result = result.copy()
            
            if request.include_ml_insights:
                # Add ML insights
                pattern_analysis = pattern_recognizer.recognize_patterns(result['data'])
                confidence_prediction = confidence_predictor.predict_confidence(result['data'])
                
                enhanced_result['ml_insights'] = {
                    'patterns': pattern_analysis,
                    'predicted_confidence': confidence_prediction['predicted_confidence'],
                    'confidence_interval': confidence_prediction['confidence_interval']
                }
            
            enhanced_results.append(enhanced_result)
        
        # Sort by requested criteria
        if request.sort_by == "confidence":
            enhanced_results.sort(key=lambda x: x['confidence'], reverse=True)
        elif request.sort_by == "ml_confidence" and request.include_ml_insights:
            enhanced_results.sort(
                key=lambda x: x['ml_insights']['predicted_confidence'], 
                reverse=True
            )
        
        # Background performance monitoring
        background_tasks.add_task(
            performance_monitor.log_api_call,
            "enhanced_search",
            len(enhanced_results)
        )
        
        return {
            "success": True,
            "results": enhanced_results,
            "total_results": len(enhanced_results),
            "search_metadata": {
                "query": request.query,
                "sort_by": request.sort_by,
                "ml_insights_included": request.include_ml_insights,
                "search_timestamp": datetime.utcnow().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Error in enhanced search: {e}")
        raise HTTPException(status_code=500, detail=f"Enhanced search failed: {str(e)}")


@enhanced_router.get("/sources/prioritization")
async def get_source_prioritization(query_type: str = QueryParam(...), location: Optional[str] = None):
    """
    Get ML-powered source prioritization recommendations
    """
    try:
        # Mock available sources
        available_sources = [
            "email_validator", "phone_lookup", "social_search", 
            "public_records", "business_search", "global_database"
        ]
        
        query_context = {
            "query_type": query_type,
            "location": location or "global"
        }
        
        prioritized_sources = source_prioritizer.prioritize_sources(
            available_sources, 
            query_context
        )
        
        return {
            "success": True,
            "prioritized_sources": [
                {
                    "source": source,
                    "priority_score": score,
                    "recommended_order": idx + 1
                }
                for idx, (source, score) in enumerate(prioritized_sources)
            ],
            "query_context": query_context,
            "total_sources": len(prioritized_sources)
        }
        
    except Exception as e:
        logger.error(f"Error in source prioritization: {e}")
        raise HTTPException(status_code=500, detail=f"Source prioritization failed: {str(e)}")


@enhanced_router.get("/performance/metrics")
async def get_performance_metrics():
    """
    Get real-time performance metrics
    """
    try:
        metrics = performance_monitor.get_system_metrics()
        cache_stats = cache_manager.get_cache_statistics()
        
        return {
            "success": True,
            "system_metrics": metrics,
            "cache_statistics": cache_stats,
            "performance_summary": {
                "avg_response_time": metrics.get('avg_api_response_time', 0),
                "cache_hit_rate": cache_stats.get('hit_rate', 0),
                "system_health": "good" if metrics.get('cpu_usage', 0) < 0.8 else "warning",
                "uptime": metrics.get('uptime_hours', 0)
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Performance metrics failed: {str(e)}")


@enhanced_router.get("/analytics/real-time-stream")
async def real_time_analytics_stream(query_id: Optional[int] = None):
    """
    Stream real-time analytics data
    """
    async def generate_analytics_stream():
        """Generate streaming analytics data"""
        try:
            for i in range(10):  # Stream 10 updates
                # Mock real-time data
                analytics_update = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "sequence": i + 1,
                    "metrics": {
                        "active_queries": 15 + i,
                        "avg_confidence": 0.75 + (i % 3) * 0.05,
                        "cache_hit_rate": 0.85 + (i % 2) * 0.02,
                        "anomalies_detected": i % 4
                    },
                    "query_id": query_id
                }
                
                yield f"data: {json.dumps(analytics_update)}\n\n"
                await asyncio.sleep(2)  # Update every 2 seconds
                
        except Exception as e:
            logger.error(f"Error in analytics stream: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate_analytics_stream(),
        media_type="text/stream-server-sent-events",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*"
        }
    )


@enhanced_router.post("/analytics/batch-processing")
async def batch_analytics_processing(
    data_batch: List[Dict[str, Any]], 
    background_tasks: BackgroundTasks,
    analysis_types: List[str] = QueryParam(default=["quality", "patterns", "risk"])
):
    """
    Process analytics for a batch of data items
    """
    try:
        if len(data_batch) > 100:
            raise HTTPException(status_code=400, detail="Batch size too large (max 100 items)")
        
        batch_id = str(uuid.uuid4())
        results = []
        
        for idx, data_item in enumerate(data_batch):
            item_results = {"item_id": idx}
            
            if "quality" in analysis_types:
                item_results["quality"] = data_quality_analyzer.analyze_data_quality(data_item)
            
            if "patterns" in analysis_types:
                item_results["patterns"] = pattern_recognizer.recognize_patterns(data_item)
            
            if "risk" in analysis_types:
                item_results["risk"] = risk_engine.assess_risk(data_item)
            
            if "anomalies" in analysis_types:
                item_results["anomalies"] = anomaly_detector.detect_anomalies(data_item)
            
            results.append(item_results)
        
        # Background task for batch processing monitoring
        background_tasks.add_task(
            performance_monitor.log_batch_processing,
            batch_id,
            len(data_batch),
            analysis_types
        )
        
        return {
            "success": True,
            "batch_id": batch_id,
            "processed_items": len(results),
            "results": results,
            "analysis_types": analysis_types,
            "processing_timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in batch processing: {e}")
        raise HTTPException(status_code=500, detail=f"Batch processing failed: {str(e)}")


@enhanced_router.get("/health/detailed")
async def detailed_health_check():
    """
    Comprehensive health check with detailed system status
    """
    try:
        system_metrics = performance_monitor.get_system_metrics()
        cache_stats = cache_manager.get_cache_statistics()
        
        # Check various system components
        health_status = {
            "overall_status": "healthy",
            "components": {
                "api": {
                    "status": "healthy",
                    "response_time": system_metrics.get('avg_api_response_time', 0),
                    "uptime": system_metrics.get('uptime_hours', 0)
                },
                "cache": {
                    "status": "healthy" if cache_stats.get('hit_rate', 0) > 0.5 else "warning",
                    "hit_rate": cache_stats.get('hit_rate', 0),
                    "total_requests": cache_stats.get('total_requests', 0)
                },
                "analytics": {
                    "status": "healthy",
                    "engines": ["quality_analyzer", "pattern_recognizer", "risk_engine", "anomaly_detector"],
                    "last_analysis": datetime.utcnow().isoformat()
                },
                "ml_intelligence": {
                    "status": "healthy",
                    "models": ["source_prioritizer", "confidence_predictor", "pattern_recognizer"],
                    "prediction_accuracy": 0.85  # Mock accuracy metric
                }
            },
            "system_resources": {
                "cpu_usage": system_metrics.get('cpu_usage', 0),
                "memory_usage": system_metrics.get('memory_usage', 0),
                "disk_usage": system_metrics.get('disk_usage', 0)
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Determine overall status
        warning_components = [
            comp for comp, details in health_status["components"].items()
            if details["status"] == "warning"
        ]
        
        if warning_components:
            health_status["overall_status"] = "warning"
            health_status["warnings"] = warning_components
        
        # Check for critical issues
        if (system_metrics.get('cpu_usage', 0) > 0.9 or 
            system_metrics.get('memory_usage', 0) > 0.9):
            health_status["overall_status"] = "critical"
            health_status["critical_issues"] = ["High system resource usage"]
        
        return health_status
        
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return {
            "overall_status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


# Export router for main app
router = enhanced_router  # Alias for backward compatibility
__all__ = ['enhanced_router', 'router']