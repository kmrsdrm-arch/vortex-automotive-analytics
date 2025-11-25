"""Sales Analytics page."""

import sys
import os
# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import streamlit as st
from datetime import datetime, timedelta
from src.dashboard.styles.theme import DARK_THEME_CSS
from src.dashboard.utils.api_client import APIClient
from src.dashboard.components.charts import create_line_chart, create_bar_chart, create_area_chart
from src.dashboard.components.page_header import get_page_header_html
import pandas as pd

st.set_page_config(page_title="Sales Analytics", page_icon="💰", layout="wide")
st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)

# Hide the main app page from navigation
st.markdown("""
<style>
    [data-testid="stSidebarNav"] ul li:first-child {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Initialize API client
if "api_client" not in st.session_state:
    st.session_state.api_client = APIClient()
api_client = st.session_state.api_client

st.markdown(get_page_header_html("Sales Analytics", "Comprehensive sales performance analysis"), unsafe_allow_html=True)

# Filters in a cleaner layout - Period + Independent Start/End Dates
col1, col2, col3, col4 = st.columns([1, 1, 1, 1], gap="medium")

# Initialize session state for dates if not exists
if "sales_start_date" not in st.session_state:
    st.session_state.sales_start_date = datetime.now().date() - timedelta(days=30)
if "sales_end_date" not in st.session_state:
    st.session_state.sales_end_date = datetime.now().date()

with col1:
    days_back = st.selectbox("📅 Period (Days)", [7, 14, 30, 60, 90, 180, 365], index=2, key="sales_period")
    # Update dates when period changes
    if days_back:
        st.session_state.sales_end_date = datetime.now().date()
        st.session_state.sales_start_date = st.session_state.sales_end_date - timedelta(days=days_back)

with col2:
    start_date = st.date_input(
        "📅 Start Date", 
        value=st.session_state.sales_start_date,
        max_value=datetime.now().date(),
        key="sales_start"
    )
    st.session_state.sales_start_date = start_date

with col3:
    end_date = st.date_input(
        "📅 End Date", 
        value=st.session_state.sales_end_date,
        min_value=start_date,
        max_value=datetime.now().date(),
        key="sales_end"
    )
    st.session_state.sales_end_date = end_date

with col4:
    st.write("")  # Spacing
    st.metric("📊 Days", (end_date - start_date).days + 1)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# Load data
with st.spinner("Loading sales data..."):
    summary = api_client.get_sales_summary(start_date, end_date)
    trends = api_client.get_sales_trends(start_date, end_date, period="D")
    regional = api_client.get_regional_performance(start_date, end_date)
    segments = api_client.get_customer_segments(start_date, end_date)
    top_vehicles = api_client.get_top_vehicles(10, start_date, end_date)

if summary:
    # Summary metrics
    st.markdown("<h3 style='color: #64b5f6; border-bottom: 2px solid #2a3342; padding-bottom: 0.5rem;'>📊 Summary Metrics</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        st.metric("💵 Total Revenue", f"${summary['total_revenue']:,.0f}")
    with col2:
        st.metric("📦 Units Sold", f"{summary['total_units']:,}")
    with col3:
        st.metric("🛒 Transactions", f"{summary['total_transactions']:,}")
    with col4:
        st.metric("💳 Avg Discount", f"{summary['avg_discount']:.2f}%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sales trends
    st.markdown("<h3 style='color: #64b5f6; border-bottom: 2px solid #2a3342; padding-bottom: 0.5rem;'>📈 Sales Trends Over Time</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if trends:
        df_trends = pd.DataFrame(trends)
        df_trends["sale_date"] = pd.to_datetime(df_trends["sale_date"])
        fig = create_area_chart(df_trends, "sale_date", "total_amount", "Daily Revenue")
        st.plotly_chart(fig, use_container_width=True, key="sales_trends_chart")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Regional and Segments
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("<h4 style='color: #4fc3f7;'>🌍 Regional Performance</h4>", unsafe_allow_html=True)
        if regional:
            df_regional = pd.DataFrame(regional)
            st.dataframe(df_regional, use_container_width=True, hide_index=True)
        else:
            st.info("No regional data available")
    
    with col2:
        st.markdown("<h4 style='color: #4fc3f7;'>👥 Customer Segments</h4>", unsafe_allow_html=True)
        if segments:
            df_segments = pd.DataFrame(segments)
            st.dataframe(df_segments, use_container_width=True, hide_index=True)
        else:
            st.info("No segment data available")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Top vehicles
    st.markdown("<h3 style='color: #64b5f6; border-bottom: 2px solid #2a3342; padding-bottom: 0.5rem;'>🏆 Top 10 Selling Vehicles</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if top_vehicles:
        df_top = pd.DataFrame(top_vehicles)
        df_top["vehicle"] = df_top["make"] + " " + df_top["model"]
        fig = create_bar_chart(df_top, "vehicle", "total_amount", "Revenue by Vehicle")
        st.plotly_chart(fig, use_container_width=True, key="top_vehicles_detailed_chart")
    else:
        st.info("No vehicle sales data available")
    
    st.markdown("<br>", unsafe_allow_html=True)
else:
    st.error("❌ Unable to load sales data. Please ensure the API is running.")

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

