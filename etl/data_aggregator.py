"""
Phase 3: ETL Pipeline - Data Aggregator Module
Computes derived metrics, aggregations, and feature engineering
Author: PhonePe Analytics Team
Version: 1.0
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataAggregator:
    """
    Compute aggregations, metrics, and features from transaction data
    Handles growth calculations, market share, rankings, and trend analysis
    """
    
    def __init__(self):
        self.logger = logger
        self.metrics_computed = {}
    
    def aggregate_by_quarter(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aggregate data by year-quarter"""
        if 'year' not in df.columns or 'quarter' not in df.columns:
            return df
        
        df = df.copy()
        
        # Group by temporal and geographic dimensions
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        groupby_cols = [col for col in ['year', 'quarter', 'level', 'region', 'category', 'type', 'device', 'entity_type', 'entity_name'] 
                        if col in df.columns]
        
        if numeric_cols.empty or not groupby_cols:
            return df
        
        aggregated = df.groupby(groupby_cols, as_index=False)[numeric_cols].sum()
        
        self.logger.info(f"✓ Aggregated by quarter: {len(df)} → {len(aggregated)} rows")
        return aggregated
    
    def compute_growth_rate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute period-over-period growth rates"""
        df = df.copy()
        
        if 'year' not in df.columns or 'quarter' not in df.columns:
            return df
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        # Sort by time period
        df = df.sort_values(['year', 'quarter'])
        
        # Calculate growth for each region/category
        for col in numeric_cols:
            growth_col = f'{col}_growth_pct'
            df[growth_col] = df.groupby([c for c in ['region', 'category', 'type', 'device'] if c in df.columns])[col].pct_change() * 100
            df[growth_col] = df[growth_col].fillna(0)
        
        self.logger.info(f"✓ Computed growth rates for {len(numeric_cols)} numeric columns")
        return df
    
    def calculate_market_share(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate market share percentages"""
        df = df.copy()
        
        numeric_cols = [col for col in df.columns if 'amount' in col.lower() or 'count' in col.lower()]
        
        for col in numeric_cols:
            # Market share by region
            if 'region' in df.columns:
                total = df[col].sum()
                if total > 0:
                    df[f'{col}_market_share_pct'] = (df[col] / total) * 100
        
        self.logger.info(f"✓ Calculated market share for {len(numeric_cols)} columns")
        return df
    
    def compute_user_engagement_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute user engagement metrics"""
        df = df.copy()
        
        # App opens per registered user
        if 'app_opens' in df.columns and 'registered_users' in df.columns:
            df['app_opens_per_user'] = df['app_opens'] / (df['registered_users'] + 1)
            self.logger.info(f"✓ Computed app_opens_per_user engagement metric")
        
        # Transaction per user
        if 'count' in df.columns and 'registered_users' in df.columns:
            df['transactions_per_user'] = df['count'] / (df['registered_users'] + 1)
            self.logger.info(f"✓ Computed transactions_per_user engagement metric")
        
        return df
    
    def identify_top_performers(self, df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
        """Identify top N performers by metric"""
        """
        Identify and rank top performers
        """
        df = df.copy()
        
        # Add ranking column
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if numeric_cols.empty:
            return df
        
        # Use count or amount as ranking metric
        ranking_col = 'count' if 'count' in df.columns else numeric_cols[0]
        
        if 'region' in df.columns:
            df['rank'] = df.groupby(['year', 'quarter'] if 'year' in df.columns else [])[ranking_col].rank(ascending=False)
        
        self.logger.info(f"✓ Identified and ranked top performers")
        return df
    
    def compute_regional_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute region-specific metrics"""
        df = df.copy()
        
        if 'region' not in df.columns:
            return df
        
        # Regional concentration (Herfindahl index approximation)
        numeric_cols = [col for col in df.columns if 'amount' in col.lower() or 'count' in col.lower()]
        
        for col in numeric_cols:
            total = df[col].sum()
            if total > 0:
                regional_shares = (df[col] / total) ** 2
                concentration = regional_shares.sum()
                self.metrics_computed[f'{col}_concentration'] = concentration
        
        self.logger.info(f"✓ Computed regional metrics")
        return df
    
    def compute_quarterly_seasonality(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute seasonal adjustment factors"""
        df = df.copy()
        
        if 'quarter' not in df.columns:
            return df
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            # Average by quarter
            quarterly_avg = df.groupby('quarter')[col].mean()
            overall_avg = df[col].mean()
            
            # Seasonal factor
            seasonal_factor = quarterly_avg / overall_avg
            df[f'{col}_seasonal_factor'] = df['quarter'].map(seasonal_factor)
        
        self.logger.info(f"✓ Computed quarterly seasonality factors")
        return df
    
    def get_summary_statistics(self, df: pd.DataFrame) -> Dict:
        """Get summary statistics of aggregated data"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        summary = {}
        for col in numeric_cols:
            summary[col] = {
                'mean': df[col].mean(),
                'median': df[col].median(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max(),
                'total': df[col].sum()
            }
        
        return summary


if __name__ == '__main__':
    # Example usage
    aggregator = DataAggregator()
    print("DataAggregator module loaded successfully")
