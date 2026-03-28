"""
Quick start test for PhonePe Dashboard
Verifies all components are properly configured
"""

import sys
import os
from pathlib import Path

print("📋 PhonePe Dashboard - Startup Verification")
print("=" * 50)
print()

# Check Python version
py_version = sys.version_info
print(f"✅ Python version: {py_version.major}.{py_version.minor}.{py_version.micro}")

if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 8):
    print("❌ Python 3.8+ required")
    sys.exit(1)

print()

# Check dependencies
print("📦 Checking dependencies...")
dependencies = [
    'streamlit',
    'pandas',
    'plotly',
    'numpy',
]

missing = []
for dep in dependencies:
    try:
        __import__(dep)
        print(f"  ✅ {dep}")
    except ImportError:
        print(f"  ❌ {dep} - MISSING")
        missing.append(dep)

if missing:
    print()
    print(f"⚠️  Missing dependencies: {', '.join(missing)}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

print()

# Check file structure
print("📁 Checking project structure...")

required_files = [
    'app.py',
    'config/__init__.py',
    'config/constants.py',
    'pages/__init__.py',
    'pages/home.py',
    'pages/transactions.py',
    'pages/users.py',
    'pages/insurance.py',
    'pages/geographic.py',
    'pages/reports.py',
    'utils/__init__.py',
    'utils/database.py',
    'utils/formatting.py',
    'utils/charts.py',
    'utils/cache.py',
    'utils/metrics.py',
    '.streamlit/config.toml',
    'requirements.txt',
]

missing_files = []
for file in required_files:
    if Path(file).exists():
        print(f"  ✅ {file}")
    else:
        print(f"  ❌ {file} - MISSING")
        missing_files.append(file)

if missing_files:
    print()
    print(f"⚠️  Missing files: {', '.join(missing_files)}")
    sys.exit(1)

print()

# Check data availability
print("📊 Checking data sources...")

data_dirs = [
    '../query_results',
    '../data_extracts',
]

for data_dir in data_dirs:
    path = Path(data_dir)
    if path.exists():
        csv_count = len(list(path.glob('*.csv')))
        print(f"  ✅ {data_dir} ({csv_count} CSV files)")
    else:
        print(f"  ⚠️  {data_dir} - not found")

print()

# Try to load test data
print("🔍 Testing data loading...")
try:
    from utils.database import load_query_data, list_available_queries
    from utils.cache import cached_query
    
    queries = list_available_queries()
    print(f"  ✅ {len(queries)} queries available")
    
    if len(queries) > 0:
        first_query = queries[0]
        try:
            df = load_query_data(first_query)
            print(f"  ✅ Successfully loaded sample query ({len(df)} rows)")
        except Exception as e:
            print(f"  ⚠️  Could not load sample data: {str(e)}")
    
except Exception as e:
    print(f"  ❌ Error testing data loading: {str(e)}")
    sys.exit(1)

print()
print("✅ All checks passed!")
print()
print("🚀 Ready to launch dashboard")
print()
print("To start, run:")
print("  streamlit run app.py")
print()
print("Dashboard will open at: http://localhost:8501")
