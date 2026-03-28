#!/usr/bin/env python
"""Debug script to diagnose KPI metric issues"""

import sys
sys.path.insert(0, '/Users/emmidev/Documents/Phone Pe/dashboard')

from utils.database import load_query_data
from utils.metrics import calculate_transaction_metrics, calculate_user_metrics
from config.column_mappings import find_column, get_column_mapping

print("\n" + "="*80)
print("DEBUG: KPI METRICS CALCULATION")
print("="*80)

# 1. Test Query_4.1 loading
print("\n📊 TEST 1: Load Query_4.1")
try:
    df = load_query_data("Query_4.1_State-Level_Transaction_Performance_Analytics_(Comprehensive)")
    print(f"✓ Loaded successfully")
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {list(df.columns)}")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

# 2. Check column mapping
print("\n📊 TEST 2: Check Column Mappings")
mappings = get_column_mapping("Query_4.1_State-Level_Transaction_Performance_Analytics_(Comprehensive)")
print(f"  Mappings configured: {mappings}")

# 3. Check find_column
print("\n📊 TEST 3: Find Specific Columns")
print(f"  find_column(df, 'transaction_count'): {find_column(df, 'transaction_count')}")
print(f"  find_column(df, 'transaction_amount'): {find_column(df, 'transaction_amount')}")
print(f"  find_column(df, 'state'): {find_column(df, 'state')}")

# 4. Check actual data
print("\n📊 TEST 4: Sample Data")
print(f"  transaction_count in columns? {'transaction_count' in df.columns}")
print(f"  transaction_amount in columns? {'transaction_amount' in df.columns}")

if 'transaction_count' in df.columns:
    print(f"  transaction_count values: {df['transaction_count'].head(3).tolist()}")
    print(f"  transaction_count sum: {df['transaction_count'].sum()}")
else:
    print(f"  ✗ transaction_count NOT in columns")
    print(f"  Available numeric-like columns: {[c for c in df.columns if 'transact' in c.lower() or 'count' in c.lower()]}")

# 5. Calculate metrics
print("\n📊 TEST 5: Calculate Metrics")
try:
    trans_metrics = calculate_transaction_metrics()
    print(f"✓ Metrics calculated")
    print(f"  Total Transactions: {trans_metrics.get('total_transactions', 0)}")
    print(f"  Total Transaction Amount: {trans_metrics.get('total_transaction_amount', 0)}")
    print(f"  Top State: {trans_metrics.get('top_state', 'N/A')}")
except Exception as e:
    print(f"✗ Failed: {e}")
    import traceback
    traceback.print_exc()

# 6. Test Query_2.1
print("\n📊 TEST 6: Load Query_2.1")
try:
    df2 = load_query_data("Query_2.1_State-Level_User_Registration_&_Engagement_Metrics")
    print(f"✓ Loaded successfully")
    print(f"  Shape: {df2.shape}")
    print(f"  Columns: {list(df2.columns)}")
    
    if 'registered_users' in df2.columns:
        print(f"  registered_users sum: {df2['registered_users'].sum()}")
    else:
        print(f"  ✗ registered_users NOT in columns")
        print(f"  Available columns: {list(df2.columns)}")
except Exception as e:
    print(f"✗ Failed: {e}")

# 7. Calculate user metrics
print("\n📊 TEST 7: Calculate User Metrics")
try:
    user_metrics = calculate_user_metrics()
    print(f"✓ Metrics calculated")
    print(f"  Total Users: {user_metrics.get('total_registered_users', 0)}")
except Exception as e:
    print(f"✗ Failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
