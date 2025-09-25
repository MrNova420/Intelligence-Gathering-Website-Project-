#!/bin/bash
# Complete Intelligence Gathering Platform Setup and Start for Termux
# This script handles the full setup and launch for Termux environments

set -e  # Exit on any error

echo "🚀 Intelligence Gathering Platform - Termux Setup & Launch"
echo "=========================================================="

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in Termux
if [[ ! "$PREFIX" =~ "com.termux" ]] && [[ ! -d "/data/data/com.termux" ]]; then
    warn "This script is optimized for Termux but can work on other Linux systems"
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check and install system dependencies
info "Checking system dependencies..."

# Check Python
if ! command_exists python; then
    error "Python not found. Please install with: pkg install python"
    exit 1
fi

# Check Node.js
if ! command_exists node; then
    warn "Node.js not found. Installing..."
    if command_exists pkg; then
        pkg install nodejs -y
    else
        error "Please install Node.js manually"
        exit 1
    fi
fi

# Check if npm is available
if ! command_exists npm; then
    error "npm not found. Please install Node.js properly"
    exit 1
fi

info "✅ System dependencies check complete"

# Setup Python backend
info "Setting up Python backend..."

cd backend

# Install Python dependencies using lite requirements
if [[ -f "requirements-lite.txt" ]]; then
    info "Installing Python dependencies (SQLite-only)..."
    pip install -r requirements-lite.txt --user
else
    warn "requirements-lite.txt not found, falling back to individual packages"
    pip install --user fastapi uvicorn sqlalchemy pydantic dnspython phonenumbers python-dotenv requests passlib[bcrypt]
fi

# Setup environment file
if [[ ! -f "../.env" ]]; then
    if [[ -f "../.env.example" ]]; then
        info "Creating environment file..."
        cp ../.env.example ../.env
        info "✅ Created .env from .env.example"
    else
        info "Creating basic .env file..."
        cat > ../.env << EOF
# Intelligence Gathering Platform Configuration
DATABASE_URL=sqlite:///./intelligence_platform.db
SECRET_KEY=termux-development-key-change-in-production
DEBUG=true
ENVIRONMENT=termux
EOF
        info "✅ Created basic .env file"
    fi
fi

# Setup database
info "Setting up SQLite database..."
if [[ -f "app/db/setup_standalone.py" ]]; then
    python app/db/setup_standalone.py
    info "✅ Database setup complete"
else
    warn "Database setup script not found, will try to initialize on startup"
fi

cd ..

# Setup Node.js frontend
info "Setting up Node.js frontend..."

cd frontend

# Install Node.js dependencies
info "Installing Node.js dependencies..."
npm install

# Build frontend for production (optional, but faster)
info "Building frontend..."
npm run build

cd ..

info "✅ Setup complete!"

# Start the platform
info "Starting Intelligence Gathering Platform..."

# Function to cleanup background processes
cleanup() {
    info "Shutting down services..."
    if [[ -n "$BACKEND_PID" ]]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [[ -n "$FRONTEND_PID" ]]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    exit 0
}

# Setup cleanup on script exit
trap cleanup EXIT INT TERM

# Check if tmux is available for better terminal management
if command_exists tmux; then
    info "Using tmux for better session management..."
    
    # Kill existing session if it exists
    tmux kill-session -t intelligence_platform 2>/dev/null || true
    
    # Create new tmux session
    tmux new-session -d -s intelligence_platform
    
    # Start backend in first window
    tmux send-keys -t intelligence_platform:0 'cd backend && python run_standalone.py' Enter
    
    # Create new window for frontend
    tmux new-window -t intelligence_platform
    tmux send-keys -t intelligence_platform:1 'cd frontend && npm start' Enter
    
    info "✅ Services started in tmux session 'intelligence_platform'"
    info ""
    info "🌐 Access Points:"
    info "   • Frontend: http://localhost:3000"
    info "   • Backend API: http://localhost:8000"
    info "   • API Docs: http://localhost:8000/docs"
    info ""
    info "📱 Session Management:"
    info "   • View services: tmux attach -t intelligence_platform"
    info "   • Switch windows: Ctrl+B then 0 (backend) or 1 (frontend)"
    info "   • Detach: Ctrl+B then D"
    info "   • Stop all: tmux kill-session -t intelligence_platform"
    info ""
    info "Press Ctrl+C to stop this script, or attach to the tmux session"
    
    # Wait for user to stop
    while true; do
        sleep 1
    done
    
else
    info "Starting services in background (install tmux for better experience)..."
    
    # Start backend in background
    cd backend
    nohup python run_standalone.py > ../backend.log 2>&1 &
    BACKEND_PID=$!
    cd ..
    
    # Wait for backend to start
    sleep 5
    
    # Start frontend in foreground
    info "Starting frontend (this will keep running)..."
    info ""
    info "🌐 Access Points:"
    info "   • Frontend: http://localhost:3000"
    info "   • Backend API: http://localhost:8000"
    info "   • API Docs: http://localhost:8000/docs"
    info ""
    info "Press Ctrl+C to stop all services"
    
    cd frontend
    npm start
fi