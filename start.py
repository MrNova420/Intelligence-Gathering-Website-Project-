#!/usr/bin/env python3
"""
Intelligence Gathering Platform - Unified Startup Script
Single command to start the complete web application
"""

import os
import sys
import argparse
import logging
import subprocess
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PlatformLauncher:
    """Unified launcher for the Intelligence Gathering Platform"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.setup_environment()
    
    def setup_environment(self):
        """Setup environment and check dependencies"""
        logger.info("🔧 Setting up environment...")
        
        # Ensure Python path includes backend
        backend_path = self.project_root / "backend"
        if str(backend_path) not in sys.path:
            sys.path.insert(0, str(backend_path))
        
        # Check if running in Termux
        self.is_termux = "com.termux" in os.environ.get("PREFIX", "")
        if self.is_termux:
            logger.info("📱 Termux environment detected")
    
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        logger.info("📦 Checking dependencies...")
        
        required_packages = [
            "fastapi", "uvicorn", "jinja2", "python-multipart"
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            logger.error(f"❌ Missing packages: {', '.join(missing_packages)}")
            logger.info("💡 Install with: pip install " + " ".join(missing_packages))
            return False
        
        logger.info("✅ All dependencies available")
        return True
    
    def run_web_application(self, host="0.0.0.0", port=8000, reload=False):
        """Run the unified web application"""
        logger.info("🚀 Starting Unified Intelligence Gathering Web Platform")
        logger.info("=" * 60)
        logger.info("🌐 Mode: Unified Web Application")
        logger.info(f"🔗 URL: http://localhost:{port}")
        logger.info(f"📱 Termux Compatible: {'Yes' if self.is_termux else 'N/A'}")
        logger.info("=" * 60)
        
        try:
            import uvicorn
            from unified_app import app
            
            uvicorn.run(
                "webapp:app",
                host=host,
                port=port,
                reload=reload,
                log_level="info"
            )
        except KeyboardInterrupt:
            logger.info("\n🛑 Platform stopped by user")
        except Exception as e:
            logger.error(f"❌ Failed to start platform: {e}")
            sys.exit(1)
    
    def run_development_mode(self):
        """Run in development mode with hot reload"""
        logger.info("🛠️ Starting in Development Mode (Hot Reload)")
        self.run_web_application(reload=True)
    
    def run_production_mode(self):
        """Run in production mode"""
        logger.info("🏭 Starting in Production Mode")
        self.run_web_application(reload=False)
    
    def run_termux_mode(self):
        """Run optimized for Termux"""
        logger.info("📱 Starting in Termux Mode")
        # Use localhost only for Termux to avoid permission issues
        self.run_web_application(host="127.0.0.1", port=8000)
    
    def install_dependencies(self):
        """Install required dependencies"""
        logger.info("📦 Installing dependencies...")
        
        requirements_file = self.project_root / "backend" / "requirements-lite.txt"
        if requirements_file.exists():
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
                ])
                logger.info("✅ Dependencies installed successfully")
            except subprocess.CalledProcessError as e:
                logger.error(f"❌ Failed to install dependencies: {e}")
                sys.exit(1)
        else:
            # Install basic requirements
            basic_packages = [
                "fastapi", "uvicorn[standard]", "jinja2", "python-multipart",
                "aiohttp", "sqlalchemy", "pydantic"
            ]
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install"
                ] + basic_packages)
                logger.info("✅ Basic dependencies installed")
            except subprocess.CalledProcessError as e:
                logger.error(f"❌ Failed to install basic dependencies: {e}")
                sys.exit(1)
    
    def validate_platform(self):
        """Validate platform is working correctly"""
        logger.info("🧪 Validating platform...")
        
        try:
            # Try to import main components
            from unified_app import app
            logger.info("✅ Main application imports successfully")
            
            # Check backend components
            try:
                from backend.app.core.enhanced_security import SecurityManager
                logger.info("✅ Security system available")
            except ImportError:
                logger.warning("⚠️ Security system not available")
            
            try:
                from backend.app.monitoring.performance_metrics import metrics_collector
                logger.info("✅ Monitoring system available")
            except ImportError:
                logger.warning("⚠️ Monitoring system not available")
            
            logger.info("🎉 Platform validation completed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Platform validation failed: {e}")
            return False
    
    def show_status(self):
        """Show platform status and information"""
        print("🔍 Intelligence Gathering Platform - Status")
        print("=" * 50)
        print(f"📁 Project Root: {self.project_root}")
        print(f"🐍 Python Version: {sys.version}")
        print(f"📱 Termux Mode: {'Yes' if self.is_termux else 'No'}")
        
        # Check if app can be imported
        try:
            from unified_app import app
            print("✅ Main Application: Available")
        except ImportError as e:
            print(f"❌ Main Application: Not available ({e})")
        
        # Check dependencies
        if self.check_dependencies():
            print("✅ Dependencies: All required packages installed")
        else:
            print("❌ Dependencies: Missing required packages")
        
        print("=" * 50)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Intelligence Gathering Platform - Unified Launcher"
    )
    
    parser.add_argument(
        "mode",
        nargs="?",
        default="web",
        choices=["web", "dev", "prod", "termux", "install", "validate", "status"],
        help="Launch mode (default: web)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run on (default: 8000)"
    )
    
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    
    args = parser.parse_args()
    
    launcher = PlatformLauncher()
    
    if args.mode == "install":
        launcher.install_dependencies()
    elif args.mode == "validate":
        launcher.validate_platform()
    elif args.mode == "status":
        launcher.show_status()
    elif args.mode == "dev":
        if launcher.check_dependencies():
            launcher.run_development_mode()
    elif args.mode == "prod":
        if launcher.check_dependencies():
            launcher.run_production_mode()
    elif args.mode == "termux":
        if launcher.check_dependencies():
            launcher.run_termux_mode()
    else:  # default "web" mode
        if launcher.check_dependencies():
            launcher.run_web_application(host=args.host, port=args.port)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Platform startup cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Platform startup failed: {e}")
        sys.exit(1)