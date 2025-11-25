"""Main Streamlit dashboard application."""

import sys
import os
# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import streamlit as st
from datetime import datetime, timedelta
from src.dashboard.styles.theme import DARK_THEME_CSS
from src.dashboard.utils.api_client import APIClient
from src.dashboard.utils.formatters import format_currency, format_number
from src.dashboard.components.charts import create_line_chart, create_bar_chart, create_pie_chart
from src.dashboard.components.metrics import display_kpi_row
from src.dashboard.components.page_header import get_page_header_html
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Dashboard App",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply dark theme
st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)

# Hide the main app page from navigation since we're the Dashboard Summary page
st.markdown("""
<style>
    [data-testid="stSidebarNav"] ul li:first-child {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Initialize API client
if "api_client" not in st.session_state:
    # Explicitly set the API URL to avoid import issues
    st.session_state.api_client = APIClient(base_url="http://localhost:8000")

api_client = st.session_state.api_client

# Initialize session state for dates if not exists
if "dashboard_start_date" not in st.session_state:
    st.session_state.dashboard_start_date = datetime.now().date() - timedelta(days=30)
if "dashboard_end_date" not in st.session_state:
    st.session_state.dashboard_end_date = datetime.now().date()

# Sidebar
with st.sidebar:
    # Vortex Logo section
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0; margin-bottom: 1rem;'>
        <svg class="logo" width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 0 15px rgba(123, 47, 247, 0.5)); animation: rotate 20s linear infinite;">
            <defs>
                <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#00d4ff;stop-opacity:1" />
                    <stop offset="50%" style="stop-color:#7b2ff7;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#f026ff;stop-opacity:1" />
                </linearGradient>
            </defs>
            <circle cx="30" cy="30" r="28" fill="none" stroke="url(#logoGradient)" stroke-width="2" opacity="0.3"/>
            <circle cx="30" cy="30" r="22" fill="none" stroke="url(#logoGradient)" stroke-width="2" opacity="0.5"/>
            <circle cx="30" cy="30" r="16" fill="none" stroke="url(#logoGradient)" stroke-width="2" opacity="0.7"/>
            <path d="M 30 14 L 38 30 L 30 46 L 22 30 Z" fill="url(#logoGradient)" opacity="0.8"/>
            <circle cx="30" cy="30" r="4" fill="#00d4ff"/>
            <circle cx="30" cy="30" r="2" fill="#ffffff"/>
        </svg>
        <style>
            @keyframes rotate {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
        </style>
    </div>
    <div style='text-align: center; margin-top: -1rem; margin-bottom: 0.5rem;'>
        <h2 style='font-family: "Orbitron", sans-serif; font-size: 1.8rem; font-weight: 900; letter-spacing: 4px;
                    background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 50%, #f026ff 100%);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                    background-clip: text; margin: 0;'>VORTEX</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #00d4ff; font-size: 0.85rem; letter-spacing: 0.1em; margin-top: 0.5rem; font-family: \"Inter\", sans-serif;'>Automotive Intelligence Platform</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("<h4 style='color: #81c784;'>📅 Date Range Filter</h4>", unsafe_allow_html=True)
    
    # Period selector
    days_back = st.select_slider(
        "Period",
        options=[7, 14, 30, 60, 90, 180, 365],
        value=30,
        format_func=lambda x: f"{x} days",
        key="dashboard_period"
    )
    # Update dates when period changes
    if days_back:
        st.session_state.dashboard_end_date = datetime.now().date()
        st.session_state.dashboard_start_date = st.session_state.dashboard_end_date - timedelta(days=days_back)
    
    # Start Date input
    start_date = st.date_input(
        "Start Date",
        value=st.session_state.dashboard_start_date,
        max_value=datetime.now().date(),
        key="dashboard_start"
    )
    st.session_state.dashboard_start_date = start_date
    
    # End Date input
    end_date = st.date_input(
        "End Date",
        value=st.session_state.dashboard_end_date,
        min_value=start_date,
        max_value=datetime.now().date(),
        key="dashboard_end"
    )
    st.session_state.dashboard_end_date = end_date
    
    # Display selected range
    days_selected = (end_date - start_date).days + 1
    st.caption(f"📊 Selected: {days_selected} days")

    st.markdown("---")
    st.caption("⚡ Vortex v2.0")
    st.caption("🚗 Automotive Intelligence")

# Main content - Page Header
st.markdown(get_page_header_html("Dashboard Summary", "Real-time insights powered by AI"), unsafe_allow_html=True)

# Overview Section
st.markdown("<h2 style='color: #00d4ff; font-family: \"Orbitron\", sans-serif; font-weight: 700; letter-spacing: 2px; border-bottom: 2px solid rgba(123, 47, 247, 0.3); padding-bottom: 0.5rem;'>📈 Key Performance Overview</h2>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Load KPIs
with st.spinner("Loading KPIs..."):
    kpis = api_client.get_kpis(start_date, end_date)

if kpis:
    # Display KPIs
    display_kpi_row(kpis)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)

    # Create two columns for charts with proper spacing
    col1, col2 = st.columns(2, gap="large")

    with col1:
        # Sales trend
        st.markdown("<h4 style='color: #4fc3f7;'>📈 Sales Trend</h4>", unsafe_allow_html=True)
        try:
            trends_data = api_client.get_sales_trends(start_date, end_date, period="D")
            if trends_data:
                df_trends = pd.DataFrame(trends_data)
                df_trends["sale_date"] = pd.to_datetime(df_trends["sale_date"])
                fig = create_line_chart(
                    df_trends, "sale_date", "total_amount", "Daily Sales Revenue"
                )
                st.plotly_chart(fig, use_container_width=True, key="sales_trend_chart")
            else:
                st.info("No sales trend data available for the selected period.")
        except Exception as e:
            st.error(f"Error loading sales trend: {str(e)}")
        st.markdown("<br>", unsafe_allow_html=True)

    with col2:
        # Top vehicles
        st.markdown("<h4 style='color: #4fc3f7;'>🏆 Top Selling Vehicles</h4>", unsafe_allow_html=True)
        top_vehicles = api_client.get_top_vehicles(5, start_date, end_date)
        if top_vehicles:
            df_top = pd.DataFrame(top_vehicles)
            df_top["vehicle_name"] = df_top["make"] + " " + df_top["model"]
            fig = create_bar_chart(
                df_top, "vehicle_name", "total_amount", "Top 5 Vehicles by Revenue"
            )
            st.plotly_chart(fig, use_container_width=True, key="top_vehicles_chart")
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)

    # Regional and Category breakdown with better spacing
    col3, col4 = st.columns(2, gap="large")

    with col3:
        st.markdown("<h4 style='color: #4fc3f7;'>🌍 Regional Performance</h4>", unsafe_allow_html=True)
        regional = api_client.get_regional_performance(start_date, end_date)
        if regional:
            df_regional = pd.DataFrame(regional)
            fig = create_pie_chart(
                df_regional, "total_amount", "region", "Revenue by Region"
            )
            st.plotly_chart(fig, use_container_width=True, key="regional_chart")
        st.markdown("<br>", unsafe_allow_html=True)

    with col4:
        st.markdown("<h4 style='color: #4fc3f7;'>🚙 Category Breakdown</h4>", unsafe_allow_html=True)
        categories = api_client.get_category_breakdown(start_date, end_date)
        if categories:
            df_categories = pd.DataFrame(categories)
            fig = create_pie_chart(
                df_categories, "total_amount", "category", "Revenue by Category"
            )
            st.plotly_chart(fig, use_container_width=True, key="category_chart")
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)

    # Inventory Overview
    st.markdown("<h4 style='color: #4fc3f7; border-bottom: 2px solid #2a3342; padding-bottom: 0.5rem;'>📦 Inventory Status</h4>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    inventory = api_client.get_inventory_summary()
    if inventory:
        col5, col6, col7, col8 = st.columns(4, gap="medium")

        with col5:
            st.metric("Total Units", format_number(inventory.get("total_units", 0)))

        with col6:
            st.metric("Total Value", format_currency(inventory.get("total_value", 0)))

        with col7:
            low_stock = inventory.get("low_stock_count", 0)
            st.metric("Low Stock Items", low_stock, delta=None if low_stock == 0 else f"-{low_stock}", delta_color="inverse")

        with col8:
            out_stock = inventory.get("out_of_stock_count", 0)
            st.metric("Out of Stock", out_stock, delta=None if out_stock == 0 else f"-{out_stock}", delta_color="inverse")
    
    st.markdown("<br>", unsafe_allow_html=True)

else:
    st.error("Unable to load KPI data. Please ensure the API is running.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 1rem;'>
    <p style='color: rgba(123, 47, 247, 0.7); font-family: "Inter", sans-serif; font-size: 0.9rem; letter-spacing: 0.05em;'>
        🤖 Powered by OpenAI GPT-4 | Built with FastAPI & Streamlit
    </p>
    <p style='font-family: "Orbitron", sans-serif; font-size: 0.8rem; color: #00d4ff; margin-top: 0.5rem; letter-spacing: 2px;'>
        © 2025 VORTEX • Automotive Intelligence Platform
    </p>
</div>
""", unsafe_allow_html=True)

