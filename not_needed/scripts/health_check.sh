#!/bin/bash
# 🏥 Comprehensive Health Check - Deep platform analysis
# Checks everything and provides detailed diagnostics

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${PURPLE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  🏥 INTELLIGENCE GATHERING PLATFORM - HEALTH CHECK            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

info() { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
error() { echo -e "${RED}✗${NC} $1"; }
step() { echo -e "${BLUE}→${NC} $1"; }

# Health scores
HEALTH_SCORE=0
MAX_SCORE=0

# Health check function
health_check() {
    local check_name="$1"
    local check_command="$2"
    local points="${3:-1}"
    
    ((MAX_SCORE += points))
    
    if eval "$check_command" >/dev/null 2>&1; then
        info "$check_name"
        ((HEALTH_SCORE += points))
        return 0
    else
        error "$check_name"
        return 1
    fi
}

# System Environment Checks
echo -e "${CYAN}🔧 System Environment${NC}"
health_check "Python 3.8+ Available" "python --version | grep -E 'Python 3\.(8|9|10|11|12)'" 2
health_check "pip Package Manager" "command -v pip" 1
health_check "Git Version Control" "command -v git" 1

if [[ -d "frontend" ]]; then
    health_check "Node.js Runtime" "command -v node" 2
    health_check "npm Package Manager" "command -v npm" 1
fi

# Optional but recommended
if command -v tmux >/dev/null 2>&1; then
    info "tmux Session Manager (recommended)"
    ((HEALTH_SCORE++))
else
    warn "tmux Session Manager (install for better experience)"
fi
((MAX_SCORE++))

echo ""

# Python Dependencies
echo -e "${CYAN}📦 Python Dependencies${NC}"
health_check "FastAPI Framework" "python -c 'import fastapi'" 3
health_check "Uvicorn Server" "python -c 'import uvicorn'" 2
health_check "SQLAlchemy ORM" "python -c 'import sqlalchemy'" 2
health_check "Pydantic Validation" "python -c 'import pydantic'" 2
health_check "DNS Resolution" "python -c 'import dns'" 1
health_check "Phone Numbers" "python -c 'import phonenumbers'" 1
health_check "Environment Variables" "python -c 'import dotenv'" 1
health_check "HTTP Requests" "python -c 'import requests'" 1
health_check "Password Hashing" "python -c 'import passlib'" 2

echo ""

# Platform Components
echo -e "${CYAN}🏗️ Platform Components${NC}"
health_check "Backend Directory" "test -d backend" 2
health_check "Frontend Directory" "test -d frontend" 2
health_check "Database Module" "test -f backend/app/db/database.py" 2
health_check "Security Module" "test -f backend/app/core/enhanced_security.py" 2
health_check "Main Application" "test -f backend/app/main.py" 3
health_check "Standalone Runner" "test -f backend/run_standalone.py" 2

echo ""

# Configuration Files
echo -e "${CYAN}⚙️ Configuration${NC}"
if [[ -f ".env" ]]; then
    info "Environment Configuration (.env)"
    ((HEALTH_SCORE++))
elif [[ -f ".env.example" ]]; then
    warn "Environment Template (.env.example) - need to create .env"
else
    error "No environment configuration found"
fi
((MAX_SCORE++))

health_check "SQLite Requirements" "test -f backend/requirements-lite.txt" 2
health_check "Frontend Package Config" "test -f frontend/package.json || echo 'no frontend'" 1

echo ""

# Database Status
echo -e "${CYAN}🗄️ Database Status${NC}"
if [[ -f "backend/intelligence_platform.db" ]]; then
    db_size=$(du -h backend/intelligence_platform.db 2>/dev/null | cut -f1)
    info "SQLite Database (${db_size:-Unknown size})"
    ((HEALTH_SCORE++))
    
    # Test database connectivity
    if python -c "
import sys
sys.path.insert(0, 'backend')
from app.db.database import engine
try:
    with engine.connect() as conn:
        conn.execute('SELECT 1')
    print('Database connection successful')
except Exception as e:
    print(f'Database connection failed: {e}')
    sys.exit(1)
    " >/dev/null 2>&1; then
        info "Database Connectivity"
        ((HEALTH_SCORE++))
    else
        error "Database Connectivity"
    fi
else
    error "SQLite Database (not found)"
fi
((MAX_SCORE += 2))

echo ""

# Management Scripts
echo -e "${CYAN}🎮 Management Scripts${NC}"
health_check "Easy Start Script" "test -x easy_start.sh" 2
health_check "Quick Run Script" "test -x run.sh" 2
health_check "Fix Problems Script" "test -x fix.sh" 1
health_check "Status Monitor" "test -x status.sh" 1
health_check "Universal Installer" "test -x install.sh" 1

echo ""

# Active Services
echo -e "${CYAN}🚀 Active Services${NC}"
if pgrep -f "python.*run_standalone.py" >/dev/null; then
    info "Backend API Server (Running)"
    ((HEALTH_SCORE++))
else
    warn "Backend API Server (Not running)"
fi

if pgrep -f "npm.*run.*dev" >/dev/null; then
    info "Frontend Website (Running)"
    ((HEALTH_SCORE++))
else
    warn "Frontend Website (Not running)"
fi

if command -v tmux >/dev/null 2>&1 && tmux has-session -t intel 2>/dev/null; then
    info "tmux Session Manager (Active)"
    ((HEALTH_SCORE++))
else
    warn "tmux Session Manager (Not active)"
fi
((MAX_SCORE += 3))

echo ""

# Network Connectivity (if services running)
if pgrep -f "python.*run_standalone.py" >/dev/null; then
    echo -e "${CYAN}🌐 Network Connectivity${NC}"
    if curl -s http://localhost:8000/health >/dev/null 2>&1; then
        info "Backend API Responsive"
        ((HEALTH_SCORE++))
    else
        warn "Backend API Not Responsive"
    fi
    ((MAX_SCORE++))
    
    if curl -s http://localhost:3000 >/dev/null 2>&1; then
        info "Frontend Website Responsive"
        ((HEALTH_SCORE++))
    else
        warn "Frontend Website Not Responsive"
    fi
    ((MAX_SCORE++))
fi

echo ""

# Calculate health percentage
HEALTH_PERCENTAGE=$((HEALTH_SCORE * 100 / MAX_SCORE))

# Health summary
echo "=" * 65
echo -e "${BLUE}📊 Health Summary${NC}"
echo "Score: $HEALTH_SCORE/$MAX_SCORE ($HEALTH_PERCENTAGE%)"

if [[ $HEALTH_PERCENTAGE -ge 90 ]]; then
    echo -e "${GREEN}🎉 Excellent Health - Platform fully operational!${NC}"
elif [[ $HEALTH_PERCENTAGE -ge 70 ]]; then
    echo -e "${YELLOW}⚠️ Good Health - Minor issues detected${NC}"
elif [[ $HEALTH_PERCENTAGE -ge 50 ]]; then
    echo -e "${YELLOW}⚠️ Fair Health - Some components need attention${NC}"
else
    echo -e "${RED}❌ Poor Health - Significant issues detected${NC}"
fi

echo ""
echo -e "${BLUE}💡 Recommendations:${NC}"

if [[ $HEALTH_PERCENTAGE -lt 90 ]]; then
    echo "• Run: ./fix.sh          # Fix common issues"
    echo "• Run: ./install.sh      # Reinstall dependencies"
fi

if [[ ! -f ".env" ]]; then
    echo "• Create .env file from .env.example"
fi

if ! pgrep -f "python.*run_standalone.py" >/dev/null; then
    echo "• Start services: ./run.sh"
fi

if [[ $HEALTH_PERCENTAGE -ge 70 ]]; then
    echo "• Platform ready for use!"
fi

echo ""