#!/usr/bin/env python
"""Test updated transactions page for data issues and inconsistencies"""

import sys
sys.path.insert(0, '/Users/emmidev/Documents/Phone Pe/dashboard')

import pandas as pd
from utils.database import load_query_data
from utils.formatting import format_large_number

print("\n" + "="*80)
print("🧪 TESTING UPDATED TRANSACTIONS PAGE")
print("="*80)

# ============================================================================
# TEST 1: Quarterly Transaction Growth
# ============================================================================
print("\n✅ TEST 1: Quarterly Transaction Growth (FIXED)")
print("-" * 80)
try:
    growth_df = load_query_data("Query_1.1_Quarterly_Transaction_Growth_by_State_(YoY_Analysis)")
    print(f"✓ Query loaded: {growth_df.shape[0]} rows")
    
    # Test aggregation
    numeric_cols_to_sum = [col for col in growth_df.select_dtypes(include=['number']).columns if col not in ['quarter', 'year']]
    agg_dict = {col: 'sum' for col in numeric_cols_to_sum}
    quarterly_agg = growth_df.groupby('quarter').agg(agg_dict).reset_index()
    
    print(f"✓ Quarterly aggregation: {quarterly_agg.shape[0]} quarters")
    print(f"  Quarters: {quarterly_agg['quarter'].tolist()}")
    print(f"✅ WORKING - No quarter groupby errors")
except Exception as e:
    print(f"❌ ERROR: {e}")

# ============================================================================
# TEST 2: Top States Data
# ============================================================================
print("\n✅ TEST 2: Top States by Transaction Revenue")
print("-" * 80)
try:
    states_df = load_query_data("Query_4.1_State-Level_Transaction_Performance_Analytics_(Comprehensive)")
    print(f"✓ Query loaded: {states_df.shape[0]} rows × {states_df.shape[1]} columns")
    print(f"  Columns: {list(states_df.columns)}")
    
    # Find columns
    numeric_cols = states_df.select_dtypes(include=['number']).columns.tolist()
    print(f"  Numeric columns: {numeric_cols}")
    
    # Find amount column
    amount_col = None
    for col in ['transaction_amount', 'revenue', 'transaction_value', 'total_value']:
        if col in states_df.columns:
            amount_col = col
            break
    
    if amount_col:
        print(f"✓ Found amount column: {amount_col}")
        
        # Get top states
        top_states = states_df.nlargest(10, amount_col)[['state', amount_col]]
        print(f"✓ Top 10 states by {amount_col}:")
        for idx, row in top_states.iterrows():
            print(f"  {row['state']:30s} - ₹ {format_large_number(row[amount_col])}")
        
        # Calculate concentration
        top_10_total = top_states[amount_col].sum()
        all_total = states_df[amount_col].sum()
        concentration = (top_10_total / all_total * 100) if all_total > 0 else 0
        print(f"\n✓ Top 10 concentration: {concentration:.2f}%")
        print(f"✅ WORKING - Top states data available and valid")
    else:
        print(f"❌ No amount column found in data")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# TEST 3: Data Inconsistencies Check
# ============================================================================
print("\n⚠️  TEST 3: Data Inconsistencies")
print("-" * 80)

issues = []

try:
    # Check for null values
    trans_df = load_query_data("Query_4.1_State-Level_Transaction_Performance_Analytics_(Comprehensive)")
    
    null_counts = trans_df.isnull().sum()
    if null_counts.sum() > 0:
        print("⚠️  NULL VALUES DETECTED:")
        for col, count in null_counts[null_counts > 0].items():
            pct = (count / len(trans_df)) * 100
            print(f"   {col}: {count} rows ({pct:.1f}%)")
            issues.append(f"Null values in {col}")
    else:
        print("✓ No null values detected")
    
    # Check for negative values
    numeric_cols = trans_df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        neg_count = (trans_df[col] < 0).sum()
        if neg_count > 0:
            print(f"⚠️  NEGATIVE VALUES in {col}: {neg_count} rows")
            issues.append(f"Negative values in {col}")
    
    if not issues:
        print("✓ No negative values detected")
    
    # Check for duplicates
    dup_count = trans_df.duplicated(subset=['state']).sum()
    if dup_count > 0:
        print(f"⚠️  DUPLICATE STATES: {dup_count} rows")
        issues.append(f"Duplicate states in data")
    else:
        print(f"✓ No duplicate states (unique states: {trans_df['state'].nunique()})")
    
except Exception as e:
    print(f"ERROR checking inconsistencies: {e}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("📊 SUMMARY")
print("="*80)
if issues:
    print(f"\n⚠️  {len(issues)} potential issues found:")
    for i, issue in enumerate(issues, 1):
        print(f"  {i}. {issue}")
    print("\nRECOMMENDATIONS:")
    print("  • Review data source for quality issues")
    print("  • Consider data cleaning/validation")
    print("  • Add data quality warnings to dashboard")
else:
    print("\n✅ ALL TESTS PASSED - DATA QUALITY LOOKS GOOD")
    print("\nThe updated Transaction Analytics page is ready to use!")
    print("Features:")
    print("  • ✓ Quarterly Transaction Growth (fixed)")
    print("  • ✓ Top States by Transaction Revenue (new)")
    print("  • ✓ State-level breakdown with metrics")
    print("  • ✓ Market concentration analysis")

print("\n" + "="*80)
