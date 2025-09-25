#!/bin/bash
# 🔧 Fix Common Issues - Automatic Problem Solver
# Run this if anything goes wrong

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔧 Intelligence Gathering Platform - Problem Solver${NC}"
echo "=================================================="

info() { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
error() { echo -e "${RED}✗${NC} $1"; }
step() { echo -e "${BLUE}→${NC} $1"; }

# Fix 1: Clean up processes
fix_processes() {
    step "Cleaning up stuck processes..."
    
    # Kill any stuck Python processes
    pkill -f "python.*run_standalone.py" 2>/dev/null && info "Killed stuck backend processes" || warn "No stuck backend processes found"
    
    # Kill any stuck Node processes
    pkill -f "npm.*run.*dev" 2>/dev/null && info "Killed stuck frontend processes" || warn "No stuck frontend processes found"
    
    # Kill tmux sessions
    tmux kill-session -t intel 2>/dev/null && info "Killed tmux session" || warn "No tmux session found"
    tmux kill-session -t intelligence_platform 2>/dev/null && info "Killed old tmux session" || true
    
    # Clean up PID files
    rm -f backend.pid frontend.pid
    
    info "Process cleanup completed"
}

# Fix 2: Reinstall dependencies
fix_dependencies() {
    step "Fixing Python dependencies..."
    
    # Try different installation methods
    if pip install -r backend/requirements-lite.txt --user --force-reinstall --break-system-packages 2>/dev/null; then
        info "Dependencies reinstalled successfully"
    elif pip install -r backend/requirements-lite.txt --user --force-reinstall 2>/dev/null; then
        info "Dependencies reinstalled successfully"
    else
        warn "Trying individual package installation..."
        pip install --user --force-reinstall fastapi uvicorn sqlalchemy pydantic dnspython phonenumbers python-dotenv requests passlib[bcrypt] --break-system-packages 2>/dev/null || \
        pip install --user --force-reinstall fastapi uvicorn sqlalchemy pydantic dnspython phonenumbers python-dotenv requests passlib[bcrypt]
        info "Core packages reinstalled"
    fi
}

# Fix 3: Reset database
fix_database() {
    step "Resetting database..."
    
    # Remove old database
    rm -f backend/intelligence_platform.db
    rm -f intelligence_platform.db
    
    # Recreate database
    cd backend
    if python app/db/setup_standalone.py; then
        info "Database reset successfully"
    else
        error "Database setup failed - check if Python dependencies are installed"
    fi
    cd ..
}

# Fix 4: Reset environment
fix_environment() {
    step "Resetting environment configuration..."
    
    # Backup existing .env
    if [[ -f ".env" ]]; then
        cp .env .env.backup
        warn "Backed up existing .env to .env.backup"
    fi
    
    # Create fresh .env
    cat > .env << 'EOF'
# Intelligence Gathering Platform Configuration
DATABASE_URL=sqlite:///./intelligence_platform.db
SECRET_KEY=fix-script-generated-key
DEBUG=true
ENVIRONMENT=development
USE_REDIS_FALLBACK=true

# Scanner API Keys (optional)
CLEARBIT_API_KEY=
HUNTER_API_KEY=
STRIPE_SECRET_KEY=
EOF
    
    info "Environment configuration reset"
}

# Fix 5: Node.js issues
fix_nodejs() {
    if [[ -d "frontend" ]]; then
        step "Fixing Node.js dependencies..."
        
        cd frontend
        
        # Clear npm cache
        npm cache clean --force 2>/dev/null || true
        
        # Remove node_modules
        rm -rf node_modules package-lock.json
        
        # Reinstall
        npm install --silent || npm install
        
        cd ..
        info "Node.js dependencies fixed"
    fi
}

# Fix 6: Permissions
fix_permissions() {
    step "Fixing file permissions..."
    
    # Make scripts executable
    chmod +x *.sh 2>/dev/null || true
    chmod +x scripts/*.sh 2>/dev/null || true
    
    # Fix backend permissions
    find backend -name "*.py" -exec chmod +r {} \; 2>/dev/null || true
    
    info "Permissions fixed"
}

# Show help
show_help() {
    echo -e "${BLUE}Available fixes:${NC}"
    echo "  all         Fix everything (recommended)"
    echo "  processes   Clean up stuck processes"
    echo "  deps        Reinstall Python dependencies"
    echo "  database    Reset database"
    echo "  env         Reset environment configuration"
    echo "  nodejs      Fix Node.js dependencies"
    echo "  perms       Fix file permissions"
    echo ""
    echo "Usage: ./fix.sh [option]"
    echo "Example: ./fix.sh all"
}

# Main logic
case "${1:-all}" in
    "all")
        echo "🔧 Running all fixes..."
        fix_processes
        fix_permissions
        fix_dependencies
        fix_environment
        fix_database
        fix_nodejs
        echo ""
        echo -e "${GREEN}🎉 All fixes applied!${NC}"
        echo ""
        echo "Try running: ./run.sh"
        ;;
    "processes")
        fix_processes
        ;;
    "deps")
        fix_dependencies
        ;;
    "database")
        fix_database
        ;;
    "env")
        fix_environment
        ;;
    "nodejs")
        fix_nodejs
        ;;
    "perms")
        fix_permissions
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        error "Unknown fix option: $1"
        show_help
        exit 1
        ;;
esac