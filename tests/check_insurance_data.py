#!/usr/bin/env python
"""Check insurance query data structure"""

import sys
sys.path.insert(0, '/Users/emmidev/Documents/Phone Pe/dashboard')

import pandas as pd
from utils.database import load_query_data

print("\n" + "="*80)
print("🔍 INSURANCE QUERY DATA STRUCTURE ANALYSIS")
print("="*80)

# Check each insurance query
queries = [
    "Query_3.1_Insurance_Growth_Trajectory_by_State_&_Quarter",
    "Query_3.2_Insurance_Penetration_by_State_&_Quarter", 
    "Query_3.3_Top_Insurance_Categories_by_Revenue_&_Metrics",
    "Query_3.4_State-Level_Insurance_Performance_Analytics"
]

for query_name in queries:
    print(f"\n📊 {query_name}")
    print("-" * 80)
    try:
        df = load_query_data(query_name)
        print(f"✓ Loaded: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"  Columns: {list(df.columns)}")
        
        # Check unique values in key columns
        if 'quarter' in df.columns:
            print(f"  Quarters: {sorted(df['quarter'].unique())}")
        
        if 'category' in df.columns:
            print(f"  Categories: {df['category'].unique().tolist()}")
        elif 'insurance_category' in df.columns:
            print(f"  Insurance Categories: {df['insurance_category'].unique().tolist()}")
        
        if 'state' in df.columns:
            print(f"  States: {df['state'].nunique()} unique (Sample: {df['state'].unique()[:3].tolist()})")
        
        # Check data types
        print(f"  Data types:")
        for col in df.columns:
            print(f"    - {col}: {df[col].dtype}")
        
        # Show first row
        print(f"\n  First row:")
        print(f"    {df.iloc[0].to_dict()}")
        
    except Exception as e:
        print(f"✗ Error: {e}")

print("\n" + "="*80)
print("📋 FINDINGS & ISSUES")
print("="*80)

# Check Query_3.1 specifically for groupby issue
print("\n✓ CHECKING QUERY_3.1 GROUPBY AGGREGATION")
try:
    df = load_query_data("Query_3.1_Insurance_Growth_Trajectory_by_State_&_Quarter")
    print(f"Original shape: {df.shape}")
    
    # Try aggregation (this is what the code does)
    numeric_cols = df.select_dtypes(include=['number']).columns
    print(f"Numeric columns: {numeric_cols.tolist()}")
    
    # This might cause the error if 'quarter' is included
    agg_dict = {col: 'sum' for col in numeric_cols}
    print(f"Aggregation dict keys: {list(agg_dict.keys())}")
    
    if 'quarter' in agg_dict:
        print("⚠️  WARNING: 'quarter' is being aggregated!")
        print("This will cause 'cannot insert quarter, already exists' error")
        
        # Fix it
        agg_dict_fixed = {col: 'sum' for col in numeric_cols if col not in ['quarter', 'year']}
        result_fixed = df.groupby('quarter').agg(agg_dict_fixed).reset_index()
        print(f"✓ Fixed aggregation shape: {result_fixed.shape}")
    
except Exception as e:
    print(f"Error: {e}")

print("\n✓ CHECKING QUERY_3.3 FOR CATEGORY COLUMN")
try:
    df = load_query_data("Query_3.3_Top_Insurance_Categories_by_Revenue_&_Metrics")
    if 'category' in df.columns:
        print("✓ 'category' column exists")
    else:
        print("✗ 'category' column NOT found")
        print(f"  Available columns: {list(df.columns)}")
        
        # Check for similar column names
        for col in df.columns:
            if 'category' in col.lower() or 'type' in col.lower():
                print(f"  → Similar column: '{col}'")
    
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*80)
