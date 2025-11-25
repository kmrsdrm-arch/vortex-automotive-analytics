"""AI Insights page."""

import sys
import os
# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import streamlit as st
from datetime import datetime, timedelta
from src.dashboard.styles.theme import DARK_THEME_CSS
from src.dashboard.utils.api_client import APIClient
from src.dashboard.components.charts import create_bar_chart, create_pie_chart, create_line_chart
from src.dashboard.components.page_header import get_page_header_html
import pandas as pd

st.set_page_config(page_title="AI Insights", page_icon="🤖", layout="wide")
st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)

# Hide the main app page from navigation and add custom animations
st.markdown("""
<style>
    [data-testid="stSidebarNav"] ul li:first-child {
        display: none;
    }
    
    /* Smooth animations for all elements */
    * {
        transition: all 0.3s ease;
    }
    
    /* Full viewport usage */
    .main .block-container {
        max-width: 100%;
        padding-left: 2rem;
        padding-right: 2rem;
        padding-top: 2rem;
    }
    
    /* Metric cards hover effect */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(42, 51, 66, 0.5);
        border-radius: 8px;
        font-weight: 600;
        padding: 1rem;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(42, 51, 66, 0.8);
    }
    
    /* Spinner customization */
    .stSpinner > div {
        border-top-color: #64b5f6 !important;
    }
    
    /* Make columns responsive */
    [data-testid="column"] {
        padding: 0.5rem;
    }
    
    /* Smooth fade-in animation */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .element-container {
        animation: fadeIn 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Initialize API client
if "api_client" not in st.session_state:
    st.session_state.api_client = APIClient()
api_client = st.session_state.api_client

st.markdown(get_page_header_html("AI-Powered Insights", "Automated analysis and recommendations from your data"), unsafe_allow_html=True)

# Generation controls with improved date controls
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

# Initialize session state for dates if not exists
if "insights_start_date" not in st.session_state:
    st.session_state.insights_start_date = datetime.now().date() - timedelta(days=30)
if "insights_end_date" not in st.session_state:
    st.session_state.insights_end_date = datetime.now().date()

with col1:
    focus_area = st.selectbox("🎯 Focus Area", ["sales", "inventory", "general"], key="insights_focus")

with col2:
    days_back = st.selectbox("📅 Period (Days)", [7, 14, 30, 60, 90, 180], index=2, key="insights_period")
    # Update dates when period changes
    if days_back:
        st.session_state.insights_end_date = datetime.now().date()
        st.session_state.insights_start_date = st.session_state.insights_end_date - timedelta(days=days_back)

with col3:
    start_date = st.date_input(
        "📅 Start Date",
        value=st.session_state.insights_start_date,
        max_value=datetime.now().date(),
        key="insights_start"
    )
    st.session_state.insights_start_date = start_date

with col4:
    end_date = st.date_input(
        "📅 End Date",
        value=st.session_state.insights_end_date,
        min_value=start_date,
        max_value=datetime.now().date(),
        key="insights_end"
    )
    st.session_state.insights_end_date = end_date

with col5:
    st.write("")  # Spacing
    st.metric("📊 Days", (end_date - start_date).days + 1)

st.write("")  # Spacing
generate_button = st.button("✨ Generate Insights", type="primary", use_container_width=False)

st.markdown("---")

if generate_button:
    with st.spinner("🤖 Generating AI insights... This may take a minute."):
        try:
            result = api_client.generate_insights(focus_area, start_date, end_date)
            
            if result and result.get("insights"):
                insights = result["insights"]
                st.success(f"✅ Successfully generated {len(insights)} insights")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Display insights in styled cards with full text
                st.markdown("""
                    <div style='background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%); 
                                padding: 1rem; border-radius: 10px; margin-bottom: 1.5rem;'>
                        <h2 style='color: #64b5f6; margin: 0; display: flex; align-items: center;'>
                            <span style='font-size: 2rem; margin-right: 0.5rem;'>💡</span>
                            Key Insights
                        </h2>
                    </div>
                """, unsafe_allow_html=True)
                
                for i, insight in enumerate(insights, 1):
                    insight_text = insight.get("text", "")
                    insight_type = insight.get("type", "general")
                    
                    # Truncate long insights to keep them concise and readable
                    if len(insight_text) > 280:
                        # Find the last sentence that fits within 280 chars
                        sentences = insight_text.split('. ')
                        truncated = ""
                        for sentence in sentences:
                            if len(truncated + sentence + '. ') <= 280:
                                truncated += sentence + '. '
                            else:
                                break
                        insight_text = truncated.strip() if truncated else insight_text[:280] + "..."
                    
                    # Color-coded cards based on type
                    if "trend" in insight_type.lower() or "sales" in insight_type.lower():
                        icon = "📈"
                        color = "#64b5f6"
                        bg_color = "rgba(100, 181, 246, 0.15)"
                        border_color = "#64b5f6"
                    elif "alert" in insight_type.lower() or "low" in insight_type.lower():
                        icon = "⚠️"
                        color = "#ffb74d"
                        bg_color = "rgba(255, 183, 77, 0.15)"
                        border_color = "#ffb74d"
                    elif "positive" in insight_type.lower() or "growth" in insight_type.lower():
                        icon = "✅"
                        color = "#81c784"
                        bg_color = "rgba(129, 199, 132, 0.15)"
                        border_color = "#81c784"
                    elif "inventory" in insight_type.lower():
                        icon = "📦"
                        color = "#ba68c8"
                        bg_color = "rgba(186, 104, 200, 0.15)"
                        border_color = "#ba68c8"
                    else:
                        icon = "💡"
                        color = "#4fc3f7"
                        bg_color = "rgba(79, 195, 247, 0.15)"
                        border_color = "#4fc3f7"
                    
                    st.markdown(f"""
                        <div style='background: {bg_color}; 
                                    border-left: 4px solid {border_color}; 
                                    padding: 1.2rem; 
                                    margin: 1rem 0; 
                                    border-radius: 8px;
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                                    transition: transform 0.2s;'>
                            <div style='display: flex; align-items: flex-start;'>
                                <span style='font-size: 1.8rem; margin-right: 1rem; min-width: 2rem;'>{icon}</span>
                                <div style='flex: 1;'>
                                    <div style='color: {color}; font-size: 0.85rem; font-weight: 600; 
                                                text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;'>
                                        {insight_type.replace('_', ' ')}
                                    </div>
                                    <div style='color: #e0e0e0; font-size: 1.1rem; line-height: 1.6;'>
                                        {insight_text}
                                    </div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br><br>", unsafe_allow_html=True)
                
                # Performance Metrics Section with enhanced visualization
                st.markdown("""
                    <div style='background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%); 
                                padding: 1rem; border-radius: 10px; margin-bottom: 1.5rem;'>
                        <h2 style='color: #81c784; margin: 0; display: flex; align-items: center;'>
                            <span style='font-size: 2rem; margin-right: 0.5rem;'>📊</span>
                            Performance Metrics
                        </h2>
                    </div>
                """, unsafe_allow_html=True)
                
                # Fetch and display comprehensive charts based on focus area
                try:
                    if focus_area == "sales":
                        # Row 1: Summary metrics
                        summary = api_client.get_sales_summary(start_date, end_date)
                        if summary:
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.markdown(f"""
                                    <div style='background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
                                                padding: 1.5rem; border-radius: 10px; text-align: center;
                                                box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
                                        <div style='font-size: 0.9rem; color: #90caf9; margin-bottom: 0.5rem;'>TOTAL REVENUE</div>
                                        <div style='font-size: 2rem; font-weight: bold; color: #fff;'>
                                            ${summary.get('total_revenue', 0):,.0f}
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                            with col2:
                                st.markdown(f"""
                                    <div style='background: linear-gradient(135deg, #43a047 0%, #2e7d32 100%);
                                                padding: 1.5rem; border-radius: 10px; text-align: center;
                                                box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
                                        <div style='font-size: 0.9rem; color: #a5d6a7; margin-bottom: 0.5rem;'>UNITS SOLD</div>
                                        <div style='font-size: 2rem; font-weight: bold; color: #fff;'>
                                            {summary.get('total_units', 0):,}
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                            with col3:
                                st.markdown(f"""
                                    <div style='background: linear-gradient(135deg, #fb8c00 0%, #ef6c00 100%);
                                                padding: 1.5rem; border-radius: 10px; text-align: center;
                                                box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
                                        <div style='font-size: 0.9rem; color: #ffcc80; margin-bottom: 0.5rem;'>AVG TRANSACTION</div>
                                        <div style='font-size: 2rem; font-weight: bold; color: #fff;'>
                                            ${summary.get('avg_transaction_value', 0):,.0f}
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                            with col4:
                                st.markdown(f"""
                                    <div style='background: linear-gradient(135deg, #8e24aa 0%, #6a1b9a 100%);
                                                padding: 1.5rem; border-radius: 10px; text-align: center;
                                                box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
                                        <div style='font-size: 0.9rem; color: #ce93d8; margin-bottom: 0.5rem;'>TRANSACTIONS</div>
                                        <div style='font-size: 2rem; font-weight: bold; color: #fff;'>
                                            {summary.get('total_transactions', 0):,}
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Row 2: Sales trend and regional performance
                        col1, col2 = st.columns(2)
                        with col1:
                            trends = api_client.get_sales_trends(start_date, end_date, period="D")
                            if trends:
                                df_trends = pd.DataFrame(trends)
                                df_trends["sale_date"] = pd.to_datetime(df_trends["sale_date"])
                                fig = create_line_chart(df_trends.tail(60), "sale_date", "total_amount", "Sales Trend Over Time")
                                st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            regional = api_client.get_regional_performance(start_date, end_date)
                            if regional:
                                df_regional = pd.DataFrame(regional)
                                fig = create_pie_chart(df_regional, "total_amount", "region", "Revenue by Region")
                                st.plotly_chart(fig, use_container_width=True)
                        
                        # Row 3: Top vehicles and category breakdown
                        col1, col2 = st.columns(2)
                        with col1:
                            top_vehicles = api_client.get_top_vehicles(10, start_date, end_date)
                            if top_vehicles:
                                df_vehicles = pd.DataFrame(top_vehicles)
                                df_vehicles["vehicle_name"] = df_vehicles["make"] + " " + df_vehicles["model"]
                                fig = create_bar_chart(df_vehicles, "vehicle_name", "quantity", "Top 10 Selling Vehicles")
                                st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            categories = api_client.get_category_breakdown(start_date, end_date)
                            if categories:
                                df_categories = pd.DataFrame(categories)
                                fig = create_pie_chart(df_categories, "total_amount", "category", "Sales by Vehicle Category")
                                st.plotly_chart(fig, use_container_width=True)
                    
                    elif focus_area == "inventory":
                        # Row 1: Inventory summary metrics
                        inv_summary = api_client.get_inventory_summary()
                        if inv_summary:
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.markdown(f"""
                                    <div style='background: linear-gradient(135deg, #00acc1 0%, #00838f 100%);
                                                padding: 1.5rem; border-radius: 10px; text-align: center;
                                                box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
                                        <div style='font-size: 0.9rem; color: #80deea; margin-bottom: 0.5rem;'>TOTAL UNITS</div>
                                        <div style='font-size: 2rem; font-weight: bold; color: #fff;'>
                                            {inv_summary.get('total_units', 0):,}
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                            with col2:
                                st.markdown(f"""
                                    <div style='background: linear-gradient(135deg, #7cb342 0%, #558b2f 100%);
                                                padding: 1.5rem; border-radius: 10px; text-align: center;
                                                box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
                                        <div style='font-size: 0.9rem; color: #c5e1a5; margin-bottom: 0.5rem;'>TOTAL VALUE</div>
                                        <div style='font-size: 2rem; font-weight: bold; color: #fff;'>
                                            ${inv_summary.get('total_value', 0):,.0f}
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                            with col3:
                                st.markdown(f"""
                                    <div style='background: linear-gradient(135deg, #f4511e 0%, #d84315 100%);
                                                padding: 1.5rem; border-radius: 10px; text-align: center;
                                                box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
                                        <div style='font-size: 0.9rem; color: #ffab91; margin-bottom: 0.5rem;'>LOW STOCK</div>
                                        <div style='font-size: 2rem; font-weight: bold; color: #fff;'>
                                            {inv_summary.get('low_stock_count', 0):,}
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                            with col4:
                                st.markdown(f"""
                                    <div style='background: linear-gradient(135deg, #e53935 0%, #c62828 100%);
                                                padding: 1.5rem; border-radius: 10px; text-align: center;
                                                box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
                                        <div style='font-size: 0.9rem; color: #ef9a9a; margin-bottom: 0.5rem;'>OUT OF STOCK</div>
                                        <div style='font-size: 2rem; font-weight: bold; color: #fff;'>
                                            {inv_summary.get('out_of_stock_count', 0):,}
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Row 2: Low stock and inventory status
                        col1, col2 = st.columns(2)
                        with col1:
                            low_stock = api_client.get_low_stock()
                            if low_stock and len(low_stock) > 0:
                                df_low = pd.DataFrame(low_stock)
                                df_low["vehicle_name"] = df_low["make"] + " " + df_low["model"]
                                fig = create_bar_chart(df_low.head(10), "vehicle_name", "quantity_available", "Low Stock Alert - Items Need Restocking")
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.info("✅ No low stock items - All inventory levels are healthy!")
                        
                        with col2:
                            status = api_client.get_inventory_by_status()
                            if status:
                                df_status = pd.DataFrame(status)
                                if "status" in df_status.columns and "total_quantity" in df_status.columns:
                                    fig = create_pie_chart(df_status, "total_quantity", "status", "Inventory Distribution by Status")
                                    st.plotly_chart(fig, use_container_width=True)
                    
                    else:  # general focus area - show comprehensive view
                        # Row 1: Combined key metrics
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("<div style='background: rgba(30, 136, 229, 0.15); padding: 1rem; border-radius: 10px; border-left: 4px solid #1e88e5;'>", unsafe_allow_html=True)
                            st.markdown("<h4 style='color: #64b5f6; margin-top: 0;'>💰 Sales Overview</h4>", unsafe_allow_html=True)
                            summary = api_client.get_sales_summary(start_date, end_date)
                            if summary:
                                subcol1, subcol2 = st.columns(2)
                                with subcol1:
                                    st.metric("Total Revenue", f"${summary.get('total_revenue', 0):,.0f}")
                                    st.metric("Units Sold", f"{summary.get('total_units', 0):,}")
                                with subcol2:
                                    st.metric("Transactions", f"{summary.get('total_transactions', 0):,}")
                                    st.metric("Avg Transaction", f"${summary.get('avg_transaction_value', 0):,.0f}")
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown("<div style='background: rgba(67, 160, 71, 0.15); padding: 1rem; border-radius: 10px; border-left: 4px solid #43a047;'>", unsafe_allow_html=True)
                            st.markdown("<h4 style='color: #81c784; margin-top: 0;'>📦 Inventory Overview</h4>", unsafe_allow_html=True)
                            inv_summary = api_client.get_inventory_summary()
                            if inv_summary:
                                subcol1, subcol2 = st.columns(2)
                                with subcol1:
                                    st.metric("Total Units", f"{inv_summary.get('total_units', 0):,}")
                                    st.metric("Total Value", f"${inv_summary.get('total_value', 0):,.0f}")
                                with subcol2:
                                    st.metric("Low Stock", f"{inv_summary.get('low_stock_count', 0):,}", 
                                             delta=None if inv_summary.get('low_stock_count', 0) == 0 else "Attention needed",
                                             delta_color="inverse")
                                    st.metric("Unique Vehicles", f"{inv_summary.get('unique_vehicles', 0):,}")
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Row 2: Sales trend and top vehicles
                        col1, col2 = st.columns(2)
                        with col1:
                            trends = api_client.get_sales_trends(start_date, end_date, period="D")
                            if trends:
                                df_trends = pd.DataFrame(trends)
                                df_trends["sale_date"] = pd.to_datetime(df_trends["sale_date"])
                                fig = create_line_chart(df_trends.tail(60), "sale_date", "total_amount", "Sales Trend Over Time")
                                st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            top_vehicles = api_client.get_top_vehicles(10, start_date, end_date)
                            if top_vehicles:
                                df_vehicles = pd.DataFrame(top_vehicles)
                                df_vehicles["vehicle_name"] = df_vehicles["make"] + " " + df_vehicles["model"]
                                fig = create_bar_chart(df_vehicles, "vehicle_name", "quantity", "Top 10 Selling Vehicles")
                                st.plotly_chart(fig, use_container_width=True)
                        
                        # Row 3: Regional performance and category breakdown
                        col1, col2 = st.columns(2)
                        with col1:
                            regional = api_client.get_regional_performance(start_date, end_date)
                            if regional:
                                df_regional = pd.DataFrame(regional)
                                fig = create_pie_chart(df_regional, "total_amount", "region", "Revenue Distribution by Region")
                                st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            categories = api_client.get_category_breakdown(start_date, end_date)
                            if categories:
                                df_categories = pd.DataFrame(categories)
                                fig = create_pie_chart(df_categories, "total_amount", "category", "Sales by Vehicle Category")
                                st.plotly_chart(fig, use_container_width=True)
                
                except Exception as e:
                    st.error(f"⚠️ Error loading performance metrics: {str(e)}")
                    st.info("💡 Some visualization data may not be available for the selected period.")
                
                st.markdown("---")
            elif result and result.get("error"):
                st.error(f"❌ Failed to generate insights: {result.get('error')}")
                st.info("💡 This might be due to insufficient data or API connectivity issues.")
            else:
                st.error("❌ Failed to generate insights")
                st.info("💡 Please check:\n- API is running on http://localhost:8000\n- OpenAI API key is configured\n- There is data available for the selected period")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("💡 Please ensure the backend is running and properly configured.")

# Historical insights section
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='background: linear-gradient(135deg, #4a148c 0%, #6a1b9a 100%); 
                padding: 1rem; border-radius: 10px; margin-bottom: 1.5rem;'>
        <h2 style='color: #ce93d8; margin: 0; display: flex; align-items: center;'>
            <span style='font-size: 2rem; margin-right: 0.5rem;'>📜</span>
            Historical Insights
        </h2>
    </div>
""", unsafe_allow_html=True)

st.markdown("<p style='color: #b0b0b0; font-size: 1rem; margin-bottom: 1rem;'>View previously generated insights and track your analytics history</p>", unsafe_allow_html=True)

if st.button("🔄 Load History", type="secondary", use_container_width=False):
    with st.spinner("📂 Loading historical insights..."):
        try:
            history = api_client.get_insight_history(20)
            
            if history and len(history) > 0:
                st.success(f"✅ Loaded {len(history)} historical insights")
                st.markdown("<br>", unsafe_allow_html=True)
                
                for item in history:
                    insight_type = item.get('type', 'general')
                    generated_at = item.get('generated_at', '')[:10]
                    insight_text = item.get("text", "")
                    
                    # Icon and color based on type
                    if "trend" in insight_type.lower() or "sales" in insight_type.lower():
                        icon = "📈"
                        color = "#64b5f6"
                        bg_color = "rgba(100, 181, 246, 0.1)"
                    elif "alert" in insight_type.lower():
                        icon = "⚠️"
                        color = "#ffb74d"
                        bg_color = "rgba(255, 183, 77, 0.1)"
                    elif "positive" in insight_type.lower():
                        icon = "✅"
                        color = "#81c784"
                        bg_color = "rgba(129, 199, 132, 0.1)"
                    elif "inventory" in insight_type.lower():
                        icon = "📦"
                        color = "#ba68c8"
                        bg_color = "rgba(186, 104, 200, 0.1)"
                    else:
                        icon = "📊"
                        color = "#4fc3f7"
                        bg_color = "rgba(79, 195, 247, 0.1)"
                    
                    with st.expander(f"{icon} **{insight_type.replace('_', ' ').title()}** - {generated_at}", expanded=False):
                        st.markdown(f"""
                            <div style='background: {bg_color}; 
                                        padding: 1rem; 
                                        border-radius: 8px; 
                                        border-left: 3px solid {color};'>
                                <div style='color: #e0e0e0; font-size: 1rem; line-height: 1.6;'>
                                    {insight_text}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("ℹ️ No historical insights found. Generate some insights to build your history!")
        except Exception as e:
            st.error(f"❌ Failed to load history: {str(e)}")
            st.info("💡 Please ensure the API is running and accessible.")

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

