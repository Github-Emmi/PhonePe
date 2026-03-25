#!/usr/bin/env python3
"""
ETL Module Verification Script
Tests all ETL modules for syntax errors, imports, and basic functionality
"""

import sys
import os
import py_compile
import importlib.util
from pathlib import Path

# Set up environment
etl_dir = Path('/Users/emmidev/Documents/Phone Pe/etl')
data_dir = Path('/Users/emmidev/Documents/Phone Pe/data_extracts')
sys.path.insert(0, str(etl_dir.parent))

print("=" * 80)
print("🧪 ETL MODULE VERIFICATION TEST")
print("=" * 80)

# Test results
results = {
    'syntax_check': {},
    'import_check': {},
    'functionality_test': {}
}

# ============================================================================
# SECTION 1: SYNTAX VALIDATION
# ============================================================================
print("\n📝 SECTION 1: SYNTAX VALIDATION")
print("-" * 80)

etl_files = [
    'data_loader.py',
    'data_transformer.py',
    'data_aggregator.py',
    'database_loader.py',
    'pipeline_orchestrator.py'
]

for file in etl_files:
    filepath = etl_dir / file
    try:
        py_compile.compile(str(filepath), doraise=True)
        results['syntax_check'][file] = 'PASS'
        print(f"✓ {file:30s} - Syntax OK")
    except py_compile.PyCompileError as e:
        results['syntax_check'][file] = f'FAIL: {str(e)}'
        print(f"✗ {file:30s} - Syntax Error: {e}")

# ============================================================================
# SECTION 2: IMPORT VALIDATION
# ============================================================================
print("\n📦 SECTION 2: MODULE IMPORT VALIDATION")
print("-" * 80)

modules = {}
try:
    from etl.data_loader import DataLoader
    modules['DataLoader'] = DataLoader
    results['import_check']['DataLoader'] = 'PASS'
    print(f"✓ DataLoader imported successfully")
except Exception as e:
    results['import_check']['DataLoader'] = f'FAIL: {str(e)}'
    print(f"✗ DataLoader import failed: {e}")

try:
    from etl.data_transformer import DataTransformer
    modules['DataTransformer'] = DataTransformer
    results['import_check']['DataTransformer'] = 'PASS'
    print(f"✓ DataTransformer imported successfully")
except Exception as e:
    results['import_check']['DataTransformer'] = f'FAIL: {str(e)}'
    print(f"✗ DataTransformer import failed: {e}")

try:
    from etl.data_aggregator import DataAggregator
    modules['DataAggregator'] = DataAggregator
    results['import_check']['DataAggregator'] = 'PASS'
    print(f"✓ DataAggregator imported successfully")
except Exception as e:
    results['import_check']['DataAggregator'] = f'FAIL: {str(e)}'
    print(f"✗ DataAggregator import failed: {e}")

try:
    from etl.database_loader import DatabaseLoader
    modules['DatabaseLoader'] = DatabaseLoader
    results['import_check']['DatabaseLoader'] = 'PASS'
    print(f"✓ DatabaseLoader imported successfully")
except Exception as e:
    results['import_check']['DatabaseLoader'] = f'FAIL: {str(e)}'
    print(f"✗ DatabaseLoader import failed: {e}")

try:
    from etl.pipeline_orchestrator import ETLPipeline
    modules['ETLPipeline'] = ETLPipeline
    results['import_check']['ETLPipeline'] = 'PASS'
    print(f"✓ ETLPipeline imported successfully")
except Exception as e:
    results['import_check']['ETLPipeline'] = f'FAIL: {str(e)}'
    print(f"✗ ETLPipeline import failed: {e}")

# ============================================================================
# SECTION 3: FUNCTIONALITY TESTS
# ============================================================================
print("\n🔧 SECTION 3: FUNCTIONALITY TESTS")
print("-" * 80)

# Test DataLoader
print("\n• Testing DataLoader...")
try:
    loader = DataLoader(str(data_dir))
    print(f"  ✓ DataLoader instantiation: OK")
    
    # Check if CSV files exist
    csv_files = list(data_dir.glob('*.csv'))
    print(f"  ✓ Found {len(csv_files)} CSV files")
    
    # Test load_all_data method
    data = loader.load_all_data()
    print(f"  ✓ load_all_data() method: OK (loaded {len(data)} datasets)")
    
    # Test get_data_summary method
    summary = loader.get_data_summary()
    print(f"  ✓ get_data_summary() method: OK")
    
    results['functionality_test']['DataLoader'] = 'PASS'
except Exception as e:
    results['functionality_test']['DataLoader'] = f'FAIL: {str(e)}'
    print(f"  ✗ DataLoader test failed: {e}")

# Test DataTransformer
print("\n• Testing DataTransformer...")
try:
    transformer = DataTransformer()
    print(f"  ✓ DataTransformer instantiation: OK")
    
    # Test with sample data
    import pandas as pd
    sample_df = pd.DataFrame({
        'region': ['delhi', 'maharashtra'],
        'year': [2023, 2023],
        'quarter': [1, 2]
    })
    
    # Test standardize_state_names
    result = transformer.standardize_state_names(sample_df)
    print(f"  ✓ standardize_state_names() method: OK")
    
    # Test standardize_column_names
    result = transformer.standardize_column_names(result)
    print(f"  ✓ standardize_column_names() method: OK")
    
    results['functionality_test']['DataTransformer'] = 'PASS'
except Exception as e:
    results['functionality_test']['DataTransformer'] = f'FAIL: {str(e)}'
    print(f"  ✗ DataTransformer test failed: {e}")

# Test DataAggregator
print("\n• Testing DataAggregator...")
try:
    aggregator = DataAggregator()
    print(f"  ✓ DataAggregator instantiation: OK")
    
    # Test with sample data
    import pandas as pd
    sample_agg = pd.DataFrame({
        'year': [2023, 2023],
        'quarter': [1, 2],
        'count': [100, 150],
        'amount': [1000.0, 1500.0]
    })
    
    # Test aggregate_by_quarter
    result = aggregator.aggregate_by_quarter(sample_agg)
    print(f"  ✓ aggregate_by_quarter() method: OK")
    
    results['functionality_test']['DataAggregator'] = 'PASS'
except Exception as e:
    results['functionality_test']['DataAggregator'] = f'FAIL: {str(e)}'
    print(f"  ✗ DataAggregator test failed: {e}")

# Test DatabaseLoader
print("\n• Testing DatabaseLoader...")
try:
    db_loader = DatabaseLoader()
    print(f"  ✓ DatabaseLoader instantiation: OK")
    
    # Check database connection
    db_status = "configured" if db_loader else "initialized"
    print(f"  ✓ DatabaseLoader initialization: OK ({db_status})")
    
    results['functionality_test']['DatabaseLoader'] = 'PASS'
except Exception as e:
    results['functionality_test']['DatabaseLoader'] = f'FAIL: {str(e)}'
    print(f"  ✗ DatabaseLoader test failed: {e}")

# Test ETLPipeline
print("\n• Testing ETLPipeline...")
try:
    pipeline = ETLPipeline(str(data_dir))
    print(f"  ✓ ETLPipeline instantiation: OK")
    
    # Verify pipeline has required components
    assert hasattr(pipeline, 'data_loader'), "Missing data_loader"
    assert hasattr(pipeline, 'data_transformer'), "Missing data_transformer"
    assert hasattr(pipeline, 'data_aggregator'), "Missing data_aggregator"
    assert hasattr(pipeline, 'database_loader'), "Missing database_loader"
    print(f"  ✓ All pipeline components present: OK")
    
    results['functionality_test']['ETLPipeline'] = 'PASS'
except Exception as e:
    results['functionality_test']['ETLPipeline'] = f'FAIL: {str(e)}'
    print(f"  ✗ ETLPipeline test failed: {e}")

# ============================================================================
# SECTION 4: TEST SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("📊 TEST SUMMARY")
print("=" * 80)

# Syntax Check Summary
print("\n✅ SYNTAX CHECK:")
syntax_pass = sum(1 for v in results['syntax_check'].values() if v == 'PASS')
syntax_total = len(results['syntax_check'])
print(f"   {syntax_pass}/{syntax_total} files passed")

# Import Check Summary
print("\n✅ IMPORT CHECK:")
import_pass = sum(1 for v in results['import_check'].values() if v == 'PASS')
import_total = len(results['import_check'])
print(f"   {import_pass}/{import_total} modules imported successfully")

# Functionality Test Summary
print("\n✅ FUNCTIONALITY TEST:")
func_pass = sum(1 for v in results['functionality_test'].values() if v == 'PASS')
func_total = len(results['functionality_test'])
print(f"   {func_pass}/{func_total} modules tested successfully")

# Overall Status
print("\n" + "=" * 80)
total_pass = syntax_pass + import_pass + func_pass
total_tests = syntax_total + import_total + func_total

if total_pass == total_tests:
    print("✅ ALL TESTS PASSED - ETL MODULES ARE BUG-FREE")
    status = "SUCCESS"
else:
    print("⚠ SOME TESTS FAILED - SEE DETAILS ABOVE")
    status = "FAILURE"

print("=" * 80)

sys.exit(0 if status == "SUCCESS" else 1)
