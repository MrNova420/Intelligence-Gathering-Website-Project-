#!/usr/bin/env python3
"""
Intelligence Gathering Website Project - Line Count Analysis
Provides comprehensive line count statistics for the entire project
"""

import os
import sys
from pathlib import Path
from collections import defaultdict

def count_lines_in_file(file_path):
    """Count lines in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return len(f.readlines())
    except Exception:
        return 0

def get_file_extension(filename):
    """Get file extension and categorize it"""
    ext = Path(filename).suffix.lower()
    
    # Language mapping
    language_map = {
        '.py': 'Python',
        '.tsx': 'TypeScript React',
        '.ts': 'TypeScript', 
        '.jsx': 'JavaScript React',
        '.js': 'JavaScript',
        '.vue': 'Vue.js',
        '.go': 'Go',
        '.java': 'Java',
        '.cpp': 'C++',
        '.c': 'C',
        '.cs': 'C#',
        '.php': 'PHP',
        '.rb': 'Ruby',
        '.rs': 'Rust',
        '.html': 'HTML',
        '.css': 'CSS',
        '.scss': 'SCSS',
        '.sass': 'Sass',
        '.json': 'JSON',
        '.yml': 'YAML',
        '.yaml': 'YAML',
        '.md': 'Markdown',
        '.txt': 'Text',
        '.sh': 'Shell Script',
        '.dockerfile': 'Dockerfile',
        '.sql': 'SQL'
    }
    
    return language_map.get(ext, f'Other ({ext})')

def analyze_project_lines():
    """Analyze line counts across the entire project"""
    print("🔍 Intelligence Gathering Website Project - Line Count Analysis")
    print("=" * 70)
    
    total_lines = 0
    total_files = 0
    language_stats = defaultdict(lambda: {'files': 0, 'lines': 0})
    directory_stats = defaultdict(lambda: {'files': 0, 'lines': 0})
    
    # Walk through all files in the project
    for root, dirs, files in os.walk('.'):
        # Skip certain directories
        skip_dirs = {'.git', 'node_modules', '__pycache__', '.pytest_cache', 
                    'dist', 'build', '.venv', 'venv', '.env'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            file_path = os.path.join(root, file)
            lines = count_lines_in_file(file_path)
            
            if lines > 0:  # Only count files with content
                total_lines += lines
                total_files += 1
                
                language = get_file_extension(file)
                language_stats[language]['files'] += 1
                language_stats[language]['lines'] += lines
                
                # Directory statistics
                rel_dir = os.path.relpath(root, '.') if root != '.' else 'root'
                directory_stats[rel_dir]['files'] += 1
                directory_stats[rel_dir]['lines'] += lines
    
    # Print summary
    print(f"\n📊 TOTAL PROJECT STATISTICS")
    print("-" * 40)
    print(f"🗂️  Total Files: {total_files:,}")
    print(f"📝 Total Lines of Code: {total_lines:,}")
    
    # Language breakdown
    print(f"\n🌐 BREAKDOWN BY LANGUAGE")
    print("-" * 40)
    sorted_languages = sorted(language_stats.items(), 
                            key=lambda x: x[1]['lines'], reverse=True)
    
    for language, stats in sorted_languages:
        percentage = (stats['lines'] / total_lines) * 100
        print(f"{language:20} {stats['files']:3} files  {stats['lines']:6,} lines  ({percentage:5.1f}%)")
    
    # Directory breakdown (top 10)
    print(f"\n📁 TOP DIRECTORIES BY LINE COUNT")
    print("-" * 40)
    sorted_dirs = sorted(directory_stats.items(), 
                        key=lambda x: x[1]['lines'], reverse=True)[:10]
    
    for directory, stats in sorted_dirs:
        percentage = (stats['lines'] / total_lines) * 100
        dir_name = directory if len(directory) <= 25 else directory[:22] + "..."
        print(f"{dir_name:25} {stats['files']:3} files  {stats['lines']:6,} lines  ({percentage:5.1f}%)")
    
    # Find largest files
    print(f"\n📄 LARGEST FILES")
    print("-" * 40)
    file_sizes = []
    for root, dirs, files in os.walk('.'):
        skip_dirs = {'.git', 'node_modules', '__pycache__', '.pytest_cache'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            file_path = os.path.join(root, file)
            lines = count_lines_in_file(file_path)
            if lines > 50:  # Only show substantial files
                file_sizes.append((file_path, lines))
    
    file_sizes.sort(key=lambda x: x[1], reverse=True)
    for file_path, lines in file_sizes[:10]:
        rel_path = os.path.relpath(file_path, '.')
        path_display = rel_path if len(rel_path) <= 50 else "..." + rel_path[-47:]
        print(f"{path_display:50} {lines:6,} lines")
    
    print("\n" + "=" * 70)
    print(f"🎯 ANSWER: The Intelligence Gathering Website Project contains {total_lines:,} lines of code")
    print(f"   across {total_files:,} files in multiple programming languages.")
    print("=" * 70)
    
    return total_lines, total_files

if __name__ == "__main__":
    try:
        total_lines, total_files = analyze_project_lines()
        print(f"\n✅ Analysis complete! Total: {total_lines:,} lines of code")
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        sys.exit(1)