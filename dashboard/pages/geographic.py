"""
Geographic Analysis Page
State-level analysis and geographic distribution
"""

import streamlit as st
import pandas as pd
from utils.database import load_query_data, get_states
from utils.formatting import format_large_number, format_percentage
from utils.charts import (
    create_comparison_bar,
    create_pie_chart,
    create_heatmap,
)


def geographic_page():
    """Render geographic analysis page"""
    
    st.title("🗺️ Geographic Analysis")
    st.markdown("---")
    
    st.info("""
    Analyze PhonePe's performance across different states and regions.
    Identify growth opportunities and market trends by geography.
    """)
    
    # Analysis type selector
    st.sidebar.subheader("📊 View Options")
    analysis_type = st.sidebar.radio(
        "Select Analysis",
        options=[
            "State Performance",
            "Market Share",
            "Growth Classification",
            "Regional Trends"
        ]
    )
    
    if analysis_type == "State Performance":
        state_performance()
    elif analysis_type == "Market Share":
        market_share()
    elif analysis_type == "Growth Classification":
        growth_classification()
    elif analysis_type == "Regional Trends":
        regional_trends()


def state_performance():
    """Show state-level performance metrics"""
    st.subheader("📊 State-Level Performance")
    
    try:
        # Load state performance data
        perf_df = load_query_data("Query_4.1_State-Level_Transaction_Performance_Analytics_(Comprehensive)")
        
        if not perf_df.empty:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                numeric_cols = perf_df.select_dtypes(include=['number']).columns
                
                if len(numeric_cols) > 0 and 'state' in perf_df.columns:
                    top_states = perf_df.nlargest(15, numeric_cols[0])
                    
                    fig = create_comparison_bar(
                        top_states,
                        "Top 15 States by Transaction Volume",
                        category_col='state',
                        value_col=numeric_cols[0],
                        orientation='h'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Summary")
                st.metric("Total States", len(perf_df['state'].unique()) if 'state' in perf_df.columns else 0)
                st.metric("Total Transactions", format_large_number(perf_df[numeric_cols[0]].sum()) if len(numeric_cols) > 0 else 0)
            
            # Detailed table
            st.subheader("Detailed State Metrics")
            st.dataframe(
                perf_df.sort_values(numeric_cols[0] if len(numeric_cols) > 0 else perf_df.columns[0], ascending=False),
                width='stretch'
            )
    
    except Exception as e:
        st.error(f"Error loading state performance: {str(e)}")


def market_share():
    """Show market share analysis"""
    st.subheader("📊 Market Share Analysis")
    
    try:
        share_df = load_query_data("Query_1.4_State-Level_Market_Share_&_Concentration_Analysis")
        
        if not share_df.empty and 'state' in share_df.columns:
            numeric_cols = share_df.select_dtypes(include=['number']).columns
            
            if len(numeric_cols) > 0:
                # Market share by state
                fig = create_pie_chart(
                    share_df.head(10),
                    "Market Share - Top 10 States",
                    values_col=numeric_cols[0],
                    names_col='state'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("---")
                
                # Concentration metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if len(share_df) > 0:
                        top_5 = share_df.nlargest(5, numeric_cols[0])[numeric_cols[0]].sum()
                        total = share_df[numeric_cols[0]].sum()
                        concentration = (top_5 / total * 100) if total > 0 else 0
                        st.metric("Top 5 Concentration", f"{concentration:.1f}%")
                
                with col2:
                    if len(share_df) > 0:
                        top_10 = share_df.nlargest(10, numeric_cols[0])[numeric_cols[0]].sum()
                        concentration = (top_10 / total * 100) if total > 0 else 0
                        st.metric("Top 10 Concentration", f"{concentration:.1f}%")
                
                with col3:
                    st.metric("Markets Analyzed", len(share_df))
                
                # Detailed data
                st.subheader("Market Share by State")
                st.dataframe(share_df, width='stretch')
    
    except Exception as e:
        st.warning(f"Could not load market share analysis: {str(e)}")


def growth_classification():
    """Show growth classification analysis"""
    st.subheader("📈 Growth Classification")
    
    try:
        growth_df = load_query_data("Query_1.3_Stagnant_vs._Growth_States_Classification_(Trend_Analysis)")
        
        if not growth_df.empty:
            if 'state' in growth_df.columns:
                numeric_cols = growth_df.select_dtypes(include=['number']).columns
                
                if len(numeric_cols) > 0 and 'classification' in growth_df.columns:
                    # Classification breakdown
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        classification_counts = growth_df['classification'].value_counts()
                        classification_df = pd.DataFrame({
                            'Classification': classification_counts.index,
                            'Count': classification_counts.values
                        })
                        
                        fig = create_pie_chart(
                            classification_df,
                            "State Classification",
                            values_col='Count',
                            names_col='Classification',
                            donut=True
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # States by classification
                        st.subheader("States by Category")
                        
                        for classification in growth_df['classification'].unique():
                            states = growth_df[growth_df['classification'] == classification]['state'].tolist()
                            st.write(f"**{classification}** ({len(states)} states)")
                            st.caption(", ".join(states[:5]) + ("..." if len(states) > 5 else ""))
            
            # Detailed table
            st.subheader("Trend Analysis Details")
            st.dataframe(growth_df, width='stretch')
    
    except Exception as e:
        st.warning(f"Could not load growth classification: {str(e)}")


def regional_trends():
    """Show regional trends"""
    st.subheader("📍 Regional Trends")
    
    try:
        # Try multiple data sources for regional analysis
        user_df = load_query_data("Query_2.1_State-Level_User_Registration_&_Engagement_Metrics")
        
        if not user_df.empty and 'state' in user_df.columns:
            numeric_cols = user_df.select_dtypes(include=['number']).columns
            
            if len(numeric_cols) > 0:
                # Regional aggregation (group by region)
                col1, col2 = st.columns(2)
                
                with col1:
                    # Top performers
                    top_performers = user_df.nlargest(10, numeric_cols[0])
                    
                    fig = create_comparison_bar(
                        top_performers,
                        "Top 10 States",
                        category_col='state',
                        value_col=numeric_cols[0],
                        orientation='h'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Bottom performers
                    bottom_performers = user_df.nsmallest(10, numeric_cols[0])
                    
                    if len(bottom_performers) > 0:
                        fig = create_comparison_bar(
                            bottom_performers,
                            "Bottom 10 States",
                            category_col='state',
                            value_col=numeric_cols[0],
                            orientation='h',
                            color="#d62728"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("---")
                st.subheader("Regional Distribution")
                st.dataframe(user_df.sort_values(numeric_cols[0], ascending=False), width='stretch')
    
    except Exception as e:
        st.warning(f"Could not load regional trends: {str(e)}")
