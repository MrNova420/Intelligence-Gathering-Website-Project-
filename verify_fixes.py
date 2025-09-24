#!/usr/bin/env python3
"""
Verification Script for Intelligence Gathering Platform Fixes
Tests all the fixes applied to address deployment issues
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

def test_requirements_lite():
    """Test that requirements-lite.txt exists and has SQLite-only deps"""
    req_file = Path("backend/requirements-lite.txt")
    if not req_file.exists():
        return False, "requirements-lite.txt not found"
    
    content = req_file.read_text()
    # Check that psycopg2-binary is NOT in the content (it should be excluded)
    if "psycopg2-binary==" in content:
        return False, "psycopg2-binary still present in lite requirements"
    
    if "fastapi" not in content or "uvicorn" not in content:
        return False, "Missing core dependencies in lite requirements"
    
    # Check that it mentions excluding PostgreSQL dependencies
    if "psycopg2-binary" not in content:
        return False, "Should mention psycopg2-binary exclusion in comments"
    
    return True, "requirements-lite.txt correctly configured"

def test_security_fallbacks():
    """Test that security module has proper fallbacks"""
    try:
        sys.path.insert(0, str(Path("backend").absolute()))
        from app.core.enhanced_security import Fernet, CRYPTOGRAPHY_AVAILABLE
        
        # If cryptography is not available, Fernet should be the mock version
        if not CRYPTOGRAPHY_AVAILABLE:
            # Test MockFernet has generate_key
            if not hasattr(Fernet, 'generate_key'):
                return False, "MockFernet missing generate_key method"
            
            # Test it works
            key = Fernet.generate_key()
            if not key:
                return False, "MockFernet.generate_key returns empty key"
        
        return True, "Security fallbacks working correctly"
    except Exception as e:
        return False, f"Security module error: {e}"

def test_database_setup():
    """Test database setup script works"""
    try:
        # Remove existing database
        db_file = Path("backend/intelligence_platform.db")
        if db_file.exists():
            db_file.unlink()
        
        # Run setup script
        result = subprocess.run([
            sys.executable, "backend/app/db/setup_standalone.py"
        ], capture_output=True, text=True, cwd=Path.cwd())
        
        if result.returncode != 0:
            return False, f"Database setup failed: {result.stderr}"
        
        if not db_file.exists():
            return False, "Database file not created"
        
        return True, "Database setup working correctly"
    except Exception as e:
        return False, f"Database setup error: {e}"

def test_imports():
    """Test that imports work correctly"""
    try:
        sys.path.insert(0, str(Path("backend").absolute()))
        
        # Test database import
        from app.db.database import Base, engine
        
        # Test models import  
        from app.db.models import User, UserRole
        
        return True, "All imports working correctly"
    except Exception as e:
        return False, f"Import error: {e}"

def test_script_graceful_handling():
    """Test that maintenance script handles missing Docker gracefully"""
    try:
        script_path = Path("scripts/enhanced_maintenance.sh")
        if not script_path.exists():
            return False, "enhanced_maintenance.sh not found"
        
        # Check for Docker availability checks
        content = script_path.read_text()
        if "command -v docker" not in content:
            return False, "Script doesn't check for Docker availability"
        
        if "systemctl" in content and "command -v systemctl" not in content:
            return False, "Script uses systemctl without availability check"
        
        return True, "Script handles missing Docker/systemctl gracefully"
    except Exception as e:
        return False, f"Script test error: {e}"

def main():
    """Run all verification tests"""
    print("🔍 Verifying Intelligence Gathering Platform Fixes")
    print("=" * 60)
    
    tests = [
        ("SQLite-only requirements", test_requirements_lite),
        ("Security fallbacks", test_security_fallbacks),
        ("Database setup", test_database_setup),
        ("Import fixes", test_imports),
        ("Script graceful handling", test_script_graceful_handling),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            success, message = test_func()
            if success:
                print(f"✅ {test_name}: {message}")
                passed += 1
            else:
                print(f"❌ {test_name}: {message}")
                failed += 1
        except Exception as e:
            print(f"❌ {test_name}: Exception - {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All fixes verified successfully!")
        return 0
    else:
        print("⚠️ Some issues remain")
        return 1

if __name__ == "__main__":
    sys.exit(main())