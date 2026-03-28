"""
Transaction Analytics Page
Detailed transaction analysis with filters and trends
"""

import streamlit as st
import pandas as pd
from utils.database import load_query_data, get_states
from utils.formatting import format_large_number, format_number
from utils.charts import (
    create_trend_line,
    create_comparison_bar,
    create_pie_chart,
)


def transactions_page():
    """Render transactions analytics page"""
    
    st.title("💰 Transaction Analytics")
    st.markdown("---")
    
    # Sidebar filters
    st.sidebar.subheader("📊 Filters")
    
    with st.sidebar:
        selected_state = st.selectbox(
            "Select State (or All)",
            options=["All States"] + get_states(),
            key="trans_state"
        )
    
    st.subheader("Quarterly Transaction Growth")
    
    try:
        # Load quarterly growth data
        growth_df = load_query_data("Query_1.1_Quarterly_Transaction_Growth_by_State_(YoY_Analysis)")
        
        # Filter by state if selected
        if selected_state != "All States":
            growth_df = growth_df[growth_df['state'].str.contains(selected_state, case=False, na=False)]
        
        if not growth_df.empty:
            # Aggregate by quarter across states if "All States" is selected
            if selected_state == "All States":
                if 'quarter' in growth_df.columns:
                    # Aggregate excluding 'year' and 'quarter' from the sum
                    numeric_cols_to_sum = [col for col in growth_df.select_dtypes(include=['number']).columns if col not in ['quarter', 'year']]
                    agg_dict = {col: 'sum' for col in numeric_cols_to_sum}
                    quarterly_agg = growth_df.groupby('quarter').agg(agg_dict).reset_index()
                else:
                    quarterly_agg = growth_df
            else:
                quarterly_agg = growth_df
            
            # Create trend chart
            if 'quarter' in quarterly_agg.columns and len(quarterly_agg) > 0:
                # Find numeric column to chart
                numeric_cols = quarterly_agg.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    value_col = numeric_cols[0]
                    fig = create_trend_line(
                        quarterly_agg,
                        f"Transaction Growth Trend - {selected_state}",
                        x_col='quarter',
                        y_col=value_col
                    )
                    st.plotly_chart(fig, width='stretch')
        else:
            st.info("No transaction data found for selected state")
    
    except Exception as e:
        st.error(f"Error loading transaction growth: {str(e)}")
    
    st.markdown("---")
    
    # Top States by Transaction Revenue
    st.subheader("🏆 Top States by Transaction Revenue")
    
    try:
        states_df = load_query_data("Query_4.1_State-Level_Transaction_Performance_Analytics_(Comprehensive)")
        
        if not states_df.empty:
            # Get top 10 states by transaction amount
            numeric_cols = states_df.select_dtypes(include=['number']).columns.tolist()
            
            # Find transaction amount column
            amount_col = None
            for col in ['transaction_amount', 'revenue', 'transaction_value', 'total_value']:
                if col in states_df.columns:
                    amount_col = col
                    break
            
            if not amount_col and len(numeric_cols) > 0:
                amount_col = numeric_cols[0]
            
            if amount_col and 'state' in states_df.columns:
                # Get top 10 states
                top_states = states_df.nlargest(10, amount_col)[['state', amount_col]]
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Bar chart of top states
                    fig = create_comparison_bar(
                        top_states,
                        "Top 10 States by Transaction Revenue",
                        category_col='state',
                        value_col=amount_col,
                        orientation='h'
                    )
                    st.plotly_chart(fig, width='stretch')
                
                with col2:
                    # Show metrics for top state
                    if not top_states.empty:
                        top_state_row = top_states.iloc[0]
                        st.write(f"**Top State:** {top_state_row['state']}")
                        st.metric(
                            "Revenue",
                            f"₹ {format_large_number(top_state_row[amount_col])}"
                        )
                        
                        # Market concentration
                        top_10_total = top_states[amount_col].sum()
                        all_total = states_df[amount_col].sum()
                        concentration = (top_10_total / all_total * 100) if all_total > 0 else 0
                        st.metric(
                            "Top 10 Concentration",
                            f"{concentration:.1f}%",
                            help="% of total revenue from top 10 states"
                        )
    
    except Exception as e:
        st.error(f"Error loading top states: {str(e)}")
    
    st.markdown("---")
    
    # Detailed statistics
    st.subheader("� Transaction Statistics by State")
    
    try:
        trans_df = load_query_data("Query_4.1_State-Level_Transaction_Performance_Analytics_(Comprehensive)")
        
        if selected_state != "All States":
            trans_df = trans_df[trans_df['state'].str.contains(selected_state, case=False, na=False)]
        
        if not trans_df.empty:
            # Key metrics
            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
            
            numeric_cols = trans_df.select_dtypes(include=['number']).columns.tolist()
            
            # Find the right columns
            trans_col = None
            amount_col = None
            
            for col in numeric_cols:
                if 'count' in col.lower() or 'volume' in col.lower() or 'transaction' in col.lower():
                    if trans_col is None:
                        trans_col = col
                if 'amount' in col.lower() or 'value' in col.lower() or 'revenue' in col.lower():
                    if amount_col is None:
                        amount_col = col
            
            # Fallback to first numeric columns
            if trans_col is None and len(numeric_cols) > 0:
                trans_col = numeric_cols[0]
            if amount_col is None and len(numeric_cols) > 1:
                amount_col = numeric_cols[1]
            
            with stat_col1:
                if trans_col:
                    total_txns = trans_df[trans_col].sum()
                    st.metric("Total Transactions", format_large_number(total_txns))
                else:
                    st.metric("Total Transactions", "N/A")
            
            with stat_col2:
                if amount_col:
                    total_amount = trans_df[amount_col].sum()
                    st.metric("Total Revenue", f"₹ {format_large_number(total_amount)}")
                else:
                    st.metric("Total Revenue", "N/A")
            
            with stat_col3:
                state_count = len(trans_df['state'].unique()) if 'state' in trans_df.columns else 0
                st.metric("States Covered", format_number(state_count))
            
            with stat_col4:
                if trans_col and state_count > 0:
                    avg_txn = trans_df[trans_col].mean()
                    st.metric("Avg per State", format_large_number(avg_txn))
                else:
                    st.metric("Avg per State", "N/A")
            
            st.markdown("---")
            
            # State-level analysis
            st.subheader("State-Level Breakdown")
            
            # Sort and display top states
            sort_col = amount_col if amount_col else trans_col
            if sort_col:
                display_df = trans_df.sort_values(sort_col, ascending=False)
                
                # Show as table
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Additional insights
                col_insight1, col_insight2 = st.columns(2)
                
                with col_insight1:
                    st.write("**Market Concentration**")
                    if trans_col:
                        top5_total = display_df[trans_col].head(5).sum()
                        all_total = display_df[trans_col].sum()
                        concentration = (top5_total / all_total * 100) if all_total > 0 else 0
                        st.write(f"Top 5 states account for **{concentration:.1f}%** of transactions")
                
                with col_insight2:
                    st.write("**State Performance**")
                    if amount_col:
                        max_state = display_df.loc[display_df[amount_col].idxmax(), 'state']
                        max_amount = display_df[amount_col].max()
                        st.write(f"Highest revenue: **{max_state}** (₹{format_large_number(max_amount)})")
        else:
            st.info("No transaction data available for selected filters")
    
    except Exception as e:
        st.warning(f"Could not load transaction statistics: {str(e)}")
