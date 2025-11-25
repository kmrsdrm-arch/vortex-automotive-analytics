"""
Executive-level theme configuration for Vortex
Premium dark theme with quantum intelligence design elements
"""

# Executive Premium Dark Theme CSS - Vortex Edition
DARK_THEME_CSS = """
<style>
    /* Import Vortex premium fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Orbitron:wght@400;500;600;700;900&display=swap');
    
    /* Global executive theme - Vortex */
    .stApp {
        background: radial-gradient(ellipse at top, #0a0a0f 0%, #000000 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Vortex Premium background pattern with quantum gradients */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(0, 212, 255, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(123, 47, 247, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(240, 38, 255, 0.02) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Main content area - full width */
    .main {
        background: transparent;
        padding: 1rem 2rem;
    }
    
    .block-container {
        padding: 1.5rem 2rem !important;
        max-width: 100% !important;
        position: relative;
        z-index: 1;
    }
    
    /* Premium page header - Vortex */
    .main-title {
        text-align: center;
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 50%, #f026ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
        letter-spacing: 2px;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: rgba(0, 212, 255, 0.7);
        margin-bottom: 3rem;
        font-weight: 300;
        letter-spacing: 0.05em;
        animation: fadeIn 1s ease-out;
    }
    
    /* Executive metric cards - Vortex */
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 50%, #f026ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.95rem !important;
        color: rgba(255, 255, 255, 0.7) !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }
    
    /* Premium metric container */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.05) 0%, rgba(0, 102, 255, 0.05) 100%) !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-4px) !important;
        border-color: rgba(0, 212, 255, 0.4) !important;
        box-shadow: 
            0 12px 48px rgba(0, 212, 255, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    }
    
    [data-testid="metric-container"]:hover::before {
        left: 100%;
    }
    
    /* Premium sidebar - Vortex */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #12121a 0%, #0a0a0f 100%) !important;
        border-right: 1px solid rgba(123, 47, 247, 0.2) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.5) !important;
        backdrop-filter: blur(20px);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: rgba(255, 255, 255, 0.9);
    }
    
    /* Headers with premium styling - Vortex */
    h1 {
        font-family: 'Orbitron', sans-serif !important;
        color: #00d4ff !important;
        font-weight: 900 !important;
        letter-spacing: 2px !important;
        font-size: 2.5rem !important;
    }
    
    h2 {
        font-family: 'Orbitron', sans-serif !important;
        color: #7b2ff7 !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        font-size: 2rem !important;
    }
    
    h3 {
        font-family: 'Orbitron', sans-serif !important;
        color: #00d4ff !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
    }
    
    /* Body text */
    p, span, div, label {
        color: rgba(255, 255, 255, 0.85) !important;
        font-weight: 400;
    }
    
    /* Premium buttons - Vortex */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 50%, #f026ff 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 12px 40px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        letter-spacing: 0.02em !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 10px 30px rgba(123, 47, 247, 0.4) !important;
        text-transform: uppercase;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(123, 47, 247, 0.5) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Premium input fields */
    .stSelectbox > div > div,
    .stTextInput > div > div > input,
    .stDateInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(0, 212, 255, 0.05) !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
        border-radius: 12px !important;
        color: #fff !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:hover,
    .stTextInput > div > div > input:hover,
    .stDateInput > div > div > input:hover,
    .stTextArea > div > div > textarea:hover {
        border-color: rgba(0, 212, 255, 0.4) !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.1) !important;
    }
    
    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div > input:focus,
    .stDateInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.3) !important;
    }
    
    /* Premium expander */
    .streamlit-expanderHeader {
        background: rgba(0, 212, 255, 0.05) !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
        border-radius: 12px !important;
        color: #00d4ff !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(0, 212, 255, 0.1) !important;
        border-color: rgba(0, 212, 255, 0.4) !important;
    }
    
    /* Premium divider */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.3), transparent) !important;
        margin: 2rem 0 !important;
    }
    
    /* Chart containers with premium styling */
    .js-plotly-plot {
        border-radius: 16px !important;
        background: rgba(0, 212, 255, 0.02) !important;
        border: 1px solid rgba(0, 212, 255, 0.1) !important;
        padding: 1rem !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(0, 212, 255, 0.05) !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        color: rgba(255, 255, 255, 0.7) !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 212, 255, 0.1) !important;
        border-color: rgba(0, 212, 255, 0.4) !important;
        color: #00d4ff !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.2) 0%, rgba(0, 102, 255, 0.2) 100%) !important;
        border-color: #00d4ff !important;
        color: #00d4ff !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.3);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00d4ff, #0099ff);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #00ffff, #00d4ff);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
    
    /* Data tables */
    .dataframe {
        background: rgba(0, 212, 255, 0.02) !important;
        border: 1px solid rgba(0, 212, 255, 0.1) !important;
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .dataframe th {
        background: rgba(0, 212, 255, 0.1) !important;
        color: #00d4ff !important;
        font-weight: 600 !important;
        padding: 1rem !important;
    }
    
    .dataframe td {
        color: rgba(255, 255, 255, 0.85) !important;
        padding: 0.75rem 1rem !important;
        border-bottom: 1px solid rgba(0, 212, 255, 0.05) !important;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: #00d4ff !important;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: rgba(0, 255, 136, 0.1) !important;
        border-left: 4px solid #00ff88 !important;
        border-radius: 8px !important;
    }
    
    .stError {
        background: rgba(255, 71, 87, 0.1) !important;
        border-left: 4px solid #ff4757 !important;
        border-radius: 8px !important;
    }
    
    .stWarning {
        background: rgba(255, 184, 0, 0.1) !important;
        border-left: 4px solid #ffb800 !important;
        border-radius: 8px !important;
    }
    
    .stInfo {
        background: rgba(0, 212, 255, 0.1) !important;
        border-left: 4px solid #00d4ff !important;
        border-radius: 8px !important;
    }
</style>
"""

# Executive Plotly dark theme config
PLOTLY_DARK_THEME = {
    "layout": {
        "plot_bgcolor": "rgba(10, 14, 39, 0.5)",
        "paper_bgcolor": "rgba(10, 14, 39, 0.3)",
        "font": {
            "color": "rgba(255, 255, 255, 0.85)", 
            "size": 13, 
            "family": "Inter, -apple-system, BlinkMacSystemFont, sans-serif"
        },
        "title": {
            "font": {
                "size": 20, 
                "color": "#00d4ff", 
                "family": "Space Grotesk, Inter"
            }
        },
        "xaxis": {
            "gridcolor": "rgba(0, 212, 255, 0.1)",
            "linecolor": "rgba(0, 212, 255, 0.2)",
            "zerolinecolor": "rgba(0, 212, 255, 0.2)",
            "tickfont": {"size": 12, "color": "rgba(255, 255, 255, 0.7)"},
        },
        "yaxis": {
            "gridcolor": "rgba(0, 212, 255, 0.1)",
            "linecolor": "rgba(0, 212, 255, 0.2)",
            "zerolinecolor": "rgba(0, 212, 255, 0.2)",
            "tickfont": {"size": 12, "color": "rgba(255, 255, 255, 0.7)"},
        },
        "colorway": [
            "#00d4ff",  # Vortex Cyan
            "#7b2ff7",  # Vortex Purple
            "#f026ff",  # Vortex Pink
            "#00ffff",  # Bright cyan
            "#a855f7",  # Light purple
            "#33e0ff",  # Light cyan
            "#9333ea",  # Deep purple
            "#ff00ff"   # Bright pink
        ],
        "margin": {"l": 60, "r": 40, "t": 80, "b": 60},
        "hovermode": "closest",
        "hoverlabel": {
            "bgcolor": "rgba(0, 0, 0, 0.9)",
            "font": {"size": 13, "color": "#00d4ff"},
            "bordercolor": "#00d4ff"
        }
    }
}
