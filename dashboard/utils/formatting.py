"""
Data formatting utilities for consistent display across the dashboard.
"""

import pandas as pd
import numpy as np
from typing import Union, Any
from datetime import datetime


def format_number(value: Union[int, float], decimals: int = 0) -> str:
    """
    Format a number with thousand separators.
    
    Args:
        value: The number to format
        decimals: Number of decimal places
        
    Returns:
        Formatted number string
    """
    if pd.isna(value) or value is None:
        return "0"
    
    return f"{value:,.{decimals}f}".rstrip('0').rstrip('.')


def format_percentage(value: Union[int, float], decimals: int = 1) -> str:
    """
    Format a number as percentage.
    
    Args:
        value: The number to format (0-1 or 0-100)
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    if pd.isna(value) or value is None:
        return "0%"
    
    # Assume 0-1 range, convert to 0-100
    if value <= 1:
        value = value * 100
    
    return f"{value:.{decimals}f}%"


def format_currency(value: Union[int, float], currency: str = "₹", decimals: int = 2) -> str:
    """
    Format a number as currency.
    
    Args:
        value: The amount
        currency: Currency symbol (default ₹)
        decimals: Number of decimal places
        
    Returns:
        Formatted currency string
    """
    if pd.isna(value) or value is None:
        return f"{currency} 0"
    
    return f"{currency} {value:,.{decimals}f}"


def format_large_number(value: Union[int, float], decimals: int = 1) -> str:
    """
    Format large numbers with abbreviated suffix (K, M, B, Cr).
    
    Args:
        value: The number to format
        decimals: Number of decimal places
        
    Returns:
        Abbreviated number string
    """
    if pd.isna(value) or value is None:
        return "0"
    
    value = float(value)
    
    if value >= 10000000:  # 1 Cr = 10 million
        return f"{value/10000000:.{decimals}f} Cr"
    elif value >= 1000000:  # 1 Million
        return f"{value/1000000:.{decimals}f} M"
    elif value >= 1000:  # 1 Thousand
        return f"{value/1000:.{decimals}f} K"
    else:
        return f"{value:.{decimals}f}"


def format_date(date_obj: Union[str, datetime], format: str = "%d-%b-%Y") -> str:
    """
    Format date to standard format.
    
    Args:
        date_obj: Date string or datetime object
        format: Desired format string
        
    Returns:
        Formatted date string
    """
    if pd.isna(date_obj) or date_obj is None:
        return "N/A"
    
    if isinstance(date_obj, str):
        try:
            date_obj = pd.to_datetime(date_obj)
        except:
            return str(date_obj)
    
    return date_obj.strftime(format)


def get_color_by_trend(value: Union[int, float, None], 
                       positive_is_good: bool = True) -> str:
    """
    Get color based on trend (positive/negative).
    
    Args:
        value: The metric value
        positive_is_good: If True, positive values are green
        
    Returns:
        Color code string
    """
    if pd.isna(value) or value is None:
        return "#808080"  # Gray
    
    is_positive = value > 0
    
    if positive_is_good:
        return "#2ca02c" if is_positive else "#d62728"  # Green or Red
    else:
        return "#d62728" if is_positive else "#2ca02c"  # Red or Green


def format_trend(current: Union[int, float], previous: Union[int, float], 
                decimals: int = 1) -> tuple:
    """
    Calculate and format trend information.
    
    Args:
        current: Current period value
        previous: Previous period value
        decimals: Number of decimal places for percentage
        
    Returns:
        Tuple of (trend_percentage, arrow_symbol, color)
    """
    if pd.isna(current) or pd.isna(previous) or previous == 0:
        return 0, "→", "#808080"
    
    trend = ((current - previous) / abs(previous)) * 100
    
    if trend > 0:
        arrow = "↑"
        color = "#2ca02c"  # Green
    elif trend < 0:
        arrow = "↓"
        color = "#d62728"  # Red
    else:
        arrow = "→"
        color = "#808080"  # Gray
    
    return f"{abs(trend):.{decimals}f}%", arrow, color


def format_dataframe(df: pd.DataFrame, 
                    number_cols: list = None,
                    currency_cols: list = None,
                    percentage_cols: list = None) -> pd.DataFrame:
    """
    Format entire DataFrame for display.
    
    Args:
        df: DataFrame to format
        number_cols: Columns to format as numbers
        currency_cols: Columns to format as currency
        percentage_cols: Columns to format as percentage
        
    Returns:
        Formatted DataFrame
    """
    df_copy = df.copy()
    
    if number_cols:
        for col in number_cols:
            if col in df_copy.columns:
                df_copy[col] = df_copy[col].apply(lambda x: format_number(x) if pd.notna(x) else "")
    
    if currency_cols:
        for col in currency_cols:
            if col in df_copy.columns:
                df_copy[col] = df_copy[col].apply(lambda x: format_currency(x) if pd.notna(x) else "")
    
    if percentage_cols:
        for col in percentage_cols:
            if col in df_copy.columns:
                df_copy[col] = df_copy[col].apply(lambda x: format_percentage(x) if pd.notna(x) else "")
    
    return df_copy


def get_metric_display_value(value: Any, format_type: str = "number") -> str:
    """
    Get formatted display value based on type.
    
    Args:
        value: Value to format
        format_type: Type of formatting (number, currency, percentage, large)
        
    Returns:
        Formatted string
    """
    if pd.isna(value) or value is None:
        return "0"
    
    format_map = {
        "number": lambda x: format_number(x),
        "currency": lambda x: format_currency(x),
        "percentage": lambda x: format_percentage(x),
        "large": lambda x: format_large_number(x),
    }
    
    return format_map.get(format_type, lambda x: str(x))(value)
