#!/usr/bin/env python3
"""
Comprehensive Codebase Audit Script for PhonePe Streamlit Dashboard
Identifies potential issues and inconsistencies
"""

import pandas as pd
import numpy as np
from pathlib import Path
import os
import sys

def audit_data_files():
    """Check data files for quality issues"""
    print("\n" + "=" * 80)
    print("📊 DATA FILE VALIDATION")
    print("=" * 80)
    
    files_to_check = [
        ("query_results/Query_1.1_Quarterly_Transaction_Growth_by_State_(YoY_Analysis).csv", "Q1.1"),
        ("query_results/Query_2.1_State-Level_User_Registration_&_Engagement_Metrics.csv", "Q2.1"),
        ("query_results/Query_3.1_Insurance_Growth_Trajectory_by_State_&_Quarter.csv", "Q3.1"),
        ("data_extracts/aggregated_transaction.csv", "Agg_Trans"),
        ("data_extracts/aggregated_user.csv", "Agg_User"),
    ]
    
    issues = []
    
    for filepath, label in files_to_check:
        try:
            if not Path(filepath).exists():
                issues.append(f"❌ {label}: FILE NOT FOUND - {filepath}")
                continue
                
            df = pd.read_csv(filepath)
            print(f"\n✅ {label}:")
            print(f"   Shape: {len(df)} rows × {len(df.columns)} cols")
            
            # Check for nulls
            null_pct = (df.isnull().sum().sum() / (len(df)*len(df.columns)) * 100)
            if null_pct > 5:
                issues.append(f"⚠️  {label}: High null percentage ({null_pct:.2f}%)")
                print(f"   ⚠️  Nulls: {null_pct:.2f}%")
            
            # Check for duplicates
            dups = len(df) - len(df.drop_duplicates())
            if dups > 0:
                dup_pct = dups / len(df) * 100
                issues.append(f"⚠️  {label}: {dups} duplicate rows ({dup_pct:.2f}%)")
                print(f"   ⚠️  Duplicates: {dups} ({dup_pct:.2f}%)")
            
            # Check column names for spaces/special chars
            bad_cols = [col for col in df.columns if '(' in col or ')' in col]
            if bad_cols:
                print(f"   ⚠️  Columns with special chars: {len(bad_cols)}")
                for col in bad_cols[:3]:
                    print(f"      - {col}")
            
        except Exception as e:
            issues.append(f"❌ {label}: ERROR - {str(e)}")
    
    return issues


def audit_dashboard_structure():
    """Check dashboard code structure"""
    print("\n" + "=" * 80)
    print("📁 DASHBOARD STRUCTURE VALIDATION")
    print("=" * 80)
    
    issues = []
    required_paths = [
        ("dashboard/app.py", "Main app"),
        ("dashboard/utils/database.py", "Database module"),
        ("dashboard/utils/charts.py", "Charts module"),
        ("dashboard/utils/formatting.py", "Formatting module"),
        ("dashboard/utils/metrics.py", "Metrics module"),
        ("dashboard/pages/home.py", "Home page"),
        ("dashboard/pages/transactions.py", "Transactions page"),
        ("dashboard/config/constants.py", "Constants config"),
    ]
    
    for filepath, desc in required_paths:
        if Path(filepath).exists():
            size = Path(filepath).stat().st_size
            print(f"✅ {desc:20} ({filepath:40}) - {size} bytes")
        else:
            issues.append(f"❌ {desc:20} - MISSING: {filepath}")
            print(f"❌ {desc:20} - MISSING")
    
    return issues


def audit_imports():
    """Check for import issues"""
    print("\n" + "=" * 80)
    print("🔧 IMPORT VALIDATION")
    print("=" * 80)
    
    issues = []
    
    # Check app.py imports
    try:
        with open("dashboard/app.py", "r") as f:
            app_content = f.read()
            required_imports = ["streamlit", "pandas", "pathlib"]
            for imp in required_imports:
                if imp.lower() in app_content.lower():
                    print(f"✅ Found import: {imp}")
                else:
                    issues.append(f"⚠️  Missing import in app.py: {imp}")
    except Exception as e:
        issues.append(f"❌ Error reading app.py: {str(e)}")
    
    return issues


def audit_requirements():
    """Check requirements.txt"""
    print("\n" + "=" * 80)
    print("📦 REQUIREMENTS VALIDATION")
    print("=" * 80)
    
    issues = []
    required_packages = [
        "streamlit",
        "pandas",
        "plotly",
        "numpy",
        "sqlalchemy",
    ]
    
    try:
        with open("dashboard/requirements.txt", "r") as f:
            req_content = f.read().lower()
            for pkg in required_packages:
                if pkg in req_content:
                    print(f"✅ {pkg}")
                else:
                    issues.append(f"⚠️  Missing from requirements: {pkg}")
                    print(f"⚠️  {pkg}")
    except Exception as e:
        issues.append(f"❌ Cannot read requirements.txt: {str(e)}")
    
    return issues


def main():
    """Main audit function"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " PHONEPE STREAMLIT DASHBOARD - COMPREHENSIVE CODEBASE AUDIT".center(78) + "║")
    print("╚" + "=" * 78 + "╝")
    
    all_issues = []
    
    # Run audits
    all_issues.extend(audit_dashboard_structure())
    all_issues.extend(audit_data_files())
    all_issues.extend(audit_imports())
    all_issues.extend(audit_requirements())
    
    # Summary
    print("\n" + "=" * 80)
    print("📋 AUDIT SUMMARY")
    print("=" * 80)
    
    if all_issues:
        print(f"\n⚠️  FOUND {len(all_issues)} ISSUES:\n")
        for i, issue in enumerate(all_issues, 1):
            print(f"{i}. {issue}")
    else:
        print("\n✅ No critical issues found!")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
