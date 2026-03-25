"""
Phase 3: ETL Pipeline - Data Loader Module
Loads data from CSV/JSON files with validation and temporal consistency checks
Author: PhonePe Analytics Team
Version: 1.0
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """
    Load and consolidate PhonePe transaction data from multiple CSV/JSON sources
    Handles aggregated, map, and top data types with validation
    """
    
    def __init__(self, data_path: str):
        """Initialize DataLoader with source directory path"""
        self.data_path = Path(data_path)
        self.logger = logger
        self.loaded_data = {}
        
    def load_aggregated_transaction(self) -> pd.DataFrame:
        """Load aggregated transaction CSV file"""
        try:
            file_path = self.data_path / 'aggregated_transaction.csv'
            df = pd.read_csv(file_path)
            self.logger.info(f"✓ Loaded aggregated_transaction: {len(df)} rows")
            return df
        except FileNotFoundError:
            self.logger.error(f"✗ File not found: {file_path}")
            return pd.DataFrame()
    
    def load_aggregated_user(self) -> pd.DataFrame:
        """Load aggregated user CSV file"""
        try:
            file_path = self.data_path / 'aggregated_user.csv'
            df = pd.read_csv(file_path)
            self.logger.info(f"✓ Loaded aggregated_user: {len(df)} rows")
            return df
        except FileNotFoundError:
            self.logger.error(f"✗ File not found: {file_path}")
            return pd.DataFrame()
    
    def load_aggregated_insurance(self) -> pd.DataFrame:
        """Load aggregated insurance CSV file"""
        try:
            file_path = self.data_path / 'aggregated_insurance.csv'
            df = pd.read_csv(file_path)
            self.logger.info(f"✓ Loaded aggregated_insurance: {len(df)} rows")
            return df
        except FileNotFoundError:
            self.logger.error(f"✗ File not found: {file_path}")
            return pd.DataFrame()
    
    def load_map_transaction(self) -> pd.DataFrame:
        """Load map transaction CSV file"""
        try:
            file_path = self.data_path / 'map_transaction.csv'
            df = pd.read_csv(file_path)
            self.logger.info(f"✓ Loaded map_transaction: {len(df)} rows")
            return df
        except FileNotFoundError:
            self.logger.error(f"✗ File not found: {file_path}")
            return pd.DataFrame()
    
    def load_map_user(self) -> pd.DataFrame:
        """Load map user CSV file"""
        try:
            file_path = self.data_path / 'map_user.csv'
            df = pd.read_csv(file_path)
            self.logger.info(f"✓ Loaded map_user: {len(df)} rows")
            return df
        except FileNotFoundError:
            self.logger.error(f"✗ File not found: {file_path}")
            return pd.DataFrame()
    
    def load_map_insurance(self) -> pd.DataFrame:
        """Load map insurance CSV file"""
        try:
            file_path = self.data_path / 'map_insurance.csv'
            df = pd.read_csv(file_path)
            self.logger.info(f"✓ Loaded map_insurance: {len(df)} rows")
            return df
        except FileNotFoundError:
            self.logger.error(f"✗ File not found: {file_path}")
            return pd.DataFrame()
    
    def load_top_transaction(self) -> pd.DataFrame:
        """Load top transaction CSV file"""
        try:
            file_path = self.data_path / 'top_transaction.csv'
            df = pd.read_csv(file_path)
            self.logger.info(f"✓ Loaded top_transaction: {len(df)} rows")
            return df
        except FileNotFoundError:
            self.logger.error(f"✗ File not found: {file_path}")
            return pd.DataFrame()
    
    def load_top_user(self) -> pd.DataFrame:
        """Load top user CSV file"""
        try:
            file_path = self.data_path / 'top_user.csv'
            df = pd.read_csv(file_path)
            self.logger.info(f"✓ Loaded top_user: {len(df)} rows")
            return df
        except FileNotFoundError:
            self.logger.error(f"✗ File not found: {file_path}")
            return pd.DataFrame()
    
    def load_top_insurance(self) -> pd.DataFrame:
        """Load top insurance CSV file"""
        try:
            file_path = self.data_path / 'top_insurance.csv'
            df = pd.read_csv(file_path)
            self.logger.info(f"✓ Loaded top_insurance: {len(df)} rows")
            return df
        except FileNotFoundError:
            self.logger.error(f"✗ File not found: {file_path}")
            return pd.DataFrame()
    
    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        """Load all 9 CSV files"""
        self.loaded_data = {
            'aggregated_transaction': self.load_aggregated_transaction(),
            'aggregated_user': self.load_aggregated_user(),
            'aggregated_insurance': self.load_aggregated_insurance(),
            'map_transaction': self.load_map_transaction(),
            'map_user': self.load_map_user(),
            'map_insurance': self.load_map_insurance(),
            'top_transaction': self.load_top_transaction(),
            'top_user': self.load_top_user(),
            'top_insurance': self.load_top_insurance(),
        }
        
        total_records = sum(len(df) for df in self.loaded_data.values())
        self.logger.info(f"\n✓ ALL DATA LOADED: {total_records} total records")
        return self.loaded_data
    
    def validate_temporal_consistency(self, df: pd.DataFrame, dataset_name: str) -> Tuple[bool, List[str]]:
        """Validate year/quarter consistency in temporal data"""
        issues = []
        
        if 'year' not in df.columns or 'quarter' not in df.columns:
            return True, []  # Not all datasets have temporal columns
        
        # Check for valid quarters (1-4)
        invalid_quarters = df[~df['quarter'].isin([1, 2, 3, 4])]
        if len(invalid_quarters) > 0:
            issues.append(f"Invalid quarters found: {invalid_quarters['quarter'].unique()}")
        
        # Check for valid years
        valid_years = range(2018, 2025)
        invalid_years = df[~df['year'].isin(valid_years)]
        if len(invalid_years) > 0:
            issues.append(f"Invalid years found: {invalid_years['year'].unique()}")
        
        if issues:
            self.logger.warning(f"⚠ {dataset_name} temporal issues: {issues}")
            return False, issues
        
        return True, []
    
    def get_data_summary(self) -> pd.DataFrame:
        """Get summary statistics of loaded data"""
        summary = []
        for name, df in self.loaded_data.items():
            summary.append({
                'Dataset': name,
                'Rows': len(df),
                'Columns': len(df.columns),
                'Memory (MB)': df.memory_usage(deep=True).sum() / (1024**2)
            })
        
        return pd.DataFrame(summary)


if __name__ == '__main__':
    # Example usage
    loader = DataLoader('/Users/emmidev/Documents/Phone Pe/data_extracts')
    data = loader.load_all_data()
    print(loader.get_data_summary())
