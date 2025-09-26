#!/usr/bin/env python3
"""
Intelligence Gathering Platform - Unified Web Application
Main entry point for the complete unified website system
"""

# Import the unified web platform - proper package import
import sys
from pathlib import Path

# Ensure we can import from the backend directory
backend_dir = Path(__file__).parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from webapp import platform, app

if __name__ == "__main__":
    import uvicorn
    import logging
    
    logger = logging.getLogger(__name__)
    
    # Get port from command line or use default
    port = 8001 if len(sys.argv) > 1 and sys.argv[1] == "alt" else 8000
    
    # Run the unified web application
    logger.info("🌐 Starting Unified Intelligence Gathering Web Platform")
    logger.info("🔍 Single system combining API + Web Interface")
    logger.info("📱 Termux/Android Compatible")
    logger.info(f"🌐 Web Interface: http://localhost:{port}")
    logger.info(f"🔧 API Docs: http://localhost:{port}/docs")
    
    uvicorn.run(
        "webapp:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )