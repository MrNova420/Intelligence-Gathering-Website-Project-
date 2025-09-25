# Intelligence Gathering Website Project - Code Statistics

## 📊 Full Line Count Answer

**The Intelligence Gathering Website Project contains approximately 61,212 lines of code across 129 files.**

## 🔍 Detailed Breakdown

### Overall Statistics
- **Total Files**: 129 files
- **Total Lines**: 61,212 lines of code
- **Primary Languages**: Python, TypeScript/React, JavaScript

### By Programming Language
- **Python**: 82 files, ~43,629 lines (71.3%)
- **TypeScript React**: 11 files, ~5,065 lines (8.3%)
- **JSON**: 4 files, ~6,256 lines (10.2%)
- **Markdown**: 9 files, ~3,363 lines (5.5%)
- **CSS**: 2 files, ~679 lines (1.1%)
- **Shell Scripts**: 3 files, ~383 lines (0.6%)
- **YAML**: 3 files, ~342 lines (0.6%)
- **JavaScript**: 2 files, ~63 lines (0.1%)
- **SQL**: 1 file, ~53 lines (0.1%)
- **Other files**: Various configuration and documentation files

### By Directory Structure
- **backend/app/core**: 21 files, ~13,166 lines (21.5%)
- **backend/app/scanners**: 18 files, ~12,851 lines (21.0%)
- **root**: 25 files, ~8,299 lines (13.6%)
- **frontend**: 8 files, ~6,398 lines (10.5%)
- **frontend/pages**: 10 files, ~4,792 lines (7.8%)
- **backend/app/api**: 8 files, ~3,496 lines (5.7%)
- **backend/tests**: 5 files, ~2,810 lines (4.6%)
- **backend/app/services**: 4 files, ~2,359 lines (3.9%)

### Largest Files
1. `frontend/package-lock.json` - 6,163 lines
2. `ultimate_stability_fixes.py` - 1,344 lines
3. `backend/app/scanners/network_scanners.py` - 1,257 lines
4. `backend/app/scanners/public_records_scanners.py` - 1,150 lines
5. `backend/app/core/aggregation_engine.py` - 1,137 lines
6. `backend/app/scanners/image_media_scanners.py` - 1,125 lines
7. `backend/app/services/advanced_reporting_service.py` - 1,107 lines
8. `backend/app/scanners/geospatial_scanners.py` - 1,088 lines
9. `backend/app/core/threat_intelligence.py` - 1,063 lines
10. `README.md` - 1,026 lines

## 🛠️ How to Check Line Count

You can verify these numbers using the included scripts:

```bash
# Quick answer
python3 get_line_count.py

# Detailed analysis
python3 line_count.py

# Use existing validation
python3 final_comprehensive_validation.py
```

Or using standard Unix tools:
```bash
find . -type f \( -name "*.py" -o -name "*.tsx" -o -name "*.ts" -o -name "*.js" -o -name "*.jsx" -o -name "*.json" -o -name "*.md" -o -name "*.css" -o -name "*.yml" -o -name "*.yaml" -o -name "*.sh" -o -name "*.sql" \) -not -path "./.git/*" -not -path "./node_modules/*" | xargs wc -l
```

## 📝 Notes

- Line counts exclude binary files (images, fonts, etc.)
- Build artifacts and dependency directories are excluded
- Empty lines and comments are included in the count
- JSON files (like package-lock.json) significantly contribute to the total

---

*Last updated: December 2024*
*Generated automatically using project analysis tools*