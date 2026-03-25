"""
Phase 3: ETL Pipeline - Data Transformer Module
Cleans, standardizes, normalizes, and enriches data
Author: Aghason Emmanuel Ibeabuchi
Version: 1.0
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataTransformer:
    """
    Transform and clean PhonePe transaction data
    Handles standardization, normalization, deduplication, and enrichment
    """
    
    def __init__(self):
        self.logger = logger
        self.transformation_log = []
    
    def standardize_state_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize state names to consistent format"""
        df = df.copy()
        
        if 'region' not in df.columns:
            return df
        
        # Mapping for common spelling variations
        state_mappings = {
            'andaman-&-nicobar-islands': 'Andaman & Nicobar Islands',
            'andhra-pradesh': 'Andhra Pradesh',
            'arunachal-pradesh': 'Arunachal Pradesh',
            'assam': 'Assam',
            'bihar': 'Bihar',
            'chhattisgarh': 'Chhattisgarh',
            'chandigarh': 'Chandigarh',
            'delhi': 'Delhi',
            'goa': 'Goa',
            'gujarat': 'Gujarat',
            'haryana': 'Haryana',
            'himachal-pradesh': 'Himachal Pradesh',
            'jharkhand': 'Jharkhand',
            'karnataka': 'Karnataka',
            'kerala': 'Kerala',
            'madhya-pradesh': 'Madhya Pradesh',
            'maharashtra': 'Maharashtra',
            'manipur': 'Manipur',
            'meghalaya': 'Meghalaya',
            'mizoram': 'Mizoram',
            'nagaland': 'Nagaland',
            'odisha': 'Odisha',
            'puducherry': 'Puducherry',
            'punjab': 'Punjab',
            'rajasthan': 'Rajasthan',
            'sikkim': 'Sikkim',
            'tamil-nadu': 'Tamil Nadu',
            'telangana': 'Telangana',
            'tripura': 'Tripura',
            'uttar-pradesh': 'Uttar Pradesh',
            'uttarakhand': 'Uttarakhand',
            'west-bengal': 'West Bengal',
            'ladakh': 'Ladakh',
            'jammu-&-kashmir': 'Jammu & Kashmir',
            'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra & Nagar Haveli & Daman & Diu',
            'lakshadweep': 'Lakshadweep'
        }
        
        df['region'] = df['region'].fillna('Unknown').str.lower()
        df['region'] = df['region'].map(lambda x: state_mappings.get(x, x.title()))
        
        self.logger.info(f"✓ Standardized state names: {df['region'].nunique()} unique states")
        return df
    
    def standardize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names to lowercase with underscores"""
        df = df.copy()
        df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
        return df
    
    def handle_missing_values(self, df: pd.DataFrame, strategy: str = 'forward_fill') -> pd.DataFrame:
        """Handle missing values with specified strategy"""
        df = df.copy()
        
        if strategy == 'drop':
            initial_rows = len(df)
            df = df.dropna()
            dropped = initial_rows - len(df)
            self.logger.info(f"✓ Dropped {dropped} rows with missing values")
        
        elif strategy == 'forward_fill':
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = df[numeric_cols].fillna(0)
            
            categorical_cols = df.select_dtypes(include=['object']).columns
            df[categorical_cols] = df[categorical_cols].fillna('Unknown')
            
            self.logger.info(f"✓ Forward filled missing values")
        
        return df
    
    def normalize_numeric_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize numeric columns (convert to appropriate types)"""
        df = df.copy()
        
        # Count/quantity columns should be integers
        count_cols = [col for col in df.columns if 'count' in col.lower() or 'users' in col.lower() or 'opens' in col.lower()]
        for col in count_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype('int64')
        
        # Amount/value columns should be decimal
        amount_cols = [col for col in df.columns if 'amount' in col.lower() or 'value' in col.lower()]
        for col in amount_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype('float64')
        
        self.logger.info(f"✓ Normalized numeric columns: {len(count_cols) + len(amount_cols)} columns")
        return df
    
    def remove_duplicates(self, df: pd.DataFrame, subset: List[str] = None) -> pd.DataFrame:
        """Remove duplicate rows"""
        df = df.copy()
        initial_rows = len(df)
        
        if subset:
            df = df.drop_duplicates(subset=subset, keep='first')
        else:
            df = df.drop_duplicates(keep='first')
        
        removed = initial_rows - len(df)
        self.logger.info(f"✓ Removed {removed} duplicate rows")
        return df
    
    def enrich_geographic_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enrich geographic data with additional attributes"""
        df = df.copy()
        
        # Add geographic levels if not present
        if 'level' not in df.columns:
            # Infer level from presence of district/pincode columns
            if 'level' not in df.columns:
                df['level'] = 'country'  # Default to country level
        
        self.logger.info(f"✓ Enriched geographic data")
        return df
    
    def add_audit_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add audit columns (created_at, updated_at)"""
        df = df.copy()
        
        from datetime import datetime
        now = datetime.now()
        
        if 'created_at' not in df.columns:
            df['created_at'] = now
        if 'updated_at' not in df.columns:
            df['updated_at'] = now
        
        return df
    
    def transform_aggregated_transaction(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform aggregated transaction data"""
        df = df.copy()
        df = self.standardize_column_names(df)
        df = self.standardize_state_names(df)
        df = self.normalize_numeric_columns(df)
        df = self.remove_duplicates(df)
        df = self.handle_missing_values(df, strategy='forward_fill')
        df = self.add_audit_columns(df)
        return df
    
    def transform_aggregated_user(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform aggregated user data"""
        df = df.copy()
        df = self.standardize_column_names(df)
        df = self.standardize_state_names(df)
        df = self.normalize_numeric_columns(df)
        df = self.remove_duplicates(df)
        df = self.handle_missing_values(df, strategy='forward_fill')
        df = self.add_audit_columns(df)
        return df
    
    def transform_map_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform map-level data"""
        df = df.copy()
        df = self.standardize_column_names(df)
        df = self.standardize_state_names(df)
        df = self.normalize_numeric_columns(df)
        df = self.remove_duplicates(df)
        df = self.handle_missing_values(df, strategy='forward_fill')
        df = self.enrich_geographic_data(df)
        df = self.add_audit_columns(df)
        return df
    
    def transform_top_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform top performers data"""
        df = df.copy()
        df = self.standardize_column_names(df)
        if 'state' in df.columns:
            df = self.standardize_state_names(df)
        df = self.normalize_numeric_columns(df)
        df = self.remove_duplicates(df)
        df = self.handle_missing_values(df, strategy='forward_fill')
        df = self.add_audit_columns(df)
        return df
    
    def get_transformation_report(self) -> Dict:
        """Get summary of transformations applied"""
        return {
            'transformations_applied': len(self.transformation_log),
            'timestamp': pd.Timestamp.now()
        }


if __name__ == '__main__':
    # Example usage
    transformer = DataTransformer()
    print("DataTransformer module loaded successfully")
