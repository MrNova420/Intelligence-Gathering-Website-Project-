#!/usr/bin/env python3
"""
Intelligence Gathering Platform - Unified Web Application
Main entry point for the complete unified website system
"""

# Import the unified web platform
from webapp import platform, app

if __name__ == "__main__":
    import uvicorn
    import logging
    
    logger = logging.getLogger(__name__)
    
    # Run the unified web application
    logger.info("🌐 Starting Unified Intelligence Gathering Web Platform")
    logger.info("🔍 Single system combining API + Web Interface")
    logger.info("📱 Termux/Android Compatible")
    logger.info("🌐 Web Interface: http://localhost:8000")
    logger.info("🔧 API Docs: http://localhost:8000/docs")
    
    uvicorn.run(
        "webapp:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )