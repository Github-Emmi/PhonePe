"""
Insurance Insights Page
Insurance market analysis, penetration, and growth
"""

import streamlit as st
import pandas as pd
from utils.database import load_query_data, get_states
from utils.formatting import format_large_number, format_currency
from utils.charts import (
    create_trend_line,
    create_comparison_bar,
    create_pie_chart,
    create_stacked_bar,
)


def insurance_page():
    """Render insurance insights page"""
    
    st.title("🛡️ Insurance Insights")
    st.markdown("---")
    
    # Sidebar filters
    st.sidebar.subheader("📊 Filters")
    
    with st.sidebar:
        selected_state = st.selectbox(
            "Select State (or All)",
            options=["All States"] + get_states(),
            key="ins_state"
        )
    
    # Insurance overview metrics
    st.subheader("📊 Insurance Market Overview")
    
    try:
        ins_df = load_query_data("Query_3.1_Insurance_Growth_Trajectory_by_State_&_Quarter")
        
        if selected_state != "All States":
            ins_df = ins_df[ins_df['state'].str.contains(selected_state, case=False, na=False)]
        
        if not ins_df.empty:
            col1, col2, col3, col4 = st.columns(4)
            
            numeric_cols = ins_df.select_dtypes(include=['number']).columns
            
            with col1:
                if 'count' in ins_df.columns:
                    total_count = ins_df['count'].sum()
                    st.metric("Insurance Policies", format_large_number(total_count))
                elif len(numeric_cols) > 0:
                    total = ins_df[numeric_cols[0]].sum()
                    st.metric("Policies", format_large_number(total))
            
            with col2:
                if 'premium_amount' in ins_df.columns:
                    total_premium = ins_df['premium_amount'].sum()
                    st.metric("Total Premium", format_currency(total_premium, decimals=0))
            
            with col3:
                if 'premium_amount' in ins_df.columns and 'count' in ins_df.columns:
                    avg_premium = ins_df['premium_amount'].sum() / ins_df['count'].sum()
                    st.metric("Avg Premium", format_currency(avg_premium))
            
            with col4:
                states_count = len(ins_df['state'].unique()) if 'state' in ins_df.columns else 1
                st.metric("States Active", format_large_number(states_count))
        
        st.markdown("---")
    
    except Exception as e:
        st.error(f"Error loading insurance metrics: {str(e)}")
    
    # Growth trajectory
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Insurance Growth by Quarter")
        try:
            if not ins_df.empty and 'quarter' in ins_df.columns:
                if selected_state != "All States":
                    growth_data = ins_df
                else:
                    # Aggregate across states (exclude quarter and year from sum)
                    numeric_cols = ins_df.select_dtypes(include=['number']).columns
                    numeric_cols_to_sum = [col for col in numeric_cols if col not in ['quarter', 'year']]
                    growth_data = ins_df.groupby('quarter').agg({
                        col: 'sum' for col in numeric_cols_to_sum
                    }).reset_index()
                
                if len(growth_data) > 0:
                    numeric_cols = growth_data.select_dtypes(include=['number']).columns
                    if len(numeric_cols) > 0:
                        fig = create_trend_line(
                            growth_data.sort_values('quarter'),
                            f"Insurance Growth - {selected_state}",
                            x_col='quarter',
                            y_col=numeric_cols[0]
                        )
                        st.plotly_chart(fig, width='stretch')
        except Exception as e:
            st.warning(f"Could not load growth trajectory: {str(e)}")
    
    with col2:
        st.subheader("🏆 Top States by Insurance")
        try:
            if not ins_df.empty and 'state' in ins_df.columns:
                numeric_cols = ins_df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    value_col = numeric_cols[0]
                    top_states = ins_df.groupby('state')[value_col].sum().reset_index()
                    top_states = top_states.nlargest(10, value_col)
                    top_states.columns = ['state', value_col]
                    
                    fig = create_comparison_bar(
                        top_states,
                        "",
                        category_col='state',
                        value_col=value_col,
                        orientation='h',
                        color="#9467bd"
                    )
                    st.plotly_chart(fig, width='stretch')
        except Exception as e:
            st.warning(f"Could not load top states: {str(e)}")
    
    st.markdown("---")
    
    # State-level insurance breakdown
    st.subheader("📊 Insurance by State")
    
    try:
        state_ins_df = load_query_data("Query_3.1_Insurance_Growth_Trajectory_by_State_&_Quarter")
        
        if not state_ins_df.empty:
            # Get latest quarter data by state
            if 'quarter' in state_ins_df.columns:
                latest_quarter = state_ins_df['quarter'].max()
                latest_data = state_ins_df[state_ins_df['quarter'] == latest_quarter]
            else:
                latest_data = state_ins_df
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Get numeric columns for visualization
                numeric_cols = latest_data.select_dtypes(include=['number']).columns.tolist()
                
                # Find the best metric column
                metric_col = None
                for col in ['insurance_transactions', 'premium_amount', 'total_policies']:
                    if col in latest_data.columns:
                        metric_col = col
                        break
                
                if not metric_col and len(numeric_cols) > 0:
                    metric_col = numeric_cols[0]
                
                if metric_col and 'state' in latest_data.columns:
                    top_states = latest_data.nlargest(10, metric_col)[['state', metric_col]]
                    
                    fig = create_comparison_bar(
                        top_states,
                        f"Top 10 States by {metric_col.replace('_', ' ').title()}",
                        category_col='state',
                        value_col=metric_col,
                        orientation='h'
                    )
                    st.plotly_chart(fig, width='stretch')
            
            with col2:
                # Market concentration
                if metric_col:
                    st.write("**Market Concentration**")
                    
                    top_5_value = latest_data.nlargest(5, metric_col)[metric_col].sum()
                    total_value = latest_data[metric_col].sum()
                    concentration = (top_5_value / total_value * 100) if total_value > 0 else 0
                    
                    st.metric(
                        "Top 5 States Share",
                        f"{concentration:.1f}%",
                        help="% of total from top 5 states"
                    )
                    
                    # Show top state
                    if not latest_data.empty:
                        top_state_row = latest_data.nlargest(1, metric_col).iloc[0]
                        st.write(f"**Top State:** {top_state_row['state']}")
                        st.metric(
                            "Premium Amount",
                            f"₹{format_large_number(top_state_row[metric_col])}"
                        )
    
    except Exception as e:
        st.warning(f"Could not load state-level insurance data: {str(e)}")

    
    st.markdown("---")
    
    # Market maturity
    st.subheader("📍 Market Maturity & Adoption")
    
    try:
        maturity_df = load_query_data("Query_3.2_Insurance_Market_Maturity_&_Adoption_Gaps")
        
        if not maturity_df.empty and len(maturity_df) > 0:
            st.dataframe(maturity_df, width='stretch')
    
    except Exception as e:
        st.info("Market maturity data not available")
