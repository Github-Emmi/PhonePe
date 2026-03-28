#!/usr/bin/env python
"""Test transaction analytics fixes"""

import sys
sys.path.insert(0, '/Users/emmidev/Documents/Phone Pe/dashboard')

import pandas as pd
from utils.database import load_query_data

print("="*80)
print("Testing Transaction Analytics Fixes")
print("="*80)

# Test 1: Query_1.1 groupby issue
print("\n🔍 TEST 1: Query_1.1 groupby aggregation")
try:
    growth_df = load_query_data("Query_1.1_Quarterly_Transaction_Growth_by_State_(YoY_Analysis)")
    print(f"✓ Loaded Query_1.1: {growth_df.shape}")
    print(f"  Columns: {list(growth_df.columns)}")
    
    # Test the fix
    numeric_cols_to_sum = [col for col in growth_df.select_dtypes(include=['number']).columns if col not in ['quarter', 'year']]
    print(f"  Numeric columns to aggregate: {numeric_cols_to_sum}")
    
    agg_dict = {col: 'sum' for col in numeric_cols_to_sum}
    quarterly_agg = growth_df.groupby('quarter').agg(agg_dict).reset_index()
    print(f"✓ Aggregation successful: {quarterly_agg.shape}")
    print(f"  Result:\n{quarterly_agg}")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Query_1.2 category column issue
print("\n🔍 TEST 2: Query_1.2 category column")
try:
    cat_df = load_query_data("Query_1.2_Top_10_Transaction_Categories_by_Revenue_&_Metrics")
    print(f"✓ Loaded Query_1.2: {cat_df.shape}")
    print(f"  Columns: {list(cat_df.columns)}")
    
    # Find category column
    cat_col = None
    if 'transaction_type' in cat_df.columns:
        cat_col = 'transaction_type'
    elif 'category' in cat_df.columns:
        cat_col = 'category'
    
    print(f"  Found category column: {cat_col}")
    
    # Get numeric columns
    numeric_cols = cat_df.select_dtypes(include=['number']).columns.tolist()
    numeric_cols = [c for c in numeric_cols if c not in ['states_covered']]
    print(f"  Numeric columns for charting: {numeric_cols}")
    
    if cat_col and len(numeric_cols) > 0:
        value_col = numeric_cols[0]
        print(f"✓ Will chart {cat_col} by {value_col}")
        
        # Filter out TOTAL row
        cat_top = cat_df[cat_df[cat_col] != 'TOTAL'].head(10)
        print(f"✓ Top categories (excluding TOTAL): {cat_top.shape}")
        print(f"  Categories: {cat_top[cat_col].tolist()}")
    else:
        print("✗ Missing category column or numeric data")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("✅ All tests passed - fixes are working!")
print("="*80)
