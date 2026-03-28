#!/usr/bin/env python
"""Check all queries for category breakdown data"""

import pandas as pd
import os

query_dir = "query_results"
print("📋 CHECKING ALL AVAILABLE QUERIES FOR CATEGORY/TYPE DATA\n")

for filename in sorted(os.listdir(query_dir)):
    if not filename.endswith('.csv'):
        continue
    
    filepath = os.path.join(query_dir, filename)
    df = pd.read_csv(filepath)
    
    # Check for category/type/category-related columns
    cat_cols = [col for col in df.columns if any(word in col.lower() for word in ['category', 'type', 'payment', 'product'])]
    
    if cat_cols:
        unique_vals = df[cat_cols[0]].nunique() if len(cat_cols) > 0 else 0
        non_total = len(df[df[cat_cols[0]] != 'TOTAL']) if unique_vals > 1 else 0
        
        print(f"{filename}")
        print(f"  Category columns: {cat_cols}")
        print(f"  Unique values: {unique_vals}, Non-TOTAL rows: {non_total}")
        if unique_vals <= 15:
            print(f"  Values: {df[cat_cols[0]].unique().tolist()}")
        print()
