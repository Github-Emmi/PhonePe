"""
Reusable chart generation utilities using Plotly.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

# Color scheme
COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "success": "#2ca02c",
    "danger": "#d62728",
    "info": "#17a2b8",
    "light": "#f8f9fa",
    "dark": "#343a40",
}

CATEGORICAL_COLORS = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17a2b8"
]


def create_trend_line(data: pd.DataFrame, title: str = "", 
                     x_col: str = "quarter", y_col: str = "value",
                     color: str = None, show_legend: bool = True) -> go.Figure:
    """
    Create a line chart for trend analysis.
    
    Args:
        data: DataFrame with trend data
        title: Chart title
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        color: Color for the line
        show_legend: Whether to show legend
        
    Returns:
        Plotly Figure object
    """
    if data.empty:
        logger.warning(f"Empty data for trend line: {title}")
        return go.Figure().add_annotation(text="No data available")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data[x_col],
        y=data[y_col],
        mode='lines+markers',
        name=y_col,
        line=dict(color=color or COLORS["primary"], width=2),
        marker=dict(size=6),
        hovertemplate='<b>%{x}</b><br>%{y:.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_col.replace('_', ' ').title(),
        yaxis_title=y_col.replace('_', ' ').title(),
        hovermode='x unified',
        height=400,
        margin=dict(l=60, r=20, t=60, b=50),
        template="plotly_white",
        showlegend=show_legend,
    )
    
    return fig


def create_comparison_bar(data: pd.DataFrame, title: str = "",
                         category_col: str = "category", 
                         value_col: str = "value",
                         orientation: str = 'v',
                         top_n: int = None,
                         color: str = None) -> go.Figure:
    """
    Create a bar chart for comparisons.
    
    Args:
        data: DataFrame with comparison data
        title: Chart title
        category_col: Column name for categories
        value_col: Column name for values
        orientation: 'v' for vertical, 'h' for horizontal
        top_n: Show only top N items
        color: Color for bars
        
    Returns:
        Plotly Figure object
    """
    if data.empty:
        logger.warning(f"Empty data for comparison bar: {title}")
        return go.Figure().add_annotation(text="No data available")
    
    # Sort and limit
    data_sorted = data.sort_values(value_col, ascending=False)
    if top_n:
        data_sorted = data_sorted.head(top_n)
    
    fig = go.Figure()
    
    if orientation == 'h':
        fig.add_trace(go.Bar(
            y=data_sorted[category_col],
            x=data_sorted[value_col],
            orientation='h',
            marker=dict(color=color or COLORS["secondary"]),
            hovertemplate='<b>%{y}</b><br>%{x:.0f}<extra></extra>'
        ))
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    else:
        fig.add_trace(go.Bar(
            x=data_sorted[category_col],
            y=data_sorted[value_col],
            marker=dict(color=color or COLORS["secondary"]),
            hovertemplate='<b>%{x}</b><br>%{y:.0f}<extra></extra>'
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title=category_col.replace('_', ' ').title() if orientation == 'v' else value_col.replace('_', ' ').title(),
        yaxis_title=value_col.replace('_', ' ').title() if orientation == 'v' else category_col.replace('_', ' ').title(),
        height=400,
        margin=dict(l=60, r=20, t=60, b=50),
        template="plotly_white",
        hovermode='closest',
        showlegend=False,
    )
    
    return fig


def create_pie_chart(data: pd.DataFrame, title: str = "",
                    values_col: str = "value",
                    names_col: str = "category",
                    donut: bool = False) -> go.Figure:
    """
    Create a pie or donut chart for composition analysis.
    
    Args:
        data: DataFrame with composition data
        title: Chart title
        values_col: Column name for values
        names_col: Column name for category names
        donut: If True, create donut chart
        
    Returns:
        Plotly Figure object
    """
    if data.empty:
        logger.warning(f"Empty data for pie chart: {title}")
        return go.Figure().add_annotation(text="No data available")
    
    fig = go.Figure(data=[go.Pie(
        labels=data[names_col],
        values=data[values_col],
        hole=0.3 if donut else 0,
        hovertemplate='<b>%{label}</b><br>%{value:.0f} (%{percent})<extra></extra>',
        marker=dict(colors=CATEGORICAL_COLORS)
    )])
    
    fig.update_layout(
        title=title,
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        template="plotly_white",
    )
    
    return fig


def create_heatmap(data: pd.DataFrame, title: str = "",
                  index_col: str = None,
                  columns_col: str = None,
                  values_col: str = "value",
                  colorscale: str = "Viridis") -> go.Figure:
    """
    Create a heatmap for correlation or multi-dimensional analysis.
    
    Args:
        data: DataFrame with heatmap data
        title: Chart title
        index_col: Column for rows
        columns_col: Column for columns
        values_col: Column for values
        colorscale: Plotly colorscale name
        
    Returns:
        Plotly Figure object
    """
    if data.empty:
        logger.warning(f"Empty data for heatmap: {title}")
        return go.Figure().add_annotation(text="No data available")
    
    # Create pivot table if needed
    if index_col and columns_col:
        pivot_data = data.pivot_table(
            index=index_col,
            columns=columns_col,
            values=values_col,
            aggfunc='sum'
        )
    else:
        pivot_data = data
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale=colorscale,
        hovertemplate='%{y}<br>%{x}<br>Value: %{z:.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=title,
        height=400,
        margin=dict(l=100, r=20, t=60, b=50),
        template="plotly_white",
    )
    
    return fig


def create_stacked_bar(data: pd.DataFrame, title: str = "",
                       x_col: str = "category",
                       stack_col: str = "type",
                       value_col: str = "value") -> go.Figure:
    """
    Create a stacked bar chart.
    
    Args:
        data: DataFrame with stacked data
        title: Chart title
        x_col: Column for x-axis
        stack_col: Column to stack by
        value_col: Column for values
        
    Returns:
        Plotly Figure object
    """
    if data.empty:
        return go.Figure().add_annotation(text="No data available")
    
    fig = go.Figure()
    
    for i, stack_val in enumerate(data[stack_col].unique()):
        stack_data = data[data[stack_col] == stack_val]
        fig.add_trace(go.Bar(
            x=stack_data[x_col],
            y=stack_data[value_col],
            name=str(stack_val),
            marker=dict(color=CATEGORICAL_COLORS[i % len(CATEGORICAL_COLORS)]),
            hovertemplate='<b>%{x}</b><br>' + str(stack_val) + ': %{y:.0f}<extra></extra>'
        ))
    
    fig.update_layout(
        title=title,
        barmode='stack',
        xaxis_title=x_col.replace('_', ' ').title(),
        yaxis_title=value_col.replace('_', ' ').title(),
        height=400,
        margin=dict(l=60, r=20, t=60, b=50),
        template="plotly_white",
        hovermode='x unified',
    )
    
    return fig


def create_metric_card(value: str, label: str, 
                      delta: str = None, delta_color: str = None) -> dict:
    """
    Create a metric card configuration.
    
    Args:
        value: Metric value to display
        label: Metric label
        delta: Change value (optional)
        delta_color: Color for delta (optional)
        
    Returns:
        Dictionary with metric card data
    """
    return {
        "value": value,
        "label": label,
        "delta": delta,
        "delta_color": delta_color
    }


def create_box_plot(data: pd.DataFrame, title: str = "",
                   category_col: str = "category",
                   value_col: str = "value") -> go.Figure:
    """
    Create a box plot for distribution analysis.
    
    Args:
        data: DataFrame with distribution data
        title: Chart title
        category_col: Column for categories
        value_col: Column for values
        
    Returns:
        Plotly Figure object
    """
    if data.empty:
        return go.Figure().add_annotation(text="No data available")
    
    fig = go.Figure()
    
    for category in data[category_col].unique():
        cat_data = data[data[category_col] == category]
        fig.add_trace(go.Box(
            y=cat_data[value_col],
            name=str(category),
            boxmean='sd',
            hovertemplate='<b>' + str(category) + '</b><br>%{y:.0f}<extra></extra>'
        ))
    
    fig.update_layout(
        title=title,
        yaxis_title=value_col.replace('_', ' ').title(),
        height=400,
        margin=dict(l=60, r=20, t=60, b=50),
        template="plotly_white",
    )
    
    return fig
