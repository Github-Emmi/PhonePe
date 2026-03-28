#!/usr/bin/env python
"""Debug the insurance page metric error"""

import sys
sys.path.insert(0, '/Users/emmidev/Documents/Phone Pe/dashboard')

import pandas as pd
from utils.database import load_query_data
from utils.formatting import format_large_number

print("\n" + "="*80)
print("🔍 DEBUGGING INSURANCE METRIC ERROR")
print("="*80)

try:
    state_ins_df = load_query_data("Query_3.1_Insurance_Growth_Trajectory_by_State_&_Quarter")
    
    if not state_ins_df.empty:
        # Get latest quarter data by state
        if 'quarter' in state_ins_df.columns:
            latest_quarter = state_ins_df['quarter'].max()
            latest_data = state_ins_df[state_ins_df['quarter'] == latest_quarter]
        else:
            latest_data = state_ins_df
        
        print(f"✓ Latest data loaded: {latest_data.shape[0]} rows")
        
        # Get numeric columns for visualization
        numeric_cols = latest_data.select_dtypes(include=['number']).columns.tolist()
        print(f"✓ Numeric columns: {numeric_cols}")
        
        # Find the best metric column
        metric_col = None
        for col in ['insurance_transactions', 'premium_amount', 'total_policies']:
            if col in latest_data.columns:
                metric_col = col
                break
        
        if not metric_col and len(numeric_cols) > 0:
            metric_col = numeric_cols[0]
        
        print(f"✓ Selected metric column: {metric_col}")
        
        if metric_col:
            # Test the metric calculation
            top_5_value = latest_data.nlargest(5, metric_col)[metric_col].sum()
            total_value = latest_data[metric_col].sum()
            concentration = (top_5_value / total_value * 100) if total_value > 0 else 0
            
            print(f"✓ Top 5 concentration: {concentration:.1f}%")
            
            # Test top state calculation
            if not latest_data.empty:
                top_state_row = latest_data.nlargest(1, metric_col).iloc[0]
                top_state = top_state_row['state']
                top_state_value = top_state_row[metric_col]
                
                print(f"✓ Top state: {top_state}")
                print(f"✓ Top state value: ₹{format_large_number(top_state_value)}")
                
                print(f"\n✅ All metrics calculated successfully")
                print(f"No issues found with the data operations")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
