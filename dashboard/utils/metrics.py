"""
KPI and metrics calculation utilities.
Includes safe column access and standardized metric calculations.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional

# Try to import validation utilities
try:
    from utils.validation import safe_numeric_column, safe_string_column
    from config.column_mappings import find_column
    VALIDATION_AVAILABLE = True
except ImportError:
    try:
        from .validation import safe_numeric_column, safe_string_column
        from ..config.column_mappings import find_column
        VALIDATION_AVAILABLE = True
    except ImportError:
        VALIDATION_AVAILABLE = False
        safe_numeric_column = None
        safe_string_column = None
        find_column = None


def calculate_transaction_metrics() -> Dict[str, float]:
    """
    Calculate transaction-related KPIs with safe column access.
    
    Returns:
        Dictionary with transaction metrics
    """
    # Import locally to avoid circular imports
    try:
        from utils.database import load_query_data
    except ImportError:
        from .database import load_query_data
    
    metrics = {}
    
    try:
        df = load_query_data("Query_4.1_State-Level_Transaction_Performance_Analytics_(Comprehensive)")
        
        if df.empty:
            print("WARNING: Query_4.1 DataFrame is empty")
            return metrics
        
        print(f"DEBUG: Query_4.1 loaded - shape {df.shape}, columns: {list(df.columns)}")
        
        # Total transactions and amount - use safe access
        if VALIDATION_AVAILABLE:
            trans_count = safe_numeric_column(df, 'transaction_count', default=0)
            trans_amount = safe_numeric_column(df, 'transaction_amount', default=0)
            state_col = find_column(df, 'state')
        else:
            print("DEBUG: VALIDATION_AVAILABLE is False, using fallback column access")
            trans_count = pd.to_numeric(df['transaction_count'], errors='coerce').fillna(0) if 'transaction_count' in df.columns else pd.Series([0] * len(df))
            trans_amount = pd.to_numeric(df['transaction_amount'], errors='coerce').fillna(0) if 'transaction_amount' in df.columns else pd.Series([0] * len(df))
            state_col = 'state' if 'state' in df.columns else None
        
        trans_count_sum = float(trans_count.sum())
        trans_amount_sum = float(trans_amount.sum())
        
        print(f"DEBUG: trans_count_sum={trans_count_sum}, trans_amount_sum={trans_amount_sum}")
        
        metrics['total_transactions'] = trans_count_sum
        metrics['total_transaction_amount'] = trans_amount_sum
        
        # Average transaction size
        if trans_count_sum > 0:
            metrics['avg_transaction_size'] = float(trans_amount_sum / trans_count_sum)
        
        # Top states
        if state_col:
            try:
                top_states = df.nlargest(1, trans_count.name if hasattr(trans_count, 'name') else 'transaction_count')
                if not top_states.empty:
                    metrics['top_state'] = str(top_states[state_col].iloc[0])
                    metrics['top_state_transactions'] = float(trans_count.iloc[top_states.index[0]])
            except Exception as e:
                print(f"DEBUG: Error finding top state: {e}")
        
        print(f"DEBUG: Final metrics = {metrics}")
        return metrics
    except Exception as e:
        print(f"ERROR calculating transaction metrics: {e}")
        import traceback
        traceback.print_exc()
        return {}


def calculate_user_metrics() -> Dict[str, float]:
    """
    Calculate user-related KPIs with safe column access.
    
    Returns:
        Dictionary with user metrics
    """
    # Import locally to avoid circular imports
    try:
        from utils.database import load_query_data
    except ImportError:
        from .database import load_query_data
    
    metrics = {}
    
    try:
        df = load_query_data("Query_2.1_State-Level_User_Registration_&_Engagement_Metrics")
        
        if df.empty:
            print("WARNING: Query_2.1 DataFrame is empty")
            return metrics
        
        print(f"DEBUG: Query_2.1 loaded - shape {df.shape}, columns: {list(df.columns)}")
        
        # Use safe column access
        if VALIDATION_AVAILABLE:
            registered = safe_numeric_column(df, 'registered_users', default=0)
        else:
            print("DEBUG: VALIDATION_AVAILABLE is False, using fallback column access")
            registered = pd.to_numeric(df['registered_users'], errors='coerce').fillna(0) if 'registered_users' in df.columns else pd.Series([0] * len(df))
        
        registered_sum = float(registered.sum())
        print(f"DEBUG: registered_sum={registered_sum}")
        
        metrics['total_registered_users'] = registered_sum
        
        # Active users - use find_column if available
        if VALIDATION_AVAILABLE:
            active = safe_numeric_column(df, 'active_users', default=None)
            if active is not None and active.sum() > 0:
                metrics['total_active_users'] = float(active.sum())
            else:
                # Estimate from registered
                metrics['total_active_users'] = float(registered.sum() * 0.7)
        else:
            if 'active_users' in df.columns:
                active = pd.to_numeric(df['active_users'], errors='coerce').fillna(0)
                metrics['total_active_users'] = float(active.sum())
            else:
                metrics['total_active_users'] = float(registered.sum() * 0.7)
        
        # User growth - average per state
        metrics['avg_users_per_state'] = float(registered.mean())
        
        return metrics
    except Exception as e:
        print(f"Error calculating user metrics: {e}")
        return {}


def calculate_insurance_metrics() -> Dict[str, float]:
    """
    Calculate insurance-related KPIs with safe column access.
    
    Returns:
        Dictionary with insurance metrics
    """
    # Import locally to avoid circular imports
    try:
        from utils.database import load_query_data
    except ImportError:
        from .database import load_query_data
    
    metrics = {}
    
    try:
        df = load_query_data("Query_3.1_Insurance_Growth_Trajectory_by_State_&_Quarter")
        
        if df.empty:
            return metrics
        
        # Use safe column access
        if VALIDATION_AVAILABLE:
            trans_count = safe_numeric_column(df, 'insurance_transactions', default=0)
            premium = safe_numeric_column(df, 'premium_amount', default=0)
        else:
            # Try to find columns, falling back to default names
            trans_col = 'insurance_transactions' if 'insurance_transactions' in df.columns else 'quarterly_policies' if 'quarterly_policies' in df.columns else 'count'
            prem_col = 'premium_amount' if 'premium_amount' in df.columns else 'quarterly_premium'
            
            trans_count = pd.to_numeric(df[trans_col], errors='coerce').fillna(0) if trans_col in df.columns else pd.Series([0] * len(df))
            premium = pd.to_numeric(df[prem_col], errors='coerce').fillna(0) if prem_col in df.columns else pd.Series([0] * len(df))
        
        metrics['total_insurance_transactions'] = float(trans_count.sum())
        metrics['total_premium_amount'] = float(premium.sum())
        
        # Average premium
        total_trans = trans_count.sum()
        if total_trans > 0:
            metrics['avg_insurance_premium'] = float(premium.sum() / total_trans)
        
        return metrics
    except Exception as e:
        print(f"Error calculating insurance metrics: {e}")
        return {}


def calculate_growth_rate(current_period: pd.Series, 
                         previous_period: pd.Series) -> float:
    """
    Calculate YoY or period-over-period growth rate.
    
    Args:
        current_period: Current period values
        previous_period: Previous period values
        
    Returns:
        Growth rate as percentage
    """
    current_sum = current_period.sum()
    previous_sum = previous_period.sum()
    
    if previous_sum == 0:
        return 0.0
    
    return ((current_sum - previous_sum) / previous_sum) * 100


def calculate_market_share(total: float, part: float) -> float:
    """
    Calculate market share percentage.
    
    Args:
        total: Total value
        part: Part value
        
    Returns:
        Market share as percentage
    """
    if total == 0:
        return 0.0
    
    return (part / total) * 100


def get_top_performers(df: pd.DataFrame, 
                       value_col: str,
                       name_col: str = "state",
                       top_n: int = 5) -> pd.DataFrame:
    """
    Get top N performers by value with safe column access.
    
    Args:
        df: DataFrame with data
        value_col: Column to rank by
        name_col: Column with names
        top_n: Number of top performers
        
    Returns:
        DataFrame with top performers
    """
    if df.empty:
        return pd.DataFrame()
    
    try:
        # Find actual column names
        if VALIDATION_AVAILABLE:
            actual_value_col = find_column(df, value_col)
            actual_name_col = find_column(df, name_col)
        else:
            actual_value_col = value_col if value_col in df.columns else None
            actual_name_col = name_col if name_col in df.columns else None
        
        if not actual_value_col or not actual_name_col:
            return pd.DataFrame()
        
        result = df.nlargest(top_n, actual_value_col)[[actual_name_col, actual_value_col]]
        return result.reset_index(drop=True)
    except Exception as e:
        print(f"Error getting top performers: {e}")
        return pd.DataFrame()


def get_trending_items(df: pd.DataFrame,
                       time_col: str,
                       value_col: str,
                       group_col: str = "state",
                       min_periods: int = 2) -> pd.DataFrame:
    """
    Identify items with strongest growth trends with safe column access.
    
    Args:
        df: DataFrame with time series data
        time_col: Time column name
        value_col: Value column name
        group_col: Column to group by
        min_periods: Minimum time periods
        
    Returns:
        DataFrame with trend scores
    """
    if df.empty:
        return pd.DataFrame()
    
    results = []
    
    try:
        # Find actual column names
        if VALIDATION_AVAILABLE:
            actual_time = find_column(df, time_col)
            actual_value = find_column(df, value_col)
            actual_group = find_column(df, group_col)
        else:
            actual_time = time_col if time_col in df.columns else None
            actual_value = value_col if value_col in df.columns else None
            actual_group = group_col if group_col in df.columns else None
        
        if not all([actual_time, actual_value, actual_group]):
            return pd.DataFrame()
        
        for group in df[actual_group].unique():
            group_data = df[df[actual_group] == group].sort_values(actual_time)
            
            if len(group_data) >= min_periods:
                # Calculate simple trend (last - first) / first
                first_val = group_data[actual_value].iloc[0]
                last_val = group_data[actual_value].iloc[-1]
                
                if first_val > 0:
                    trend = ((last_val - first_val) / first_val) * 100
                    results.append({
                        'group': group,
                        'trend': trend,
                        'current': last_val
                    })
        
        if results:
            trend_df = pd.DataFrame(results)
            return trend_df.nlargest(10, 'trend')
        
        return pd.DataFrame()
    except Exception as e:
        print(f"Error calculating trends: {e}")
        return pd.DataFrame()


def get_correlation_matrix(df: pd.DataFrame, 
                          numeric_cols: list = None) -> pd.DataFrame:
    """
    Calculate correlation matrix for numeric columns.
    
    Args:
        df: DataFrame with data
        numeric_cols: Specific columns to use (optional)
        
    Returns:
        Correlation matrix DataFrame
    """
    if numeric_cols:
        return df[numeric_cols].corr()
    else:
        return df.select_dtypes(include=[np.number]).corr()
