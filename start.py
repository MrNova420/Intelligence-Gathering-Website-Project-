#!/usr/bin/env python3
"""
Intelligence Gathering Platform - Quick Start
============================================

Simplified startup script for the unified platform.
"""

import sys
import subprocess
import os
from pathlib import Path

def main():
    """Main startup function"""
    print("🚀 Starting Intelligence Gathering Platform...")
    print("🔍 Unified all-in-one intelligence gathering solution")
    print("📡 Web Interface: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("⚙️  System Admin: http://localhost:8000/admin")
    print("-" * 60)
    
    # Check if we're in the right directory
    if not Path("unified_app.py").exists():
        print("❌ Error: unified_app.py not found")
        print("Please run this script from the project root directory")
        sys.exit(1)
    
    # Start the unified application
    try:
        subprocess.run([sys.executable, "unified_app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Platform stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting platform: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()