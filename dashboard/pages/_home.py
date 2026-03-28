"""
Home Dashboard Page
Displays key performance indicators and overview metrics
Includes data validation and error handling.
"""

import streamlit as st
import pandas as pd
from utils.database import get_kpi_metrics, load_query_data, get_states
from utils.formatting import format_large_number, format_currency
from utils.charts import create_comparison_bar, create_trend_line
from utils.metrics import (
    calculate_transaction_metrics,
    calculate_user_metrics,
    calculate_insurance_metrics,
    get_top_performers
)

# Try to import validation utilities
try:
    from utils.validation import validate_dataframe, safe_numeric_column, get_data_quality_score
    from config.column_mappings import find_column
    VALIDATION_AVAILABLE = True
except ImportError:
    VALIDATION_AVAILABLE = False


def home_page():
    """Render home dashboard page with validation"""
    
    st.title("🏠 Home Dashboard")
    st.markdown("---")
    
    # Main KPI metrics
    st.subheader("📊 Key Performance Indicators")
    
    # Load and validate metrics
    trans_metrics = {}
    user_metrics = {}
    ins_metrics = {}
    
    with st.spinner("Loading and validating metrics..."):
        try:
            trans_metrics = calculate_transaction_metrics()
            if not trans_metrics:
                st.warning("⚠️ Transaction metrics empty. Check Query_4.1 data.")
            
            user_metrics = calculate_user_metrics()
            if not user_metrics:
                st.warning("⚠️ User metrics empty. Check Query_2.1 data.")
            
            ins_metrics = calculate_insurance_metrics()
            if not ins_metrics:
                st.warning("⚠️ Insurance metrics empty. Check Query_3.1 data.")
            
            if not any([trans_metrics, user_metrics, ins_metrics]):
                st.warning("⚠️ No metrics data available. Please check data sources.")
        except Exception as e:
            st.error(f"❌ Error calculating metrics: {str(e)}")
            st.info("The dashboard will display with limited data. Please try refreshing.")
            import traceback
            st.text("Debug info:\n" + traceback.format_exc())
    
    # Display KPI cards in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Transactions",
            value=format_large_number(trans_metrics.get('total_transactions', 0)),
            delta=None
        )
    
    with col2:
        st.metric(
            label="Total Users",
            value=format_large_number(user_metrics.get('total_registered_users', 0)),
            delta=None
        )
    
    with col3:
        st.metric(
            label="Insurance Transactions",
            value=format_large_number(ins_metrics.get('total_insurance_transactions', 0)),
            delta=None
        )
    
    with col4:
        st.metric(
            label="Total Transaction Value",
            value=format_currency(trans_metrics.get('total_transaction_amount', 0), decimals=0),
            delta=None
        )
    
    st.markdown("---")
    
    # Top performers section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Top Transaction States")
        try:
            trans_df = load_query_data("Query_4.1_State-Level_Transaction_Performance_Analytics_(Comprehensive)")
            
            # Validate data
            if not trans_df.empty:
                if VALIDATION_AVAILABLE:
                    is_valid, errors = validate_dataframe(trans_df, "Query_4.1", strict=False)
                    if not is_valid:
                        st.warning(f"⚠️ Data quality issues: {', '.join(errors[:2])}")
                
                # Find actual column names
                state_col = find_column(trans_df, "state") if VALIDATION_AVAILABLE else "state"
                trans_col = find_column(trans_df, "transaction_count") if VALIDATION_AVAILABLE else "transaction_count"
                
                if state_col and trans_col and state_col in trans_df.columns and trans_col in trans_df.columns:
                    top_states = trans_df.nlargest(8, trans_col)[[state_col, trans_col]].copy()
                    top_states = top_states.rename(columns={state_col: 'state', trans_col: 'transaction_count'})
                    
                    fig = create_comparison_bar(
                        top_states,
                        "",
                        category_col='state',
                        value_col='transaction_count',
                        orientation='h'
                    )
                    st.plotly_chart(fig, width='stretch')
                else:
                    st.info("Transaction data columns not found in expected format")
            else:
                st.info("No transaction data available")
        except Exception as e:
            st.error(f"Error loading transaction data: {str(e)}")
    
    with col2:
        st.subheader("👥 Top User States")
        try:
            user_df = load_query_data("Query_2.1_State-Level_User_Registration_&_Engagement_Metrics")
            
            # Validate data
            if not user_df.empty:
                if VALIDATION_AVAILABLE:
                    is_valid, errors = validate_dataframe(user_df, "Query_2.1", strict=False)
                    if not is_valid:
                        st.warning(f"⚠️ Data quality issues: {', '.join(errors[:2])}")
                
                # Find actual column names
                state_col = find_column(user_df, "state") if VALIDATION_AVAILABLE else "state"
                user_col = find_column(user_df, "registered_users") if VALIDATION_AVAILABLE else "registered_users"
                
                if state_col and user_col and state_col in user_df.columns and user_col in user_df.columns:
                    top_users = user_df.nlargest(8, user_col)[[state_col, user_col]].copy()
                    top_users = top_users.rename(columns={state_col: 'state', user_col: 'registered_users'})
                    
                    fig = create_comparison_bar(
                        top_users,
                        "",
                        category_col='state',
                        value_col='registered_users',
                        orientation='h',
                        color="#2ca02c"
                    )
                    st.plotly_chart(fig, width='stretch')
                else:
                    st.info("User data columns not found in expected format")
            else:
                st.info("No user data available")
        except Exception as e:
            st.error(f"Error loading user data: {str(e)}")
    
    st.markdown("---")
    
    # Transaction trends
    st.subheader("📈 Transaction Growth Trends")
    try:
        growth_df = load_query_data("Query_1.1_Quarterly_Transaction_Growth_by_State_(YoY_Analysis)")
        
        if not growth_df.empty:
            # Validate data
            if VALIDATION_AVAILABLE:
                is_valid, errors = validate_dataframe(growth_df, "Query_1.1", strict=False)
                if not is_valid:
                    st.warning(f"⚠️ Data quality note: {errors[0] if errors else 'Minor issues'}")
            
            # Find actual column names
            state_col = find_column(growth_df, "state") if VALIDATION_AVAILABLE else "state"
            quarter_col = find_column(growth_df, "quarter") if VALIDATION_AVAILABLE else "quarter"
            trans_col = find_column(growth_df, "transaction_count") if VALIDATION_AVAILABLE else "transaction_count"
            
            if state_col in growth_df.columns and quarter_col in growth_df.columns and trans_col in growth_df.columns:
                # Create trend view for top states
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    states_list = sorted(growth_df[state_col].unique())[:5]
                    if states_list:
                        selected_state = st.selectbox("Select State:", states_list, key="trend_state")
                    else:
                        st.info("No states available")
                        return
                
                with col2:
                    state_data = growth_df[growth_df[state_col] == selected_state].copy()
                    state_data = state_data.sort_values(quarter_col)
                    
                    if not state_data.empty:
                        try:
                            fig = create_trend_line(
                                state_data,
                                f"Transaction Trend - {selected_state}",
                                x_col=quarter_col,
                                y_col=trans_col
                            )
                            st.plotly_chart(fig, width='stretch')
                        except Exception as e:
                            st.warning(f"Could not render trend chart: {str(e)}")
                    else:
                        st.info("No trend data for selected state")
            else:
                st.info("Growth trend data format not compatible")
        else:
            st.info("No growth trend data available")
    except Exception as e:
        st.warning(f"Could not load growth trends: {str(e)}")
    
    st.markdown("---")
    
    # Summary statistics
    st.subheader("📉 Summary Statistics")
    
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    with stat_col1:
        if trans_metrics.get('avg_transaction_size') and trans_metrics.get('avg_transaction_size') > 0:
            st.metric(
                "Avg Transaction Size",
                format_currency(trans_metrics['avg_transaction_size'])
            )
        else:
            st.info("Avg Transaction Size: N/A")
    
    with stat_col2:
        if trans_metrics.get('top_state'):
            st.metric(
                "Top State",
                trans_metrics['top_state'],
                f"{format_large_number(trans_metrics.get('top_state_transactions', 0))} txns"
            )
        else:
            st.info("Top State: N/A")
    
    with stat_col3:
        if user_metrics.get('avg_users_per_state') and user_metrics.get('avg_users_per_state') > 0:
            st.metric(
                "Avg Users/State",
                format_large_number(user_metrics['avg_users_per_state'])
            )
        else:
            st.info("Avg Users/State: N/A")
