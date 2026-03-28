"""
Database connection and data loading module.
Supports both CSV-based and SQL database sources.
Integrates data standardization and validation.
"""

import pandas as pd
import os
from pathlib import Path
from typing import Optional, Dict, List
import logging

# Configuration
DATA_DIR = Path(__file__).parent.parent.parent / "query_results"
DATA_EXTRACTS_DIR = Path(__file__).parent.parent.parent / "data_extracts"

# Import standardization utilities
try:
    from utils.data_standardizer import standardize_dataframe, calculate_active_users
    from utils.validation import (
        validate_dataframe,
        safe_numeric_column,
        safe_string_column,
        ValidationError,
    )
    from config.column_mappings import find_column
    UTILS_AVAILABLE = True
except ImportError:
    try:
        from .data_standardizer import standardize_dataframe, calculate_active_users
        from .validation import (
            validate_dataframe,
            safe_numeric_column,
            safe_string_column,
            ValidationError,
        )
        from ..config.column_mappings import find_column
        UTILS_AVAILABLE = True
    except ImportError as e:
        UTILS_AVAILABLE = False

logger = logging.getLogger(__name__)

# Cache for loaded data
_data_cache: Dict[str, pd.DataFrame] = {}


def load_query_data(query_name: str, refresh: bool = False) -> pd.DataFrame:
    """
    Load data from CSV query results with standardization.
    
    Args:
        query_name: Name of the query CSV file (without .csv extension)
        refresh: Force reload from disk
        
    Returns:
        DataFrame with standardized column names and validated data
    """
    global _data_cache
    
    if not refresh and query_name in _data_cache:
        return _data_cache[query_name].copy()
    
    # Try to find the CSV file
    csv_path = DATA_DIR / f"{query_name}.csv"
    
    if not csv_path.exists():
        # Try data_extracts directory
        csv_path = DATA_EXTRACTS_DIR / f"{query_name}.csv"
    
    if not csv_path.exists():
        raise FileNotFoundError(f"Query file not found: {query_name}")
    
    try:
        df = pd.read_csv(csv_path)
        logger.debug(f"Loaded raw CSV {query_name}: {len(df)} rows, {len(df.columns)} cols")
        
        # Apply standardization if utilities available
        if UTILS_AVAILABLE:
            try:
                df = standardize_dataframe(df, query_name)
                logger.debug(f"Standardized {query_name}")
            except Exception as e:
                logger.warning(f"Standardization failed for {query_name}: {e}")
            
            # Validate data
            try:
                is_valid, errors = validate_dataframe(df, query_name, strict=False)
                if not is_valid:
                    logger.warning(f"Validation warnings for {query_name}: {errors}")
            except Exception as e:
                logger.warning(f"Validation check failed: {e}")
        
        _data_cache[query_name] = df.copy()
        logger.info(f"✓ Loaded {query_name}: {len(df)} rows, {len(df.columns)} columns")
        return df.copy()
    except Exception as e:
        logger.error(f"Error loading {query_name}: {str(e)}")
        raise


def get_kpi_metrics() -> Dict[str, float]:
    """
    Get KPI metrics for the home dashboard with proper column handling.
    
    Returns:
        Dictionary with KPI values
    """
    metrics = {}
    
    try:
        # Total transactions
        try:
            trans_df = load_query_data("Query_4.1_State-Level_Transaction_Performance_Analytics_(Comprehensive)")
            if not trans_df.empty and UTILS_AVAILABLE:
                trans_count = safe_numeric_column(trans_df, "transaction_count", default=0).sum()
                trans_amount = safe_numeric_column(trans_df, "transaction_amount", default=0).sum()
                metrics['total_transactions'] = float(trans_count)
                metrics['total_transaction_amount'] = float(trans_amount)
            else:
                metrics['total_transactions'] = 0
                metrics['total_transaction_amount'] = 0
        except Exception as e:
            logger.warning(f"Error getting transaction metrics: {e}")
            metrics['total_transactions'] = 0
            metrics['total_transaction_amount'] = 0
        
        # Total users
        try:
            user_df = load_query_data("Query_2.1_State-Level_User_Registration_&_Engagement_Metrics")
            if not user_df.empty:
                if UTILS_AVAILABLE:
                    # Calculate active users if not present
                    user_df = calculate_active_users(user_df)
                    registered = safe_numeric_column(user_df, "registered_users", default=0).sum()
                    active = safe_numeric_column(user_df, "active_users", default=0).sum()
                else:
                    registered = user_df['registered_users'].sum() if 'registered_users' in user_df.columns else 0
                    active = user_df['active_users'].sum() if 'active_users' in user_df.columns else registered * 0.7
                
                metrics['total_users'] = float(registered)
                metrics['active_users'] = float(active)
            else:
                metrics['total_users'] = 0
                metrics['active_users'] = 0
        except Exception as e:
            logger.warning(f"Error getting user metrics: {e}")
            metrics['total_users'] = 0
            metrics['active_users'] = 0
        
        # Insurance metrics
        try:
            ins_df = load_query_data("Query_3.1_Insurance_Growth_Trajectory_by_State_&_Quarter")
            if not ins_df.empty and UTILS_AVAILABLE:
                premium = safe_numeric_column(ins_df, "premium_amount", default=0).sum()
                trans = safe_numeric_column(ins_df, "insurance_transactions", default=0).sum()
                metrics['total_insurance_premiums'] = float(premium)
                metrics['insurance_count'] = float(trans)
            else:
                metrics['total_insurance_premiums'] = 0
                metrics['insurance_count'] = 0
        except Exception as e:
            logger.warning(f"Error getting insurance metrics: {e}")
            metrics['total_insurance_premiums'] = 0
            metrics['insurance_count'] = 0
        
        return metrics
    except Exception as e:
        logger.error(f"Error calculating KPI metrics: {str(e)}")
        return {
            'total_transactions': 0,
            'total_transaction_amount': 0,
            'total_users': 0,
            'active_users': 0,
            'total_insurance_premiums': 0,
            'insurance_count': 0,
        }


def get_transaction_data(state: Optional[str] = None, 
                        category: Optional[str] = None) -> pd.DataFrame:
    """
    Get transaction data with optional filters.
    
    Args:
        state: Filter by state
        category: Filter by category
        
    Returns:
        Filtered transaction DataFrame
    """
    try:
        df = load_query_data("Query_4.1_State-Level_Transaction_Performance_Analytics_(Comprehensive)")
        
        if df.empty:
            return df
        
        # Use find_column for safe access (if available)
        if UTILS_AVAILABLE:
            state_col = find_column(df, "state")
            category_col = find_column(df, "category") or find_column(df, "type")
        else:
            state_col = "state" if "state" in df.columns else None
            category_col = "category" if "category" in df.columns else "type" if "type" in df.columns else None
        
        if state and state_col:
            df = df[df[state_col].str.contains(state, case=False, na=False)]
        
        if category and category_col:
            df = df[df[category_col].str.contains(category, case=False, na=False)]
        
        return df.reset_index(drop=True)
    except Exception as e:
        logger.error(f"Error getting transaction data: {e}")
        return pd.DataFrame()


def get_user_data(state: Optional[str] = None) -> pd.DataFrame:
    """
    Get user engagement data with optional filters and calculated active users.
    
    Args:
        state: Filter by state
        
    Returns:
        Filtered user DataFrame with active_users calculated if needed
    """
    try:
        df = load_query_data("Query_2.1_State-Level_User_Registration_&_Engagement_Metrics")
        
        if df.empty:
            return df
        
        # Calculate active users if not present
        if UTILS_AVAILABLE and "active_users" not in df.columns:
            df = calculate_active_users(df)
        
        # Filter by state if specified
        if state:
            state_col = find_column(df, "state") if UTILS_AVAILABLE else "state"
            if state_col and state_col in df.columns:
                df = df[df[state_col].str.contains(state, case=False, na=False)]
        
        return df.reset_index(drop=True)
    except Exception as e:
        logger.error(f"Error getting user data: {e}")
        return pd.DataFrame()


def get_insurance_data(state: Optional[str] = None,
                      category: Optional[str] = None) -> pd.DataFrame:
    """
    Get insurance data with optional filters.
    
    Args:
        state: Filter by state
        category: Filter by category
        
    Returns:
        Filtered insurance DataFrame
    """
    try:
        df = load_query_data("Query_3.1_Insurance_Growth_Trajectory_by_State_&_Quarter")
        
        if df.empty:
            return df
        
        # Use find_column for safe access
        if UTILS_AVAILABLE:
            state_col = find_column(df, "state")
            category_col = find_column(df, "category") or find_column(df, "type")
        else:
            state_col = "state" if "state" in df.columns else None
            category_col = "category" if "category" in df.columns else "type" if "type" in df.columns else None
        
        if state and state_col:
            df = df[df[state_col].str.contains(state, case=False, na=False)]
        
        if category and category_col:
            df = df[df[category_col].str.contains(category, case=False, na=False)]
        
        return df.reset_index(drop=True)
    except Exception as e:
        logger.error(f"Error getting insurance data: {e}")
        return pd.DataFrame()


def list_available_queries() -> List[str]:
    """
    List all available query CSV files.
    
    Returns:
        List of available query names
    """
    queries = []
    
    if DATA_DIR.exists():
        queries.extend([f.stem for f in DATA_DIR.glob("*.csv")])
    
    if DATA_EXTRACTS_DIR.exists():
        queries.extend([f.stem for f in DATA_EXTRACTS_DIR.glob("*.csv")])
    
    return sorted(list(set(queries)))


def get_states() -> List[str]:
    """
    Get list of all states in the dataset.
    
    Returns:
        Sorted list of state names
    """
    states = set()
    
    try:
        df = load_query_data("Query_2.1_State-Level_User_Registration_&_Engagement_Metrics")
        if 'state' in df.columns:
            states.update(df['state'].unique())
    except:
        pass
    
    try:
        df = load_query_data("Query_4.1_State-Level_Transaction_Performance_Analytics_(Comprehensive)")
        if 'state' in df.columns:
            states.update(df['state'].unique())
    except:
        pass
    
    return sorted([s for s in states if pd.notna(s)])


def get_quarters() -> List[str]:
    """
    Get list of all quarters in the dataset.
    
    Returns:
        Sorted list of quarters
    """
    quarters = set()
    
    try:
        df = load_query_data("Query_1.1_Quarterly_Transaction_Growth_by_State_(YoY_Analysis)")
        if 'quarter' in df.columns or 'q' in df.columns.str.lower():
            col = 'quarter' if 'quarter' in df.columns else [c for c in df.columns if 'q' in c.lower()][0]
            quarters.update(df[col].unique())
    except:
        pass
    
    return sorted([q for q in quarters if pd.notna(q)])


def clear_cache():
    """Clear the data cache."""
    global _data_cache
    _data_cache = {}
