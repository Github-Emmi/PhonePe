#!/usr/bin/env python3
"""
End-to-End ETL Pipeline Test
Tests complete pipeline execution with sample data
"""

import sys
from pathlib import Path
import pandas as pd

# Setup path
etl_root = Path('/Users/emmidev/Documents/Phone Pe')
sys.path.insert(0, str(etl_root))

print("=" * 80)
print("🚀 END-TO-END ETL PIPELINE TEST")
print("=" * 80)

try:
    # Import all components
    from etl.pipeline_orchestrator import ETLPipeline
    print("\n✓ ETLPipeline imported successfully")
    
    # Initialize pipeline
    data_path = str(etl_root / 'data_extracts')
    pipeline = ETLPipeline(data_path)
    print("✓ Pipeline initialized successfully")
    
    # Execute full pipeline
    print("\n" + "-" * 80)
    print("Executing full ETL pipeline...")
    print("-" * 80)
    
    success, summary = pipeline.execute_full_pipeline()
    
    # Display results
    print("\n" + "=" * 80)
    print("📊 PIPELINE EXECUTION RESULTS")
    print("=" * 80)
    
    print(f"\nStatus: {summary['status'].upper()}")
    print(f"Duration: {summary['duration_seconds']:.2f} seconds")
    
    if 'load_statistics' in summary:
        stats = summary['load_statistics']
        print(f"\nLoad Statistics:")
        print(f"  • Total Records Loaded: {stats['total_records']:,}")
        print(f"  • Tables Loaded: {stats['tables_loaded']}")
        
        print(f"\nBy Table:")
        for table, count in stats['by_table'].items():
            print(f"  • {table}: {count:,} records")
    
    if summary['errors']:
        print(f"\nErrors ({len(summary['errors'])}):")
        for error in summary['errors']:
            print(f"  ✗ {error}")
    
    # Final status
    print("\n" + "=" * 80)
    if success and not summary['errors']:
        print("✅ END-TO-END TEST PASSED - PIPELINE IS FULLY OPERATIONAL")
    else:
        print("⚠ END-TO-END TEST COMPLETED WITH WARNINGS")
    print("=" * 80)
    
    sys.exit(0 if success else 1)

except Exception as e:
    print(f"\n✗ Pipeline test failed with error:")
    print(f"  {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
