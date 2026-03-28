"""
Data standardization utilities for handling CSV variations.
Standardizes column names and data types across different data sources.
"""

import pandas as pd
import numpy as np
from typing import Optional
import logging
from config.column_mappings import (
    get_column_mapping,
    find_column,
    COLUMN_TYPES,
)

logger = logging.getLogger(__name__)


def standardize_dataframe(
    df: pd.DataFrame,
    query_name: str,
    rename_columns: bool = True,
    convert_types: bool = True,
    fill_nulls: bool = True,
) -> pd.DataFrame:
    """
    Standardize DataFrame by renaming columns and converting data types.
    
    Args:
        df: Input DataFrame
        query_name: Name of the query/file (for mapping lookup)
        rename_columns: Whether to rename columns to standard names
        convert_types: Whether to convert to standard data types
        fill_nulls: Whether to fill null values intelligently
        
    Returns:
        Standardized DataFrame
    """
    result = df.copy()
    
    # Step 1: Rename columns to standard names
    if rename_columns:
        mappings = get_column_mapping(query_name)
        if mappings:
            result = result.rename(columns=mappings)
            logger.debug(f"Renamed columns: {mappings}")
    
    # Step 2: Convert data types
    if convert_types:
        result = _convert_types(result, query_name)
    
    # Step 3: Handle null values
    if fill_nulls:
        result = _handle_nulls(result, query_name)
    
    logger.info(f"✓ Standardized {query_name}: {result.shape[0]} rows, {result.shape[1]} cols")
    return result


def _convert_types(df: pd.DataFrame, query_name: str) -> pd.DataFrame:
    """Convert columns to standard data types"""
    result = df.copy()
    
    for col in result.columns:
        target_type = COLUMN_TYPES.get(col)
        if target_type:
            try:
                if target_type == str:
                    result[col] = result[col].astype(str)
                else:
                    result[col] = pd.to_numeric(result[col], errors='coerce')
            except Exception as e:
                logger.warning(f"Could not convert {col} to {target_type}: {str(e)}")
    
    return result


def _handle_nulls(df: pd.DataFrame, query_name: str) -> pd.DataFrame:
    """Intelligently handle null values"""
    result = df.copy()
    
    # Numeric columns: fill with 0
    numeric_cols = result.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        null_count = result[col].isnull().sum()
        if null_count > 0:
            result[col] = result[col].fillna(0)
            logger.debug(f"Filled {null_count} nulls in {col} with 0")
    
    # String columns: fill with 'Unknown'
    string_cols = result.select_dtypes(include=[object]).columns
    for col in string_cols:
        null_count = result[col].isnull().sum()
        if null_count > 0 and col != 'state':  # Never fill state
            result[col] = result[col].fillna('Unknown')
            logger.debug(f"Filled {null_count} nulls in {col} with 'Unknown'")
    
    return result


def ensure_column_exists(
    df: pd.DataFrame,
    col_name: str,
    fallback_cols: Optional[list] = None,
    default_value: any = 0,
) -> tuple:
    """
    Ensure a column exists in DataFrame, using fallbacks if needed.
    
    Args:
        df: Input DataFrame
        col_name: Primary column name
        fallback_cols: List of alternative column names
        default_value: Value to use if column doesn't exist
        
    Returns:
        Tuple of (DataFrame with column, actual column name used)
    """
    result = df.copy()
    
    # Try to find the column
    actual_col = find_column(result, col_name)
    
    if actual_col:
        return result, actual_col
    
    # Try fallback columns
    if fallback_cols:
        for fallback in fallback_cols:
            actual_col = find_column(result, fallback)
            if actual_col:
                # Rename to primary name
                result = result.rename(columns={actual_col: col_name})
                return result, col_name
    
    # Create column with default value
    logger.warning(f"Column {col_name} not found, creating with default value {default_value}")
    result[col_name] = default_value
    return result, col_name


def calculate_active_users(
    df: pd.DataFrame,
    registered_col: str = "registered_users",
    engagement_col: Optional[str] = None,
) -> pd.DataFrame:
    """
    Calculate estimated active users if not present.
    
    Args:
        df: Input DataFrame
        registered_col: Column name for registered users
        engagement_col: Optional engagement level column
        
    Returns:
        DataFrame with active_users column
    """
    result = df.copy()
    
    if "active_users" not in result.columns:
        if registered_col in result.columns:
            # Base estimate: 70% of registered users
            result["active_users"] = result[registered_col] * 0.7
            
            # Adjust if engagement level is specified
            if engagement_col and engagement_col in result.columns:
                high_engaged = result[engagement_col] == "HIGHLY_ENGAGED"
                medium_engaged = result[engagement_col] == "MEDIUM_ENGAGED"
                result.loc[high_engaged, "active_users"] = result.loc[high_engaged, registered_col] * 0.85
                result.loc[medium_engaged, "active_users"] = result.loc[medium_engaged, registered_col] * 0.65
            
            logger.debug("Calculated active_users from registered_users")
    
    return result


def validate_data_integrity(df: pd.DataFrame) -> dict:
    """
    Validate data integrity and return report.
    
    Args:
        df: DataFrame to validate
        
    Returns:
        Dictionary with validation results
    """
    report = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "null_values": df.isnull().sum().to_dict(),
        "duplicates": len(df) - len(df.drop_duplicates()),
        "numeric_columns": list(df.select_dtypes(include=[np.number]).columns),
        "string_columns": list(df.select_dtypes(include=[object]).columns),
        "issues": [],
    }
    
    # Check for empty DataFrame
    if df.empty:
        report["issues"].append("DataFrame is empty")
    
    # Check for high null percentage
    null_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)
    if null_pct > 20:
        report["issues"].append(f"High null percentage: {null_pct:.2f}%")
    
    # Check for duplicates
    if report["duplicates"] > 0:
        dup_pct = (report["duplicates"] / len(df) * 100)
        report["issues"].append(f"Found {report['duplicates']} duplicates ({dup_pct:.2f}%)")
    
    return report
