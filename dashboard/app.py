"""
PhonePe Analytics Dashboard
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
from pathlib import Path

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

# Sidebar navigation
st.sidebar.title("📱 PhonePe Dashboard")
st.sidebar.markdown("---")

# Navigation menu
nav_options = {
    "🏠 Home": "home",
    "💰 Transactions": "transactions",
    "👥 Users": "users",
    "🛡️ Insurance": "insurance",
    "🗺️ Geographic": "geographic",
    "📊 Reports": "reports",
}

selected_page = st.sidebar.radio(
    "Select Page",
    options=list(nav_options.keys()),
    index=0
)

# Sidebar information
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

# Route to appropriate page with error handling
page_key = nav_options[selected_page]

def show_error_page(error_msg: str, page_name: str):
    """Display a user-friendly error page"""
    st.error(f"❌ Error Loading {page_name}")
    st.write(f"**Error Details:** {error_msg}")
    st.info(
        """
        **What happened?**
        - The page encountered an error while loading
        - This may be due to missing data or configuration issues
        
        **What you can do:**
        - Try refreshing the page
        - Select a different page and try again
        - Contact support if the issue persists
        """
    )

try:
    if page_key == "home":
        try:
            from pages.home import home_page
            home_page()
        except ImportError as e:
            show_error_page(f"Could not import home page: {str(e)}", "Home")
        except Exception as e:
            show_error_page(f"Home page error: {str(e)}", "Home")
    
    elif page_key == "transactions":
        try:
            from pages.transactions import transactions_page
            transactions_page()
        except ImportError as e:
            show_error_page(f"Could not import transactions page: {str(e)}", "Transactions")
        except Exception as e:
            show_error_page(f"Transactions page error: {str(e)}", "Transactions")
    
    elif page_key == "users":
        try:
            from pages.users import users_page
            users_page()
        except ImportError as e:
            show_error_page(f"Could not import users page: {str(e)}", "Users")
        except Exception as e:
            show_error_page(f"Users page error: {str(e)}", "Users")
    
    elif page_key == "insurance":
        try:
            from pages.insurance import insurance_page
            insurance_page()
        except ImportError as e:
            show_error_page(f"Could not import insurance page: {str(e)}", "Insurance")
        except Exception as e:
            show_error_page(f"Insurance page error: {str(e)}", "Insurance")
    
    elif page_key == "geographic":
        try:
            from pages.geographic import geographic_page
            geographic_page()
        except ImportError as e:
            show_error_page(f"Could not import geographic page: {str(e)}", "Geographic")
        except Exception as e:
            show_error_page(f"Geographic page error: {str(e)}", "Geographic")
    
    elif page_key == "reports":
        try:
            from pages.reports import reports_page
            reports_page()
        except ImportError as e:
            show_error_page(f"Could not import reports page: {str(e)}", "Reports")
        except Exception as e:
            show_error_page(f"Reports page error: {str(e)}", "Reports")

except Exception as e:
    st.error(f"❌ Critical Application Error")
    st.write(f"**Error Details:** {str(e)}")
    st.info("The dashboard encountered an unexpected error. Please refresh your browser and try again.")

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
