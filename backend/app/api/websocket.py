"""
Real-time WebSocket functionality for live scanning updates
As promised in PR #2 for comprehensive real-time intelligence gathering
"""

import asyncio
import json
import logging
from typing import Dict, Any, Set, List, Optional
from datetime import datetime
import uuid
from fastapi import WebSocket, WebSocketDisconnect
from ..scanners.implementations import get_all_scanners
from ..core.aggregation_engine import aggregation_engine

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections for real-time scanning updates"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.scan_sessions: Dict[str, Dict[str, Any]] = {}
        
    async def connect(self, websocket: WebSocket, client_id: str):
        """Connect a new WebSocket client"""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"WebSocket client {client_id} connected")
        
    def disconnect(self, client_id: str):
        """Disconnect a WebSocket client"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if client_id in self.scan_sessions:
            del self.scan_sessions[client_id]
        logger.info(f"WebSocket client {client_id} disconnected")
        
    async def send_personal_message(self, message: Dict[str, Any], client_id: str):
        """Send a message to a specific client"""
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error sending message to {client_id}: {e}")
                self.disconnect(client_id)
                
    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast a message to all connected clients"""
        if self.active_connections:
            await asyncio.gather(
                *[self.send_personal_message(message, client_id) 
                  for client_id in list(self.active_connections.keys())],
                return_exceptions=True
            )


# Global connection manager instance
manager = ConnectionManager()


class RealTimeScanEngine:
    """Real-time scanning engine with WebSocket updates"""
    
    def __init__(self, connection_manager: ConnectionManager):
        self.manager = connection_manager
        
    async def start_realtime_scan(self, client_id: str, scan_request: Dict[str, Any]) -> str:
        """Start a real-time scanning session"""
        scan_id = str(uuid.uuid4())
        
        # Initialize scan session
        self.manager.scan_sessions[client_id] = {
            "scan_id": scan_id,
            "request": scan_request,
            "status": "initializing",
            "progress": 0,
            "scanners_completed": 0,
            "total_scanners": 0,
            "results": {},
            "started_at": datetime.utcnow().isoformat()
        }
        
        # Send initial status
        await self.manager.send_personal_message({
            "type": "scan_started",
            "scan_id": scan_id,
            "status": "initializing",
            "message": "Preparing scanners..."
        }, client_id)
        
        # Start the scanning process
        asyncio.create_task(self._execute_realtime_scan(client_id, scan_id, scan_request))
        
        return scan_id
        
    async def _execute_realtime_scan(self, client_id: str, scan_id: str, request: Dict[str, Any]):
        """Execute the real-time scanning process"""
        try:
            # Get applicable scanners
            all_scanners = get_all_scanners()
            query_type = request.get("query_type", "email")
            applicable_scanners = self._filter_scanners(all_scanners, query_type)
            
            # Update session with scanner count
            if client_id in self.manager.scan_sessions:
                self.manager.scan_sessions[client_id]["total_scanners"] = len(applicable_scanners)
                self.manager.scan_sessions[client_id]["status"] = "scanning"
            
            # Send scanner list
            await self.manager.send_personal_message({
                "type": "scanners_identified",
                "scan_id": scan_id,
                "total_scanners": len(applicable_scanners),
                "scanners": [getattr(s, 'name', 'unknown') for s in applicable_scanners]
            }, client_id)
            
            # Execute scanners in batches for real-time updates
            batch_size = 3
            scanner_batches = [applicable_scanners[i:i + batch_size] 
                             for i in range(0, len(applicable_scanners), batch_size)]
            
            all_results = {}
            completed_count = 0
            
            for batch_index, batch in enumerate(scanner_batches):
                # Update status
                await self.manager.send_personal_message({
                    "type": "batch_started",
                    "scan_id": scan_id,
                    "batch_index": batch_index + 1,
                    "total_batches": len(scanner_batches),
                    "scanners_in_batch": [getattr(s, 'name', 'unknown') for s in batch]
                }, client_id)
                
                # Execute batch
                batch_results = await self._execute_scanner_batch(
                    batch, request, client_id, scan_id
                )
                
                all_results.update(batch_results)
                completed_count += len(batch)
                
                # Update progress
                progress = int((completed_count / len(applicable_scanners)) * 100)
                
                if client_id in self.manager.scan_sessions:
                    self.manager.scan_sessions[client_id].update({
                        "progress": progress,
                        "scanners_completed": completed_count,
                        "results": all_results
                    })
                
                await self.manager.send_personal_message({
                    "type": "progress_update",
                    "scan_id": scan_id,
                    "progress": progress,
                    "completed": completed_count,
                    "total": len(applicable_scanners),
                    "batch_results": batch_results
                }, client_id)
                
                # Small delay between batches for better UX
                await asyncio.sleep(0.5)
            
            # Perform aggregation and analysis
            await self.manager.send_personal_message({
                "type": "aggregating",
                "scan_id": scan_id,
                "message": "Analyzing and aggregating results..."
            }, client_id)
            
            # Simulate aggregation (replace with actual aggregation engine)
            aggregated_results = await self._aggregate_results(all_results, request)
            
            # Mark as completed
            if client_id in self.manager.scan_sessions:
                self.manager.scan_sessions[client_id].update({
                    "status": "completed",
                    "progress": 100,
                    "aggregated_results": aggregated_results,
                    "completed_at": datetime.utcnow().isoformat()
                })
            
            # Send final results
            await self.manager.send_personal_message({
                "type": "scan_completed",
                "scan_id": scan_id,
                "results": all_results,
                "aggregated_results": aggregated_results,
                "summary": {
                    "total_scanners": len(applicable_scanners),
                    "successful_scans": len([r for r in all_results.values() if not r.get("error")]),
                    "confidence_score": aggregated_results.get("confidence_score", 0.0),
                    "entities_found": len(aggregated_results.get("entities", [])),
                    "sources_count": len(aggregated_results.get("sources", []))
                }
            }, client_id)
            
        except Exception as e:
            logger.error(f"Real-time scan error for {client_id}: {e}")
            await self.manager.send_personal_message({
                "type": "scan_error",
                "scan_id": scan_id,
                "error": str(e),
                "message": "Scan failed due to an internal error"
            }, client_id)
            
            if client_id in self.manager.scan_sessions:
                self.manager.scan_sessions[client_id]["status"] = "failed"
    
    async def _execute_scanner_batch(self, scanners: List[Any], request: Dict[str, Any], 
                                   client_id: str, scan_id: str) -> Dict[str, Any]:
        """Execute a batch of scanners concurrently"""
        batch_results = {}
        
        # Create mock query object
        class MockQuery:
            def __init__(self, query_type, query_value):
                self.query_type = query_type
                self.query_value = query_value
                self.id = scan_id
        
        mock_query = MockQuery(request.get("query_type"), request.get("query_value"))
        
        # Execute scanners concurrently
        tasks = []
        for scanner in scanners:
            task = asyncio.create_task(
                self._execute_single_scanner(scanner, mock_query, client_id, scan_id)
            )
            tasks.append((getattr(scanner, 'name', 'unknown'), task))
        
        for scanner_name, task in tasks:
            try:
                result = await task
                batch_results[scanner_name] = result
                
                # Send individual scanner completion
                await self.manager.send_personal_message({
                    "type": "scanner_completed",
                    "scan_id": scan_id,
                    "scanner": scanner_name,
                    "success": not result.get("error"),
                    "data_points": len(result.get("data", {})) if isinstance(result.get("data"), dict) else 0
                }, client_id)
                
            except Exception as e:
                batch_results[scanner_name] = {
                    "error": str(e),
                    "status": "failed",
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                await self.manager.send_personal_message({
                    "type": "scanner_failed",
                    "scan_id": scan_id,
                    "scanner": scanner_name,
                    "error": str(e)
                }, client_id)
        
        return batch_results
    
    async def _execute_single_scanner(self, scanner: Any, query: Any, client_id: str, scan_id: str) -> Dict[str, Any]:
        """Execute a single scanner with real-time status updates"""
        scanner_name = getattr(scanner, 'name', 'unknown')
        
        # Send scanner start notification
        await self.manager.send_personal_message({
            "type": "scanner_started",
            "scan_id": scan_id,
            "scanner": scanner_name,
            "message": f"Starting {scanner_name}..."
        }, client_id)
        
        try:
            result = await scanner.scan(query)
            return result
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed",
                "scanner": scanner_name,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _filter_scanners(self, all_scanners: List[Any], query_type: str) -> List[Any]:
        """Filter scanners based on query type"""
        applicable_scanners = []
        
        for scanner in all_scanners:
            scanner_type = getattr(scanner, 'scanner_type', 'unknown')
            scanner_name = getattr(scanner, 'name', 'unknown')
            
            # Filter based on query type
            if query_type == "email" and ("email" in scanner_type or "email" in scanner_name):
                applicable_scanners.append(scanner)
            elif query_type == "phone" and ("phone" in scanner_type or "phone" in scanner_name):
                applicable_scanners.append(scanner)
            elif query_type == "name" and ("social" in scanner_type or "name" in scanner_name):
                applicable_scanners.append(scanner)
            elif query_type == "username" and ("social" in scanner_type or "api" in scanner_type):
                applicable_scanners.append(scanner)
            elif query_type == "image" and ("image" in scanner_type or "media" in scanner_name):
                applicable_scanners.append(scanner)
        
        # Limit to first 20 for real-time performance
        return applicable_scanners[:20]
    
    async def _aggregate_results(self, results: Dict[str, Any], request: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate and analyze scan results"""
        # Basic aggregation logic
        successful_results = {k: v for k, v in results.items() if not v.get("error")}
        
        entities = []
        sources = []
        confidence_scores = []
        
        for scanner_name, result in successful_results.items():
            if isinstance(result, dict):
                # Extract entities
                if "email" in result:
                    entities.append({"type": "email", "value": result["email"], "source": scanner_name})
                if "phone" in result:
                    entities.append({"type": "phone", "value": result["phone"], "source": scanner_name})
                if "name" in result:
                    entities.append({"type": "name", "value": result["name"], "source": scanner_name})
                
                # Extract confidence scores
                if "confidence" in result:
                    confidence_scores.append(result["confidence"])
                
                # Add source
                sources.append(scanner_name)
        
        # Calculate overall confidence
        overall_confidence = statistics.mean(confidence_scores) if confidence_scores else 0.0
        
        return {
            "entities": entities,
            "sources": sources,
            "confidence_score": round(overall_confidence, 2),
            "total_sources": len(sources),
            "successful_scans": len(successful_results),
            "total_scans": len(results),
            "aggregated_at": datetime.utcnow().isoformat()
        }


# Global real-time scan engine
realtime_engine = RealTimeScanEngine(manager)


async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time scanning"""
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "start_scan":
                # Start real-time scanning
                scan_id = await realtime_engine.start_realtime_scan(
                    client_id, message.get("data", {})
                )
                
            elif message.get("type") == "get_status":
                # Send current scan status
                if client_id in manager.scan_sessions:
                    session = manager.scan_sessions[client_id]
                    await manager.send_personal_message({
                        "type": "status_update",
                        "scan_id": session.get("scan_id"),
                        "status": session.get("status"),
                        "progress": session.get("progress", 0),
                        "scanners_completed": session.get("scanners_completed", 0),
                        "total_scanners": session.get("total_scanners", 0)
                    }, client_id)
                else:
                    await manager.send_personal_message({
                        "type": "no_active_scan",
                        "message": "No active scan session"
                    }, client_id)
            
            elif message.get("type") == "cancel_scan":
                # Cancel current scan
                if client_id in manager.scan_sessions:
                    manager.scan_sessions[client_id]["status"] = "cancelled"
                    await manager.send_personal_message({
                        "type": "scan_cancelled",
                        "message": "Scan cancelled by user"
                    }, client_id)
                    
    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"WebSocket error for {client_id}: {e}")
        manager.disconnect(client_id)