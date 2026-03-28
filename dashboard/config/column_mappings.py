"""
Column mapping configuration for handling CSV data variations.
Maps variations in column names across different data sources to standard names.
"""

# Column name mappings by query/file
COLUMN_MAPPINGS = {
    # Query 1.x - Transaction queries
    "Query_1.1": {
        "quarterly_volume": "transaction_count",
        "quarterly_total": "transaction_amount",
        "transaction_type": "type",
        "qoq_growth_rate": "growth_rate",
    },
    "Query_1.2": {
        # Query_1.2 already has standard names (total_transactions, total_revenue)
    },
    "Query_1.3": {
        # Already standard names
    },
    "Query_1.4": {
        # Already standard names
    },
    
    # Query 2.x - User queries
    "Query_2.1": {
        "total_users": "registered_users",
        "device_types": "num_device_types",
        "user_market_share_pct": "market_share",
    },
    "Query_2.2": {
        "prev_quarter_users": "previous_quarter_users",
    },
    "Query_2.4": {
        # Already standard names
    },
    
    # Query 3.x - Insurance queries
    "Query_3.1": {
        "quarterly_policies": "insurance_transactions",
        "quarterly_premium": "premium_amount",
        "insurance_type": "type",
        "qoq_growth_rate": "growth_rate",
    },
    "Query_3.2": {
        # Already standard names
    },
    "Query_3.3": {
        # Already standard names
    },
    "Query_3.4": {
        # Already standard names
    },
    
    # Query 4.x - Comprehensive analytics
    "Query_4.1": {
        "annual_transaction_count": "transaction_count",
        "annual_transaction_value": "transaction_amount",
    },
    
    # Query 5.x - User growth
    "Query_5.1": {
        "quarterly_users": "registered_users",
        "prev_quarter_users": "previous_quarter_users",
    },
    
    # Aggregated data
    "aggregated_transaction": {
        "transaction_total": "transaction_amount",
        "transaction_vol": "transaction_count",
    },
}

# Required columns per dataset
REQUIRED_COLUMNS = {
    "Query_1.1": ["state", "quarter", "transaction_count", "transaction_amount"],
    "Query_2.1": ["state", "registered_users"],
    "Query_3.1": ["state", "quarter", "insurance_transactions", "premium_amount"],
    "aggregated_transaction": ["state", "transaction_count", "transaction_amount"],
    "aggregated_user": ["state", "total_users"],
}

# Data type specifications
COLUMN_TYPES = {
    "state": str,
    "quarter": "int64",
    "year": "int64",
    "transaction_count": "float64",
    "transaction_amount": "float64",
    "registered_users": "float64",
    "active_users": "float64",
    "insurance_transactions": "float64",
    "premium_amount": "float64",
    "growth_rate": "float64",
    "market_share": "float64",
}

# Column aliases for flexible searching
COLUMN_ALIASES = {
    "transaction_count": [
        "quarterly_volume",
        "transaction_count",
        "volume",
        "transaction_vol",
        "trans_count",
    ],
    "transaction_amount": [
        "quarterly_total",
        "transaction_amount",
        "amount",
        "transaction_total",
        "trans_amount",
        "total",
    ],
    "registered_users": [
        "total_users",
        "registered_users",
        "users",
        "total_registered",
    ],
    "active_users": [
        "active_users",
        "engaged_users",
        "monthly_active",
    ],
    "insurance_transactions": [
        "quarterly_policies",
        "insurance_transactions",
        "policies",
        "insurance_vol",
    ],
    "premium_amount": [
        "quarterly_premium",
        "premium_amount",
        "premium",
        "premium_total",
    ],
    "growth_rate": [
        "qoq_growth_rate",
        "growth_rate",
        "yoy_growth",
        "growth",
    ],
}

def get_column_mapping(query_name: str) -> dict:
    """Get column mappings for a specific query"""
    # Extract query base name
    query_base = None
    for key in COLUMN_MAPPINGS.keys():
        if key in query_name:
            query_base = key
            break
    
    return COLUMN_MAPPINGS.get(query_base, {})


def get_required_columns(query_name: str) -> list:
    """Get required columns for a specific query"""
    query_base = None
    for key in REQUIRED_COLUMNS.keys():
        if key in query_name:
            query_base = key
            break
    
    return REQUIRED_COLUMNS.get(query_base, [])


def find_column(df, primary_name: str) -> str:
    """
    Find column in DataFrame by primary name or aliases.
    
    Args:
        df: DataFrame to search
        primary_name: Primary column name to look for
        
    Returns:
        Actual column name if found, None otherwise
    """
    # First try exact match
    if primary_name in df.columns:
        return primary_name
    
    # Try case-insensitive match
    lower_cols = {col.lower(): col for col in df.columns}
    if primary_name.lower() in lower_cols:
        return lower_cols[primary_name.lower()]
    
    # Try aliases
    aliases = COLUMN_ALIASES.get(primary_name, [])
    for alias in aliases:
        if alias in df.columns:
            return alias
        if alias.lower() in lower_cols:
            return lower_cols[alias.lower()]
    
    return None
