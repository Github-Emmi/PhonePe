"""
User Engagement Analytics Page
User registration, activation, and engagement metrics
"""

import streamlit as st
import pandas as pd
from utils.database import load_query_data, get_states
from utils.formatting import format_large_number, format_percentage
from utils.charts import (
    create_trend_line,
    create_comparison_bar,
    create_pie_chart,
)


def users_page():
    """Render users analytics page"""
    
    st.title("👥 User Engagement Analytics")
    st.markdown("---")
    
    # Sidebar filters
    st.sidebar.subheader("📊 Filters")
    
    with st.sidebar:
        selected_state = st.selectbox(
            "Select State (or All)",
            options=["All States"] + get_states(),
            key="user_state"
        )
        
        show_devices = st.checkbox("Show Device Breakdown", value=True)
    
    # User registration metrics
    st.subheader("👤 User Registration & Engagement")
    
    try:
        user_df = load_query_data("Query_2.1_State-Level_User_Registration_&_Engagement_Metrics")
        
        if selected_state != "All States":
            user_df = user_df[user_df['state'].str.contains(selected_state, case=False, na=False)]
        
        if not user_df.empty:
            col1, col2, col3 = st.columns(3)
            
            numeric_cols = user_df.select_dtypes(include=['number']).columns
            
            with col1:
                if 'registered_users' in user_df.columns:
                    total = user_df['registered_users'].sum()
                    st.metric("Total Registered Users", format_large_number(total))
                elif len(numeric_cols) > 0:
                    total = user_df[numeric_cols[0]].sum()
                    st.metric("Registered Users", format_large_number(total))
            
            with col2:
                if 'active_users' in user_df.columns:
                    active = user_df['active_users'].sum()
                    st.metric("Active Users", format_large_number(active))
            
            with col3:
                states_count = len(user_df['state'].unique()) if 'state' in user_df.columns else 1
                st.metric("States Covered", format_large_number(states_count))
        
        st.markdown("---")
    
    except Exception as e:
        st.error(f"Error loading user metrics: {str(e)}")
    
    # Top user states
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top States by User Registration")
        try:
            if not user_df.empty and 'registered_users' in user_df.columns:
                top_users = user_df.nlargest(10, 'registered_users')[['state', 'registered_users']]
                
                fig = create_comparison_bar(
                    top_users,
                    "",
                    category_col='state',
                    value_col='registered_users',
                    orientation='h',
                    color="#2ca02c"
                )
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not load top states: {str(e)}")
    
    with col2:
        st.subheader("📊 User Growth Trends")
        try:
            growth_df = load_query_data("Query_5.1_User_Growth_Trajectory_by_Quarter_(Acquisition_Momentum)")
            
            if not growth_df.empty and 'quarter' in growth_df.columns:
                if selected_state != "All States":
                    growth_df = growth_df[growth_df['state'].str.contains(selected_state, case=False, na=False)]
                
                numeric_cols = growth_df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0 and len(growth_df) > 0:
                    fig = create_trend_line(
                        growth_df.sort_values('quarter'),
                        f"User Growth - {selected_state}",
                        x_col='quarter',
                        y_col=numeric_cols[0]
                    )
                    st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not load growth trends: {str(e)}")
    
    st.markdown("---")
    
    if show_devices:
        st.subheader("📱 Device Distribution")
        
        try:
            device_df = load_query_data("Query_2.4_Device_Type_Engagement_Breakdown_by_State")
            
            if not device_df.empty:
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    if 'device' in device_df.columns or 'device_type' in device_df.columns:
                        device_col = 'device' if 'device' in device_df.columns else 'device_type'
                        numeric_cols = device_df.select_dtypes(include=['number']).columns
                        
                        if len(numeric_cols) > 0:
                            value_col = numeric_cols[0]
                            device_agg = device_df.groupby(device_col)[value_col].sum().reset_index()
                            device_agg.columns = [device_col, value_col]
                            
                            fig = create_pie_chart(
                                device_agg,
                                "Device Distribution",
                                values_col=value_col,
                                names_col=device_col,
                                donut=True
                            )
                            st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Engagement by device
                    if len(numeric_cols) > 1:
                        device_comparison = device_df.groupby(device_col)[numeric_cols[1]].sum().reset_index()
                        device_comparison.columns = [device_col, 'engagement']
                        
                        fig = create_comparison_bar(
                            device_comparison,
                            "Engagement by Device",
                            category_col=device_col,
                            value_col='engagement'
                        )
                        st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.warning(f"Could not load device breakdown: {str(e)}")
    
    st.markdown("---")
    
    # Engagement patterns
    st.subheader("📈 Engagement Patterns")
    
    try:
        engagement_df = load_query_data("Query_2.2_User_Engagement_Trends_by_Quarter_&_Year")
        
        if not engagement_df.empty and 'quarter' in engagement_df.columns:
            numeric_cols = engagement_df.select_dtypes(include=['number']).columns
            
            if len(numeric_cols) > 0 and len(engagement_df) > 0:
                fig = create_trend_line(
                    engagement_df.sort_values('quarter'),
                    "Quarterly Engagement Trends",
                    x_col='quarter',
                    y_col=numeric_cols[0],
                    color="#ff7f0e"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.warning(f"Could not load engagement patterns: {str(e)}")
    
    st.markdown("---")
    
    # Data table
    st.subheader("Data Table")
    try:
        if 'user_df' in locals() and not user_df.empty:
            st.dataframe(user_df, width='stretch')
    except:
        st.info("Select filters to view detailed data")
