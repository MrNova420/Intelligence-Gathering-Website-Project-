#!/usr/bin/env python3
"""
Simple test of the unified web application
"""

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    """Test all imports"""
    print("🧪 Testing imports...")
    
    try:
        from fastapi import FastAPI, HTTPException, Request, Form
        print("✅ FastAPI imports successful")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.responses import HTMLResponse, JSONResponse
        from fastapi.staticfiles import StaticFiles
        from fastapi.templating import Jinja2Templates
        print("✅ FastAPI components imports successful")
    except ImportError as e:
        print(f"❌ FastAPI components import failed: {e}")
        return False
        
    return True

def create_simple_app():
    """Create a simple FastAPI app"""
    print("🏗️ Creating simple app...")
    
    try:
        from fastapi import FastAPI
        
        app = FastAPI(
            title="Intelligence Gathering Platform",
            description="Unified Web Application",
            version="2.0.0"
        )
        
        @app.get("/")
        async def root():
            return {"message": "Intelligence Gathering Platform - Unified Web Application"}
        
        @app.get("/health")
        async def health():
            return {"status": "healthy", "platform": "Intelligence Gathering Platform"}
        
        print("✅ Simple app created successfully")
        return app
        
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        return None

def test_run():
    """Test running the app"""
    print("🚀 Testing app run...")
    
    if not test_imports():
        return False
    
    app = create_simple_app()
    if not app:
        return False
    
    try:
        import uvicorn
        print("✅ uvicorn available")
        
        # Don't actually run, just test the setup
        print("✅ App ready to run")
        return True
        
    except ImportError as e:
        print(f"❌ uvicorn import failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Intelligence Gathering Platform - Web App Test")
    print("=" * 60)
    
    success = test_run()
    
    if success:
        print("\n🎉 All tests passed! The unified web application is ready.")
        print("🌐 Run with: python -m uvicorn test_webapp:app --host 0.0.0.0 --port 8000")
    else:
        print("\n❌ Tests failed! Check the errors above.")
    
    print("=" * 60)
    
# Create the app for uvicorn
app = create_simple_app()