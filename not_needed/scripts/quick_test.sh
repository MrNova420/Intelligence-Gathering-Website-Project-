#!/bin/bash
# 🧪 Quick Test Script - Validate platform functionality
# Tests core functionality without full setup

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🧪 Intelligence Gathering Platform - Quick Test${NC}"
echo "=================================================="

info() { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
error() { echo -e "${RED}✗${NC} $1"; }
step() { echo -e "${BLUE}→${NC} $1"; }

# Test counters
PASSED=0
FAILED=0

# Test function
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    step "Testing: $test_name"
    
    if eval "$test_command" >/dev/null 2>&1; then
        info "$test_name: PASSED"
        ((PASSED++))
    else
        error "$test_name: FAILED"
        ((FAILED++))
    fi
}

# Core tests
echo ""
step "Running core functionality tests..."

# Test 1: Python availability
run_test "Python Installation" "command -v python"

# Test 2: Node.js availability (if frontend exists)
if [[ -d "frontend" ]]; then
    run_test "Node.js Installation" "command -v node"
else
    warn "Frontend directory not found - skipping Node.js test"
fi

# Test 3: Dependencies can be imported
run_test "Python Dependencies" "python -c 'import fastapi, uvicorn, sqlalchemy, pydantic'"

# Test 4: Database setup
run_test "Database Module" "python -c 'from backend.app.db.database import Base, engine'"

# Test 5: Security module
run_test "Security Module" "python -c 'from backend.app.core.enhanced_security import security_manager'"

# Test 6: Backend can start (import test)
run_test "Backend Import" "python -c 'import sys; sys.path.insert(0, \"backend\"); from app.main import app'"

# Test 7: Scripts are executable
run_test "Scripts Executable" "test -x easy_start.sh && test -x run.sh && test -x fix.sh"

# Test 8: Configuration files exist
run_test "Config Files" "test -f backend/requirements-lite.txt && test -f .env || test -f .env.example"

# Test 9: Database can be created
run_test "Database Creation" "cd backend && python app/db/setup_standalone.py"

# Test 10: Verification script works
run_test "Verification System" "python verify_fixes.py"

# Summary
echo ""
echo "=" * 50
if [[ $FAILED -eq 0 ]]; then
    echo -e "${GREEN}🎉 All tests passed! ($PASSED/$((PASSED + FAILED)))${NC}"
    echo ""
    echo -e "${BLUE}✅ Platform is ready to use!${NC}"
    echo ""
    echo "Quick start commands:"
    echo "  • ./run.sh           # Simple start"
    echo "  • ./easy_start.sh    # Advanced control"
    echo "  • ./status.sh        # Check status"
else
    echo -e "${RED}❌ Some tests failed! ($PASSED passed, $FAILED failed)${NC}"
    echo ""
    echo -e "${BLUE}🔧 Try fixing issues:${NC}"
    echo "  • ./fix.sh           # Auto-fix common issues"
    echo "  • ./install.sh       # Reinstall dependencies"
    echo ""
    exit 1
fi