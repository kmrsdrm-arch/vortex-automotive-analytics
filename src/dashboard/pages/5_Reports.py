"""Reports page."""

import sys
import os
# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import streamlit as st
from datetime import datetime, timedelta
from src.dashboard.styles.theme import DARK_THEME_CSS
from src.dashboard.utils.api_client import APIClient
from src.dashboard.components.page_header import get_page_header_html

st.set_page_config(page_title="Reports", page_icon="📄", layout="wide")
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

st.markdown(get_page_header_html("Report Generator", "Generate comprehensive reports powered by AI"), unsafe_allow_html=True)

# Report configuration with improved date controls
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

# Initialize session state for dates if not exists
if "report_start_date" not in st.session_state:
    st.session_state.report_start_date = datetime.now().date() - timedelta(days=30)
if "report_end_date" not in st.session_state:
    st.session_state.report_end_date = datetime.now().date()

with col1:
    report_type = st.selectbox(
        "📋 Report Type",
        ["executive", "detailed"],
        format_func=lambda x: x.capitalize(),
        key="report_type"
    )

with col2:
    days_back = st.selectbox("📅 Period (Days)", [7, 14, 30, 60, 90, 180, 365], index=2, key="report_period")
    # Update dates when period changes
    if days_back:
        st.session_state.report_end_date = datetime.now().date()
        st.session_state.report_start_date = st.session_state.report_end_date - timedelta(days=days_back)

with col3:
    start_date = st.date_input(
        "📅 Start Date",
        value=st.session_state.report_start_date,
        max_value=datetime.now().date(),
        key="report_start"
    )
    st.session_state.report_start_date = start_date

with col4:
    end_date = st.date_input(
        "📅 End Date",
        value=st.session_state.report_end_date,
        min_value=start_date,
        max_value=datetime.now().date(),
        key="report_end"
    )
    st.session_state.report_end_date = end_date

st.write(f"**Report Period:** {start_date} to {end_date} ({(end_date - start_date).days + 1} days)")

st.markdown("---")

# Generate button
if st.button("🔄 Generate Report", type="primary", use_container_width=False):
    with st.spinner(f"🤖 Generating {report_type} report... This may take a minute."):
        try:
            report = api_client.generate_report(report_type, start_date, end_date)
            
            if report and report.get("content"):
                # Store in session state
                st.session_state.last_report = report
                st.success("✅ Report generated successfully!")
            elif report and report.get("error"):
                st.error(f"❌ Failed to generate report: {report.get('error')}")
                st.info("💡 This might be due to:\n- Insufficient data for the selected period\n- OpenAI API issues\n- Backend configuration")
            else:
                st.error("❌ Failed to generate report")
                st.info("💡 Please check:\n- API is running on http://localhost:8000\n- OpenAI API key is configured\n- There is data available for the selected period")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("💡 Please ensure the backend is running and properly configured.")

# Display report
if "last_report" in st.session_state and st.session_state.last_report:
    report = st.session_state.last_report
    
    st.markdown("---")
    
    # Report metadata in a nice card
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📄 Report Type", report.get('report_type', 'N/A').capitalize())
    with col2:
        generated_at = report.get('generated_at', '')[:19].replace('T', ' ')
        st.metric("🕐 Generated", generated_at if generated_at else 'N/A')
    with col3:
        word_count = len(report.get('content', '').split())
        st.metric("📝 Word Count", f"{word_count:,}")
    
    st.markdown("---")
    
    # Report content in a styled container
    st.markdown(f"<h2 style='color: #64b5f6; border-bottom: 2px solid #2a3342; padding-bottom: 0.5rem;'>📊 {report.get('report_title', 'Report')}</h2>", unsafe_allow_html=True)
    
    # Display content with nice formatting
    content = report.get('content', '')
    if content:
        st.markdown(content)
    else:
        st.warning("⚠️ Report content is empty")
    
    # Download options
    st.markdown("---")
    st.markdown("<h3 style='color: #64b5f6; border-bottom: 2px solid #2a3342; padding-bottom: 0.5rem;'>💾 Download Report</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        # Markdown download
        md_content = f"# {report.get('report_title', 'Report')}\n\n{content}"
        st.download_button(
            label="📥 Markdown",
            data=md_content,
            file_name=f"report_{report.get('report_type', 'report')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True,
        )
    
    with col2:
        # Text download
        st.download_button(
            label="📥 Text",
            data=content,
            file_name=f"report_{report.get('report_type', 'report')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

else:
    st.info("👆 Click 'Generate Report' above to create a comprehensive AI-powered report")

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

