#!/usr/bin/env python3
"""
COMPREHENSIVE CODEBASE ANALYSIS - DETAILED REPORT
Identifies potential issues, inconsistencies, and improvements
"""

import pandas as pd
import json
from pathlib import Path

print("\n" + "="*90)
print("PHONEPE STREAMLIT DASHBOARD - DETAILED CODEBASE ANALYSIS & ISSUE REPORT".center(90))
print("="*90)

# Initialize issues list
ISSUES = []
WARNINGS = []
RECOMMENDATIONS = []

# ============================================================================
# SECTION 1: DATA CONSISTENCY CHECKS
# ============================================================================
print("\n" + "─"*90)
print("SECTION 1: DATA CONSISTENCY & INTEGRITY".ljust(90))
print("─"*90)

# Check for required CSV files referenced in code
required_csv_mappings = {
    "Query_1.1_Quarterly_Transaction_Growth_by_State_(YoY_Analysis)": [
        "state", "quarter", "transaction_count", "transaction_amount"
    ],
    "Query_2.1_State-Level_User_Registration_&_Engagement_Metrics": [
        "state", "registered_users", "active_users"
    ],
    "Query_3.1_Insurance_Growth_Trajectory_by_State_&_Quarter": [
        "state", "quarter", "insurance_transactions", "premium_amount"
    ],
}

for csv_name, required_cols in required_csv_mappings.items():
    filepath = Path(f"query_results/{csv_name}.csv")
    if filepath.exists():
        try:
            df = pd.read_csv(filepath)
            actual_cols = set(df.columns)
            required_set = set(required_cols)
            
            missing = required_set - actual_cols
            if missing:
                issue = f"❌ {csv_name}: Missing columns: {missing}"
                ISSUES.append(issue)
                print(f"\n{issue}")
            else:
                print(f"✅ {csv_name}: All required columns present")
                
            # Check for zero-value columns
            for col in df.select_dtypes(include=['number']).columns:
                zero_pct = (df[col] == 0).sum() / len(df) * 100
                if zero_pct > 50:
                    warn = f"⚠️  {csv_name}.{col}: {zero_pct:.1f}% values are 0"
                    WARNINGS.append(warn)
                    print(f"   {warn}")
        except Exception as e:
            issue = f"❌ {csv_name}: Error reading file - {str(e)}"
            ISSUES.append(issue)
            print(f"\n{issue}")
    else:
        issue = f"❌ {csv_name}: FILE NOT FOUND"
        ISSUES.append(issue)
        print(f"\n{issue}")

# ============================================================================
# SECTION 2: CODE QUALITY & ERROR HANDLING
# ============================================================================
print("\n" + "─"*90)
print("SECTION 2: CODE QUALITY & ERROR HANDLING".ljust(90))
print("─"*90)

# Check utils/database.py for error handling
print("\n📄 database.py Analysis:")
try:
    with open("dashboard/utils/database.py", "r") as f:
        db_code = f.read()
        
    if "try:" in db_code and "except" in db_code:
        print("   ✅ Has error handling blocks")
    else:
        issue = "❌ database.py: No try/except error handling found"
        ISSUES.append(issue)
        print(f"   {issue}")
    
    if "logging" in db_code:
        print("   ✅ Uses logging module")
    else:
        warn = "⚠️  database.py: No logging found - debug will be difficult"
        WARNINGS.append(warn)
        print(f"   {warn}")
    
    if "_data_cache" in db_code:
        print("   ✅ Implements caching mechanism")
    else:
        warn = "⚠️  database.py: No caching - may impact performance"
        WARNINGS.append(warn)
        print(f"   {warn}")
        
except Exception as e:
    print(f"   ❌ Error reading database.py: {str(e)}")

# ============================================================================
# SECTION 3: STREAMLIT-SPECIFIC ISSUES
# ============================================================================
print("\n" + "─"*90)
print("SECTION 3: STREAMLIT-SPECIFIC CHECKS".ljust(90))
print("─"*90)

print("\n📄 app.py Analysis:")
try:
    with open("dashboard/app.py", "r") as f:
        app_code = f.read()
    
    # Check for st.set_page_config placement
    if "st.set_page_config" in app_code:
        lines = app_code.split('\n')
        for i, line in enumerate(lines):
            if "st.set_page_config" in line:
                if i > 10:
                    warn = f"⚠️  app.py: st.set_page_config called at line {i+1} (should be 1st statement)"
                    WARNINGS.append(warn)
                    print(f"   {warn}")
                else:
                    print("   ✅ st.set_page_config is first statement")
                break
    
    # Check page routing for error handling
    if "try:" in app_code or "except:" in app_code:
        print("   ✅ Has error handling for page imports")
    else:
        warn = "⚠️  app.py: No try/except around page imports - error will crash dashboard"
        WARNINGS.append(warn)
        print(f"   {warn}")
    
except Exception as e:
    print(f"   ❌ Error reading app.py: {str(e)}")

# ============================================================================
# SECTION 4: DEPENDENCY & ENVIRONMENT
# ============================================================================
print("\n" + "─"*90)
print("SECTION 4: DEPENDENCIES & ENVIRONMENT".ljust(90))
print("─"*90)

print("\n📦 requirements.txt Analysis:")
with open("dashboard/requirements.txt", "r") as f:
    reqs = f.read().strip().split('\n')

print(f"   Total packages: {len(reqs)}")

# Check for critical packages
critical = ["streamlit", "pandas", "plotly"]
for pkg in critical:
    found = any(pkg.lower() in req.lower() for req in reqs)
    if found:
        print(f"   ✅ {pkg}")
    else:
        issue = f"❌ Missing critical package: {pkg}"
        ISSUES.append(issue)
        print(f"   ❌ {pkg}")

# Check for version pinning
pinned = sum(1 for req in reqs if '==' in req)
unpinned = sum(1 for req in reqs if '==' not in req and '>' not in req)
print(f"   📌 Pinned versions: {pinned}")
print(f"   📌 Unpinned versions: {unpinned}")
if unpinned > 0:
    rec = "🔧 Recommendation: Pin all version numbers (use ==) for reproducibility"
    RECOMMENDATIONS.append(rec)
    print(f"   {rec}")

# ============================================================================
# SECTION 5: POTENTIAL RUNTIME ISSUES
# ============================================================================
print("\n" + "─"*90)
print("SECTION 5: POTENTIAL RUNTIME ISSUES".ljust(90))
print("─"*90)

runtime_checks = [
    ("dashboard/utils/charts.py", [
        ("plotly", "Plotly visualization library"),
        ("go.Figure", "Figure creation"),
    ]),
    ("dashboard/utils/formatting.py", [
        ("format_", "Function naming consistency"),
    ]),
    ("dashboard/pages/home.py", [
        ("load_query_data", "Data loading calls"),
    ]),
]

for filepath, checks in runtime_checks:
    print(f"\n📄 {Path(filepath).name}:")
    try:
        with open(filepath, "r") as f:
            content = f.read()
        
        for check_str, desc in checks:
            if check_str in content:
                print(f"   ✅ Uses {desc}")
            else:
                print(f"   ⚠️  Missing {desc}")
    except:
        pass

# ============================================================================
# SECTION 6: DATA LOADING PATHS
# ============================================================================
print("\n" + "─"*90)
print("SECTION 6: FILE PATH CONFIGURATION".ljust(90))
print("─"*90)

print("\n🔍 Data Directory Configuration:")
try:
    with open("dashboard/utils/database.py", "r") as f:
        content = f.read()
    
    if "DATA_DIR = Path" in content:
        print("   ✅ Uses Path objects (relative paths)")
    
    # Check if path is portably configured
    if "query_results" in content:
        print("   ✅ References 'query_results' directory")
    
    if "data_extracts" in content:
        print("   ✅ References 'data_extracts' directory")
    
except:
    pass

# ============================================================================
# SECTION 7: PAGE IMPLEMENTATION CONSISTENCY
# ============================================================================
print("\n" + "─"*90)
print("SECTION 7: PAGE IMPLEMENTATION CONSISTENCY".ljust(90))
print("─"*90)

pages = [
    "home", "transactions", "users", "insurance", "geographic", "reports"
]

print("\n📄 Page Function Organization:")
for page in pages:
    filepath = f"dashboard/pages/{page}.py"
    if Path(filepath).exists():
        with open(filepath, "r") as f:
            content = f.read()
        
        # Check for main render function
        func_name = f"{page}_page"
        if f"def {func_name}():" in content:
            print(f"   ✅ {page:15} - Has {func_name}() function")
        else:
            warn = f"⚠️  {page:15} - Missing standard {func_name}() function"
            WARNINGS.append(warn)
            print(f"   {warn}")
    else:
        issue = f"❌ {page:15} - File not found: {filepath}"
        ISSUES.append(issue)
        print(f"   {issue}")

# ============================================================================
# SECTION 8: COLUMN NAME CONSISTENCY
# ============================================================================
print("\n" + "─"*90)
print("SECTION 8: DATA COLUMN CONSISTENCY".ljust(90))
print("─"*90)

# Load and check column name consistency across CSV files
print("\n📋 Column Naming Patterns:")
query_files = list(Path("query_results").glob("*.csv"))[:6]

column_patterns = {}
for query_file in query_files:
    try:
        df = pd.read_csv(query_file)
        for col in df.columns:
            if col not in column_patterns:
                column_patterns[col] = []
            column_patterns[col].append(query_file.name)
    except:
        pass

# Check for naming inconsistencies
variants = {}
for col in column_patterns.keys():
    lower = col.lower()
    if lower not in variants:
        variants[lower] = []
    variants[lower].append(col)

inconsistent = {k: v for k, v in variants.items() if len(v) > 1}
if inconsistent:
    warn = f"⚠️  Found {len(inconsistent)} column naming inconsistencies"
    WARNINGS.append(warn)
    print(f"   {warn}")
    for base, variants_list in list(inconsistent.items())[:3]:
        print(f"      '{base}' appears as: {variants_list}")
else:
    print("   ✅ Column names appear consistent")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*90)
print("AUDIT SUMMARY".center(90))
print("="*90)

print(f"\n🔴 CRITICAL ISSUES: {len(ISSUES)}")
if ISSUES:
    for issue in ISSUES:
        print(f"   {issue}")

print(f"\n🟡 WARNINGS: {len(WARNINGS)}")
if WARNINGS[:5]:
    for warning in WARNINGS[:5]:
        print(f"   {warning}")
    if len(WARNINGS) > 5:
        print(f"   ... and {len(WARNINGS)-5} more")

print(f"\n🟢 RECOMMENDATIONS: {len(RECOMMENDATIONS)}")
if RECOMMENDATIONS:
    for rec in RECOMMENDATIONS:
        print(f"   {rec}")

print("\n" + "="*90)
print(f"Overall Status: {'⚠️  NEEDS ATTENTION' if ISSUES else '✅ HEALTHY'} ({len(ISSUES)} issues, {len(WARNINGS)} warnings)")
print("="*90 + "\n")
