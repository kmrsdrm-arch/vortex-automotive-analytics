"""Natural Language Query page."""

import sys
import os
# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import streamlit as st
from src.dashboard.styles.theme import DARK_THEME_CSS
from src.dashboard.utils.api_client import APIClient
from src.dashboard.components.charts import create_bar_chart, create_pie_chart, create_line_chart
from src.dashboard.components.page_header import get_page_header_html
import pandas as pd

st.set_page_config(page_title="Natural Language Query", page_icon="💬", layout="wide")
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

st.markdown(get_page_header_html("Natural Language Query", "Ask questions about your data in plain English"), unsafe_allow_html=True)

# Example questions
st.markdown("<h3 style='color: #64b5f6; border-bottom: 2px solid #2a3342; padding-bottom: 0.5rem;'>💡 Example Questions</h3>", unsafe_allow_html=True)
examples = [
    "Show me the top 5 vehicles by total sales revenue",
    "What is the total revenue by region?",
    "List all vehicles in inventory with quantity less than 10",
    "What is the average discount_applied for fleet customer_segment?",
    "Show me total sales revenue for sedan category",
]

col1, col2 = st.columns(2)
for i, example in enumerate(examples):
    if i < 3:
        if col1.button(example, key=f"ex{i}"):
            st.session_state.question = example
    else:
        if col2.button(example, key=f"ex{i}"):
            st.session_state.question = example

st.markdown("---")

# Query input
question = st.text_area(
    "Your Question",
    value=st.session_state.get("question", ""),
    height=100,
    placeholder="Type your question here...",
)

col1, col2 = st.columns([1, 5])
with col1:
    query_button = st.button("🔍 Query", type="primary", use_container_width=True)

if query_button and question:
    with st.spinner("🔍 Analyzing your question..."):
        try:
            result = api_client.nl_query(question)
            
            if result and result.get("success"):
                st.success("✅ Query executed successfully!")
                
                # Show explanation as bullet points
                st.markdown("<h3 style='color: #64b5f6;'>💡 Key Insights</h3>", unsafe_allow_html=True)
                explanation = result.get("explanation", "")
                
                # Convert explanation to bullet points (max 20 words each)
                sentences = [s.strip() for s in explanation.replace('\n', '. ').split('.') if s.strip()]
                bullet_points = []
                for sentence in sentences[:5]:  # Limit to 5 key points
                    words = sentence.split()
                    if len(words) > 20:
                        sentence = ' '.join(words[:20]) + '...'
                    bullet_points.append(f"• {sentence}")
                
                for bullet in bullet_points:
                    st.markdown(f"**{bullet}**")
                
                # Show results with visualization
                if result.get("results"):
                    df = pd.DataFrame(result["results"])
                    
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.markdown(f"<h3 style='color: #64b5f6;'>📊 Data ({result.get('row_count', 0)} rows)</h3>", unsafe_allow_html=True)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    with col2:
                        st.markdown("<h3 style='color: #64b5f6;'>📈 Visualization</h3>", unsafe_allow_html=True)
                        # Auto-detect chart type based on columns
                        if len(df.columns) >= 2:
                            numeric_cols = df.select_dtypes(include=['number']).columns
                            non_numeric_cols = df.select_dtypes(exclude=['number']).columns
                            
                            if len(numeric_cols) > 0 and len(non_numeric_cols) > 0:
                                # Bar chart for categorical + numeric
                                x_col = non_numeric_cols[0]
                                y_col = numeric_cols[0]
                                if len(df) <= 10:
                                    fig = create_bar_chart(df.head(10), x_col, y_col, f"{y_col} by {x_col}")
                                else:
                                    fig = create_bar_chart(df.head(10), x_col, y_col, f"Top 10: {y_col} by {x_col}")
                                st.plotly_chart(fig, use_container_width=True)
                            elif len(numeric_cols) >= 2:
                                # Line chart for time series or numeric comparison
                                fig = create_line_chart(df.head(50), df.columns[0], df.columns[1], "Trend Analysis")
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.info("📊 Data displayed in table format")
                        else:
                            st.info("📊 Data displayed in table format")
                    
                    # Show SQL (expandable)
                    with st.expander("🔍 View Generated SQL", expanded=False):
                        st.code(result.get("sql", ""), language="sql")
                    
                    # Store in history
                    if "query_history" not in st.session_state:
                        st.session_state.query_history = []
                    st.session_state.query_history.append(question)
                else:
                    st.info("ℹ️ Query executed but no results were returned")
            elif result:
                error_msg = result.get('error', 'Unknown error occurred')
                st.error(f"❌ Query failed: {error_msg}")
                st.info("💡 Try rephrasing your question or use one of the example questions above")
            else:
                st.error("❌ Unable to connect to the API. Please ensure the backend is running.")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("💡 Please check that the API is running on http://localhost:8000")

# Query history
if st.checkbox("📜 Show Query History"):
    st.markdown("<h3 style='color: #64b5f6; border-bottom: 2px solid #2a3342; padding-bottom: 0.5rem;'>📜 Recent Queries</h3>", unsafe_allow_html=True)
    if "query_history" not in st.session_state:
        st.session_state.query_history = []
    
    if st.session_state.query_history:
        for i, q in enumerate(reversed(st.session_state.query_history[-10:])):
            st.text(f"{i+1}. {q}")
    else:
        st.info("No query history yet")

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

