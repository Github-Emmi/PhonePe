"""
Data validation utilities for ensuring data quality and consistency.
Provides validation gates and error handling for dashboard data processing.
"""

import pandas as pd
import numpy as np
from typing import Tuple, List, Optional
import logging

from config.column_mappings import (
    get_required_columns,
    find_column,
    COLUMN_ALIASES,
)

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for validation failures"""
    pass


def validate_dataframe(
    df: pd.DataFrame,
    query_name: str,
    strict: bool = False,
) -> Tuple[bool, List[str]]:
    """
    Validate DataFrame against requirements.
    
    Args:
        df: DataFrame to validate
        query_name: Query/file name for requirement lookup
        strict: If True, raise exception on validation failure
        
    Returns:
        Tuple of (is_valid, error_list)
    """
    errors = []
    
    # Check 1: DataFrame not empty
    if df.empty:
        errors.append("DataFrame is empty")
    
    # Check 2: No required columns missing
    required = get_required_columns(query_name)
    missing_cols = []
    
    for req_col in required:
        actual_col = find_column(df, req_col)
        if not actual_col:
            missing_cols.append(req_col)
    
    if missing_cols:
        errors.append(f"Missing required columns: {missing_cols}")
    
    # Check 3: High null percentage
    if not df.empty:
        null_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)
        if null_pct > 50:
            errors.append(f"Too many nulls: {null_pct:.2f}%")
    
    # Check 4: Duplicate rows
    if not df.empty:
        dup_count = len(df) - len(df.drop_duplicates())
        if dup_count > len(df) * 0.1:  # More than 10% duplicates
            errors.append(f"Too many duplicates: {dup_count} rows ({dup_count/len(df)*100:.2f}%)")
    
    is_valid = len(errors) == 0
    
    if not is_valid:
        msg = f"Validation failed for {query_name}: {'; '.join(errors)}"
        if strict:
            logger.error(msg)
            raise ValidationError(msg)
        else:
            logger.warning(msg)
    
    return is_valid, errors


def check_column_exists(
    df: pd.DataFrame,
    col_name: str,
    raise_error: bool = True,
) -> bool:
    """Check if column exists (by name or alias)"""
    if find_column(df, col_name):
        return True
    
    if raise_error:
        raise ValidationError(f"Required column '{col_name}' not found in DataFrame")
    
    return False


def safe_numeric_column(
    df: pd.DataFrame,
    col_name: str,
    default: float = 0,
) -> pd.Series:
    """
    Get numeric column safely, converting as needed.
    
    Args:
        df: DataFrame
        col_name: Column name (supports aliases)
        default: Default value for null/missing
        
    Returns:
        Numeric Series
    """
    actual_col = find_column(df, col_name)
    
    if not actual_col:
        logger.warning(f"Column {col_name} not found, returning default values")
        return pd.Series([default] * len(df), name=col_name)
    
    series = df[actual_col].copy()
    
    # Convert to numeric
    series = pd.to_numeric(series, errors='coerce')
    
    # Fill nulls
    null_count = series.isnull().sum()
    if null_count > 0:
        series = series.fillna(default)
        logger.debug(f"Filled {null_count} nulls in {col_name} with {default}")
    
    return series


def safe_string_column(
    df: pd.DataFrame,
    col_name: str,
    default: str = "Unknown",
) -> pd.Series:
    """
    Get string column safely, handling nulls.
    
    Args:
        df: DataFrame
        col_name: Column name (supports aliases)
        default: Default value for null/missing
        
    Returns:
        String Series
    """
    actual_col = find_column(df, col_name)
    
    if not actual_col:
        logger.warning(f"Column {col_name} not found, returning default values")
        return pd.Series([default] * len(df), name=col_name)
    
    series = df[actual_col].astype(str).copy()
    
    # Fill nulls
    null_count = (series == "nan") | (series == "None") | series.isnull()
    if null_count.sum() > 0:
        series[null_count] = default
        logger.debug(f"Filled {null_count.sum()} nulls in {col_name} with '{default}'")
    
    return series


def safe_groupby_aggregation(
    df: pd.DataFrame,
    groupby_cols: List[str],
    agg_dict: dict,
    fill_zero: bool = True,
) -> pd.DataFrame:
    """
    Perform groupby aggregation safely with error handling.
    
    Args:
        df: Input DataFrame
        groupby_cols: Columns to group by
        agg_dict: Aggregation specification
        fill_zero: Fill null values with 0 for numeric columns
        
    Returns:
        Aggregated DataFrame
    """
    try:
        # Find actual column names for groupby
        actual_groupby = []
        for col in groupby_cols:
            actual_col = find_column(df, col)
            if actual_col:
                actual_groupby.append(actual_col)
            else:
                logger.warning(f"Groupby column {col} not found, skipping")
        
        if not actual_groupby:
            logger.error(f"No valid groupby columns found")
            return pd.DataFrame()
        
        # Find actual column names for aggregation
        actual_agg = {}
        for col, func in agg_dict.items():
            actual_col = find_column(df, col)
            if actual_col:
                actual_agg[actual_col] = func
        
        if not actual_agg:
            logger.error("No valid aggregation columns found")
            return pd.DataFrame()
        
        # Perform aggregation
        result = df.groupby(actual_groupby, as_index=False).agg(actual_agg)
        
        if fill_zero:
            numeric_cols = result.select_dtypes(include=[np.number]).columns
            result[numeric_cols] = result[numeric_cols].fillna(0)
        
        logger.debug(f"Aggregation successful: {result.shape[0]} groups")
        return result
        
    except Exception as e:
        logger.error(f"Aggregation failed: {str(e)}")
        return pd.DataFrame()


def validate_filters(
    df: pd.DataFrame,
    filters: dict,
) -> Tuple[bool, List[str]]:
    """
    Validate filter parameters against DataFrame.
    
    Args:
        df: DataFrame to filter
        filters: Dictionary of {column: value(s)}
        
    Returns:
        Tuple of (is_valid, error_list)
    """
    errors = []
    
    for col_name, value in filters.items():
        # Check column exists
        actual_col = find_column(df, col_name)
        if not actual_col:
            errors.append(f"Filter column {col_name} not found")
            continue
        
        # Check value exists in column
        if isinstance(value, str):
            if value not in df[actual_col].astype(str).values:
                errors.append(f"Filter value '{value}' not found in {col_name}")
        elif isinstance(value, (list, tuple)):
            for v in value:
                if v not in df[actual_col].values:
                    errors.append(f"Filter value '{v}' not found in {col_name}")
    
    is_valid = len(errors) == 0
    if not is_valid:
        logger.warning(f"Filter validation failed: {'; '.join(errors)}")
    
    return is_valid, errors


def get_data_quality_score(df: pd.DataFrame) -> float:
    """
    Calculate data quality score (0-100).
    
    Factors:
    - Completeness (no nulls): 40%
    - Uniqueness (no duplicates): 30%
    - Validity (numeric columns numeric): 20%
    - Row count (has data): 10%
    
    Returns:
        Quality score 0-100
    """
    if df.empty:
        return 0.0
    
    total_cells = len(df) * len(df.columns)
    null_cells = df.isnull().sum().sum()
    dup_rows = len(df) - len(df.drop_duplicates())
    
    # Completeness score (40%)
    completeness = (1 - null_cells / total_cells) * 40
    
    # Uniqueness score (30%)
    uniqueness = (1 - dup_rows / len(df)) * 30 if len(df) > 0 else 0
    
    # Validity score (20%) - check if numeric columns are numeric
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        invalid_ratio = 0
        for col in numeric_cols:
            try:
                pd.to_numeric(df[col], errors='coerce').notna().sum()
                # Score based on how many could be converted
                converted = pd.to_numeric(df[col], errors='coerce').notna().sum()
                invalid_ratio += (1 - converted / len(df))
            except:
                invalid_ratio += 1
        
        validity = (1 - invalid_ratio / len(numeric_cols)) * 20
    else:
        validity = 20
    
    # Row count score (10%)
    row_score = min(10, len(df) / 100 * 10)
    
    total_score = completeness + uniqueness + validity + row_score
    return min(100, total_score)
