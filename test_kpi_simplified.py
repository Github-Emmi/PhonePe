#!/usr/bin/env python
"""
Simplified KPI metrics test - standalone version
"""
import sys
import pandas as pd

# Add dashboard to path
sys.path.insert(0, '/Users/emmidev/Documents/Phone Pe/dashboard')

print("="*80)
print("TESTING KPI METRICS CALCULATION")
print("="*80)

# Test 1: Load raw CSV directly
print("\n🔍 TEST 1: Load CSV directly (no standardization)")
try:
    query_4_1_path = "/Users/emmidev/Documents/Phone Pe/query_results/Query_4.1_State-Level_Transaction_Performance_Analytics_(Comprehensive).csv"
    df_raw = pd.read_csv(query_4_1_path)
    print(f"✓ Loaded: {df_raw.shape}")
    print(f"  Columns: {list(df_raw.columns)}")
    print(f"  Expected column mappings:")
    print(f"    annual_transaction_count → transaction_count")
    print(f"    annual_transaction_value → transaction_amount")
    
    if 'annual_transaction_count' in df_raw.columns:
        print(f"  ✓ annual_transaction_count found")
        print(f"    Sum: {df_raw['annual_transaction_count'].sum()}")
    
    if 'annual_transaction_value' in df_raw.columns:
        print(f"  ✓ annual_transaction_value found")
        print(f"    Sum: {df_raw['annual_transaction_value'].sum()}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Try to load with standardization
print("\n🔍 TEST 2: Load with standardization")
try:
    from utils.database import load_query_data
    df = load_query_data("Query_4.1_State-Level_Transaction_Performance_Analytics_(Comprehensive)")
    print(f"✓ Loaded: {df.shape}")
    print(f"  Columns: {list(df.columns)}")
    
    if 'transaction_count' in df.columns:
        print(f"  ✓ transaction_count found")
        print(f"    Sum: {df['transaction_count'].sum()}")
    else:
        print(f"  ✗ transaction_count NOT found in standardized data")
    
    if 'transaction_amount' in df.columns:
        print(f"  ✓ transaction_amount found")
        print(f"    Sum: {df['transaction_amount'].sum()}")
    else:
        print(f"  ✗ transaction_amount NOT found in standardized data")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Try metrics calculation
print("\n🔍 TEST 3: Calculate metrics")
try:
    from utils.metrics import calculate_transaction_metrics
    metrics = calculate_transaction_metrics()
    print(f"✓ Metrics calculated: {dict(metrics)}")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Format the numbers
print("\n🔍 TEST 4: Format for display")
try:
    from utils.formatting import format_large_number, format_currency
    if 'metrics' in locals() and metrics:
        total_trans = metrics.get('total_transactions', 0)
        total_amount = metrics.get('total_transaction_amount', 0)
        print(f"  Formatted total_transactions: {format_large_number(total_trans)}")
        print(f"  Formatted total_transaction_amount: {format_currency(total_amount, decimals=0)}")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
