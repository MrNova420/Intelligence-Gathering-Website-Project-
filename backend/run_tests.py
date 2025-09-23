#!/usr/bin/env python3
"""
Test runner for the Intelligence Gathering Platform
Runs all test suites and generates coverage reports.
"""

import sys
import subprocess
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and report results"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ PASSED")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ FAILED")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def main():
    """Run all tests"""
    print("🚀 Intelligence Gathering Platform - Test Suite")
    print("=" * 60)
    
    # Change to backend directory
    os.chdir(Path(__file__).parent)
    
    # Test commands
    test_commands = [
        ("python -m pytest tests/test_scanners.py -v", "Scanner Module Tests"),
        ("python -m pytest tests/test_aggregation_engine.py -v", "Aggregation Engine Tests"),
        ("python -m pytest tests/test_security.py -v", "Security Module Tests"),
        ("python -m pytest tests/ -v --tb=short", "All Tests Summary"),
    ]
    
    passed_tests = 0
    total_tests = len(test_commands)
    
    for command, description in test_commands:
        if run_command(command, description):
            passed_tests += 1
    
    # Results summary
    print(f"\n{'='*60}")
    print(f"📊 TEST RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Passed: {passed_tests}/{total_tests}")
    print(f"❌ Failed: {total_tests - passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED!")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED!")
        return 1

if __name__ == "__main__":
    sys.exit(main())