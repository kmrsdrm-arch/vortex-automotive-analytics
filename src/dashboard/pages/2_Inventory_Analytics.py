"""Inventory Analytics page."""

import sys
import os
# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import streamlit as st
from datetime import datetime, timedelta
from src.dashboard.styles.theme import DARK_THEME_CSS
from src.dashboard.utils.api_client import APIClient
from src.dashboard.utils.formatters import format_currency, format_number
from src.dashboard.components.page_header import get_page_header_html
import pandas as pd

st.set_page_config(page_title="Inventory Analytics", page_icon="📦", layout="wide")
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

st.markdown(get_page_header_html("Inventory Analytics", "Real-time inventory monitoring and alerts"), unsafe_allow_html=True)

# Filters in a cleaner layout - Allow date range selection
col1, col2, col3, col4 = st.columns([1, 1, 1, 1], gap="medium")

# Initialize session state for dates if not exists
if "inventory_start_date" not in st.session_state:
    st.session_state.inventory_start_date = datetime.now().date() - timedelta(days=30)
if "inventory_end_date" not in st.session_state:
    st.session_state.inventory_end_date = datetime.now().date()

with col1:
    days_back = st.selectbox("📅 Period (Days)", [7, 14, 30, 60, 90, 180, 365], index=2, key="inventory_period")
    # Update dates when period changes
    if days_back:
        st.session_state.inventory_end_date = datetime.now().date()
        st.session_state.inventory_start_date = st.session_state.inventory_end_date - timedelta(days=days_back)

with col2:
    start_date = st.date_input(
        "📅 Start Date", 
        value=st.session_state.inventory_start_date,
        max_value=datetime.now().date(),
        key="inventory_start"
    )
    st.session_state.inventory_start_date = start_date

with col3:
    end_date = st.date_input(
        "📅 End Date", 
        value=st.session_state.inventory_end_date,
        min_value=start_date,
        max_value=datetime.now().date(),
        key="inventory_end"
    )
    st.session_state.inventory_end_date = end_date

with col4:
    st.write("")  # Spacing
    st.metric("📊 Days", (end_date - start_date).days + 1)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# Load data
with st.spinner("Loading inventory data..."):
    status = api_client.get_inventory_status()
    low_stock = api_client.get_low_stock()

if status:
    summary = status.get("summary", {})
    by_region = status.get("by_region", [])
    by_category = status.get("by_category", [])
    
    # Summary metrics
    st.markdown("<h3 style='color: #64b5f6; border-bottom: 2px solid #2a3342; padding-bottom: 0.5rem;'>📊 Inventory Summary</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📦 Total Units", format_number(summary.get("total_units", 0)))
    with col2:
        st.metric("💰 Total Value", format_currency(summary.get("total_value", 0)))
    with col3:
        low_stock_count = summary.get("low_stock_count", 0)
        st.metric("⚠️ Low Stock", low_stock_count, delta=None if low_stock_count == 0 else f"-{low_stock_count}", delta_color="inverse")
    with col4:
        out_stock_count = summary.get("out_of_stock_count", 0)
        st.metric("🚫 Out of Stock", out_stock_count, delta=None if out_stock_count == 0 else f"-{out_stock_count}", delta_color="inverse")
    
    st.markdown("---")
    
    # Regional and Category distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h4 style='color: #4fc3f7;'>🌍 Inventory by Region</h4>", unsafe_allow_html=True)
        if by_region:
            df_region = pd.DataFrame(by_region)
            st.dataframe(df_region, use_container_width=True, hide_index=True)
        else:
            st.info("No regional data available")
    
    with col2:
        st.markdown("<h4 style='color: #4fc3f7;'>🚙 Inventory by Category</h4>", unsafe_allow_html=True)
        if by_category:
            df_category = pd.DataFrame(by_category)
            st.dataframe(df_category, use_container_width=True, hide_index=True)
        else:
            st.info("No category data available")
    
    # Low stock alerts
    st.markdown("<h3 style='color: #64b5f6; border-bottom: 2px solid #2a3342; padding-bottom: 0.5rem;'>⚠️ Low Stock Alerts</h3>", unsafe_allow_html=True)
    if low_stock:
        df_low = pd.DataFrame(low_stock)
        st.warning(f"**{len(low_stock)} items need restocking**")
        
        # Display in a clean format with key columns
        display_columns = []
        if 'make' in df_low.columns and 'model' in df_low.columns:
            df_low['Vehicle'] = df_low['make'] + ' ' + df_low['model']
            display_columns.append('Vehicle')
        
        # Add other useful columns
        for col in ['region', 'quantity_available', 'min_stock_level', 'reorder_point']:
            if col in df_low.columns:
                display_columns.append(col)
        
        if display_columns:
            st.dataframe(
                df_low[display_columns], 
                use_container_width=True,
                hide_index=True
            )
        else:
            st.dataframe(df_low, use_container_width=True, hide_index=True)
    else:
        st.success("✅ All inventory levels are healthy!")
else:
    st.error("❌ Unable to load inventory data. Please ensure the API is running.")

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

