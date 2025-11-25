"""About page - Project information and architecture."""

import sys
import os
# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import streamlit as st
from src.dashboard.styles.theme import DARK_THEME_CSS
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

st.set_page_config(page_title="Vortex | About", page_icon="⚡", layout="wide")
st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)

# Hide the main app page from navigation since we have Dashboard Summary page now
st.markdown("""
<style>
    [data-testid="stSidebarNav"] ul li:first-child {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Page header - Executive style
st.markdown("""
<div style='text-align: center; margin-bottom: 3rem;'>
    <svg viewBox="0 0 60 60" style="width: 60px; height: 60px; margin: 0 auto; display: block;">
        <defs>
            <linearGradient id="aboutLogoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#00d4ff;stop-opacity:1" />
                <stop offset="50%" style="stop-color:#7b2ff7;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#f026ff;stop-opacity:1" />
            </linearGradient>
        </defs>
        <circle cx="30" cy="30" r="28" fill="none" stroke="url(#aboutLogoGradient)" stroke-width="2" opacity="0.3"/>
        <circle cx="30" cy="30" r="22" fill="none" stroke="url(#aboutLogoGradient)" stroke-width="2" opacity="0.5"/>
        <circle cx="30" cy="30" r="16" fill="none" stroke="url(#aboutLogoGradient)" stroke-width="2" opacity="0.7"/>
        <path d="M 30 14 L 38 30 L 30 46 L 22 30 Z" fill="url(#aboutLogoGradient)" opacity="0.8"/>
        <circle cx="30" cy="30" r="4" fill="#00d4ff"/>
    </svg>
    <h1 style='font-family: "Orbitron", sans-serif; font-size: 3rem; font-weight: 900; 
                color: #00d4ff;
                display: inline-block;
                margin: 1rem 0 0.5rem 0; letter-spacing: 4px;'>
        VORTEX
    </h1>
    <h2 style='font-family: "Orbitron", sans-serif; font-size: 1.8rem; color: #00d4ff; font-weight: 700; 
                margin: 0.5rem 0 1rem 0; letter-spacing: 2px;'>
        About
    </h2>
    <p style='font-size: 1.2rem; font-family: "Inter", sans-serif; color: #00d4ff; font-weight: 300; letter-spacing: 0.05em;'>
        Automotive Intelligence Platform
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# ========== SECTION 1: Project Overview ==========
st.markdown("<h2 style='color: #00d4ff; font-family: \"Orbitron\", sans-serif; letter-spacing: 1px;'>⚡ Platform Overview</h2>", unsafe_allow_html=True)
st.markdown("""
<div style='background: linear-gradient(135deg, rgba(0, 212, 255, 0.05) 0%, rgba(123, 47, 247, 0.05) 100%); 
            padding: 2rem; border-radius: 16px; border: 1px solid rgba(123, 47, 247, 0.3); margin-bottom: 1.5rem;'>
<p style='font-size: 1.15rem; line-height: 1.9; color: rgba(255, 255, 255, 0.9); margin: 0; font-family: "Inter", sans-serif;'>
<strong style='background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 50%, #f026ff 100%);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                background-clip: text; font-size: 1.3rem; font-family: "Orbitron", sans-serif; letter-spacing: 2px;'>VORTEX</strong> is an enterprise-grade 
<strong style='color: #7b2ff7;'>automotive analytics platform</strong> that transforms sales and inventory data into actionable insights. 
Built for executives and analysts who demand excellence, we combine <strong style='color: #00d4ff;'>AI-powered intelligence</strong> with elegant, 
intuitive design to deliver <strong style='color: #f026ff;'>real-time business intelligence</strong> for the automotive industry.
</p>
</div>
""", unsafe_allow_html=True)

# ========== SECTION 2: Dataset Information ==========
st.markdown("<h2 style='color: #4fc3f7;'>📊 Dataset Information</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid #2a3342;'>
    <h4 style='color: #81c784; margin-top: 0;'>📝 Data Composition</h4>
    <ul style='color: #e0e0e0; line-height: 2; font-size: 1rem;'>
        <li><strong>Type:</strong> Artificially generated data</li>
        <li><strong>Domain:</strong> Automotive sales & inventory</li>
        <li><strong>Purpose:</strong> Demonstration & testing</li>
        <li><strong>Realism:</strong> Mimics real-world patterns</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid #2a3342;'>
    <h4 style='color: #81c784; margin-top: 0;'>🔢 Key Metrics</h4>
    <ul style='color: #e0e0e0; line-height: 2; font-size: 1rem;'>
        <li>Sales transactions across multiple regions</li>
        <li>Inventory levels for various vehicle types</li>
        <li>Customer segments and demographics</li>
        <li>Time-series data for trend analysis</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ========== SECTION 3: Dashboard Capabilities ==========
st.markdown("<h2 style='color: #4fc3f7;'>🚀 Dashboard Capabilities</h2>", unsafe_allow_html=True)

# Create 3 columns for capabilities
cap_col1, cap_col2, cap_col3 = st.columns(3, gap="medium")

with cap_col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid #2a3342; height: 100%;'>
    <h4 style='color: #4fc3f7; margin-top: 0; text-align: center;'>📈 Analytics</h4>
    <ul style='color: #e0e0e0; line-height: 1.8; font-size: 0.95rem;'>
        <li>Real-time KPI monitoring</li>
        <li>Sales trend analysis</li>
        <li>Inventory tracking</li>
        <li>Regional performance</li>
        <li>Category breakdowns</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with cap_col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid #2a3342; height: 100%;'>
    <h4 style='color: #4fc3f7; margin-top: 0; text-align: center;'>🤖 AI Features</h4>
    <ul style='color: #e0e0e0; line-height: 1.8; font-size: 0.95rem;'>
        <li>Natural language queries</li>
        <li>Automated insights</li>
        <li>Smart recommendations</li>
        <li>Report generation</li>
        <li>Pattern recognition</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with cap_col3:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid #2a3342; height: 100%;'>
    <h4 style='color: #4fc3f7; margin-top: 0; text-align: center;'>🎨 User Experience</h4>
    <ul style='color: #e0e0e0; line-height: 1.8; font-size: 0.95rem;'>
        <li>Interactive visualizations</li>
        <li>Customizable date ranges</li>
        <li>Responsive design</li>
        <li>Dark theme interface</li>
        <li>Export capabilities</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# ========== SECTION 4: Architecture ==========
st.markdown("<h2 style='color: #4fc3f7;'>🏗️ System Architecture</h2>", unsafe_allow_html=True)

st.markdown("""
<div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 2rem; border-radius: 16px; border: 1px solid #2a3342; margin-bottom: 1.5rem;'>
<p style='font-size: 1.05rem; line-height: 1.8; color: #e0e0e0; margin-bottom: 0;'>
The system follows a modern <strong style='color: #4fc3f7;'>three-tier architecture</strong> that separates concerns and enables scalability.
Below are <strong style='color: #81c784;'>interactive visualizations</strong> - hover over elements to see details!
</p>
</div>
""", unsafe_allow_html=True)

# Three-Layer Architecture Visual
col_arch1, col_arch2, col_arch3 = st.columns(3, gap="medium")

with col_arch1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 2rem; border-radius: 16px; border: 2px solid #42A5F5; text-align: center; height: 280px; display: flex; flex-direction: column; justify-content: space-between;'>
        <div>
            <h3 style='color: #42A5F5; margin-top: 0; margin-bottom: 1rem;'>🌐 PRESENTATION</h3>
            <div style='background: rgba(66, 165, 245, 0.15); padding: 1rem; border-radius: 12px;'>
                <p style='color: #64B5F6; font-weight: 600; margin: 0;'>📊 Streamlit</p>
                <p style='color: #e0e0e0; font-size: 0.85rem; margin: 0.5rem 0 0 0;'>Port 8501</p>
            </div>
        </div>
        <p style='color: #e0e0e0; font-size: 0.9rem; line-height: 1.5; margin: 0; padding-top: 1rem;'>
            Interactive UI<br>Charts & Forms<br>Real-time Updates
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_arch2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 2rem; border-radius: 16px; border: 2px solid #00BCD4; text-align: center; height: 280px; display: flex; flex-direction: column; justify-content: space-between;'>
        <div>
            <h3 style='color: #00BCD4; margin-top: 0; margin-bottom: 1rem;'>⚙️ APPLICATION</h3>
            <div style='background: rgba(0, 188, 212, 0.15); padding: 1rem; border-radius: 12px;'>
                <p style='color: #26C6DA; font-weight: 600; margin: 0;'>🚀 FastAPI</p>
                <p style='color: #e0e0e0; font-size: 0.85rem; margin: 0.5rem 0 0 0;'>Port 8000</p>
            </div>
        </div>
        <p style='color: #e0e0e0; font-size: 0.9rem; line-height: 1.5; margin: 0; padding-top: 1rem;'>
            Business Logic<br>Analytics • Pipeline<br>LLM Services
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_arch3:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 2rem; border-radius: 16px; border: 2px solid #66BB6A; text-align: center; height: 280px; display: flex; flex-direction: column; justify-content: space-between;'>
        <div>
            <h3 style='color: #66BB6A; margin-top: 0; margin-bottom: 1rem;'>💾 DATA</h3>
            <div style='background: rgba(102, 187, 106, 0.15); padding: 1rem; border-radius: 12px;'>
                <p style='color: #81C784; font-weight: 600; margin: 0;'>🗄️ PostgreSQL</p>
                <p style='color: #e0e0e0; font-size: 0.85rem; margin: 0.5rem 0 0 0;'>Port 5432</p>
            </div>
        </div>
        <p style='color: #e0e0e0; font-size: 0.9rem; line-height: 1.5; margin: 0; padding-top: 1rem;'>
            Database Storage<br>OpenAI GPT-4<br>ChromaDB Vectors
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Create Sankey Diagram for Data Flow
fig_sankey = go.Figure(data=[go.Sankey(
    arrangement='snap',
    node = dict(
        pad = 30,
        thickness = 30,
        line = dict(color = "#42A5F5", width = 2),
        label = [
            "👤 User",
            "📊 Streamlit<br>Dashboard<br>(Port 8501)",
            "🚀 FastAPI<br>Server<br>(Port 8000)",
            "📊 Analytics<br>Engine",
            "🔄 Pipeline<br>Manager",
            "🤖 LLM<br>Services",
            "🗄️ PostgreSQL<br>(Port 5432)",
            "🧠 OpenAI<br>GPT-4",
            "📚 ChromaDB<br>Vector Store",
            "📈 Visualization"
        ],
        color = ["#2196F3", "#42A5F5", "#00BCD4", "#FF9800", "#FF5722", "#AB47BC", 
                 "#66BB6A", "#9C27B0", "#9CCC65", "#64B5F6"],
        customdata = [
            "User Interface - End User",
            "Presentation Layer - Port 8501",
            "API Layer - Port 8000",
            "Processing - Analytics Service",
            "Processing - Data Pipeline",
            "Processing - AI Service",
            "Storage - Relational Database",
            "External - AI Language Model",
            "Storage - Vector Database",
            "Presentation - Charts & Graphs"
        ],
        hovertemplate='<b>%{label}</b><br>%{customdata}<extra></extra>'
    ),
    link = dict(
        source = [0, 1, 2, 2, 2, 3, 4, 5, 6, 7, 8, 3, 4, 5],
        target = [1, 2, 3, 4, 5, 6, 6, 7, 9, 9, 9, 2, 2, 2],
        value =  [10, 10, 3, 3, 4, 3, 3, 4, 3, 4, 3, 3, 3, 4],
        color = ["rgba(33, 150, 243, 0.3)", "rgba(66, 165, 245, 0.3)", 
                 "rgba(255, 152, 0, 0.3)", "rgba(255, 87, 34, 0.3)", "rgba(171, 71, 188, 0.3)",
                 "rgba(255, 152, 0, 0.3)", "rgba(255, 87, 34, 0.3)", "rgba(171, 71, 188, 0.3)",
                 "rgba(102, 187, 106, 0.3)", "rgba(156, 39, 176, 0.3)", "rgba(156, 204, 101, 0.3)",
                 "rgba(255, 152, 0, 0.3)", "rgba(255, 87, 34, 0.3)", "rgba(171, 71, 188, 0.3)"],
        hovertemplate='%{source.label} → %{target.label}<br>Data Flow<extra></extra>'
    )
)])

fig_sankey.update_layout(
    title={
        'text': "📊 End-to-End Data Flow Architecture",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 20, 'color': '#42A5F5', 'family': 'Inter'}
    },
    font=dict(size=12, color='#e0e0e0', family='Inter'),
    plot_bgcolor='#1c2331',
    paper_bgcolor='#1c2331',
    height=600,
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(fig_sankey, use_container_width=True, key="architecture_sankey")

st.markdown("<br>", unsafe_allow_html=True)

# Request-Response Flow Timeline
st.markdown("<h3 style='color: #00BCD4; text-align: center; font-size: 1.8rem; margin-bottom: 1rem;'>🔄 Request-Response Flow Timeline</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #e0e0e0; font-size: 1.05rem; margin-bottom: 2rem;'>Follow the journey from user action to visualization in 5 clear steps</p>", unsafe_allow_html=True)

# Create animated timeline diagram
fig_timeline = go.Figure()

# Define steps - User Interaction should be step 1, so it goes at the top
steps = [
    {"name": "👤 User Interaction", "desc": "Selects filters & queries", "y": 5, "color": "#2196F3", "step": 1},
    {"name": "🌐 HTTP Request", "desc": "API call to backend", "y": 4, "color": "#42A5F5", "step": 2},
    {"name": "⚙️ Backend Processing", "desc": "Validation & routing", "y": 3, "color": "#FFA726", "step": 3},
    {"name": "💾 Data Retrieval", "desc": "DB query or AI call", "y": 2, "color": "#81C784", "step": 4},
    {"name": "📊 Visualization", "desc": "Render charts", "y": 1, "color": "#64B5F6", "step": 5}
]

# Add horizontal bars for each step with improved sizing
for i, step in enumerate(steps):
    fig_timeline.add_trace(go.Bar(
        x=[3],
        y=[step["y"]],
        orientation='h',
        name=step["name"],
        text=f"<b style='font-size: 16px;'>{step['name']}</b><br><span style='font-size: 14px;'>{step['desc']}</span>",
        textposition='inside',
        textfont=dict(size=16, color='white', family='Inter'),
        marker=dict(
            color=step["color"],
            line=dict(color='#2a3342', width=2),
        ),
        hovertemplate=f"<b>Step {step['step']}: {step['name']}</b><br>{step['desc']}<extra></extra>",
        showlegend=False
    ))

# Add arrows between steps
for i in range(len(steps)-1):
    fig_timeline.add_annotation(
        x=3.15,
        y=steps[i]["y"] - 0.5,
        ax=3.15,
        ay=steps[i+1]["y"] + 0.5,
        xref="x",
        yref="y",
        axref="x",
        ayref="y",
        text="",
        showarrow=True,
        arrowhead=2,
        arrowsize=1.8,
        arrowwidth=4,
        arrowcolor="#00BCD4"
    )

# Add step numbers - CORRECTED: Step 1 is User Interaction (top), Step 5 is Visualization (bottom)
for i, step in enumerate(steps):
    fig_timeline.add_annotation(
        x=-0.4,
        y=step["y"],
        text=f"<b>{step['step']}</b>",
        showarrow=False,
        font=dict(size=32, color=step["color"], family='Inter'),
        bgcolor='#1c2331',
        bordercolor=step["color"],
        borderwidth=4,
        borderpad=12
    )

fig_timeline.update_layout(
    title={
        'text': "📊 Request → 🔄 Process → 💾 Store → 🤖 Analyze → 📈 Display",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 20, 'color': '#00BCD4', 'family': 'Inter'}
    },
    xaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[-0.6, 3.5]
    ),
    yaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[0, 6]
    ),
    plot_bgcolor='#1c2331',
    paper_bgcolor='#1c2331',
    height=600,
    margin=dict(l=100, r=100, t=80, b=40),
    bargap=0.25
)

st.plotly_chart(fig_timeline, use_container_width=True, key="flow_timeline")

st.markdown("<br>", unsafe_allow_html=True)

# How it works
st.markdown("<h3 style='color: #00BCD4;'>🔄 How It Works</h3>", unsafe_allow_html=True)

work_col1, work_col2 = st.columns([1, 1], gap="large")

with work_col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid #2a3342;'>
    <h4 style='color: #4fc3f7; margin-top: 0;'>1️⃣ User Interaction</h4>
    <p style='color: #e0e0e0; line-height: 1.8; font-size: 0.95rem;'>
    Users interact with the <strong>Streamlit dashboard</strong> through an intuitive web interface. 
    They can select date ranges, view charts, ask natural language questions, and generate reports.
    </p>
    </div>
    <br>
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid #2a3342;'>
    <h4 style='color: #4fc3f7; margin-top: 0;'>2️⃣ API Communication</h4>
    <p style='color: #e0e0e0; line-height: 1.8; font-size: 0.95rem;'>
    The dashboard sends <strong>HTTP requests</strong> to the FastAPI backend. The API receives requests, 
    validates them, and routes them to the appropriate service for processing.
    </p>
    </div>
    """, unsafe_allow_html=True)

with work_col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid #2a3342;'>
    <h4 style='color: #4fc3f7; margin-top: 0;'>3️⃣ Data Processing</h4>
    <p style='color: #e0e0e0; line-height: 1.8; font-size: 0.95rem;'>
    The backend queries the <strong>PostgreSQL database</strong> for sales and inventory data. 
    For AI features, it communicates with <strong>OpenAI's GPT-4</strong> to process natural language and generate insights.
    </p>
    </div>
    <br>
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid #2a3342;'>
    <h4 style='color: #4fc3f7; margin-top: 0;'>4️⃣ Response Delivery</h4>
    <p style='color: #e0e0e0; line-height: 1.8; font-size: 0.95rem;'>
    Processed data is returned to the dashboard where it's transformed into beautiful 
    <strong>interactive charts and tables</strong> that users can explore and analyze.
    </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# ========== SECTION 5: Tech Stack ==========
st.markdown("<h2 style='color: #4fc3f7;'>🛠️ Technology Stack</h2>", unsafe_allow_html=True)

tech_col1, tech_col2 = st.columns(2, gap="large")

with tech_col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid #2a3342;'>
    <h4 style='color: #81c784; margin-top: 0;'>🎨 Frontend Technologies</h4>
    <table style='width: 100%; color: #e0e0e0; font-size: 0.95rem;'>
        <tr style='border-bottom: 1px solid #2a3342;'>
            <td style='padding: 0.75rem; color: #4fc3f7; font-weight: bold;'>Streamlit</td>
            <td style='padding: 0.75rem;'>Web dashboard framework</td>
        </tr>
        <tr style='border-bottom: 1px solid #2a3342;'>
            <td style='padding: 0.75rem; color: #4fc3f7; font-weight: bold;'>Plotly</td>
            <td style='padding: 0.75rem;'>Interactive charts & graphs</td>
        </tr>
        <tr style='border-bottom: 1px solid #2a3342;'>
            <td style='padding: 0.75rem; color: #4fc3f7; font-weight: bold;'>HTML/CSS</td>
            <td style='padding: 0.75rem;'>Custom styling & layouts</td>
        </tr>
        <tr>
            <td style='padding: 0.75rem; color: #4fc3f7; font-weight: bold;'>Pandas</td>
            <td style='padding: 0.75rem;'>Data manipulation</td>
        </tr>
    </table>
    </div>
    <br>
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid #2a3342;'>
    <h4 style='color: #81c784; margin-top: 0;'>🤖 AI & Machine Learning</h4>
    <table style='width: 100%; color: #e0e0e0; font-size: 0.95rem;'>
        <tr style='border-bottom: 1px solid #2a3342;'>
            <td style='padding: 0.75rem; color: #4fc3f7; font-weight: bold;'>OpenAI GPT-4</td>
            <td style='padding: 0.75rem;'>Natural language processing</td>
        </tr>
        <tr style='border-bottom: 1px solid #2a3342;'>
            <td style='padding: 0.75rem; color: #4fc3f7; font-weight: bold;'>LangChain</td>
            <td style='padding: 0.75rem;'>LLM application framework</td>
        </tr>
        <tr>
            <td style='padding: 0.75rem; color: #4fc3f7; font-weight: bold;'>ChromaDB</td>
            <td style='padding: 0.75rem;'>Vector database for RAG</td>
        </tr>
    </table>
    </div>
    """, unsafe_allow_html=True)

with tech_col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid #2a3342;'>
    <h4 style='color: #81c784; margin-top: 0;'>⚙️ Backend Technologies</h4>
    <table style='width: 100%; color: #e0e0e0; font-size: 0.95rem;'>
        <tr style='border-bottom: 1px solid #2a3342;'>
            <td style='padding: 0.75rem; color: #4fc3f7; font-weight: bold;'>FastAPI</td>
            <td style='padding: 0.75rem;'>High-performance REST API</td>
        </tr>
        <tr style='border-bottom: 1px solid #2a3342;'>
            <td style='padding: 0.75rem; color: #4fc3f7; font-weight: bold;'>Python 3.11</td>
            <td style='padding: 0.75rem;'>Core programming language</td>
        </tr>
        <tr style='border-bottom: 1px solid #2a3342;'>
            <td style='padding: 0.75rem; color: #4fc3f7; font-weight: bold;'>Pydantic</td>
            <td style='padding: 0.75rem;'>Data validation & schemas</td>
        </tr>
        <tr>
            <td style='padding: 0.75rem; color: #4fc3f7; font-weight: bold;'>Uvicorn</td>
            <td style='padding: 0.75rem;'>ASGI web server</td>
        </tr>
    </table>
    </div>
    <br>
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid #2a3342;'>
    <h4 style='color: #81c784; margin-top: 0;'>💾 Data & Storage</h4>
    <table style='width: 100%; color: #e0e0e0; font-size: 0.95rem;'>
        <tr style='border-bottom: 1px solid #2a3342;'>
            <td style='padding: 0.75rem; color: #4fc3f7; font-weight: bold;'>PostgreSQL</td>
            <td style='padding: 0.75rem;'>Relational database</td>
        </tr>
        <tr style='border-bottom: 1px solid #2a3342;'>
            <td style='padding: 0.75rem; color: #4fc3f7; font-weight: bold;'>SQLAlchemy</td>
            <td style='padding: 0.75rem;'>ORM & database toolkit</td>
        </tr>
        <tr>
            <td style='padding: 0.75rem; color: #4fc3f7; font-weight: bold;'>Alembic</td>
            <td style='padding: 0.75rem;'>Database migrations</td>
        </tr>
    </table>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# ========== SECTION 6: Key Features ==========
st.markdown("<h2 style='color: #4fc3f7;'>✨ Key Features</h2>", unsafe_allow_html=True)

feat_col1, feat_col2, feat_col3 = st.columns(3, gap="medium")

with feat_col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid #2a3342; text-align: center;'>
    <h3 style='color: #4fc3f7; font-size: 2.5rem; margin: 0;'>📊</h3>
    <h4 style='color: #81c784; margin: 0.5rem 0;'>Real-time Analytics</h4>
    <p style='color: #e0e0e0; font-size: 0.9rem; line-height: 1.6;'>
    Monitor KPIs, track sales trends, and analyze inventory levels in real-time with 
    responsive charts and metrics.
    </p>
    </div>
    """, unsafe_allow_html=True)

with feat_col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid #2a3342; text-align: center;'>
    <h3 style='color: #4fc3f7; font-size: 2.5rem; margin: 0;'>🤖</h3>
    <h4 style='color: #81c784; margin: 0.5rem 0;'>AI-Powered Insights</h4>
    <p style='color: #e0e0e0; font-size: 0.9rem; line-height: 1.6;'>
    Ask questions in plain English and get instant answers. The AI automatically 
    identifies trends and generates recommendations.
    </p>
    </div>
    """, unsafe_allow_html=True)

with feat_col3:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid #2a3342; text-align: center;'>
    <h3 style='color: #4fc3f7; font-size: 2.5rem; margin: 0;'>📈</h3>
    <h4 style='color: #81c784; margin: 0.5rem 0;'>Interactive Reports</h4>
    <p style='color: #e0e0e0; font-size: 0.9rem; line-height: 1.6;'>
    Generate comprehensive reports with AI-written summaries, export data, 
    and share insights with stakeholders.
    </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# ========== SECTION 7: Project Info ==========
st.markdown("<h2 style='color: #4fc3f7;'>📌 Project Information</h2>", unsafe_allow_html=True)

info_col1, info_col2 = st.columns(2, gap="large")

with info_col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid #2a3342;'>
    <h4 style='color: #81c784; margin-top: 0;'>🎯 Purpose</h4>
    <p style='color: #e0e0e0; line-height: 1.8; font-size: 0.95rem;'>
    This is a <strong style='color: #4fc3f7;'>pilot demonstration project</strong> created to showcase how modern 
    analytics platforms can combine traditional business intelligence with cutting-edge AI capabilities. 
    It serves as a proof-of-concept for data-driven decision making.
    </p>
    </div>
    <br>
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid #2a3342;'>
    <h4 style='color: #81c784; margin-top: 0;'>🔒 Data Privacy</h4>
    <p style='color: #e0e0e0; line-height: 1.8; font-size: 0.95rem;'>
    All data used in this dashboard is <strong style='color: #4fc3f7;'>artificially generated</strong> and does not 
    contain any real customer or business information. It's designed purely for demonstration and testing purposes.
    </p>
    </div>
    """, unsafe_allow_html=True)

with info_col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid #2a3342;'>
    <h4 style='color: #81c784; margin-top: 0;'>🚀 Future Enhancements</h4>
    <ul style='color: #e0e0e0; line-height: 1.8; font-size: 0.95rem;'>
        <li>Real-time data streaming</li>
        <li>Predictive analytics & forecasting</li>
        <li>Custom alert notifications</li>
        <li>Multi-user collaboration</li>
        <li>Mobile responsive design</li>
    </ul>
    </div>
    <br>
    <div style='background: linear-gradient(135deg, #1c2331 0%, #232b3a 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid #2a3342;'>
    <h4 style='color: #81c784; margin-top: 0;'>📞 Support & Repository</h4>
    <p style='color: #e0e0e0; line-height: 1.8; font-size: 0.95rem;'>
    For questions or feedback, please refer to the project documentation in the repository. 
    This is an actively maintained pilot project.
    </p>
    <div style='text-align: center; margin-top: 1.5rem; padding: 1rem; background: rgba(0, 212, 255, 0.05); border-radius: 12px; border: 1px solid rgba(0, 212, 255, 0.2);'>
        <p style='color: #00d4ff; font-weight: 600; margin-bottom: 0.5rem; font-size: 1rem;'>
            <svg viewBox="0 0 16 16" style="width: 18px; height: 18px; display: inline-block; vertical-align: middle; margin-right: 8px;" fill="#00d4ff">
                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
            </svg>
            GitHub Repository
        </p>
        <a href='https://github.com/kmrsdrm-arch/vortex-automotive-analytics' target='_blank' style='color: #4fc3f7; text-decoration: none; font-size: 0.9rem; font-family: "Courier New", monospace; border: 1px solid #4fc3f7; padding: 0.5rem 1rem; border-radius: 8px; display: inline-block; transition: all 0.3s;'>
            kmrsdrm-arch/vortex-automotive-analytics
        </a>
    </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(0, 212, 255, 0.05) 0%, rgba(123, 47, 247, 0.05) 100%); 
            border-radius: 16px; border: 1px solid rgba(123, 47, 247, 0.3); margin-top: 2rem;'>
    <p style='background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 50%, #f026ff 100%);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                background-clip: text; font-size: 1.5rem; font-weight: 900; margin-bottom: 0.5rem; font-family: "Orbitron", sans-serif; letter-spacing: 4px;'>
        ⚡ VORTEX
    </p>
    <p style='color: #00d4ff; font-size: 0.95rem; margin-bottom: 0; letter-spacing: 0.05em; font-family: "Inter", sans-serif;'>
        Automotive Intelligence Platform
    </p>
    <p style='color: rgba(255, 255, 255, 0.5); font-size: 0.85rem; margin-top: 1rem; font-family: "Inter", sans-serif;'>
        Built with FastAPI • Streamlit • PostgreSQL • OpenAI GPT-4 • ChromaDB
    </p>
    <p style='color: rgba(255, 255, 255, 0.4); font-size: 0.8rem; margin-top: 0.5rem; font-family: "Inter", sans-serif;'>
        © 2025 VORTEX • Automotive Intelligence Platform v2.0
    </p>
    <div style='margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid rgba(123, 47, 247, 0.3);'>
        <a href='https://github.com/kmrsdrm-arch/vortex-automotive-analytics' target='_blank' 
           style='color: #00d4ff; text-decoration: none; font-size: 0.9rem; font-family: "Inter", sans-serif; display: inline-flex; align-items: center; gap: 8px; padding: 0.5rem 1rem; border: 1px solid rgba(0, 212, 255, 0.3); border-radius: 8px; transition: all 0.3s;'>
            <svg viewBox="0 0 16 16" style="width: 16px; height: 16px;" fill="currentColor">
                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
            </svg>
            View on GitHub
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

