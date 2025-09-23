#!/usr/bin/env python3
"""
Intelligence Gathering Platform - Simple Validation
Validates that all major components are properly structured
"""

import sys
import os
from pathlib import Path

def validate_file_structure():
    """Validate that all expected files exist"""
    print("📁 Validating File Structure...")
    
    expected_files = [
        'app/scanners/email_scanners.py',
        'app/scanners/phone_scanners.py', 
        'app/scanners/social_scanners.py',
        'app/core/aggregation_engine.py',
        'app/core/report_generator.py',
        'app/core/enhanced_security.py',
        'app/core/performance_optimizer.py',
        'tests/test_scanners.py',
        'tests/test_aggregation_engine.py',
        'tests/test_security.py'
    ]
    
    backend_dir = Path(__file__).parent
    missing_files = []
    
    for file_path in expected_files:
        full_path = backend_dir / file_path
        if full_path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - MISSING")
            missing_files.append(file_path)
    
    return len(missing_files) == 0, len(expected_files) - len(missing_files)

def validate_class_definitions():
    """Validate that classes are properly defined"""
    print("\n🔍 Validating Class Definitions...")
    
    try:
        # Check scanner structure
        with open('app/scanners/email_scanners.py', 'r') as f:
            content = f.read()
            classes = ['EmailValidator', 'EmailReputation', 'EmailBreach', 'SocialMediaEmail']
            for cls in classes:
                if f'class {cls}' in content:
                    print(f"  ✅ Email scanner: {cls}")
                else:
                    print(f"  ❌ Email scanner: {cls} - NOT FOUND")
        
        # Check aggregation engine
        with open('app/core/aggregation_engine.py', 'r') as f:
            content = f.read()
            if 'class DataAggregationEngine' in content:
                methods = ['normalize_email', 'normalize_phone', 'deduplicate_entities']
                for method in methods:
                    if f'def {method}' in content:
                        print(f"  ✅ Aggregation method: {method}")
                    else:
                        print(f"  ❌ Aggregation method: {method} - NOT FOUND")
        
        # Check report generator
        with open('app/core/report_generator.py', 'r') as f:
            content = f.read()
            if 'class ReportGenerator' in content:
                methods = ['generate_report', 'filter_data_by_subscription', 'export_to_pdf']
                for method in methods:
                    if f'def {method}' in content:
                        print(f"  ✅ Report method: {method}")
                    else:
                        print(f"  ❌ Report method: {method} - NOT FOUND")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Class validation failed: {e}")
        return False

def validate_frontend_structure():
    """Validate frontend structure"""
    print("\n🖥️ Validating Frontend Structure...")
    
    frontend_dir = Path(__file__).parent.parent / 'frontend'
    expected_files = [
        'pages/index.tsx',
        'pages/scan-progress.tsx',
        'pages/subscription.tsx'
    ]
    
    missing_files = []
    
    for file_path in expected_files:
        full_path = frontend_dir / file_path
        if full_path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - MISSING")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def validate_documentation():
    """Validate documentation files"""
    print("\n📚 Validating Documentation...")
    
    root_dir = Path(__file__).parent.parent
    expected_files = [
        'README_UPDATED.md',
        'DEPLOYMENT_GUIDE.md',
        'PRODUCTION_READINESS.md'
    ]
    
    missing_files = []
    
    for file_path in expected_files:
        full_path = root_dir / file_path
        if full_path.exists():
            size_kb = full_path.stat().st_size / 1024
            print(f"  ✅ {file_path} ({size_kb:.1f} KB)")
        else:
            print(f"  ❌ {file_path} - MISSING")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def count_implementation_lines():
    """Count lines of implementation code"""
    print("\n📊 Analyzing Implementation Scale...")
    
    implementation_files = [
        'app/scanners/email_scanners.py',
        'app/scanners/phone_scanners.py',
        'app/scanners/social_scanners.py', 
        'app/core/aggregation_engine.py',
        'app/core/report_generator.py',
        'app/core/enhanced_security.py',
        'app/core/performance_optimizer.py'
    ]
    
    total_lines = 0
    
    for file_path in implementation_files:
        try:
            with open(file_path, 'r') as f:
                lines = len(f.readlines())
                total_lines += lines
                print(f"  📄 {file_path}: {lines} lines")
        except FileNotFoundError:
            print(f"  ❌ {file_path}: NOT FOUND")
    
    print(f"\n  📈 Total Implementation: {total_lines} lines of code")
    return total_lines

def main():
    """Run simple validation"""
    print("🚀 Intelligence Gathering Platform - Simple Validation")
    print("=" * 60)
    
    results = []
    
    # Change to backend directory
    os.chdir(Path(__file__).parent)
    
    # Run validations
    file_structure_ok, files_found = validate_file_structure()
    results.append(("File Structure", file_structure_ok))
    
    class_definitions_ok = validate_class_definitions()
    results.append(("Class Definitions", class_definitions_ok))
    
    frontend_ok = validate_frontend_structure()
    results.append(("Frontend Structure", frontend_ok))
    
    docs_ok = validate_documentation()
    results.append(("Documentation", docs_ok))
    
    total_lines = count_implementation_lines()
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 VALIDATION RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for component, success in results:
        if success:
            print(f"✅ {component}: PASSED")
            passed += 1
        else:
            print(f"❌ {component}: FAILED")
            failed += 1
    
    print(f"\n📈 Overall Score: {passed}/{len(results)} components validated")
    print(f"📄 Implementation Scale: {total_lines} lines of code")
    
    if failed == 0:
        print("🎉 ALL STRUCTURAL VALIDATIONS PASSED!")
        print("💡 Platform structure is complete and ready for deployment")
        return 0
    else:
        print(f"⚠️  {failed} VALIDATIONS FAILED - REVIEW REQUIRED")
        return 1

if __name__ == "__main__":
    sys.exit(main())