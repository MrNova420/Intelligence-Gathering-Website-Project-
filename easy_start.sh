#!/bin/bash
# 🚀 Intelligence Gathering Platform - Super Easy Start
# One script to handle EVERYTHING - setup, install, start, restart, stop
# Works on all platforms: Termux, Linux, macOS, Windows (WSL)

set -e

# Color codes for beautiful output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Banner
echo -e "${PURPLE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║        🔍 INTELLIGENCE GATHERING PLATFORM                    ║"
echo "║               Super Easy Management Script                   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

info() { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
error() { echo -e "${RED}✗${NC} $1"; }
step() { echo -e "${BLUE}➤${NC} $1"; }
success() { echo -e "${GREEN}🎉${NC} $1"; }

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Detect platform
detect_platform() {
    if [[ "$PREFIX" =~ "com.termux" ]] || [[ -d "/data/data/com.termux" ]]; then
        PLATFORM="termux"
        PACKAGE_MANAGER="pkg"
    elif command_exists apt; then
        PLATFORM="debian"
        PACKAGE_MANAGER="apt"
    elif command_exists yum; then
        PLATFORM="redhat"
        PACKAGE_MANAGER="yum"
    elif command_exists brew; then
        PLATFORM="macos"
        PACKAGE_MANAGER="brew"
    else
        PLATFORM="unknown"
        PACKAGE_MANAGER="unknown"
    fi
    info "Platform detected: $PLATFORM"
}

# Install system dependencies
install_system_deps() {
    step "Installing system dependencies..."
    
    case $PLATFORM in
        "termux")
            pkg update -y
            pkg install -y python nodejs git tmux sqlite
            ;;
        "debian")
            sudo apt update
            sudo apt install -y python3 python3-pip nodejs npm git tmux sqlite3
            ;;
        "redhat")
            sudo yum install -y python3 python3-pip nodejs npm git tmux sqlite
            ;;
        "macos")
            brew install python node git tmux sqlite
            ;;
        *)
            warn "Unknown platform. Please install manually: python, nodejs, git, tmux, sqlite"
            ;;
    esac
    
    info "System dependencies installed"
}

# Install Python dependencies
install_python_deps() {
    step "Installing Python dependencies..."
    
    # Use requirements-lite.txt for lightweight installation
    if [[ -f "backend/requirements-lite.txt" ]]; then
        pip install -r backend/requirements-lite.txt --user --break-system-packages 2>/dev/null || pip install -r backend/requirements-lite.txt --user
        info "Python dependencies installed (SQLite-only)"
    else
        # Fallback to core packages
        pip install --user fastapi uvicorn sqlalchemy pydantic dnspython phonenumbers python-dotenv requests passlib[bcrypt] --break-system-packages 2>/dev/null || pip install --user fastapi uvicorn sqlalchemy pydantic dnspython phonenumbers python-dotenv requests passlib[bcrypt]
        info "Python dependencies installed (core packages)"
    fi
}

# Install Node.js dependencies
install_node_deps() {
    step "Installing Node.js dependencies..."
    
    if [[ -d "frontend" ]]; then
        cd frontend
        npm install --silent
        cd ..
        info "Node.js dependencies installed"
    else
        warn "Frontend directory not found, skipping Node.js dependencies"
    fi
}

# Setup environment
setup_environment() {
    step "Setting up environment..."
    
    # Create .env if it doesn't exist
    if [[ ! -f ".env" ]]; then
        if [[ -f ".env.example" ]]; then
            cp .env.example .env
            info "Created .env from .env.example"
        else
            cat > .env << 'EOF'
# Intelligence Gathering Platform Configuration
DATABASE_URL=sqlite:///./intelligence_platform.db
SECRET_KEY=easy-start-development-key-change-in-production
DEBUG=true
ENVIRONMENT=development
USE_REDIS_FALLBACK=true
EOF
            info "Created basic .env file"
        fi
    else
        info "Environment file already exists"
    fi
}

# Setup database
setup_database() {
    step "Setting up database..."
    
    cd backend
    if python app/db/setup_standalone.py; then
        info "Database setup completed"
    else
        warn "Database setup failed, but continuing..."
    fi
    cd ..
}

# Start services
start_services() {
    step "Starting services..."
    
    # Check if tmux is available
    if command_exists tmux; then
        # Kill existing session if it exists
        tmux kill-session -t intel 2>/dev/null || true
        
        # Create new session
        tmux new-session -d -s intel -c "$PWD"
        
        # Start backend
        tmux send-keys -t intel:0 'cd backend && python run_standalone.py' Enter
        
        # Create window for frontend
        if [[ -d "frontend" ]]; then
            tmux new-window -t intel -c "$PWD/frontend"
            tmux send-keys -t intel:1 'npm run dev' Enter
        fi
        
        success "Services started in tmux session 'intel'"
        echo ""
        echo -e "${CYAN}🌐 Access Points:${NC}"
        echo "   • Backend API: http://localhost:8000"
        echo "   • API Docs: http://localhost:8000/docs"
        if [[ -d "frontend" ]]; then
            echo "   • Frontend Website: http://localhost:3000"
        fi
        echo ""
        echo -e "${BLUE}📱 Session Management:${NC}"
        echo "   • View services: tmux attach -t intel"
        echo "   • Switch windows: Ctrl+B then 0 (backend) or 1 (frontend)"
        echo "   • Detach: Ctrl+B then D"
        echo "   • Stop all: ./easy_start.sh stop"
        
    else
        # Start without tmux
        cd backend
        nohup python run_standalone.py > ../backend.log 2>&1 &
        echo $! > ../backend.pid
        cd ..
        
        if [[ -d "frontend" ]]; then
            cd frontend
            nohup npm run dev > ../frontend.log 2>&1 &
            echo $! > ../frontend.pid
            cd ..
        fi
        
        success "Services started in background"
        echo ""
        echo -e "${CYAN}🌐 Access Points:${NC}"
        echo "   • Backend API: http://localhost:8000"
        echo "   • API Docs: http://localhost:8000/docs"
        if [[ -d "frontend" ]]; then
            echo "   • Frontend Website: http://localhost:3000"
        fi
        echo ""
        echo "   • Stop all: ./easy_start.sh stop"
    fi
}

# Stop services
stop_services() {
    step "Stopping services..."
    
    # Stop tmux session
    if command_exists tmux; then
        tmux kill-session -t intel 2>/dev/null && info "Stopped tmux session" || warn "No tmux session found"
    fi
    
    # Stop background processes
    if [[ -f "backend.pid" ]]; then
        kill $(cat backend.pid) 2>/dev/null && info "Stopped backend" || warn "Backend not running"
        rm -f backend.pid
    fi
    
    if [[ -f "frontend.pid" ]]; then
        kill $(cat frontend.pid) 2>/dev/null && info "Stopped frontend" || warn "Frontend not running"
        rm -f frontend.pid
    fi
    
    # Additional cleanup
    pkill -f "python.*run_standalone.py" 2>/dev/null || true
    pkill -f "npm.*run.*dev" 2>/dev/null || true
    
    success "All services stopped"
}

# Status check
check_status() {
    step "Checking service status..."
    
    echo ""
    echo -e "${BLUE}🔍 Service Status:${NC}"
    
    # Check tmux session
    if command_exists tmux && tmux has-session -t intel 2>/dev/null; then
        echo -e "   ${GREEN}✓${NC} tmux session 'intel' is running"
        tmux list-windows -t intel
    else
        echo -e "   ${YELLOW}⚠${NC} No tmux session found"
    fi
    
    # Check processes
    if pgrep -f "python.*run_standalone.py" >/dev/null; then
        echo -e "   ${GREEN}✓${NC} Backend is running"
    else
        echo -e "   ${RED}✗${NC} Backend is not running"
    fi
    
    if pgrep -f "npm.*run.*dev" >/dev/null; then
        echo -e "   ${GREEN}✓${NC} Frontend is running"
    else
        echo -e "   ${RED}✗${NC} Frontend is not running"
    fi
    
    echo ""
    echo -e "${BLUE}🌐 Access Points:${NC}"
    echo "   • Backend API: http://localhost:8000"
    echo "   • API Docs: http://localhost:8000/docs"
    echo "   • Frontend Website: http://localhost:3000"
}

# Full setup (install everything)
full_setup() {
    echo -e "${PURPLE}🚀 Starting full setup...${NC}"
    echo ""
    
    detect_platform
    install_system_deps
    install_python_deps
    install_node_deps
    setup_environment
    setup_database
    
    success "Full setup completed!"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "   • Start services: ./easy_start.sh start"
    echo "   • Or do everything: ./easy_start.sh"
}

# Quick setup (dependencies only)
quick_setup() {
    echo -e "${PURPLE}⚡ Starting quick setup...${NC}"
    echo ""
    
    detect_platform
    install_python_deps
    setup_environment
    setup_database
    
    success "Quick setup completed!"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "   • Start services: ./easy_start.sh start"
}

# Restart services
restart_services() {
    step "Restarting services..."
    stop_services
    sleep 2
    start_services
}

# Show help
show_help() {
    echo -e "${CYAN}🔧 Intelligence Gathering Platform - Easy Start${NC}"
    echo ""
    echo "Usage: ./easy_start.sh [command]"
    echo ""
    echo -e "${BLUE}Commands:${NC}"
    echo "  (no args)     Full setup + start (recommended for first time)"
    echo "  start         Start all services"
    echo "  stop          Stop all services"
    echo "  restart       Restart all services"
    echo "  status        Check service status"
    echo "  setup         Full setup (install everything)"
    echo "  quick         Quick setup (dependencies only)"
    echo "  help          Show this help"
    echo ""
    echo -e "${BLUE}Examples:${NC}"
    echo "  ./easy_start.sh           # First time setup + start"
    echo "  ./easy_start.sh start     # Just start services"
    echo "  ./easy_start.sh restart   # Restart everything"
    echo "  ./easy_start.sh stop      # Stop everything"
    echo ""
    echo -e "${BLUE}Access Points:${NC}"
    echo "  🌐 Website: http://localhost:3000"
    echo "  🔧 API: http://localhost:8000"
    echo "  📖 Docs: http://localhost:8000/docs"
}

# Main logic
case "${1:-}" in
    "start")
        start_services
        ;;
    "stop")
        stop_services
        ;;
    "restart")
        restart_services
        ;;
    "status")
        check_status
        ;;
    "setup")
        full_setup
        ;;
    "quick")
        quick_setup
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    "")
        # Default: full setup + start
        full_setup
        start_services
        ;;
    *)
        error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac