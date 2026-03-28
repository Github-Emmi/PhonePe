"""
Caching utilities for Streamlit dashboard.
Uses Streamlit's built-in caching with TTL support.
"""

import streamlit as st
from functools import wraps
from typing import Callable, Any
import time
import logging

logger = logging.getLogger(__name__)


def cached_query(ttl_seconds: int = 3600):
    """
    Decorator for caching query results using Streamlit cache.
    
    Args:
        ttl_seconds: Time to live in seconds (default 1 hour)
        
    Returns:
        Decorated function with caching
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        @st.cache_data(ttl=ttl_seconds, show_spinner=False)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in cached query {func.__name__}: {str(e)}")
                raise
        return wrapper
    return decorator


def cached_metric(ttl_seconds: int = 300):
    """
    Decorator for caching metric queries (shorter TTL).
    
    Args:
        ttl_seconds: Time to live in seconds (default 5 minutes)
        
    Returns:
        Decorated function with caching
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        @st.cache_data(ttl=ttl_seconds, show_spinner=False)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in cached metric {func.__name__}: {str(e)}")
                raise
        return wrapper
    return decorator


def clear_cache_on_change(key: str):
    """
    Helper to clear cache when a filter changes.
    
    Args:
        key: Session state key to watch
    """
    if key in st.session_state:
        st.cache_data.clear()


@st.cache_resource
def get_session_cache() -> dict:
    """
    Get or create session-level cache dictionary.
    
    Returns:
        Session cache dictionary
    """
    return {}


def cache_summary() -> dict:
    """
    Get cache statistics.
    
    Returns:
        Dictionary with cache stats
    """
    return {
        "cache_info": "Available via Streamlit client.cache_data.clear()"
    }
