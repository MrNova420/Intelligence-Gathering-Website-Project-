#!/usr/bin/env python3
"""
Intelligence Gathering Platform - Unified Setup Script
One-click setup for the complete web platform
"""

import os
import sys
import subprocess
import shutil
import logging
from pathlib import Path
from typing import List, Dict, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PlatformSetup:
    """Unified setup for Intelligence Gathering Platform"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.is_termux = "com.termux" in os.environ.get("PREFIX", "")
        self.python_executable = sys.executable
        
    def print_banner(self):
        """Print setup banner"""
        print("=" * 70)
        print("🔍 INTELLIGENCE GATHERING PLATFORM - UNIFIED SETUP")
        print("=" * 70)
        print("🌐 Complete Web Application Setup")
        print("📱 Termux/Android Compatible")
        print("🚀 Production Ready")
        print("=" * 70)
        print()
    
    def check_system_requirements(self) -> bool:
        """Check system requirements"""
        logger.info("🔍 Checking system requirements...")
        
        # Check Python version
        if sys.version_info < (3.8, 0):
            logger.error("❌ Python 3.8+ required")
            return False
        
        logger.info(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        
        # Check pip
        try:
            import pip
            logger.info("✅ pip available")
        except ImportError:
            logger.error("❌ pip not available")
            return False
        
        # Termux specific checks
        if self.is_termux:
            logger.info("📱 Termux environment detected")
            # Check essential Termux packages
            termux_packages = ["python", "python-pip"]
            for package in termux_packages:
                if not shutil.which(package):
                    logger.warning(f"⚠️ Termux package might be missing: {package}")
        
        return True
    
    def install_dependencies(self) -> bool:
        """Install required dependencies"""
        logger.info("📦 Installing dependencies...")
        
        # Core dependencies for unified web platform
        core_dependencies = [
            "fastapi>=0.104.1",
            "uvicorn[standard]>=0.24.0",
            "jinja2>=3.1.2",
            "python-multipart>=0.0.6",
            "aiofiles>=23.2.1",
            "sqlalchemy>=2.0.23",
            "pydantic[email]>=2.5.0",
            "python-dotenv>=1.0.0",
            "aiohttp>=3.9.1",
            "requests>=2.31.0"
        ]
        
        # Enhanced features dependencies (optional)
        enhanced_dependencies = [
            "psutil>=5.9.6",           # Performance monitoring
            "redis>=5.0.1",            # Caching (optional)
            "cryptography>=41.0.7",    # Security
            "passlib[bcrypt]>=1.7.4",  # Password hashing
            "reportlab>=4.0.7",        # PDF reports
            "pillow>=10.1.0",          # Image processing
            "dnspython>=2.4.2",        # DNS lookups
            "phonenumbers>=8.13.26",   # Phone validation
            "python-jose[cryptography]>=3.3.0"  # JWT tokens
        ]
        
        # Install core dependencies
        logger.info("📦 Installing core dependencies...")
        if not self._install_packages(core_dependencies):
            logger.error("❌ Failed to install core dependencies")
            return False
        
        # Install enhanced dependencies (with fallbacks)
        logger.info("📦 Installing enhanced features...")
        failed_enhanced = []
        for package in enhanced_dependencies:
            if not self._install_packages([package], ignore_errors=True):
                failed_enhanced.append(package)
        
        if failed_enhanced:
            logger.warning(f"⚠️ Optional packages not installed: {', '.join(failed_enhanced)}")
            logger.info("💡 Platform will use fallback implementations")
        
        logger.info("✅ Dependencies installation completed")
        return True
    
    def _install_packages(self, packages: List[str], ignore_errors: bool = False) -> bool:
        """Install Python packages"""
        try:
            cmd = [self.python_executable, "-m", "pip", "install", "--user"] + packages
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode != 0:
                if not ignore_errors:
                    logger.error(f"❌ pip install failed: {result.stderr}")
                return False
            
            return True
            
        except subprocess.TimeoutExpired:
            logger.error("❌ Package installation timed out")
            return False
        except Exception as e:
            if not ignore_errors:
                logger.error(f"❌ Installation error: {e}")
            return False
    
    def setup_project_structure(self) -> bool:
        """Setup project directory structure"""
        logger.info("📁 Setting up project structure...")
        
        # Create directories
        directories = [
            "web/templates",
            "web/static/css",
            "web/static/js", 
            "web/static/images",
            "data/scans",
            "data/reports",
            "data/backups",
            "data/database",
            "logs",
            "plugins",
            "config"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Created directory: {directory}")
        
        logger.info("✅ Project structure created")
        return True
    
    def create_configuration_files(self) -> bool:
        """Create configuration files"""
        logger.info("⚙️ Creating configuration files...")
        
        # Create .env file
        env_content = f"""# Intelligence Gathering Platform Configuration
# Environment
ENVIRONMENT=production
DEBUG=false
HOST=0.0.0.0
PORT=8000

# Security
SECRET_KEY=intelligence-platform-{os.urandom(16).hex()}

# Database
DATABASE_URL=sqlite:///data/database/platform.db

# Features
ENABLE_MONITORING=true
ENABLE_ERROR_TRACKING=true
ENABLE_AUTO_BACKUP=true

# Termux specific (auto-detected)
TERMUX_MODE={'true' if self.is_termux else 'false'}
"""
        
        env_file = self.project_root / ".env"
        env_file.write_text(env_content)
        logger.info("✅ Created .env configuration file")
        
        # Create .gitignore if it doesn't exist
        gitignore_additions = """
# Platform specific
.env
*.env
data/database/
data/scans/
data/backups/
logs/
web/static/uploads/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.pytest_cache/
.coverage
htmlcov/
"""
        
        gitignore_file = self.project_root / ".gitignore"
        if gitignore_file.exists():
            gitignore_content = gitignore_file.read_text()
            if "# Platform specific" not in gitignore_content:
                gitignore_file.write_text(gitignore_content + "\n" + gitignore_additions)
        else:
            gitignore_file.write_text(gitignore_additions)
        
        logger.info("✅ Updated .gitignore")
        return True
    
    def test_installation(self) -> bool:
        """Test the installation"""
        logger.info("🧪 Testing installation...")
        
        try:
            # Test core imports
            import fastapi
            import uvicorn
            import jinja2
            logger.info("✅ Core web framework imports successful")
            
            # Test configuration
            from config import config
            logger.info("✅ Configuration system working")
            
            # Test app creation
            from app import app
            logger.info("✅ Web application created successfully")
            
            logger.info("🎉 Installation test passed!")
            return True
            
        except ImportError as e:
            logger.error(f"❌ Import error: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Test failed: {e}")
            return False
    
    def create_startup_scripts(self) -> bool:
        """Create convenient startup scripts"""
        logger.info("📜 Creating startup scripts...")
        
        # Windows batch file
        batch_content = """@echo off
echo Starting Intelligence Gathering Platform...
python start.py web
pause
"""
        batch_file = self.project_root / "start.bat"
        batch_file.write_text(batch_content)
        
        # Unix shell script
        shell_content = """#!/bin/bash
echo "Starting Intelligence Gathering Platform..."
python3 start.py web
"""
        shell_file = self.project_root / "start.sh"
        shell_file.write_text(shell_content)
        
        # Make shell script executable on Unix systems
        if os.name != 'nt':
            try:
                os.chmod(shell_file, 0o755)
            except:
                pass
        
        logger.info("✅ Startup scripts created")
        return True
    
    def show_completion_message(self):
        """Show setup completion message"""
        print("\n" + "=" * 70)
        print("🎉 SETUP COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print()
        print("🚀 Your Intelligence Gathering Platform is ready!")
        print()
        print("📋 QUICK START:")
        print("  1. Start the platform:")
        print("     • python start.py web           (Standard mode)")
        print("     • python start.py dev           (Development mode)")
        print("     • python start.py termux        (Termux optimized)")
        print("     • ./start.sh                    (Unix systems)")
        print("     • start.bat                     (Windows)")
        print()
        print("  2. Open your browser and go to:")
        print("     • http://localhost:8000         (Web Interface)")
        print("     • http://localhost:8000/docs    (API Documentation)")
        print("     • http://localhost:8000/health  (Health Check)")
        print()
        print("🔧 CONFIGURATION:")
        print("  • Edit .env file for custom settings")
        print("  • Check config.py for advanced options")
        print()
        print("📱 TERMUX USERS:")
        print("  • Use: python start.py termux")
        print("  • Platform automatically optimized for Android")
        print()
        print("🆘 SUPPORT:")
        print("  • Run: python start.py status    (Check system status)")
        print("  • Run: python start.py validate  (Validate installation)")
        print()
        print("=" * 70)
        print("🌟 Enjoy your Intelligence Gathering Platform! 🔍")
        print("=" * 70)
    
    def run_setup(self) -> bool:
        """Run the complete setup process"""
        self.print_banner()
        
        steps = [
            ("System Requirements", self.check_system_requirements),
            ("Project Structure", self.setup_project_structure),
            ("Dependencies", self.install_dependencies),
            ("Configuration", self.create_configuration_files),
            ("Startup Scripts", self.create_startup_scripts),
            ("Installation Test", self.test_installation)
        ]
        
        for step_name, step_func in steps:
            print(f"\n🔄 {step_name}...")
            if not step_func():
                print(f"\n❌ Setup failed at: {step_name}")
                return False
            print(f"✅ {step_name} completed")
        
        self.show_completion_message()
        return True

def main():
    """Main setup entry point"""
    try:
        setup = PlatformSetup()
        success = setup.run_setup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()