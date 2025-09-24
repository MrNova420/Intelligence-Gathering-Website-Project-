#!/usr/bin/env python3
"""
Local Development Setup Script for Intelligence Gathering Platform
This script sets up everything needed to run the full website locally on localhost
"""

import os
import sys
import subprocess
import time
import platform
import json
from pathlib import Path

def print_banner():
    print("=" * 70)
    print("🌐 Intelligence Gathering Platform - Local Setup")
    print("=" * 70)
    print("This script will set up the complete website for local testing")
    print("You'll be able to access it at http://localhost:3000")
    print()

def check_system():
    """Check system requirements and installed software"""
    print("🔍 Checking system requirements...")
    
    requirements = {
        'python': {'cmd': ['python3', '--version'], 'min_version': '3.9'},
        'node': {'cmd': ['node', '--version'], 'min_version': '16.0'},
        'npm': {'cmd': ['npm', '--version'], 'min_version': '8.0'},
        'docker': {'cmd': ['docker', '--version'], 'optional': True},
        'git': {'cmd': ['git', '--version'], 'required': True}
    }
    
    missing = []
    for tool, config in requirements.items():
        try:
            result = subprocess.run(config['cmd'], capture_output=True, text=True, check=True)
            print(f"  ✅ {tool}: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            if config.get('optional'):
                print(f"  ⚠️  {tool}: Not installed (optional)")
            else:
                print(f"  ❌ {tool}: Not installed")
                missing.append(tool)
    
    if missing:
        print(f"\n❌ Missing required tools: {', '.join(missing)}")
        print("Please install these tools before continuing.")
        return False
    
    print("✅ System requirements check passed!")
    return True

def setup_backend():
    """Set up the backend environment"""
    print("\n🔧 Setting up backend...")
    
    backend_dir = Path('backend')
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return False
    
    os.chdir(backend_dir)
    
    # Check if virtual environment exists
    venv_dir = Path('venv')
    if not venv_dir.exists():
        print("  📦 Creating Python virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
    
    # Activate virtual environment and install dependencies
    if platform.system() == "Windows":
        pip_cmd = str(venv_dir / 'Scripts' / 'pip')
        python_cmd = str(venv_dir / 'Scripts' / 'python')
    else:
        pip_cmd = str(venv_dir / 'bin' / 'pip')
        python_cmd = str(venv_dir / 'bin' / 'python')
    
    print("  📥 Installing Python dependencies...")
    subprocess.run([pip_cmd, 'install', '-r', 'requirements.txt'], check=True)
    
    # Create local SQLite database
    print("  🗄️  Setting up local database...")
    env_content = """# Local Development Environment
DATABASE_URL=sqlite:///./intelligence_platform.db
REDIS_URL=redis://localhost:6379/0
USE_REDIS_FALLBACK=true
SECRET_KEY=local-development-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=true
ENVIRONMENT=development
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]

# Optional API Keys (add your own)
CLEARBIT_API_KEY=
HUNTER_API_KEY=
STRIPE_SECRET_KEY=
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    os.chdir('..')
    print("✅ Backend setup complete!")
    return True

def setup_frontend():
    """Set up the frontend environment"""
    print("\n🎨 Setting up frontend...")
    
    frontend_dir = Path('frontend')
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False
    
    os.chdir(frontend_dir)
    
    # Install npm dependencies
    print("  📥 Installing Node.js dependencies...")
    subprocess.run(['npm', 'install'], check=True)
    
    # Create environment file
    env_content = """NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENVIRONMENT=development
"""
    
    with open('.env.local', 'w') as f:
        f.write(env_content)
    
    os.chdir('..')
    print("✅ Frontend setup complete!")
    return True

def create_startup_scripts():
    """Create convenient startup scripts"""
    print("\n📝 Creating startup scripts...")
    
    # Backend startup script
    backend_script = """#!/bin/bash
# Start the Intelligence Gathering Platform Backend
echo "🚀 Starting Intelligence Gathering Platform Backend..."
cd backend

# Activate virtual environment
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Start the server
echo "🌐 Backend will be available at http://localhost:8000"
echo "📖 API documentation at http://localhost:8000/docs"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
"""
    
    with open('start_backend.sh', 'w') as f:
        f.write(backend_script)
    
    # Frontend startup script
    frontend_script = """#!/bin/bash
# Start the Intelligence Gathering Platform Frontend
echo "🎨 Starting Intelligence Gathering Platform Frontend..."
cd frontend

echo "🌐 Frontend will be available at http://localhost:3000"
npm run dev
"""
    
    with open('start_frontend.sh', 'w') as f:
        f.write(frontend_script)
    
    # Complete startup script
    complete_script = """#!/bin/bash
# Start the complete Intelligence Gathering Platform
echo "🚀 Starting Complete Intelligence Gathering Platform..."
echo "This will start both backend and frontend services"
echo ""

# Check if tmux is available for better terminal management
if command -v tmux &> /dev/null; then
    echo "Using tmux for better session management..."
    
    # Create new tmux session
    tmux new-session -d -s intelligence_platform
    
    # Start backend in first window
    tmux send-keys -t intelligence_platform:0 './start_backend.sh' Enter
    
    # Create new window for frontend
    tmux new-window -t intelligence_platform
    tmux send-keys -t intelligence_platform:1 './start_frontend.sh' Enter
    
    echo "✅ Services started in tmux session 'intelligence_platform'"
    echo "📱 Use 'tmux attach -t intelligence_platform' to view services"
    echo "🌐 Frontend: http://localhost:3000"
    echo "🔧 Backend API: http://localhost:8000"
    echo "📖 API Docs: http://localhost:8000/docs"
    
else
    echo "Starting services in background..."
    echo "Note: Install tmux for better session management"
    
    # Start backend in background
    nohup ./start_backend.sh > backend.log 2>&1 &
    BACKEND_PID=$!
    
    # Wait a moment for backend to start
    sleep 3
    
    # Start frontend
    echo "Starting frontend..."
    ./start_frontend.sh
fi
"""
    
    with open('start_platform.sh', 'w') as f:
        f.write(complete_script)
    
    # Make scripts executable on Unix-like systems
    if platform.system() != "Windows":
        os.chmod('start_backend.sh', 0o755)
        os.chmod('start_frontend.sh', 0o755)
        os.chmod('start_platform.sh', 0o755)
    
    print("✅ Startup scripts created!")
    return True

def create_docker_setup():
    """Create simplified Docker setup for easy deployment"""
    print("\n🐳 Creating Docker setup...")
    
    # Simple docker-compose for local development
    docker_compose_dev = """version: '3.8'

services:
  # Backend API
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./intelligence_platform.db
      - DEBUG=true
      - ENVIRONMENT=development
    volumes:
      - ./backend:/app
    restart: unless-stopped

  # Frontend
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - backend
    restart: unless-stopped
"""
    
    with open('docker-compose.dev.yml', 'w') as f:
        f.write(docker_compose_dev)
    
    # Quick Docker startup script
    docker_script = """#!/bin/bash
# Quick Docker setup for Intelligence Gathering Platform
echo "🐳 Starting Intelligence Gathering Platform with Docker..."

# Build and start services
docker-compose -f docker-compose.dev.yml up --build

echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
"""
    
    with open('start_with_docker.sh', 'w') as f:
        f.write(docker_script)
    
    if platform.system() != "Windows":
        os.chmod('start_with_docker.sh', 0o755)
    
    print("✅ Docker setup created!")
    return True

def main():
    """Main setup function"""
    print_banner()
    
    # Check system requirements
    if not check_system():
        return False
    
    # Setup components
    success = True
    success &= setup_backend()
    success &= setup_frontend()
    success &= create_startup_scripts()
    success &= create_docker_setup()
    
    if success:
        print("\n" + "=" * 70)
        print("🎉 LOCAL SETUP COMPLETE!")
        print("=" * 70)
        print()
        print("🚀 How to start the platform:")
        print("  Option 1 (Recommended): ./start_platform.sh")
        print("  Option 2 (Backend only): ./start_backend.sh")
        print("  Option 3 (Frontend only): ./start_frontend.sh")
        print("  Option 4 (Docker): ./start_with_docker.sh")
        print()
        print("🌐 Access URLs:")
        print("  Frontend (Main Website): http://localhost:3000")
        print("  Backend API: http://localhost:8000")
        print("  API Documentation: http://localhost:8000/docs")
        print()
        print("📝 Next Steps:")
        print("  1. Run './start_platform.sh' to start everything")
        print("  2. Open http://localhost:3000 in your browser")
        print("  3. Test the intelligence gathering features")
        print()
        print("💡 Tip: Use Ctrl+C to stop services")
        print("=" * 70)
        return True
    else:
        print("\n❌ Setup failed! Please check the errors above.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)