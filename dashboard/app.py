"""
PhonePe Analytics Dashboard
Main Streamlit Application
"""

import streamlit as st
import pandas as pd

# Configure page
st.set_page_config(
    page_title="PhonePe Analytics Dashboard",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
    .main {
        padding-top: 0rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    h1 {
        color: #1f77b4;
        margin-top: 0;
    }
    h2 {
        color: #ff7f0e;
    }
    .stTabs>button {
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Import home page
from pages._home import home_page

# Sidebar information
st.sidebar.title("📱 PhonePe Dashboard")
st.sidebar.markdown("---")

st.sidebar.subheader("Dashboard Info")
st.sidebar.info(
    """
    **PhonePe Analytics Dashboard**
    
    Real-time analysis of:
    - 💸 Transaction data across 36 states
    - 👤 User engagement metrics
    - 🛡️ Insurance penetration
    - 📍 Geographic distribution
    """
)

st.sidebar.markdown("---")
st.sidebar.subheader("Data Last Updated")
st.sidebar.caption("Query results from data_extracts and query_results")

# Load and display home page
try:
    home_page()
except Exception as e:
    st.error(f"❌ Error Loading Dashboard")
    st.write(f"**Error Details:** {str(e)}")
    st.info(
        """
        **What happened?**
        - The dashboard encountered an error while loading
        - This may be due to missing data or configuration issues
        
        **What you can do:**
        - Try refreshing the page
        - Contact support if the issue persists
        """
    )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 12px; padding: 20px;'>
    PhonePe Analytics Dashboard | Built with Streamlit | Data Source: Query Results
    </div>
    """,
    unsafe_allow_html=True
)
