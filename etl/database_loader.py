"""
Phase 3: ETL Pipeline - Database Loader Module
Handles database connections, insertions, batch operations
Author: PhonePe Analytics Team
Version: 1.0
"""

import pandas as pd
import sqlite3
from typing import Dict, List, Tuple, Optional
import logging
from sqlalchemy import create_engine
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseLoader:
    """
    Handle database operations for PhonePe analytics
    Supports both SQLite (development) and production databases
    """
    
    def __init__(self, database_url: str = None):
        """Initialize DatabaseLoader"""
        self.logger = logger
        self.engine = None
        self.connection = None
        self.load_statistics = {}
        
        if database_url:
            self.connect_database(database_url)
        else:
            # Use SQLite for development if no DB URL provided
            self.setup_sqlite()
    
    def setup_sqlite(self):
        """Setup SQLite database for development/testing"""
        try:
            sqlite_path = '/Users/emmidev/Documents/Phone Pe/phonpe_analytics.db'
            self.engine = create_engine(f'sqlite:///{sqlite_path}')
            self.connection = self.engine.connect()
            self.logger.info(f"✓ Connected to SQLite database: {sqlite_path}")
            return True
        except Exception as e:
            self.logger.error(f"✗ Failed to connect to SQLite: {str(e)}")
            return False
    
    def connect_database(self, connection_string: str) -> bool:
        """Connect to PostgreSQL or MySQL database"""
        try:
            self.engine = create_engine(connection_string, pool_size=10, max_overflow=20)
            self.connection = self.engine.connect()
            self.logger.info(f"✓ Connected to database")
            return True
        except Exception as e:
            self.logger.error(f"✗ Database connection failed: {str(e)}")
            return False
    
    def insert_aggregated_transaction(self, df: pd.DataFrame) -> int:
        """Insert aggregated transaction data"""
        try:
            table_name = 'fact_aggregated_transaction'
            records = df.to_sql(table_name, self.connection, if_exists='append', index=False)
            self.logger.info(f"✓ Inserted {records} records into {table_name}")
            self.load_statistics[table_name] = records
            return records
        except Exception as e:
            self.logger.error(f"✗ Failed to insert {table_name}: {str(e)}")
            return 0
    
    def insert_aggregated_user(self, df: pd.DataFrame) -> int:
        """Insert aggregated user data"""
        try:
            table_name = 'fact_aggregated_user'
            records = df.to_sql(table_name, self.connection, if_exists='append', index=False)
            self.logger.info(f"✓ Inserted {records} records into {table_name}")
            self.load_statistics[table_name] = records
            return records
        except Exception as e:
            self.logger.error(f"✗ Failed to insert {table_name}: {str(e)}")
            return 0
    
    def insert_aggregated_insurance(self, df: pd.DataFrame) -> int:
        """Insert aggregated insurance data"""
        try:
            table_name = 'fact_aggregated_insurance'
            records = df.to_sql(table_name, self.connection, if_exists='append', index=False)
            self.logger.info(f"✓ Inserted {records} records into {table_name}")
            self.load_statistics[table_name] = records
            return records
        except Exception as e:
            self.logger.error(f"✗ Failed to insert {table_name}: {str(e)}")
            return 0
    
    def insert_map_transaction(self, df: pd.DataFrame) -> int:
        """Insert map transaction data"""
        try:
            table_name = 'fact_map_transaction'
            records = df.to_sql(table_name, self.connection, if_exists='append', index=False)
            self.logger.info(f"✓ Inserted {records} records into {table_name}")
            self.load_statistics[table_name] = records
            return records
        except Exception as e:
            self.logger.error(f"✗ Failed to insert {table_name}: {str(e)}")
            return 0
    
    def insert_map_user(self, df: pd.DataFrame) -> int:
        """Insert map user data"""
        try:
            table_name = 'fact_map_user'
            records = df.to_sql(table_name, self.connection, if_exists='append', index=False)
            self.logger.info(f"✓ Inserted {records} records into {table_name}")
            self.load_statistics[table_name] = records
            return records
        except Exception as e:
            self.logger.error(f"✗ Failed to insert {table_name}: {str(e)}")
            return 0
    
    def insert_map_insurance(self, df: pd.DataFrame) -> int:
        """Insert map insurance data"""
        try:
            table_name = 'fact_map_insurance'
            records = df.to_sql(table_name, self.connection, if_exists='append', index=False)
            self.logger.info(f"✓ Inserted {records} records into {table_name}")
            self.load_statistics[table_name] = records
            return records
        except Exception as e:
            self.logger.error(f"✗ Failed to insert {table_name}: {str(e)}")
            return 0
    
    def insert_top_transaction(self, df: pd.DataFrame) -> int:
        """Insert top transaction data"""
        try:
            table_name = 'fact_top_transaction'
            records = df.to_sql(table_name, self.connection, if_exists='append', index=False)
            self.logger.info(f"✓ Inserted {records} records into {table_name}")
            self.load_statistics[table_name] = records
            return records
        except Exception as e:
            self.logger.error(f"✗ Failed to insert {table_name}: {str(e)}")
            return 0
    
    def insert_top_user(self, df: pd.DataFrame) -> int:
        """Insert top user data"""
        try:
            table_name = 'fact_top_user'
            records = df.to_sql(table_name, self.connection, if_exists='append', index=False)
            self.logger.info(f"✓ Inserted {records} records into {table_name}")
            self.load_statistics[table_name] = records
            return records
        except Exception as e:
            self.logger.error(f"✗ Failed to insert {table_name}: {str(e)}")
            return 0
    
    def insert_top_insurance(self, df: pd.DataFrame) -> int:
        """Insert top insurance data"""
        try:
            table_name = 'fact_top_insurance'
            records = df.to_sql(table_name, self.connection, if_exists='append', index=False)
            self.logger.info(f"✓ Inserted {records} records into {table_name}")
            self.load_statistics[table_name] = records
            return records
        except Exception as e:
            self.logger.error(f"✗ Failed to insert {table_name}: {str(e)}")
            return 0
    
    def batch_insert(self, df: pd.DataFrame, table_name: str, batch_size: int = 1000) -> int:
        """Insert data in batches for better performance"""
        try:
            total_records = 0
            num_batches = (len(df) + batch_size - 1) // batch_size
            
            for i in range(num_batches):
                start_idx = i * batch_size
                end_idx = min((i + 1) * batch_size, len(df))
                batch = df.iloc[start_idx:end_idx]
                
                records = batch.to_sql(table_name, self.connection, if_exists='append', index=False)
                total_records += records
                
                self.logger.info(f"✓ Batch {i+1}/{num_batches} inserted ({records} records)")
            
            self.logger.info(f"✓ Batch insertion complete: {total_records} total records")
            return total_records
        except Exception as e:
            self.logger.error(f"✗ Batch insertion failed: {str(e)}")
            return 0
    
    def handle_duplicates(self, df: pd.DataFrame, table_name: str, key_columns: List[str]) -> Tuple[pd.DataFrame, int]:
        """Handle duplicate records (upsert logic)"""
        try:
            # For SQLite, we'll use drop_duplicates
            initial_rows = len(df)
            df = df.drop_duplicates(subset=key_columns, keep='first')
            removed = initial_rows - len(df)
            
            self.logger.info(f"✓ Removed {removed} duplicate records from {table_name}")
            return df, removed
        except Exception as e:
            self.logger.error(f"✗ Duplicate handling failed: {str(e)}")
            return df, 0
    
    def get_table_record_count(self, table_name: str) -> int:
        """Get record count from a specific table"""
        try:
            query = f"SELECT COUNT(*) as count FROM {table_name}"
            result = self.connection.execute(query).fetchall()
            count = result[0][0] if result else 0
            return count
        except Exception as e:
            self.logger.error(f"✗ Failed to get record count for {table_name}: {str(e)}")
            return 0
    
    def get_load_statistics(self) -> Dict:
        """Get statistics of data loaded"""
        stats = {
            'total_records': sum(self.load_statistics.values()),
            'tables_loaded': len(self.load_statistics),
            'by_table': self.load_statistics,
            'timestamp': datetime.now().isoformat()
        }
        return stats
    
    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.logger.info("✓ Database connection closed")


if __name__ == '__main__':
    # Example usage
    loader = DatabaseLoader()
    print("DatabaseLoader module loaded successfully")
