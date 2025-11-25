"""Reusable chart components."""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from src.dashboard.styles.theme import PLOTLY_DARK_THEME


def create_line_chart(df: pd.DataFrame, x: str, y: str, title: str):
    """Create line chart with enhanced styling."""
    fig = px.line(df, x=x, y=y)
    
    # Create layout dict without margin to avoid conflicts
    layout = {**PLOTLY_DARK_THEME["layout"]}
    layout.update({
        "height": 450,
        "margin": dict(l=40, r=40, t=80, b=60),
        "title": dict(
            text=f"<b>📊 {title}</b>",
            font=dict(size=18, color="#64b5f6"),
            x=0.5,
            xanchor='center'
        ),
        "hovermode": 'x unified'
    })
    
    fig.update_layout(**layout)
    fig.update_traces(
        line=dict(width=3, color='#4fc3f7'),
        mode='lines+markers',
        marker=dict(size=8, color='#4fc3f7', line=dict(width=2, color='#81c784')),
        fill='tozeroy',
        fillcolor='rgba(79, 195, 247, 0.1)'
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(42, 51, 66, 0.5)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(42, 51, 66, 0.5)')
    return fig


def create_bar_chart(df: pd.DataFrame, x: str, y: str, title: str, color: str = None):
    """Create bar chart with enhanced styling."""
    fig = px.bar(df, x=x, y=y, color=color)
    
    # Create layout dict without margin to avoid conflicts
    layout = {**PLOTLY_DARK_THEME["layout"]}
    layout.update({
        "height": 450,
        "margin": dict(l=40, r=40, t=80, b=100),
        "title": dict(
            text=f"<b>📊 {title}</b>",
            font=dict(size=18, color="#64b5f6"),
            x=0.5,
            xanchor='center'
        ),
        "xaxis_tickangle": -45,
        "hovermode": 'x unified',
        "showlegend": False if color is None else True
    })
    
    fig.update_layout(**layout)
    fig.update_traces(
        marker=dict(
            line=dict(width=1, color='rgba(42, 51, 66, 0.5)'),
            opacity=0.95,
            pattern_shape=""
        ),
        hovertemplate='<b>%{x}</b><br>Value: %{y:,.0f}<extra></extra>'
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(42, 51, 66, 0.5)')
    return fig


def create_pie_chart(df: pd.DataFrame, values: str, names: str, title: str):
    """Create pie chart with enhanced styling."""
    fig = px.pie(df, values=values, names=names, hole=0.45)
    
    # Create layout dict without margin to avoid conflicts
    layout = {**PLOTLY_DARK_THEME["layout"]}
    layout.update({
        "height": 450,
        "margin": dict(l=40, r=140, t=80, b=60),
        "title": dict(
            text=f"<b>📊 {title}</b>",
            font=dict(size=18, color="#64b5f6"),
            x=0.5,
            xanchor='center'
        ),
        "showlegend": True,
        "legend": dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(size=12, color="#e0e0e0"),
            bgcolor='rgba(28, 35, 49, 0.5)',
            bordercolor='#2a3342',
            borderwidth=1
        )
    })
    
    fig.update_layout(**layout)
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont=dict(size=13, color='white'),
        marker=dict(
            line=dict(color='#1c2331', width=3),
            colors=['#4fc3f7', '#81c784', '#ef5350', '#ffb74d', '#ba68c8', '#4db6ac', '#ff8a80', '#ffd54f']
        ),
        hovertemplate='<b>%{label}</b><br>Value: %{value:,.0f}<br>Percent: %{percent}<extra></extra>'
    )
    return fig


def create_area_chart(df: pd.DataFrame, x: str, y: str, title: str):
    """Create area chart with enhanced styling."""
    fig = px.area(df, x=x, y=y)
    
    # Create layout dict without margin to avoid conflicts
    layout = {**PLOTLY_DARK_THEME["layout"]}
    layout.update({
        "height": 450,
        "margin": dict(l=40, r=40, t=80, b=60),
        "title": dict(
            text=f"<b>📊 {title}</b>",
            font=dict(size=18, color="#64b5f6"),
            x=0.5,
            xanchor='center'
        ),
        "hovermode": 'x unified'
    })
    
    fig.update_layout(**layout)
    fig.update_traces(
        fillcolor='rgba(79, 195, 247, 0.25)',
        line=dict(color='#4fc3f7', width=3),
        hovertemplate='<b>%{x}</b><br>Value: %{y:,.0f}<extra></extra>'
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(42, 51, 66, 0.5)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(42, 51, 66, 0.5)')
    return fig
