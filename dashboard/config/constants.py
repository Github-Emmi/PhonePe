"""
Application-wide constants and configuration values
"""

import os
from pathlib import Path

# Paths
DASHBOARD_DIR = Path(__file__).parent.parent
DATA_DIR = DASHBOARD_DIR.parent / "query_results"
DATA_EXTRACTS_DIR = DASHBOARD_DIR.parent / "data_extracts"

# Page Configuration
PAGE_TITLES = {
    "home": "🏠 Home Dashboard",
    "transactions": "💰 Transaction Analytics",
    "users": "👥 User Engagement",
    "insurance": "🛡️ Insurance Insights",
    "geographic": "🗺️ Geographic Analysis",
    "predictions": "🔮 Predictive Insights",
    "reports": "📊 Reports & Export"
}

# Color Scheme (Brand Colors)
PRIMARY_COLOR = "#1f77b4"      # Blue
SECONDARY_COLOR = "#ff7f0e"    # Orange
SUCCESS_COLOR = "#2ca02c"      # Green
DANGER_COLOR = "#d62728"       # Red
INFO_COLOR = "#17a2b8"         # Teal
WARNING_COLOR = "#ffc107"      # Yellow
LIGHT_COLOR = "#f8f9fa"        # Light gray
DARK_COLOR = "#343a40"         # Dark gray

# Categorical Colors
CATEGORICAL_COLORS = [
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    SUCCESS_COLOR,
    DANGER_COLOR,
    "#9467bd",  # Purple
    "#8c564b",  # Brown
    "#e377c2",  # Pink
    "#7f7f7f",  # Gray
    "#bcbd22",  # Yellow-green
    INFO_COLOR,
]

# Data Configuration
DATA_CACHE_TTL = 3600  # 1 hour
METRIC_CACHE_TTL = 300  # 5 minutes

# Chart Configuration
CHART_HEIGHT = 400
CHART_MARGIN = dict(l=60, r=20, t=60, b=50)
CHART_TEMPLATE = "plotly_white"

# Metrics Configuration
KPI_COLUMNS = 4
TOP_N_DEFAULT = 10

# Page Layout
LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

# Number Formatting
THOUSAND_SEPARATOR = ","
DECIMAL_PLACES = 2

# Indian States
INDIAN_STATES = [
    "Andaman and Nicobar Islands",
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chandigarh",
    "Chhattisgarh",
    "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Ladakh",
    "Lakshadweep",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Puducherry",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal"
]

# Quarter Configuration
QUARTERS = ["Q1", "Q2", "Q3", "Q4"]

# Metric Thresholds
GROWTH_THRESHOLD_HIGH = 0.20      # 20% growth
GROWTH_THRESHOLD_LOW = -0.10      # -10% decline