#!/usr/bin/env python3
"""
Final Comprehensive Validation Suite
===================================
Ultimate validation for the Intelligence Gathering Platform
Checks all components, dependencies, and production readiness
"""

import os
import sys
import importlib
import traceback
from pathlib import Path
from typing import Dict, List, Any, Tuple
import json
import time
from datetime import datetime

class ComprehensiveValidator:
    """Final comprehensive platform validator"""
    
    def __init__(self):
        self.results = {}
        self.total_score = 0
        self.max_score = 0
        self.issues = []
        self.successes = []
        
    def log_success(self, component: str, message: str, points: int = 1):
        """Log successful validation"""
        self.successes.append(f"✅ {component}: {message}")
        self.total_score += points
        self.max_score += points
        
    def log_issue(self, component: str, message: str, points: int = 1):
        """Log validation issue"""
        self.issues.append(f"⚠️  {component}: {message}")
        self.max_score += points
        
    def validate_file_structure(self) -> bool:
        """Validate complete file structure"""
        print("🏗️  Validating File Structure...")
        
        required_files = [
            "backend/app/core/aggregation_engine.py",
            "backend/app/core/report_generator.py", 
            "backend/app/core/enhanced_security.py",
            "backend/app/core/performance_optimizer.py",
            "backend/app/core/advanced_analytics.py",
            "backend/app/core/ml_intelligence.py",
            "backend/app/scanners/email_scanners.py",
            "backend/app/scanners/phone_scanners.py",
            "backend/app/scanners/social_scanners.py",
            "backend/app/api/enhanced_endpoints.py",
            "backend/requirements.txt",
            "frontend/pages/index.tsx",
            "frontend/pages/scan-progress.tsx",
            "frontend/pages/subscription.tsx"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
                
        if missing_files:
            self.log_issue("File Structure", f"Missing files: {missing_files}")
            return False
        else:
            self.log_success("File Structure", f"All {len(required_files)} required files present", 2)
            return True
    
    def validate_dependencies(self) -> bool:
        """Validate all dependencies are properly installed"""
        print("📦 Validating Dependencies...")
        
        required_packages = [
            "fastapi", "uvicorn", "sqlalchemy", "redis", "aiohttp",
            "dnspython", "phonenumbers", "pyotp", "qrcode", "reportlab",
            "email_validator", "bcrypt", "cryptography", "requests"
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                importlib.import_module(package.replace("-", "_"))
            except ImportError:
                missing_packages.append(package)
                
        if missing_packages:
            self.log_issue("Dependencies", f"Missing packages: {missing_packages}")
            return False
        else:
            self.log_success("Dependencies", f"All {len(required_packages)} packages available", 2)
            return True
    
    def validate_scanner_implementations(self) -> bool:
        """Validate scanner implementations"""
        print("🔍 Validating Scanner Implementations...")
        
        try:
            sys.path.append("backend")
            from app.scanners.email_scanners import EmailValidator, EmailReputation
            from app.scanners.phone_scanners import PhoneValidator, PhoneLocation
            from app.scanners.social_scanners import TwitterScanner, LinkedInScanner
            
            # Test instantiation
            scanners = [
                EmailValidator(), EmailReputation(),
                PhoneValidator(), PhoneLocation(), 
                TwitterScanner(), LinkedInScanner()
            ]
            
            self.log_success("Scanner Implementations", f"All {len(scanners)} scanner classes instantiated", 3)
            return True
            
        except Exception as e:
            self.log_issue("Scanner Implementations", f"Failed to load scanners: {str(e)}")
            return False
    
    def validate_core_engines(self) -> bool:
        """Validate core processing engines"""
        print("🧠 Validating Core Engines...")
        
        try:
            sys.path.append("backend")
            from app.core.aggregation_engine import AdvancedAggregationEngine
            from app.core.report_generator import EnhancedReportGenerator
            from app.core.enhanced_security import SecurityManager
            from app.core.performance_optimizer import RedisCache, PerformanceMonitor
            from app.core.advanced_analytics import AdvancedAnalyticsEngine
            from app.core.ml_intelligence import MLIntelligenceEngine
            
            # Test core functionality
            engines = {
                'aggregation': AdvancedAggregationEngine(),
                'security': SecurityManager(),
                'analytics': AdvancedAnalyticsEngine(),
                'ml': MLIntelligenceEngine()
            }
            
            self.log_success("Core Engines", f"All {len(engines)} engines initialized", 3)
            return True
            
        except Exception as e:
            self.log_issue("Core Engines", f"Failed to initialize engines: {str(e)}")
            return False
    
    def validate_api_endpoints(self) -> bool:
        """Validate API endpoint implementations"""
        print("🌐 Validating API Endpoints...")
        
        try:
            sys.path.append("backend")
            from app.api.enhanced_endpoints import router
            
            # Check router has endpoints
            if hasattr(router, 'routes') and len(router.routes) > 0:
                self.log_success("API Endpoints", f"{len(router.routes)} API routes registered", 2)
                return True
            else:
                self.log_issue("API Endpoints", "No API routes found")
                return False
                
        except Exception as e:
            self.log_issue("API Endpoints", f"Failed to load API endpoints: {str(e)}")
            return False
    
    def validate_frontend_components(self) -> bool:
        """Validate frontend components"""
        print("🖥️  Validating Frontend Components...")
        
        frontend_files = [
            "frontend/pages/index.tsx",
            "frontend/pages/scan-progress.tsx", 
            "frontend/pages/subscription.tsx"
        ]
        
        valid_components = 0
        for file_path in frontend_files:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    content = f.read()
                    if 'export default' in content and ('function' in content or 'const' in content):
                        valid_components += 1
                        
        if valid_components == len(frontend_files):
            self.log_success("Frontend Components", f"All {valid_components} React components valid", 2)
            return True
        else:
            self.log_issue("Frontend Components", f"Only {valid_components}/{len(frontend_files)} components valid")
            return False
    
    def validate_documentation(self) -> bool:
        """Validate documentation completeness"""
        print("📚 Validating Documentation...")
        
        doc_files = [
            "README.md", "DEPLOYMENT_GUIDE.md", 
            "PRODUCTION_READINESS.md", "COMPREHENSIVE_ENHANCEMENT_SUMMARY.md"
        ]
        
        valid_docs = 0
        total_chars = 0
        for doc_file in doc_files:
            if os.path.exists(doc_file):
                with open(doc_file, 'r') as f:
                    content = f.read()
                    if len(content) > 1000:  # Substantial documentation
                        valid_docs += 1
                        total_chars += len(content)
        
        if valid_docs >= 3:
            self.log_success("Documentation", f"{valid_docs} comprehensive docs ({total_chars:,} chars)", 2)
            return True
        else:
            self.log_issue("Documentation", f"Only {valid_docs} substantial documentation files")
            return False
    
    def calculate_code_metrics(self) -> Dict[str, Any]:
        """Calculate comprehensive code metrics"""
        print("📊 Calculating Code Metrics...")
        
        metrics = {
            'total_files': 0,
            'total_lines': 0,
            'python_files': 0,
            'python_lines': 0,
            'frontend_files': 0,
            'frontend_lines': 0,
            'test_files': 0,
            'test_lines': 0
        }
        
        for root, dirs, files in os.walk('.'):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = len(f.readlines())
                        metrics['total_files'] += 1
                        metrics['total_lines'] += lines
                        
                        if file.endswith('.py'):
                            metrics['python_files'] += 1
                            metrics['python_lines'] += lines
                            if 'test' in file.lower():
                                metrics['test_files'] += 1  
                                metrics['test_lines'] += lines
                        elif file.endswith(('.tsx', '.ts', '.jsx', '.js')):
                            metrics['frontend_files'] += 1
                            metrics['frontend_lines'] += lines
                except:
                    pass
                    
        return metrics
    
    def run_functional_tests(self) -> bool:
        """Run basic functional tests"""
        print("🧪 Running Functional Tests...")
        
        try:
            sys.path.append("backend")
            
            # Test email normalization
            from app.core.aggregation_engine import AdvancedAggregationEngine
            engine = AdvancedAggregationEngine()
            normalized = engine.normalize_email("Test.User+tag@Gmail.com")
            if normalized and normalized.get('normalized') == 'testuser@gmail.com':
                self.log_success("Functional Tests", "Email normalization working", 1)
            else:
                self.log_issue("Functional Tests", "Email normalization failed")
                
            # Test security functions
            from app.core.enhanced_security import SecurityManager
            security = SecurityManager()
            strength = security.calculate_password_strength("weak")
            if strength and 'score' in strength:
                self.log_success("Functional Tests", "Password strength calculation working", 1)
            else:
                self.log_issue("Functional Tests", "Password strength calculation failed")
                
            return True
            
        except Exception as e:
            self.log_issue("Functional Tests", f"Tests failed: {str(e)}")
            return False
    
    def generate_final_report(self) -> Dict[str, Any]:
        """Generate comprehensive final report"""
        
        # Calculate metrics
        metrics = self.calculate_code_metrics()
        
        # Calculate final score
        percentage = (self.total_score / self.max_score * 100) if self.max_score > 0 else 0
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'overall_score': f"{self.total_score}/{self.max_score}",
            'percentage': f"{percentage:.1f}%",
            'status': 'PRODUCTION READY' if percentage >= 85 else 'NEEDS ATTENTION',
            'code_metrics': metrics,
            'successes': self.successes,
            'issues': self.issues,
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        if self.issues:
            recommendations.append("Address all identified issues before production deployment")
        
        percentage = (self.total_score / self.max_score * 100) if self.max_score > 0 else 0
        
        if percentage >= 95:
            recommendations.append("Platform is fully ready for production deployment")
        elif percentage >= 85:
            recommendations.append("Platform is production ready with minor optimizations needed")
        else:
            recommendations.append("Platform needs additional work before production deployment")
            
        return recommendations
    
    def run_complete_validation(self) -> Dict[str, Any]:
        """Run complete validation suite"""
        print("=" * 60)
        print("🚀 FINAL COMPREHENSIVE VALIDATION SUITE")
        print("=" * 60)
        print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        start_time = time.time()
        
        # Run all validations
        validations = [
            self.validate_file_structure,
            self.validate_dependencies,
            self.validate_scanner_implementations,
            self.validate_core_engines,
            self.validate_api_endpoints,
            self.validate_frontend_components,
            self.validate_documentation,
            self.run_functional_tests
        ]
        
        for validation in validations:
            try:
                validation()
            except Exception as e:
                self.log_issue("Validation Error", f"{validation.__name__}: {str(e)}")
            print()
        
        # Generate final report
        report = self.generate_final_report()
        duration = time.time() - start_time
        
        print("=" * 60)
        print("📋 FINAL VALIDATION REPORT")
        print("=" * 60)
        print(f"🎯 Overall Score: {report['overall_score']} ({report['percentage']})")
        print(f"📊 Status: {report['status']}")
        print(f"⏱️  Duration: {duration:.2f} seconds")
        print()
        
        print("✅ SUCCESSES:")
        for success in self.successes:
            print(f"  {success}")
        print()
        
        if self.issues:
            print("⚠️  ISSUES:")
            for issue in self.issues:
                print(f"  {issue}")
            print()
        
        print("📈 CODE METRICS:")
        metrics = report['code_metrics']
        print(f"  Total Files: {metrics['total_files']:,}")
        print(f"  Total Lines: {metrics['total_lines']:,}")
        print(f"  Python Files: {metrics['python_files']} ({metrics['python_lines']:,} lines)")
        print(f"  Frontend Files: {metrics['frontend_files']} ({metrics['frontend_lines']:,} lines)")
        print(f"  Test Files: {metrics['test_files']} ({metrics['test_lines']:,} lines)")
        print()
        
        print("💡 RECOMMENDATIONS:")
        for rec in report['recommendations']:
            print(f"  • {rec}")
        print()
        
        if report['status'] == 'PRODUCTION READY':
            print("🎉 PLATFORM VALIDATION COMPLETE - READY FOR DEPLOYMENT!")
        else:
            print("🔧 PLATFORM NEEDS ADDITIONAL WORK")
            
        print("=" * 60)
        
        return report

def main():
    """Main validation execution"""
    validator = ComprehensiveValidator()
    report = validator.run_complete_validation()
    
    # Save report
    with open('final_validation_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Full report saved to: final_validation_report.json")
    
    # Exit with appropriate code
    if report['status'] == 'PRODUCTION READY':
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()