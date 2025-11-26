"""
Reusable chart components with Vortex Premium Design
====================================================
Enhanced plotly charts with Vortex color scheme and modern animations.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from src.dashboard.styles.theme import PLOTLY_DARK_THEME

# Vortex color palette
VORTEX_COLORS = {
    'primary': '#00d4ff',      # Vortex Cyan
    'secondary': '#7b2ff7',    # Vortex Purple
    'accent': '#f026ff',       # Vortex Pink
    'gradient_start': 'rgba(0, 212, 255, 0.8)',
    'gradient_end': 'rgba(123, 47, 247, 0.8)',
    'fill': 'rgba(0, 212, 255, 0.15)',
    'grid': 'rgba(0, 212, 255, 0.1)',
}


def create_line_chart(df: pd.DataFrame, x: str, y: str, title: str):
    """Create line chart with Vortex premium styling and animations."""
    fig = px.line(df, x=x, y=y)
    
    layout = {**PLOTLY_DARK_THEME["layout"]}
    layout.update({
        "height": 500,  # Increased height for better visibility
        "margin": dict(l=60, r=40, t=100, b=80),
        "title": dict(
            text=f"<b>{title}</b>",
            font=dict(size=22, color=VORTEX_COLORS['primary'], family="Orbitron"),
            x=0.5,
            xanchor='center',
            y=0.95,
            yanchor='top'
        ),
        "hovermode": 'x unified',
        "plot_bgcolor": "rgba(0, 0, 0, 0.2)",
        "paper_bgcolor": "rgba(0, 0, 0, 0.1)",
    })
    
    fig.update_layout(**layout)
    fig.update_traces(
        line=dict(width=4, color=VORTEX_COLORS['primary'], shape='spline'),
        mode='lines+markers',
        marker=dict(
            size=10, 
            color=VORTEX_COLORS['primary'], 
            line=dict(width=2, color=VORTEX_COLORS['secondary']),
            symbol='circle'
        ),
        fill='tozeroy',
        fillcolor=VORTEX_COLORS['fill'],
        hovertemplate='<b>%{x}</b><br>Value: $%{y:,.0f}<extra></extra>'
    )
    fig.update_xaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor=VORTEX_COLORS['grid'],
        tickfont=dict(size=12, color='rgba(255, 255, 255, 0.7)')
    )
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor=VORTEX_COLORS['grid'],
        tickfont=dict(size=12, color='rgba(255, 255, 255, 0.7)')
    )
    return fig


def create_bar_chart(df: pd.DataFrame, x: str, y: str, title: str, color: str = None):
    """Create bar chart with Vortex premium gradient styling."""
    fig = px.bar(df, x=x, y=y, color=color)
    
    layout = {**PLOTLY_DARK_THEME["layout"]}
    layout.update({
        "height": 500,
        "margin": dict(l=60, r=40, t=100, b=120),
        "title": dict(
            text=f"<b>{title}</b>",
            font=dict(size=22, color=VORTEX_COLORS['primary'], family="Orbitron"),
            x=0.5,
            xanchor='center',
            y=0.95,
            yanchor='top'
        ),
        "xaxis_tickangle": -35,
        "hovermode": 'x unified',
        "showlegend": False if color is None else True,
        "plot_bgcolor": "rgba(0, 0, 0, 0.2)",
        "paper_bgcolor": "rgba(0, 0, 0, 0.1)",
    })
    
    fig.update_layout(**layout)
    
    # Create gradient effect for bars
    colors = [VORTEX_COLORS['primary'], VORTEX_COLORS['secondary'], VORTEX_COLORS['accent']] * (len(df) // 3 + 1)
    
    fig.update_traces(
        marker=dict(
            color=colors[:len(df)],
            line=dict(width=2, color='rgba(0, 0, 0, 0.3)'),
            opacity=0.9
        ),
        hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'
    )
    fig.update_xaxes(
        showgrid=False,
        tickfont=dict(size=11, color='rgba(255, 255, 255, 0.7)')
    )
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor=VORTEX_COLORS['grid'],
        tickfont=dict(size=12, color='rgba(255, 255, 255, 0.7)')
    )
    return fig


def create_pie_chart(df: pd.DataFrame, values: str, names: str, title: str):
    """Create donut chart with Vortex premium gradient colors."""
    fig = px.pie(df, values=values, names=names, hole=0.5)  # Larger hole for modern donut look
    
    layout = {**PLOTLY_DARK_THEME["layout"]}
    layout.update({
        "height": 500,
        "margin": dict(l=40, r=180, t=100, b=60),
        "title": dict(
            text=f"<b>{title}</b>",
            font=dict(size=22, color=VORTEX_COLORS['primary'], family="Orbitron"),
            x=0.5,
            xanchor='center',
            y=0.95,
            yanchor='top'
        ),
        "showlegend": True,
        "legend": dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(size=13, color='rgba(255, 255, 255, 0.85)', family="Inter"),
            bgcolor='rgba(0, 0, 0, 0.3)',
            bordercolor=VORTEX_COLORS['primary'],
            borderwidth=1
        ),
        "plot_bgcolor": "rgba(0, 0, 0, 0.2)",
        "paper_bgcolor": "rgba(0, 0, 0, 0.1)",
    })
    
    fig.update_layout(**layout)
    
    # Vortex color palette for pie slices
    vortex_palette = [
        VORTEX_COLORS['primary'],   # Cyan
        VORTEX_COLORS['secondary'], # Purple
        VORTEX_COLORS['accent'],    # Pink
        '#00ffff',  # Bright cyan
        '#a855f7',  # Light purple
        '#33e0ff',  # Light cyan
        '#9333ea',  # Deep purple
        '#ff00ff'   # Bright pink
    ]
    
    fig.update_traces(
        textposition='auto',
        textinfo='percent',
        textfont=dict(size=14, color='white', family="Orbitron", weight=600),
        marker=dict(
            line=dict(color='rgba(0, 0, 0, 0.4)', width=3),
            colors=vortex_palette
        ),
        hovertemplate='<b>%{label}</b><br>Value: $%{value:,.0f}<br>Percent: %{percent}<extra></extra>',
        pull=[0.05] * len(df)  # Slight separation for modern look
    )
    return fig


def create_area_chart(df: pd.DataFrame, x: str, y: str, title: str):
    """Create area chart with Vortex gradient fill."""
    fig = px.area(df, x=x, y=y)
    
    layout = {**PLOTLY_DARK_THEME["layout"]}
    layout.update({
        "height": 500,
        "margin": dict(l=60, r=40, t=100, b=80),
        "title": dict(
            text=f"<b>{title}</b>",
            font=dict(size=22, color=VORTEX_COLORS['primary'], family="Orbitron"),
            x=0.5,
            xanchor='center',
            y=0.95,
            yanchor='top'
        ),
        "hovermode": 'x unified',
        "plot_bgcolor": "rgba(0, 0, 0, 0.2)",
        "paper_bgcolor": "rgba(0, 0, 0, 0.1)",
    })
    
    fig.update_layout(**layout)
    fig.update_traces(
        fillcolor='rgba(0, 212, 255, 0.2)',
        line=dict(color=VORTEX_COLORS['primary'], width=3, shape='spline'),
        hovertemplate='<b>%{x}</b><br>Value: $%{y:,.0f}<extra></extra>'
    )
    fig.update_xaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor=VORTEX_COLORS['grid'],
        tickfont=dict(size=12, color='rgba(255, 255, 255, 0.7)')
    )
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor=VORTEX_COLORS['grid'],
        tickfont=dict(size=12, color='rgba(255, 255, 255, 0.7)')
    )
    return fig
