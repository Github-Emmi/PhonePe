"""
Reports & Export Page
Data export and report generation
"""

import streamlit as st
import pandas as pd
from io import BytesIO
from utils.database import load_query_data, list_available_queries


def reports_page():
    """Render reports and export page"""
    
    st.title("📊 Reports & Data Export")
    st.markdown("---")
    
    # Report type selector
    report_type = st.radio(
        "Select Report Type",
        options=[
            "Export Query Data",
            "Summary Report",
            "Comparison Report",
        ]
    )
    
    if report_type == "Export Query Data":
        export_query_data()
    elif report_type == "Summary Report":
        summary_report()
    elif report_type == "Comparison Report":
        comparison_report()
    
    st.markdown("---")
    st.subheader("📌 Available Queries")
    
    try:
        queries = list_available_queries()
        st.info(f"Total {len(queries)} queries available")
        
        # Show query list in columns
        col1, col2, col3 = st.columns(3)
        
        for i, query in enumerate(queries):
            with col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3:
                st.caption(f"• {query[:40]}...")
    
    except Exception as e:
        st.warning(f"Could not load query list: {str(e)}")


def export_query_data():
    """Export individual query data"""
    
    st.subheader("📥 Export Query Data")
    
    try:
        queries = list_available_queries()
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_query = st.selectbox(
                "Select Query to Export",
                options=queries,
                key="export_query"
            )
        
        with col2:
            export_format = st.selectbox(
                "Export Format",
                options=["CSV", "Excel"],
                key="export_format"
            )
        
        if st.button("📥 Load & Export Data", key="export_btn"):
            try:
                with st.spinner("Loading data..."):
                    df = load_query_data(selected_query)
                
                if not df.empty:
                    st.success(f"✅ Loaded {len(df)} rows × {len(df.columns)} columns")
                    
                    # Show preview
                    st.subheader("Data Preview")
                    st.dataframe(df.head(10), width='stretch')
                    
                    st.subheader("📊 Statistics")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Rows", len(df))
                    with col2:
                        st.metric("Columns", len(df.columns))
                    with col3:
                        numeric_cols = len(df.select_dtypes(include=['number']).columns)
                        st.metric("Numeric Columns", numeric_cols)
                    
                    # Export button
                    st.markdown("---")
                    
                    if export_format == "CSV":
                        csv_data = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download as CSV",
                            data=csv_data,
                            file_name=f"{selected_query}.csv",
                            mime="text/csv"
                        )
                    
                    elif export_format == "Excel":
                        buffer = BytesIO()
                        df.to_excel(buffer, sheet_name="Data", index=False)
                        buffer.seek(0)
                        
                        st.download_button(
                            label="📥 Download as Excel",
                            data=buffer.getvalue(),
                            file_name=f"{selected_query}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
            
            except Exception as e:
                st.error(f"Error exporting data: {str(e)}")
    
    except Exception as e:
        st.error(f"Error initializing export: {str(e)}")


def summary_report():
    """Generate summary report"""
    
    st.subheader("📊 Dashboard Summary Report")
    
    try:
        from utils.metrics import (
            calculate_transaction_metrics,
            calculate_user_metrics,
            calculate_insurance_metrics
        )
        
        with st.spinner("Generating report..."):
            trans_metrics = calculate_transaction_metrics()
            user_metrics = calculate_user_metrics()
            ins_metrics = calculate_insurance_metrics()
        
        st.success("✅ Report Generated")
        
        # Transaction summary
        st.subheader("💰 Transaction Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            from utils.formatting import format_large_number
            value = trans_metrics.get('total_transactions', 0)
            st.metric("Total Transactions", format_large_number(value))
        
        with col2:
            from utils.formatting import format_currency
            value = trans_metrics.get('total_transaction_amount', 0)
            st.metric("Total Value", format_currency(value, decimals=0))
        
        with col3:
            value = trans_metrics.get('avg_transaction_size', 0)
            st.metric("Avg Transaction Size", format_currency(value))
        
        # User summary
        st.subheader("👥 User Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            value = user_metrics.get('total_registered_users', 0)
            st.metric("Registered Users", format_large_number(value))
        
        with col2:
            value = user_metrics.get('total_active_users', 0)
            st.metric("Active Users", format_large_number(value))
        
        with col3:
            if user_metrics.get('total_registered_users', 0) > 0:
                active = user_metrics.get('total_active_users', 0)
                registered = user_metrics.get('total_registered_users', 0)
                percent = (active / registered * 100) if registered > 0 else 0
                st.metric("Activation Rate", f"{percent:.1f}%")
        
        # Insurance summary
        st.subheader("🛡️ Insurance Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            value = ins_metrics.get('total_insurance_transactions', 0)
            st.metric("Insurance Policies", format_large_number(value))
        
        with col2:
            value = ins_metrics.get('total_premium_amount', 0)
            st.metric("Total Premium", format_currency(value, decimals=0))
        
        with col3:
            value = ins_metrics.get('avg_insurance_premium', 0)
            st.metric("Avg Premium", format_currency(value))
        
        # Export report
        st.markdown("---")
        if st.button("📥 Export Summary as CSV", key="export_summary"):
            summary_data = {
                'Metric': [
                    'Total Transactions',
                    'Transaction Value',
                    'Avg Transaction Size',
                    'Registered Users',
                    'Active Users',
                    'Insurance Policies',
                    'Total Premium'
                ],
                'Value': [
                    trans_metrics.get('total_transactions', 0),
                    trans_metrics.get('total_transaction_amount', 0),
                    trans_metrics.get('avg_transaction_size', 0),
                    user_metrics.get('total_registered_users', 0),
                    user_metrics.get('total_active_users', 0),
                    ins_metrics.get('total_insurance_transactions', 0),
                    ins_metrics.get('total_premium_amount', 0),
                ]
            }
            
            summary_df = pd.DataFrame(summary_data)
            csv_data = summary_df.to_csv(index=False)
            
            st.download_button(
                label="📥 Download Summary",
                data=csv_data,
                file_name="dashboard_summary.csv",
                mime="text/csv"
            )
    
    except Exception as e:
        st.error(f"Error generating report: {str(e)}")


def comparison_report():
    """Generate comparison report between two queries or states"""
    
    st.subheader("📊 Comparison Report")
    
    comparison_type = st.selectbox(
        "Compare by",
        options=["States", "Quarters"],
        key="comp_type"
    )
    
    if comparison_type == "States":
        compare_states()
    elif comparison_type == "Quarters":
        compare_quarters()


def compare_states():
    """Compare metrics between two states"""
    
    try:
        from utils.database import get_states
        from utils.formatting import format_large_number, format_currency
        
        states = get_states()
        
        col1, col2 = st.columns(2)
        
        with col1:
            state1 = st.selectbox("State 1", options=states, key="state1")
        
        with col2:
            state2 = st.selectbox("State 2", options=states, key="state2", index=1)
        
        if st.button("🔄 Generate State Comparison", key="gen_comp_states"):
            try:
                # Load transaction data
                trans_df = load_query_data("Query_1.1_Quarterly_Transaction_Growth_by_State_(YoY_Analysis)")
                
                state1_data = trans_df[trans_df['state'] == state1]
                state2_data = trans_df[trans_df['state'] == state2]
                
                if state1_data.empty or state2_data.empty:
                    st.warning("One or both states have no data")
                    return
                
                # Calculate comparison metrics
                st.subheader(f"📊 {state1} vs {state2}")
                
                cols = st.columns(2)
                
                # Find numeric columns for comparison
                numeric_cols = state1_data.select_dtypes(include=['number']).columns.tolist()
                
                # Filter useful columns
                comparison_cols = [col for col in numeric_cols 
                                  if col not in ['quarter', 'year'] and state1_data[col].sum() > 0]
                
                if len(comparison_cols) == 0:
                    st.warning("No numeric data available for comparison")
                    return
                
                # Use first metric column for comparison
                metric_col = comparison_cols[0]
                
                with cols[0]:
                    st.write(f"### {state1}")
                    state1_total = state1_data[metric_col].sum()
                    st.metric("Total", format_large_number(state1_total))
                    
                    if 'quarter' in state1_data.columns:
                        q_data = state1_data.groupby('quarter')[metric_col].sum()
                        st.write("**By Quarter:**")
                        for q, val in q_data.items():
                            st.write(f"Q{q}: {format_large_number(val)}")
                
                with cols[1]:
                    st.write(f"### {state2}")
                    state2_total = state2_data[metric_col].sum()
                    st.metric("Total", format_large_number(state2_total))
                    
                    if 'quarter' in state2_data.columns:
                        q_data = state2_data.groupby('quarter')[metric_col].sum()
                        st.write("**By Quarter:**")
                        for q, val in q_data.items():
                            st.write(f"Q{q}: {format_large_number(val)}")
                
                # Comparison insights
                st.markdown("---")
                st.subheader("📈 Comparison Insights")
                
                diff = state1_total - state2_total
                diff_pct = (diff / state2_total * 100) if state2_total > 0 else 0
                
                if diff > 0:
                    st.success(f"✓ {state1} is **{abs(diff_pct):.1f}%** higher than {state2}")
                elif diff < 0:
                    st.info(f"→ {state2} is **{abs(diff_pct):.1f}%** higher than {state1}")
                else:
                    st.info("Both states are equal")
                
                # Show comparison dataframe
                st.write("**Detailed Comparison:**")
                comparison_data = {
                    'Metric': [state1, state2, 'Difference'],
                    'Value': [state1_total, state2_total, diff]
                }
                comparison_df = pd.DataFrame(comparison_data)
                st.dataframe(comparison_df, use_container_width=True, hide_index=True)
                
            except Exception as e:
                st.error(f"Error generating comparison: {str(e)}")
    
    except Exception as e:
        st.warning(f"Could not load states: {str(e)}")


def compare_quarters():
    """Compare metrics between two quarters"""
    
    try:
        # Load quarterly data
        trans_df = load_query_data("Query_1.1_Quarterly_Transaction_Growth_by_State_(YoY_Analysis)")
        
        if 'quarter' not in trans_df.columns:
            st.warning("Quarterly data not available")
            return
        
        quarters = sorted(trans_df['quarter'].unique())
        
        col1, col2 = st.columns(2)
        
        with col1:
            quarter1 = st.selectbox("Quarter 1", options=quarters, key="quarter1")
        
        with col2:
            quarter2 = st.selectbox("Quarter 2", options=quarters, key="quarter2", index=1)
        
        if st.button("🔄 Generate Quarterly Comparison", key="gen_comp_quarters"):
            try:
                from utils.formatting import format_large_number
                
                # Filter data by quarters
                q1_data = trans_df[trans_df['quarter'] == quarter1]
                q2_data = trans_df[trans_df['quarter'] == quarter2]
                
                # Find numeric columns for comparison
                numeric_cols = q1_data.select_dtypes(include=['number']).columns.tolist()
                comparison_cols = [col for col in numeric_cols 
                                  if col not in ['quarter', 'year'] and q1_data[col].sum() > 0]
                
                if len(comparison_cols) == 0:
                    st.warning("No numeric data available for comparison")
                    return
                
                st.subheader(f"📊 Quarter {quarter1} vs Quarter {quarter2}")
                
                # Create comparison table for all metrics
                comparison_data = []
                
                for metric_col in comparison_cols[:5]:  # Top 5 metrics
                    q1_total = q1_data[metric_col].sum()
                    q2_total = q2_data[metric_col].sum()
                    diff = q1_total - q2_total
                    diff_pct = (diff / q2_total * 100) if q2_total > 0 else 0
                    
                    comparison_data.append({
                        'Metric': metric_col.replace('_', ' ').title(),
                        f'Q{quarter1}': format_large_number(q1_total),
                        f'Q{quarter2}': format_large_number(q2_total),
                        'Change %': f"{diff_pct:+.1f}%"
                    })
                
                comparison_df = pd.DataFrame(comparison_data)
                st.dataframe(comparison_df, use_container_width=True, hide_index=True)
                
                # Key insights
                st.markdown("---")
                st.subheader("📈 Quarterly Insights")
                
                # Overall trend
                primary_metric = comparison_cols[0]
                q1_primary = q1_data[primary_metric].sum()
                q2_primary = q2_data[primary_metric].sum()
                trend = ((q1_primary - q2_primary) / q2_primary * 100) if q2_primary > 0 else 0
                
                if trend > 0:
                    st.success(f"✓ **{trend:+.1f}%** growth from Q{quarter2} to Q{quarter1}")
                elif trend < 0:
                    st.warning(f"↓ **{trend:.1f}%** decline from Q{quarter2} to Q{quarter1}")
                else:
                    st.info("No change in quarterly metrics")
                
                # Top states analysis
                st.subheader("Top States in Each Quarter")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Q{quarter1} Top States**")
                    q1_states = q1_data.groupby('state')[primary_metric].sum().nlargest(5)
                    for state, val in q1_states.items():
                        st.write(f"• {state}: {format_large_number(val)}")
                
                with col2:
                    st.write(f"**Q{quarter2} Top States**")
                    q2_states = q2_data.groupby('state')[primary_metric].sum().nlargest(5)
                    for state, val in q2_states.items():
                        st.write(f"• {state}: {format_large_number(val)}")
                
            except Exception as e:
                st.error(f"Error generating quarterly comparison: {str(e)}")
    
    except Exception as e:
        st.warning(f"Could not load quarterly data: {str(e)}")
