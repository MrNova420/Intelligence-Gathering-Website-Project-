#!/bin/bash
# 🔧 Universal Installer for Intelligence Gathering Platform
# Works on: Termux, Ubuntu, Debian, CentOS, macOS, WSL

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo -e "${PURPLE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  🔧 INTELLIGENCE GATHERING PLATFORM - UNIVERSAL INSTALLER      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

info() { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
error() { echo -e "${RED}✗${NC} $1"; exit 1; }
step() { echo -e "${BLUE}→${NC} $1"; }

# Detect OS and platform
detect_os() {
    if [[ "$OSTYPE" == "linux-android"* ]] || [[ -d "/data/data/com.termux" ]]; then
        OS="termux"
        PACKAGE_MANAGER="pkg"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt >/dev/null 2>&1; then
            OS="debian"
            PACKAGE_MANAGER="apt"
        elif command -v yum >/dev/null 2>&1; then
            OS="redhat"
            PACKAGE_MANAGER="yum"
        elif command -v pacman >/dev/null 2>&1; then
            OS="arch"
            PACKAGE_MANAGER="pacman"
        else
            OS="linux"
            PACKAGE_MANAGER="unknown"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        PACKAGE_MANAGER="brew"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]]; then
        OS="windows"
        PACKAGE_MANAGER="unknown"
    else
        OS="unknown"
        PACKAGE_MANAGER="unknown"
    fi
    
    info "Detected OS: $OS"
}

# Install system dependencies
install_system_deps() {
    step "Installing system dependencies..."
    
    case $OS in
        "termux")
            pkg update -y || warn "Package update failed"
            pkg install -y python nodejs git tmux sqlite || error "Failed to install packages"
            ;;
        "debian")
            sudo apt update || warn "Package update failed"
            sudo apt install -y python3 python3-pip nodejs npm git tmux sqlite3 || error "Failed to install packages"
            # Create python symlink if needed
            if ! command -v python >/dev/null 2>&1; then
                sudo ln -sf /usr/bin/python3 /usr/bin/python
            fi
            ;;
        "redhat")
            sudo yum update -y || warn "Package update failed"
            sudo yum install -y python3 python3-pip nodejs npm git tmux sqlite || error "Failed to install packages"
            ;;
        "arch")
            sudo pacman -Syu --noconfirm || warn "Package update failed"
            sudo pacman -S --noconfirm python python-pip nodejs npm git tmux sqlite || error "Failed to install packages"
            ;;
        "macos")
            if ! command -v brew >/dev/null 2>&1; then
                step "Installing Homebrew..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            brew update || warn "Brew update failed"
            brew install python node git tmux sqlite || error "Failed to install packages"
            ;;
        *)
            warn "Unknown OS. Please install manually:"
            echo "  - Python 3.8+"
            echo "  - Node.js 16+"
            echo "  - Git"
            echo "  - tmux (optional)"
            echo "  - SQLite3"
            read -p "Press Enter when dependencies are installed..."
            ;;
    esac
    
    info "System dependencies installed"
}

# Install Python dependencies
install_python_deps() {
    step "Installing Python dependencies..."
    
    # Try requirements-lite.txt first
    if [[ -f "backend/requirements-lite.txt" ]]; then
        pip install -r backend/requirements-lite.txt --user --break-system-packages 2>/dev/null || \
        pip install -r backend/requirements-lite.txt --user 2>/dev/null || \
        pip3 install -r backend/requirements-lite.txt --user || \
        error "Failed to install Python dependencies"
    else
        # Fallback to essential packages
        pip install --user fastapi uvicorn sqlalchemy pydantic dnspython phonenumbers python-dotenv requests passlib[bcrypt] --break-system-packages 2>/dev/null || \
        pip install --user fastapi uvicorn sqlalchemy pydantic dnspython phonenumbers python-dotenv requests passlib[bcrypt] 2>/dev/null || \
        pip3 install --user fastapi uvicorn sqlalchemy pydantic dnspython phonenumbers python-dotenv requests passlib[bcrypt] || \
        error "Failed to install Python dependencies"
    fi
    
    info "Python dependencies installed"
}

# Install Node.js dependencies
install_node_deps() {
    if [[ -d "frontend" ]]; then
        step "Installing Node.js dependencies..."
        cd frontend
        npm install --silent || npm install || error "Failed to install Node.js dependencies"
        cd ..
        info "Node.js dependencies installed"
    else
        warn "Frontend directory not found, skipping Node.js setup"
    fi
}

# Setup environment
setup_env() {
    step "Setting up environment..."
    
    if [[ ! -f ".env" ]]; then
        if [[ -f ".env.example" ]]; then
            cp .env.example .env
            info "Created .env from .env.example"
        else
            cat > .env << 'EOF'
# Intelligence Gathering Platform Configuration
DATABASE_URL=sqlite:///./intelligence_platform.db
SECRET_KEY=installer-generated-key-change-in-production
DEBUG=true
ENVIRONMENT=development
USE_REDIS_FALLBACK=true

# Optional API Keys (add your own)
# CLEARBIT_API_KEY=your_key_here
# HUNTER_API_KEY=your_key_here
EOF
            info "Created default .env file"
        fi
    else
        info "Environment file already exists"
    fi
}

# Setup database
setup_db() {
    step "Setting up database..."
    
    cd backend
    if python app/db/setup_standalone.py; then
        info "Database initialized successfully"
    else
        warn "Database setup encountered issues, but continuing..."
    fi
    cd ..
}

# Create helper scripts
create_helpers() {
    step "Creating helper scripts..."
    
    # Make all scripts executable
    chmod +x *.sh 2>/dev/null || true
    
    info "Helper scripts are ready"
}

# Main installation
main() {
    echo ""
    step "Starting installation process..."
    echo ""
    
    detect_os
    install_system_deps
    install_python_deps
    install_node_deps
    setup_env
    setup_db
    create_helpers
    
    echo ""
    echo -e "${GREEN}🎉 Installation completed successfully!${NC}"
    echo ""
    echo -e "${BLUE}🚀 Quick Start:${NC}"
    echo "   ./run.sh                 # Super simple start"
    echo "   ./easy_start.sh          # Full control"
    echo "   ./easy_start.sh start    # Just start services"
    echo ""
    echo -e "${BLUE}🌐 Access Points:${NC}"
    echo "   • Website: http://localhost:3000"
    echo "   • API: http://localhost:8000"
    echo "   • Docs: http://localhost:8000/docs"
    echo ""
    echo -e "${BLUE}💡 Next Steps:${NC}"
    echo "   1. Run: ./run.sh"
    echo "   2. Open your browser to the URLs above"
    echo "   3. Start exploring the platform!"
    echo ""
}

# Run main installation
main "$@"