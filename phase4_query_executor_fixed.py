"""
Phase 4 Query Execution Framework - Updated for Actual Schema
Executes all 25 analytical SQL queries with corrected schema mapping
"""

import sqlite3
import pandas as pd
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any
import sys
import re

class Phase4QueryExecutorFixed:
    """Execute and validate Phase 4 analytical SQL queries with actual schema"""
    
    def __init__(self, db_path: str = "phonpe_analytics.db", sql_dir: str = "sql_queries"):
        self.db_path = db_path
        self.sql_dir = Path(sql_dir)
        self.conn = None
        self.results = {}
        self.performance_metrics = {}
        self.errors = []
        self.warnings = []
        
    def connect_database(self) -> bool:
        """Connect to SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            print(f"✓ Connected to database: {self.db_path}")
            return True
        except Exception as e:
            self.errors.append(f"Database connection failed: {str(e)}")
            print(f"✗ Failed to connect to database: {e}")
            return False
    
    def extract_queries_from_sql(self, content: str) -> Dict[str, str]:
        """Extract individual queries from SQL file by splitting on Query comments"""
        queries = {}
        
        # Split by "-- Query" comments
        query_blocks = re.split(r'(?=-- Query)', content)
        
        for block in query_blocks:
            if not block.strip():
                continue
            
            lines = block.strip().split('\n')
            
            # Extract query name from first line
            query_name = "Unknown"
            query_sql_lines = []
            
            for i, line in enumerate(lines):
                if i == 0 and line.startswith('-- Query'):
                    # Extract query name (e.g., "-- Query 1.1: Description")
                    query_name = line.replace('--', '').strip()
                else:
                    query_sql_lines.append(line)
            
            # Build SQL query
            query_sql = '\n'.join(query_sql_lines).strip()
            
            # Remove trailing semicolon if present
            if query_sql.endswith(';'):
                query_sql = query_sql[:-1].strip()
            
            # Remove empty lines and comment-only lines
            clean_lines = [l for l in query_sql.split('\n') 
                          if l.strip() and not l.strip().startswith('--')]
            query_sql_clean = '\n'.join(clean_lines).strip()
            
            if query_sql_clean and 'SELECT' in query_sql_clean.upper():
                queries[query_name] = query_sql_clean
        
        return queries
    
    def load_sql_file(self, filepath: Path) -> Dict[str, str]:
        """Load SQL file and extract queries"""
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            
            queries = self.extract_queries_from_sql(content)
            return queries
        except Exception as e:
            self.errors.append(f"Failed to load SQL file {filepath}: {str(e)}")
            return {}
    
    def execute_query(self, query_name: str, query_sql: str) -> Tuple[pd.DataFrame, float, str]:
        """Execute a single query and return results with timing"""
        try:
            start_time = time.time()
            df = pd.read_sql_query(query_sql, self.conn)
            execution_time = time.time() - start_time
            
            status = "SUCCESS"
            return df, execution_time, status
        except Exception as e:
            error_msg = str(e)
            self.errors.append(f"{query_name}: {error_msg}")
            return pd.DataFrame(), 0, f"ERROR: {error_msg}"
    
    def validate_query_result(self, query_name: str, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate query results"""
        validation = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "has_nulls": df.isnull().any().any(),
            "null_count": df.isnull().sum().sum(),
            "is_empty": len(df) == 0,
            "issues": []
        }
        
        # Check for common issues
        if len(df) == 0:
            validation["issues"].append("Result set is empty")
        
        if len(df.columns) == 0:
            validation["issues"].append("No columns in result set")
        
        return validation
    
    def execute_business_case(self, bc_num: int, bc_slug: str) -> Dict[str, Any]:
        """Execute all queries for a business case using corrected files"""
        print(f"\n{'='*70}")
        print(f"Business Case {bc_num}: {bc_slug.upper()}")
        print('='*70)
        
        bc_results = {
            "bc_number": bc_num,
            "bc_slug": bc_slug,
            "queries": {},
            "total_queries": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "total_time": 0.0,
            "avg_time": 0.0
        }
        
        # Construct filename for corrected queries
        filename = f"bc{bc_num}_{bc_slug}_corrected.sql"
        filepath = self.sql_dir / filename
        
        if not filepath.exists():
            self.warnings.append(f"Query file not found: {filepath}")
            print(f"  ✗ Query file not found: {filename}")
            return bc_results
        
        # Load queries
        queries = self.load_sql_file(filepath)
        
        if not queries:
            self.warnings.append(f"No queries found in {filename}")
            print(f"  ✗ No queries parsed from {filename}")
            return bc_results
        
        bc_results["total_queries"] = len(queries)
        print(f"  Found {len(queries)} queries")
        
        # Execute each query
        for query_name, query_sql in queries.items():
            print(f"\n  > {query_name}")
            
            df, exec_time, status = self.execute_query(query_name, query_sql)
            validation = self.validate_query_result(query_name, df)
            
            query_result = {
                "status": status,
                "execution_time": round(exec_time, 3),
                "row_count": len(df),
                "column_count": len(df.columns),
                "validation": validation
            }
            
            bc_results["queries"][query_name] = query_result
            bc_results["total_time"] += exec_time
            
            if status == "SUCCESS":
                bc_results["successful_queries"] += 1
                print(f"    ✓ SUCCESS | Time: {exec_time:.3f}s | Rows: {len(df):,} | Cols: {len(df.columns)}")
                
                # Show column names
                if len(df.columns) > 0:
                    cols_str = ", ".join(df.columns[:5])
                    if len(df.columns) > 5:
                        cols_str += f", ... +{len(df.columns)-5}"
                    print(f"    Columns: {cols_str}")
                
                # Store result for later use
                self.results[query_name] = df
                self.performance_metrics[query_name] = exec_time
            else:
                bc_results["failed_queries"] += 1
                print(f"    ✗ {status}")
        
        if bc_results["total_queries"] > 0:
            bc_results["avg_time"] = bc_results["total_time"] / bc_results["total_queries"]
        
        return bc_results
    
    def execute_all_queries(self) -> Dict[str, Any]:
        """Execute all queries across all business cases"""
        print("\n" + "="*70)
        print("PHASE 4: ANALYTICAL SQL QUERIES EXECUTION (CORRECTED)")
        print("="*70)
        print(f"Execution Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Database: {self.db_path}")
        print(f"SQL Directory: {self.sql_dir}")
        
        # Connect to database
        if not self.connect_database():
            return None
        
        # Business cases to execute
        business_cases = [
            (1, "transaction_dynamics"),
            (2, "device_engagement"),
            (3, "insurance_penetration"),
            (4, "market_expansion"),
            (5, "user_engagement_growth"),
        ]
        
        execution_summary = {
            "timestamp": datetime.now().isoformat(),
            "database": self.db_path,
            "business_cases": {},
            "total_queries": 0,
            "total_successful": 0,
            "total_failed": 0,
            "total_execution_time": 0.0,
            "avg_query_time": 0.0,
            "overall_status": "PENDING"
        }
        
        overall_start = time.time()
        
        # Execute each business case
        for bc_num, bc_slug in business_cases:
            bc_result = self.execute_business_case(bc_num, bc_slug)
            execution_summary["business_cases"][f"bc{bc_num}"] = bc_result
            
            execution_summary["total_queries"] += bc_result["total_queries"]
            execution_summary["total_successful"] += bc_result["successful_queries"]
            execution_summary["total_failed"] += bc_result["failed_queries"]
        
        overall_time = time.time() - overall_start
        execution_summary["total_execution_time"] = round(overall_time, 2)
        
        if execution_summary["total_queries"] > 0:
            execution_summary["avg_query_time"] = round(
                execution_summary["total_execution_time"] / execution_summary["total_queries"], 3
            )
        
        # Determine overall status
        if execution_summary["total_failed"] == 0 and execution_summary["total_successful"] > 0:
            execution_summary["overall_status"] = "SUCCESS"
        elif execution_summary["total_successful"] > 0:
            execution_summary["overall_status"] = "PARTIAL_SUCCESS"
        else:
            execution_summary["overall_status"] = "FAILED"
        
        # Add errors and warnings
        execution_summary["errors"] = self.errors
        execution_summary["warnings"] = self.warnings
        execution_summary["error_count"] = len(self.errors)
        execution_summary["warning_count"] = len(self.warnings)
        
        # Close connection
        if self.conn:
            self.conn.close()
        
        return execution_summary
    
    def print_summary(self, summary: Dict[str, Any]):
        """Print execution summary"""
        print("\n" + "="*70)
        print("EXECUTION SUMMARY")
        print("="*70)
        print(f"Overall Status: {summary['overall_status']}")
        print(f"Total Execution Time: {summary['total_execution_time']:.2f}s")
        print(f"Average Query Time: {summary['avg_query_time']:.3f}s")
        print(f"\nTotal Queries: {summary['total_queries']}")
        print(f"  Successful: {summary['total_successful']} ✓")
        print(f"  Failed: {summary['total_failed']} ✗")
        print(f"  Success Rate: {(summary['total_successful']/max(summary['total_queries'], 1)*100):.1f}%")
        
        print(f"\nBusiness Case Results:")
        for bc_key, bc_data in summary["business_cases"].items():
            if bc_data["total_queries"] > 0:
                success_rate = (bc_data["successful_queries"] / bc_data["total_queries"]) * 100
                print(f"  {bc_key}: {bc_data['successful_queries']}/{bc_data['total_queries']} queries " +
                      f"({success_rate:.0f}%) | {bc_data['total_time']:.2f}s total")
        
        if summary["errors"]:
            print(f"\nErrors ({len(summary['errors'])}):")
            for error in summary["errors"][:5]:
                error_short = error[:65] + "..." if len(error) > 65 else error
                print(f"  - {error_short}")
            if len(summary["errors"]) > 5:
                print(f"  ... and {len(summary['errors']) - 5} more errors")
        
        print("\n" + "="*70)
    
    def save_summary_json(self, summary: Dict[str, Any], output_file: str = "phase4_execution_summary.json"):
        """Save execution summary to JSON"""
        try:
            with open(output_file, 'w') as f:
                json.dump(summary, f, indent=2, default=str)
            print(f"✓ Summary saved to {output_file}")
            print(f"✓ {summary['total_successful']} queries executed successfully")
            if summary['total_failed'] > 0:
                print(f"⚠ {summary['total_failed']} queries failed")
        except Exception as e:
            print(f"✗ Failed to save summary: {e}")
    
    def export_query_results(self, output_dir: str = "phase4_results"):
        """Export all successful query results to CSV files"""
        try:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
            
            exported_count = 0
            for query_name, df in self.results.items():
                if len(df) > 0:
                    filename = f"{query_name.replace(' ', '_').replace(':', '')}.csv"
                    filepath = output_path / filename
                    df.to_csv(filepath, index=False)
                    exported_count += 1
            
            print(f"✓ Exported {exported_count} query results to {output_dir}/")
        except Exception as e:
            print(f"✗ Failed to export results: {e}")


def main():
    """Main execution"""
    executor = Phase4QueryExecutorFixed(
        db_path="phonpe_analytics.db",
        sql_dir="sql_queries"
    )
    
    # Execute all queries
    summary = executor.execute_all_queries()
    
    if summary:
        # Print summary
        executor.print_summary(summary)
        
        # Save to JSON
        executor.save_summary_json(summary, "phase4_execution_summary.json")
        
        # Export results to CSV
        executor.export_query_results("phase4_results")
        
        # Return status code
        if summary["overall_status"] == "SUCCESS":
            return 0
        elif summary["overall_status"] == "PARTIAL_SUCCESS":
            return 1
        else:
            return 2
    else:
        print("✗ Execution failed")
        return 2


if __name__ == "__main__":
    sys.exit(main())
