#!/usr/bin/env python3
"""
Simple script to answer: "What is the full line count of code for this project?"
"""

import os

def get_total_line_count():
    """Get the total line count for the Intelligence Gathering Website Project"""
    
    print("🔍 Intelligence Gathering Website Project - Full Line Count")
    print("=" * 60)
    
    total_lines = 0
    total_files = 0
    
    # Count all text-based files, excluding binary files and build artifacts
    for root, dirs, files in os.walk('.'):
        # Skip certain directories
        skip_dirs = {'.git', 'node_modules', '__pycache__', '.pytest_cache', 
                    'dist', 'build', '.venv', 'venv'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            # Skip binary files
            if any(file.lower().endswith(ext) for ext in [
                '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', 
                '.woff', '.woff2', '.ttf', '.eot', '.bin', '.exe'
            ]):
                continue
                
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = len(f.readlines())
                    total_lines += lines
                    total_files += 1
            except Exception:
                # Skip files that can't be read as text
                continue
    
    print(f"📝 Total Files Analyzed: {total_files:,}")
    print(f"📊 TOTAL LINES OF CODE: {total_lines:,}")
    print("=" * 60)
    print(f"✅ ANSWER: This project contains {total_lines:,} lines of code")
    
    return total_lines

if __name__ == "__main__":
    get_total_line_count()