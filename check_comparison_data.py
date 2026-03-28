#!/usr/bin/env python
"""Analyze available data for comparison reports"""

import sys
sys.path.insert(0, '/Users/emmidev/Documents/Phone Pe/dashboard')

import pandas as pd
from utils.database import load_query_data, list_available_queries, get_states

print("\n" + "="*80)
print("🔍 ANALYZING COMPARISON REPORT DATA")
print("="*80)

# Get available queries
queries = list_available_queries()
print(f"\n✓ Total available queries: {len(queries)}")

# ============================================================================
# Check what quarterly data is available
# ============================================================================
print("\n📊 CHECKING QUARTERLY COMPARISON DATA")
print("-" * 80)

quarterly_queries = [q for q in queries if 'quarter' in q.lower()]
print(f"✓ Queries with 'quarter': {len(quarterly_queries)}")
for q in quarterly_queries[:3]:
    print(f"  - {q}")

if len(quarterly_queries) > 0:
    print(f"\n✓ Loading first quarterly query for structure check...")
    try:
        df = load_query_data(quarterly_queries[0])
        print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"  Columns: {list(df.columns)}")
        
        # Check for quarter values
        if 'quarter' in df.columns:
            quarters = sorted(df['quarter'].unique())
            print(f"  Quarters available: {quarters}")
        
        # Check numeric columns for comparison
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        print(f"  Numeric columns: {numeric_cols[:5]}")
        
    except Exception as e:
        print(f"  Error: {e}")

# ============================================================================
# Check what state comparison data is available
# ============================================================================
print("\n📍 CHECKING STATE COMPARISON DATA")
print("-" * 80)

available_states = get_states()
print(f"✓ Available states: {len(available_states)}")
print(f"  Sample states: {available_states[:5]}")

# Try to load a transaction query to see state-level data
try:
    trans_df = load_query_data("Query_1.1_Quarterly_Transaction_Growth_by_State_(YoY_Analysis)")
    print(f"\n✓ Transaction data by state:")
    print(f"  Total rows: {trans_df.shape[0]}")
    print(f"  Unique states: {trans_df['state'].nunique()}")
    print(f"  Unique quarters: {trans_df['quarter'].nunique() if 'quarter' in trans_df.columns else 'N/A'}")
    
    # Sample two states for comparison
    sample_states = trans_df['state'].unique()[:2]
    print(f"\n  ✓ Can compare data for states: {list(sample_states)}")
    
    # Show what comparison would look like
    state1_data = trans_df[trans_df['state'] == sample_states[0]]
    state2_data = trans_df[trans_df['state'] == sample_states[1]]
    
    print(f"    State 1 ({sample_states[0]}): {state1_data.shape[0]} records")
    print(f"    State 2 ({sample_states[1]}): {state2_data.shape[0]} records")
    
except Exception as e:
    print(f"Error loading transaction data: {e}")

# ============================================================================
# Check category data
# ============================================================================
print("\n📂 CHECKING CATEGORY COMPARISON DATA")
print("-" * 80)

category_queries = [q for q in queries if 'category' in q.lower() or 'type' in q.lower()]
print(f"✓ Queries with categories: {len(category_queries)}")

if len(category_queries) > 0:
    try:
        df = load_query_data(category_queries[0])
        print(f"  First query: {category_queries[0][:50]}")
        print(f"  Shape: {df.shape}")
        
        # Find category column
        for col in df.columns:
            if 'category' in col.lower() or 'type' in col.lower():
                unique_values = df[col].nunique()
                print(f"  Category column: '{col}' ({unique_values} unique values)")
                print(f"    Sample: {df[col].unique()[:3]}")
                break
    except Exception as e:
        print(f"  Error: {e}")

print("\n" + "="*80)
print("📋 FINDINGS & RECOMMENDATIONS")
print("="*80)

print("""
✓ STATE COMPARISON: Fully implementable
  - Can compare any two states across all timeframes
  - Data available in quarterly queries
  - Can show side-by-side metrics

⚠️  QUARTERLY COMPARISON: Limited by data structure
  - Data is organized by state + quarter
  - To compare quarters meaningfully, need to aggregate across states
  - Feasible but requires aggregation logic

❌ CATEGORY COMPARISON: Not viable
  - Query files don't have meaningful category breakdowns
  - Most queries only have 'TOTAL' rows
  - Should be removed or replaced

RECOMMENDED FIX:
1. Implement full state comparison (side-by-side metrics, charts)
2. Implement quarterly comparison (aggregate by quarter across states)
3. Replace category comparison with available alternatives (e.g., device types for user data)
""")

print("="*80)
