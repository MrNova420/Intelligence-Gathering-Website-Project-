#!/bin/bash
# 📊 Status Dashboard - Quick overview of platform status

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${PURPLE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║        📊 INTELLIGENCE GATHERING PLATFORM STATUS            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Helper functions
check_port() {
    if command -v nc >/dev/null 2>&1; then
        nc -z localhost $1 2>/dev/null
    elif command -v netstat >/dev/null 2>&1; then
        netstat -tuln 2>/dev/null | grep ":$1 " >/dev/null
    else
        curl -s "http://localhost:$1" >/dev/null 2>&1
    fi
}

status_icon() {
    if $1; then
        echo -e "${GREEN}🟢${NC}"
    else
        echo -e "${RED}🔴${NC}"
    fi
}

# Check services
echo -e "${CYAN}🔍 Service Status:${NC}"

# Backend check
if pgrep -f "python.*run_standalone.py" >/dev/null || check_port 8000; then
    BACKEND_STATUS=true
    echo -e "   $(status_icon true) Backend API Server (Port 8000)"
else
    BACKEND_STATUS=false
    echo -e "   $(status_icon false) Backend API Server (Port 8000)"
fi

# Frontend check
if pgrep -f "npm.*run.*dev" >/dev/null || check_port 3000; then
    FRONTEND_STATUS=true
    echo -e "   $(status_icon true) Frontend Website (Port 3000)"
else
    FRONTEND_STATUS=false
    echo -e "   $(status_icon false) Frontend Website (Port 3000)"
fi

# Database check
if [[ -f "backend/intelligence_platform.db" ]]; then
    DB_STATUS=true
    DB_SIZE=$(du -h backend/intelligence_platform.db 2>/dev/null | cut -f1)
    echo -e "   $(status_icon true) SQLite Database (${DB_SIZE:-Unknown size})"
else
    DB_STATUS=false
    echo -e "   $(status_icon false) SQLite Database (Not found)"
fi

# tmux session check
if command -v tmux >/dev/null 2>&1 && tmux has-session -t intel 2>/dev/null; then
    TMUX_STATUS=true
    echo -e "   $(status_icon true) tmux Session 'intel'"
else
    TMUX_STATUS=false
    echo -e "   $(status_icon false) tmux Session 'intel'"
fi

echo ""

# Access points
echo -e "${CYAN}🌐 Access Points:${NC}"
if $BACKEND_STATUS; then
    echo -e "   ${GREEN}✓${NC} Backend API: http://localhost:8000"
    echo -e "   ${GREEN}✓${NC} API Documentation: http://localhost:8000/docs"
else
    echo -e "   ${RED}✗${NC} Backend API: http://localhost:8000 (Not running)"
    echo -e "   ${RED}✗${NC} API Documentation: http://localhost:8000/docs (Not running)"
fi

if $FRONTEND_STATUS; then
    echo -e "   ${GREEN}✓${NC} Frontend Website: http://localhost:3000"
else
    echo -e "   ${RED}✗${NC} Frontend Website: http://localhost:3000 (Not running)"
fi

echo ""

# Overall status
if $BACKEND_STATUS && $FRONTEND_STATUS && $DB_STATUS; then
    echo -e "${GREEN}🎉 Platform Status: FULLY OPERATIONAL${NC}"
    echo ""
    echo -e "${BLUE}💡 Quick Actions:${NC}"
    echo "   • ./easy_start.sh restart   # Restart all services"
    echo "   • ./easy_start.sh stop      # Stop all services"
    echo "   • ./fix.sh                  # Fix any issues"
elif $BACKEND_STATUS && $DB_STATUS; then
    echo -e "${YELLOW}⚠️  Platform Status: BACKEND ONLY${NC}"
    echo ""
    echo -e "${BLUE}💡 To start frontend:${NC}"
    echo "   • ./easy_start.sh start     # Start all services"
elif $DB_STATUS; then
    echo -e "${RED}❌ Platform Status: SERVICES DOWN${NC}"
    echo ""
    echo -e "${BLUE}💡 To start services:${NC}"
    echo "   • ./run.sh                  # Simple start"
    echo "   • ./easy_start.sh start     # Advanced start"
else
    echo -e "${RED}❌ Platform Status: NOT SETUP${NC}"
    echo ""
    echo -e "${BLUE}💡 To setup and start:${NC}"
    echo "   • ./run.sh                  # Complete setup + start"
    echo "   • ./install.sh              # Just install"
fi

echo ""

# Resource usage (if available)
if command -v ps >/dev/null 2>&1; then
    echo -e "${CYAN}📈 Resource Usage:${NC}"
    
    # Backend process info
    if $BACKEND_STATUS; then
        BACKEND_PID=$(pgrep -f "python.*run_standalone.py" | head -1)
        if [[ -n "$BACKEND_PID" ]]; then
            BACKEND_MEM=$(ps -o pid,pmem,pcpu,etime,comm -p $BACKEND_PID 2>/dev/null | tail -1 | awk '{print $2"%"}')
            BACKEND_CPU=$(ps -o pid,pmem,pcpu,etime,comm -p $BACKEND_PID 2>/dev/null | tail -1 | awk '{print $3"%"}')
            echo -e "   ${GREEN}Backend:${NC} CPU: ${BACKEND_CPU}, Memory: ${BACKEND_MEM}"
        fi
    fi
    
    # Frontend process info
    if $FRONTEND_STATUS; then
        FRONTEND_PID=$(pgrep -f "npm.*run.*dev" | head -1)
        if [[ -n "$FRONTEND_PID" ]]; then
            FRONTEND_MEM=$(ps -o pid,pmem,pcpu,etime,comm -p $FRONTEND_PID 2>/dev/null | tail -1 | awk '{print $2"%"}')
            FRONTEND_CPU=$(ps -o pid,pmem,pcpu,etime,comm -p $FRONTEND_PID 2>/dev/null | tail -1 | awk '{print $3"%"}')
            echo -e "   ${GREEN}Frontend:${NC} CPU: ${FRONTEND_CPU}, Memory: ${FRONTEND_MEM}"
        fi
    fi
    
    echo ""
fi

# Show logs shortcut
echo -e "${BLUE}📋 View Logs:${NC}"
echo "   • tail -f backend.log       # Backend logs"
echo "   • tail -f frontend.log      # Frontend logs"
echo "   • tmux attach -t intel      # Live session"

echo ""