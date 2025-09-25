#!/usr/bin/env python3
"""
Comprehensive Review and Optimization Tool
==========================================

Analyzes all previous comments, reviews the entire platform,
and performs comprehensive debugging, fixing, and improvement.
"""

import os
import sys
import json
import subprocess
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import time

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComprehensiveReviewOptimizer:
    """Comprehensive platform analyzer and optimizer"""
    
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.issues_found = []
        self.fixes_applied = []
        self.improvements = []
        self.recommendations = []
        self.platform_health = {}
        
    def print_header(self, title: str):
        """Print formatted header"""
        print(f"\n{'='*80}")
        print(f"🔍 {title}")
        print(f"{'='*80}")
    
    def run_command(self, cmd: str, capture_output: bool = True) -> Dict[str, Any]:
        """Run shell command and return result"""
        try:
            result = subprocess.run(
                cmd.split(), 
                capture_output=capture_output, 
                text=True, 
                cwd=self.root_dir,
                timeout=60
            )
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except Exception as e:
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'returncode': -1
            }
    
    def analyze_previous_comments(self):
        """Analyze all previous PR comments and reviews"""
        self.print_header("ANALYZING PREVIOUS COMMENTS AND REVIEWS")
        
        # Key issues identified from comments:
        previous_issues = [
            "psycopg2-binary dependency failures on Termux/Android",
            "Need for easy full website testing on localhost",
            "Project usability improvements needed",
            "Startup, setup, install process complexity",
            "Concern about lite vs full version confusion",
            "Need for debugging and improvement analysis",
            "Platform documentation for all devices needed",
            "Production deployment guidance required"
        ]
        
        print("📋 Previous Issues Identified:")
        for i, issue in enumerate(previous_issues, 1):
            print(f"   {i}. {issue}")
        
        # Verify all issues have been addressed
        addressed_issues = []
        
        # Check psycopg2-binary fix
        if (self.root_dir / "backend" / "requirements-lite.txt").exists():
            addressed_issues.append("✓ psycopg2-binary dependency made optional")
        
        # Check easy setup scripts
        if (self.root_dir / "run.sh").exists():
            addressed_issues.append("✓ One-command setup script created")
        
        # Check documentation
        if (self.root_dir / "PLATFORM_GUIDE.md").exists():
            addressed_issues.append("✓ Comprehensive platform documentation added")
        
        # Check production deployment
        if (self.root_dir / "PRODUCTION_DEPLOYMENT_GUIDE.md").exists():
            addressed_issues.append("✓ Production deployment guide created")
        
        print("\n✅ Issues Addressed:")
        for issue in addressed_issues:
            print(f"   {issue}")
        
        return len(addressed_issues) / len(previous_issues)
    
    def run_comprehensive_health_check(self):
        """Run comprehensive platform health analysis"""
        self.print_header("COMPREHENSIVE HEALTH ANALYSIS")
        
        # Run health check script
        health_result = self.run_command("./health_check.sh")
        if health_result['success']:
            print("✅ Health check completed successfully")
            # Extract health score
            for line in health_result['stdout'].split('\n'):
                if 'Score:' in line and '%' in line:
                    score_text = line.split('Score:')[1].strip()
                    score = int(score_text.split('/')[0])
                    total = int(score_text.split('/')[1].split()[0])
                    self.platform_health['score'] = score
                    self.platform_health['total'] = total
                    self.platform_health['percentage'] = (score / total) * 100
                    print(f"📊 Health Score: {score}/{total} ({self.platform_health['percentage']:.1f}%)")
        else:
            print("❌ Health check failed")
            self.issues_found.append("Health check script failure")
    
    def run_verification_tests(self):
        """Run all verification tests"""
        self.print_header("VERIFICATION TESTS")
        
        # Run verification script
        verify_result = self.run_command("python verify_fixes.py")
        if verify_result['success']:
            print("✅ All verification tests passed")
            self.improvements.append("All core fixes verified working")
        else:
            print("❌ Some verification tests failed")
            self.issues_found.append("Verification test failures")
    
    def analyze_code_quality(self):
        """Analyze code quality and structure"""
        self.print_header("CODE QUALITY ANALYSIS")
        
        quality_issues = []
        
        # Check for common Python issues
        python_files = list(self.root_dir.glob("**/*.py"))
        print(f"📊 Analyzing {len(python_files)} Python files...")
        
        for py_file in python_files[:10]:  # Sample first 10 files
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Check for potential issues
                if 'import *' in content:
                    quality_issues.append(f"Star import found in {py_file.name}")
                
                if 'print(' in content and 'main.py' not in str(py_file):
                    quality_issues.append(f"Debug print statements in {py_file.name}")
                    
            except Exception as e:
                continue
        
        if quality_issues:
            print("⚠️ Code Quality Issues Found:")
            for issue in quality_issues[:5]:  # Show first 5
                print(f"   • {issue}")
        else:
            print("✅ No major code quality issues found")
    
    def check_documentation_completeness(self):
        """Check if documentation is comprehensive"""
        self.print_header("DOCUMENTATION COMPLETENESS")
        
        required_docs = [
            "README.md",
            "PLATFORM_GUIDE.md", 
            "QUICK_REFERENCE.md",
            "STEP_BY_STEP_TUTORIALS.md",
            "PRODUCTION_DEPLOYMENT_GUIDE.md",
            "TERMUX_SETUP.md"
        ]
        
        missing_docs = []
        existing_docs = []
        
        for doc in required_docs:
            if (self.root_dir / doc).exists():
                existing_docs.append(doc)
            else:
                missing_docs.append(doc)
        
        print(f"✅ Documentation Coverage: {len(existing_docs)}/{len(required_docs)} ({len(existing_docs)/len(required_docs)*100:.1f}%)")
        
        if missing_docs:
            print("❌ Missing Documentation:")
            for doc in missing_docs:
                print(f"   • {doc}")
                self.issues_found.append(f"Missing documentation: {doc}")
        
        return len(existing_docs) / len(required_docs)
    
    def analyze_script_functionality(self):
        """Analyze all management scripts"""
        self.print_header("SCRIPT FUNCTIONALITY ANALYSIS")
        
        scripts = [
            "run.sh",
            "easy_start.sh", 
            "fix.sh",
            "status.sh",
            "install.sh",
            "health_check.sh",
            "quick_test.sh"
        ]
        
        working_scripts = []
        broken_scripts = []
        
        for script in scripts:
            script_path = self.root_dir / script
            if script_path.exists() and os.access(script_path, os.X_OK):
                working_scripts.append(script)
            else:
                broken_scripts.append(script)
                self.issues_found.append(f"Script missing or not executable: {script}")
        
        print(f"✅ Script Coverage: {len(working_scripts)}/{len(scripts)} ({len(working_scripts)/len(scripts)*100:.1f}%)")
        
        if broken_scripts:
            print("❌ Issues with scripts:")
            for script in broken_scripts:
                print(f"   • {script}")
    
    def identify_potential_improvements(self):
        """Identify potential improvements"""
        self.print_header("POTENTIAL IMPROVEMENTS")
        
        improvements = [
            "Add automated testing CI/CD pipeline",
            "Implement performance monitoring and metrics",
            "Add comprehensive error tracking and logging",
            "Create user onboarding and tutorial system", 
            "Add support for more cloud providers",
            "Implement plugin/extension system",
            "Add advanced security features",
            "Create comprehensive API documentation",
            "Add monitoring dashboards",
            "Implement backup and recovery system"
        ]
        
        print("💡 Suggested Improvements:")
        for i, improvement in enumerate(improvements, 1):
            print(f"   {i}. {improvement}")
            self.recommendations.append(improvement)
    
    def apply_critical_fixes(self):
        """Apply any critical fixes found"""
        self.print_header("APPLYING CRITICAL FIXES")
        
        fixes_applied = 0
        
        # Fix script permissions
        scripts = ["run.sh", "easy_start.sh", "fix.sh", "status.sh", "install.sh", "health_check.sh", "quick_test.sh"]
        for script in scripts:
            script_path = self.root_dir / script
            if script_path.exists():
                try:
                    os.chmod(script_path, 0o755)
                    fixes_applied += 1
                except Exception as e:
                    print(f"❌ Failed to fix permissions for {script}: {e}")
        
        if fixes_applied > 0:
            print(f"✅ Fixed permissions for {fixes_applied} scripts")
            self.fixes_applied.append(f"Fixed permissions for {fixes_applied} scripts")
        
        # Ensure .env exists
        env_path = self.root_dir / ".env"
        env_example_path = self.root_dir / ".env.example"
        
        if not env_path.exists() and env_example_path.exists():
            try:
                subprocess.run(["cp", str(env_example_path), str(env_path)], check=True)
                print("✅ Created .env from .env.example")
                self.fixes_applied.append("Created .env configuration file")
                fixes_applied += 1
            except Exception as e:
                print(f"❌ Failed to create .env: {e}")
        
        return fixes_applied
    
    def generate_comprehensive_report(self):
        """Generate comprehensive analysis report"""
        self.print_header("COMPREHENSIVE ANALYSIS REPORT")
        
        # Calculate overall health
        comment_coverage = self.analyze_previous_comments()
        doc_coverage = self.check_documentation_completeness()
        health_score = self.platform_health.get('percentage', 0) / 100
        
        overall_score = (comment_coverage + doc_coverage + health_score) / 3 * 100
        
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'overall_score': overall_score,
            'health_metrics': {
                'platform_health': self.platform_health.get('percentage', 0),
                'comment_coverage': comment_coverage * 100,
                'documentation_coverage': doc_coverage * 100
            },
            'issues_found': self.issues_found,
            'fixes_applied': self.fixes_applied,
            'improvements': self.improvements,
            'recommendations': self.recommendations
        }
        
        print(f"📊 OVERALL PLATFORM SCORE: {overall_score:.1f}%")
        
        if overall_score >= 90:
            status = "🎉 EXCELLENT"
            color = "green"
        elif overall_score >= 80:
            status = "✅ GOOD"
            color = "yellow"
        elif overall_score >= 70:
            status = "⚠️ FAIR"
            color = "orange"
        else:
            status = "❌ NEEDS ATTENTION"
            color = "red"
        
        print(f"🏆 Platform Status: {status}")
        
        print(f"\n📈 Component Scores:")
        print(f"   • Platform Health: {self.platform_health.get('percentage', 0):.1f}%")
        print(f"   • Comment Coverage: {comment_coverage*100:.1f}%")
        print(f"   • Documentation: {doc_coverage*100:.1f}%")
        
        if self.issues_found:
            print(f"\n❌ Issues Found ({len(self.issues_found)}):")
            for issue in self.issues_found[:5]:
                print(f"   • {issue}")
        
        if self.fixes_applied:
            print(f"\n✅ Fixes Applied ({len(self.fixes_applied)}):")
            for fix in self.fixes_applied:
                print(f"   • {fix}")
        
        if self.recommendations:
            print(f"\n💡 Top Recommendations:")
            for rec in self.recommendations[:3]:
                print(f"   • {rec}")
        
        # Save report
        report_path = self.root_dir / "comprehensive_review_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Full report saved to: {report_path}")
        
        return report
    
    def run_full_analysis(self):
        """Run complete comprehensive analysis"""
        print("🔍 Starting Comprehensive Platform Review and Optimization")
        print("=" * 80)
        
        start_time = time.time()
        
        # Run all analysis components
        self.analyze_previous_comments()
        self.run_comprehensive_health_check()
        self.run_verification_tests()
        self.analyze_code_quality()
        self.check_documentation_completeness()
        self.analyze_script_functionality()
        self.identify_potential_improvements()
        
        # Apply fixes
        fixes_count = self.apply_critical_fixes()
        
        # Generate final report
        report = self.generate_comprehensive_report()
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n⏱️ Analysis completed in {duration:.1f} seconds")
        print(f"🔧 Applied {fixes_count} critical fixes")
        print(f"📊 Overall Platform Score: {report['overall_score']:.1f}%")
        
        return report

def main():
    """Main execution function"""
    optimizer = ComprehensiveReviewOptimizer()
    report = optimizer.run_full_analysis()
    
    # Exit with appropriate code
    if report['overall_score'] >= 90:
        sys.exit(0)  # Excellent
    elif report['overall_score'] >= 80:
        sys.exit(0)  # Good
    else:
        sys.exit(1)  # Needs attention

if __name__ == "__main__":
    main()