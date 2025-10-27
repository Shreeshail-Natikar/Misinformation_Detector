# app_web.py - Professional Streamlit Interface for CrediCheck AI

import streamlit as st
import os
import sys

# --- 1. SETUP & IMPORTS ---

# Add the src directory to the path to allow importing modules (e.g., FusionEngine)
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import the core analysis class
try:
    from src.main_app import MisinformationPlatform
except ImportError:
    st.error("Error: Could not import MisinformationPlatform. Check your file structure.")
    st.stop()


# --- 2. PROFESSIONAL DESIGN CONSTANTS ---

# Color Palette for Trust and Urgency
COLORS = {
    'trust_green': '#388E3C',      # Success Green - Universal "Safe" signal
    'warning_red': '#B00020',      # Warning Red - Universal "Danger" signal  
    'primary_blue': '#1976D2',     # Primary Blue - Trust and branding
    'background_gray': '#F5F5F5',  # Light Gray - Clean, modern background
    'text_dark': '#212121',        # Dark text for readability
    'border_light': '#E0E0E0'      # Light border for subtle separation
}

# Dynamic Background Constants
THRESHOLD = 0.5                      # Score below this value is Misinformation
COLOR_MISINFORMATION_RED = "#E0B0FF" # Dark Warning Red
COLOR_NEUTRAL_BG = "#DAB1DA"         # Light Purple (Your Preferred Color)

def apply_ui_color(score: float):
    """
    Applies the background color change and ensures text is visible.
    
    - Misinformation (score < 0.5): Dark overlay with red tint, White text.
    - Credible (score >= 0.5): Dark overlay with blue tint, White text.
    """
    if score < THRESHOLD:
        color_hex = "#ff4757"  # Red tint for misinformation
        text_color = 'white'   # White text on dark background
    else:
        # Credible result: Blue tint
        color_hex = "#3742fa"  # Blue tint for credible content
        text_color = 'white'   # White text on dark background

    # --- INJECT CUSTOM CSS ---
    st.markdown(
        f"""
        <style>
        /* 1. Dynamic 3D color overlay */
        .stApp .dynamic-overlay {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, {color_hex}20, transparent, {color_hex}10);
            opacity: 0.4;
            z-index: 1;
            transition: all 0.5s ease;
            pointer-events: none;
        }}

        /* 2. Set ALL text elements to bright white for readability on dark background */
        .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label, 
        .stApp div[data-testid*="stText"], 
        .stApp div[data-testid*="stHeader"],
        .stApp .stMarkdown,
        .stApp .stWrite,
        .stApp .stSelectbox,
        .stApp .stSlider,
        .stApp .stButton {{
            color: #ffffff !important; 
            text-shadow: 0 2px 8px rgba(0,0,0,0.8);
            font-weight: 600;
        }}
        
        /* 3. Ensure sidebar text is bright white with strong shadows */
        .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar p, .stSidebar label,
        .stSidebar .stMarkdown,
        .stSidebar .stWrite,
        .stSidebar div[data-testid*="stText"],
        .stSidebar div[data-testid*="stHeader"],
        .stSidebar .stSelectbox,
        .stSidebar .stSlider {{
            color: #ffffff !important; 
            text-shadow: 0 2px 8px rgba(0,0,0,0.8);
            font-weight: 600;
        }}
        
        /* 4. Ensure input boxes have high contrast backgrounds */
        div[data-testid="stTextInput"] > div, 
        div[data-testid="stFileUploader"] > div,
        div[data-testid="stTextArea"] > div {{
            background-color: rgba(0, 0, 0, 0.8) !important;
            color: #ffffff !important;
            border: 2px solid rgba(0, 255, 255, 0.3) !important;
            backdrop-filter: blur(10px);
            text-shadow: 0 1px 3px rgba(0,0,0,0.8);
        }}
        
        /* 5. Enhanced button styling for dark background */
        .stButton > button {{
            background: linear-gradient(45deg, {COLORS['primary_blue']}, #00ffff) !important;
            color: #ffffff !important;
            border: 2px solid rgba(0, 255, 255, 0.5) !important;
            backdrop-filter: blur(10px);
            text-shadow: 0 1px 3px rgba(0,0,0,0.8);
            box-shadow: 0 4px 15px rgba(0, 255, 255, 0.3);
        }}
        
        /* 6. Enhanced metric cards for better visibility */
        .metric-card {{
            background: rgba(0, 0, 0, 0.7) !important;
            border: 1px solid rgba(0, 255, 255, 0.3) !important;
            color: #ffffff !important;
            backdrop-filter: blur(10px);
        }}
        
        /* 7. Enhanced verdict containers */
        .verdict-container {{
            background: rgba(0, 0, 0, 0.8) !important;
            border: 2px solid rgba(0, 255, 255, 0.4) !important;
            color: #ffffff !important;
            backdrop-filter: blur(15px);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    # --- END CSS INJECTION ---

# --- 3. STREAMLIT CACHING (Performance Optimization) ---

@st.cache_resource
def load_platform():
    """Loads the core analysis modules only once for efficient execution."""
    try:
        # Initialize the platform. It will load all mock ML components.
        platform = MisinformationPlatform()
        return platform
    except Exception as e:
        # FIX: Clearer error message and return None instead of re-running/stopping haphazardly
        st.error(f"FATAL ERROR: Failed to load AI platform components. Please check your terminal for library or memory errors. Details: {e}")
        return None # Return None on failure

# --- 4. PROFESSIONAL UI DEFINITION & LAYOUT ---

st.set_page_config(
    page_title="CrediCheck AI - Multi-modal Misinformation Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling with animated background
st.markdown(f"""
<style>
    /* 3D Geometric Background */
    .stApp {{
        background: linear-gradient(135deg, #0f0f23, #1a1a2e, #16213e, #0f3460);
        position: relative;
        overflow: hidden;
    }}
    
    /* 3D Geometric Shapes */
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            /* Large geometric shapes */
            polygon(50% 0%, 0% 100%, 100% 100%),
            polygon(0% 0%, 100% 0%, 50% 100%),
            polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
        background-size: 300px 300px, 200px 200px, 150px 150px;
        background-position: 0% 0%, 100% 100%, 50% 50%;
        background-repeat: no-repeat;
        opacity: 0.1;
        animation: geometricFloat 20s ease-in-out infinite;
        z-index: 0;
    }}
    
    /* Holographic Earth with Dynamic Lines */
    .stApp::after {{
        content: '';
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 250px;
        height: 250px;
        border-radius: 50%;
        background: 
            /* Holographic Earth base */
            radial-gradient(circle at 50% 50%, rgba(0, 255, 255, 0.1) 0%, rgba(0, 150, 255, 0.2) 30%, rgba(0, 100, 200, 0.3) 70%, rgba(0, 50, 150, 0.4) 100%),
            /* Dynamic grid lines */
            linear-gradient(0deg, transparent 48%, rgba(0, 255, 255, 0.3) 49%, rgba(0, 255, 255, 0.3) 51%, transparent 52%),
            linear-gradient(90deg, transparent 48%, rgba(0, 255, 255, 0.3) 49%, rgba(0, 255, 255, 0.3) 51%, transparent 52%),
            linear-gradient(45deg, transparent 48%, rgba(0, 255, 255, 0.2) 49%, rgba(0, 255, 255, 0.2) 51%, transparent 52%),
            linear-gradient(-45deg, transparent 48%, rgba(0, 255, 255, 0.2) 49%, rgba(0, 255, 255, 0.2) 51%, transparent 52%);
        background-size: 100% 100%, 50px 50px, 50px 50px, 35px 35px, 35px 35px;
        box-shadow: 
            0 0 80px rgba(0, 255, 255, 0.6),
            0 0 120px rgba(0, 150, 255, 0.4),
            inset 0 0 50px rgba(0, 255, 255, 0.2),
            inset -30px -30px 60px rgba(0, 0, 0, 0.4),
            inset 30px 30px 60px rgba(255, 255, 255, 0.1);
        animation: holographicRotate 15s linear infinite, earthFloat 6s ease-in-out infinite, gridPulse 3s ease-in-out infinite;
        z-index: 0;
    }}
    
    /* Holographic rings around Earth */
    .stApp .holographic-rings {{
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 250px;
        height: 250px;
        border-radius: 50%;
        border: 2px solid rgba(0, 255, 255, 0.3);
        animation: ringRotate 10s linear infinite;
        z-index: 0;
    }}
    
    .stApp .holographic-rings::before {{
        content: '';
        position: absolute;
        top: -20px;
        left: -20px;
        width: 290px;
        height: 290px;
        border-radius: 50%;
        border: 1px solid rgba(0, 255, 255, 0.2);
        animation: ringRotate 15s linear infinite reverse;
    }}
    
    .stApp .holographic-rings::after {{
        content: '';
        position: absolute;
        top: -40px;
        left: -40px;
        width: 330px;
        height: 330px;
        border-radius: 50%;
        border: 1px solid rgba(0, 255, 255, 0.1);
        animation: ringRotate 20s linear infinite;
    }}
    
    /* Additional floating elements */
    .stApp .floating-elements {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            /* CSS 3D cubes using gradients */
            linear-gradient(45deg, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            linear-gradient(-45deg, rgba(255, 255, 255, 0.05) 0%, transparent 50%),
            linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, transparent 50%),
            linear-gradient(-135deg, rgba(255, 255, 255, 0.03) 0%, transparent 50%);
        background-size: 100px 100px, 80px 80px, 120px 120px, 60px 60px;
        background-position: 10% 20%, 80% 30%, 30% 70%, 70% 80%;
        animation: cubeFloat 15s ease-in-out infinite;
        z-index: 0;
        pointer-events: none;
    }}
    
    @keyframes geometricFloat {{
        0%, 100% {{ 
            transform: translateY(0px) rotateX(0deg) rotateY(0deg);
            opacity: 0.1;
        }}
        25% {{ 
            transform: translateY(-20px) rotateX(15deg) rotateY(15deg);
            opacity: 0.15;
        }}
        50% {{ 
            transform: translateY(-40px) rotateX(30deg) rotateY(30deg);
            opacity: 0.2;
        }}
        75% {{ 
            transform: translateY(-20px) rotateX(15deg) rotateY(45deg);
            opacity: 0.15;
        }}
    }}
    
    @keyframes cubeFloat {{
        0%, 100% {{ 
            transform: translateY(0px) rotateZ(0deg) scale(1);
            opacity: 0.05;
        }}
        33% {{ 
            transform: translateY(-30px) rotateZ(120deg) scale(1.2);
            opacity: 0.1;
        }}
        66% {{ 
            transform: translateY(-60px) rotateZ(240deg) scale(0.8);
            opacity: 0.08;
        }}
    }}
    
    @keyframes holographicRotate {{
        0% {{ 
            transform: rotateY(0deg) rotateX(0deg);
        }}
        25% {{ 
            transform: rotateY(90deg) rotateX(15deg);
        }}
        50% {{ 
            transform: rotateY(180deg) rotateX(0deg);
        }}
        75% {{ 
            transform: rotateY(270deg) rotateX(-15deg);
        }}
        100% {{ 
            transform: rotateY(360deg) rotateX(0deg);
        }}
    }}
    
    @keyframes earthFloat {{
        0%, 100% {{ 
            transform: translateY(0px) scale(1);
        }}
        50% {{ 
            transform: translateY(-25px) scale(1.08);
        }}
    }}
    
    @keyframes gridPulse {{
        0%, 100% {{ 
            opacity: 0.3;
            filter: brightness(1);
        }}
        50% {{ 
            opacity: 0.6;
            filter: brightness(1.5);
        }}
    }}
    
    @keyframes ringRotate {{
        0% {{ 
            transform: rotateZ(0deg);
        }}
        100% {{ 
            transform: rotateZ(360deg);
        }}
    }}
    
    /* Ensure content is above the background */
    .stApp > div {{
        position: relative;
        z-index: 1;
    }}
    
    .credicheck-header {{
        background: linear-gradient(135deg, {COLORS['primary_blue']}, {COLORS['trust_green']});
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        background-color: rgba(25, 118, 210, 0.8);
    }}
    .verdict-container {{
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }}
    .verdict-trust {{
        background-color: rgba(232, 245, 232, 0.9);
        border-left: 5px solid {COLORS['trust_green']};
    }}
    .verdict-warning {{
        background-color: rgba(255, 235, 238, 0.9);
        border-left: 5px solid {COLORS['warning_red']};
    }}
    .verdict-caution {{
        background-color: rgba(255, 243, 224, 0.9);
        border-left: 5px solid #FF9800;
    }}
    .metric-card {{
        background: rgba(0, 0, 0, 0.7);
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(0, 255, 255, 0.3);
        color: #ffffff;
    }}
    .score-high {{ color: {COLORS['trust_green']}; font-weight: bold; }}
    .score-medium {{ color: #FF9800; font-weight: bold; }}
    .score-low {{ color: {COLORS['warning_red']}; font-weight: bold; }}
    
    /* Sidebar styling with black background */
    .stSidebar {{
        background-color: rgba(0, 0, 0, 0.9);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    /* Settings toggle button styling */
    .stButton > button {{
        background: linear-gradient(45deg, {COLORS['primary_blue']}, #00ffff) !important;
        color: #ffffff !important;
        border: 2px solid rgba(0, 255, 255, 0.5) !important;
        backdrop-filter: blur(10px);
        text-shadow: 0 1px 3px rgba(0,0,0,0.8);
        box-shadow: 0 4px 15px rgba(0, 255, 255, 0.3);
        border-radius: 8px !important;
        font-weight: 600 !important;
    }}
    
    .stButton > button:hover {{
        box-shadow: 0 6px 20px rgba(0, 255, 255, 0.5) !important;
        transform: translateY(-2px) !important;
    }}
    
    /* Sliding animation for settings panel */
    .settings-panel {{
        transition: transform 0.3s ease-in-out, opacity 0.3s ease-in-out;
        transform: translateX(0);
        opacity: 1;
    }}
    
    .settings-panel.hidden {{
        transform: translateX(-100%);
        opacity: 0;
    }}
    
    /* Enhanced sidebar with sliding effect */
    .stSidebar {{
        background-color: rgba(0, 0, 0, 0.9);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.3s ease-in-out;
    }}
    
    .stSidebar.collapsed {{
        transform: translateX(-100%);
    }}
</style>
""", unsafe_allow_html=True)

# --- 5. INITIAL BACKGROUND SETUP ---

# Add floating elements, holographic rings, and dynamic overlay
st.markdown('<div class="floating-elements"></div>', unsafe_allow_html=True)
st.markdown('<div class="holographic-rings"></div>', unsafe_allow_html=True)
st.markdown('<div class="dynamic-overlay"></div>', unsafe_allow_html=True)

# Set initial neutral background before any analysis
apply_ui_color(1.0)  # High score = neutral background

# --- 6. PROFESSIONAL HEADER & BRANDING ---

st.markdown("""
<div class="credicheck-header">
    <h1>🛡️ CrediCheck AI</h1>
    <h3>Multi-modal Misinformation Detector</h3>
    <p style="font-size: 1.1em; margin-top: 1rem; opacity: 0.9;">
        Advanced AI-powered analysis of news credibility using Source Verification, 
        Tone Analysis, Image Context, and Deepfake Detection
    </p>
</div>
""", unsafe_allow_html=True)

# --- 6. PROFESSIONAL SIDEBAR SETTINGS ---

# Initialize session state for sidebar visibility
if 'sidebar_visible' not in st.session_state:
    st.session_state.sidebar_visible = True

# Create a collapsible settings panel
with st.sidebar:
    st.title("⚙️ Analysis Settings")
    
    # Toggle button with sliding animation
    if st.session_state.sidebar_visible:
        if st.button("🔽 Hide Settings", help="Hide Analysis Settings Panel"):
            st.session_state.sidebar_visible = False
            st.rerun()
    else:
        if st.button("🔼 Show Settings", help="Show Analysis Settings Panel"):
            st.session_state.sidebar_visible = True
            st.rerun()
    
    # Settings content - completely hidden when sidebar_visible is False
    if st.session_state.sidebar_visible:
        st.markdown("---")
        
        # Risk Threshold Configuration
        st.subheader("🎯 Risk Assessment")
        misinformation_threshold = st.slider(
            'Credibility Threshold',
    min_value=0.20,
    max_value=0.80,
            value=0.60,
    step=0.05,
            help="Scores below this value trigger 'High Risk' warnings"
        )

        # Advanced Settings
        with st.expander("🔧 Advanced Settings"):
            st.info("🔬 **Development Mode** - Adjust mock components for testing")
            mock_deepfake_score = st.slider(
    'Deepfake Mock Score',
    min_value=0.0,
    max_value=1.0,
    value=0.90, 
    step=0.01,
                help="Mock score for deepfake detection testing"
            )

        st.markdown("---")
        st.markdown("**🚀 Powered by:**")
        st.markdown("• **NLP Analysis** (VADER)")
        st.markdown("• **Computer Vision** (BLIP)")
        st.markdown("• **Source Verification**")
        st.markdown("• **Fusion AI Engine**")
    else:
        # Default values when sidebar is hidden - no content shown
        misinformation_threshold = 0.60
        mock_deepfake_score = 0.90

# --- 7. PROFESSIONAL INPUT ZONE ---

st.markdown("### 📝 Input Your Claim for Analysis")

# Initialize media_key before the container
media_key = None 

# Professional input container with better styling
with st.container():
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Enhanced text input with better placeholder
        claim_text = st.text_area(
            "**Article Text or Claim:**",
            "SHOCKING NEW VIDEO shows government cover-up of alien contact! They are lying to us! MUST WATCH!",
            height=120,
            help="Paste the suspicious news article, headline, or claim you want to analyze",
            placeholder="Enter the text content you want to verify..."
        )
        
        # Enhanced URL input
        claim_url = st.text_input(
            "**Source URL:**",
            "http://bunkerville.com/secret-file-exposed",
            help="Enter the website or source URL where this claim was found",
            placeholder="https://example.com/article..."
        )
        
    with col2:
        st.markdown("**📸 Media Analysis**")
        st.markdown("*Upload image/video for visual verification*")
        
        # Enhanced file uploader
        uploaded_file = st.file_uploader(
            "Choose Media File", 
            type=['png', 'jpg', 'jpeg', 'mp4', 'mov', 'avi'], 
            accept_multiple_files=False,
            help="📷 Images: JPG, PNG | 🎥 Videos: MP4, MOV, AVI (Max 200MB)"
        )
        
        # Professional media preview
        if uploaded_file is not None:
            file_type = uploaded_file.type
            st.success(f"✅ **{uploaded_file.name}** uploaded")
            
            # Use the actual uploaded file name
            media_key = uploaded_file.name 
            
            if 'image' in file_type:
                st.image(uploaded_file, caption='📷 Image Preview', width=200) 
            elif 'video' in file_type:
                st.video(uploaded_file, format=file_type, start_time=0) 
            
        else:
            # Set mock key for demo
            media_key = "old_news_fire_photo.jpg" 
            st.info("🔬 **Demo Mode**: Using mock media for analysis")
    
    # Professional analysis button
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        analyze_clicked = st.button(
            "🔍 **Analyze Credibility**", 
            type="primary", 
            use_container_width=True,
            help="Run comprehensive multi-modal analysis"
        )
    
    if analyze_clicked:
        
        # --- 8. EXECUTION & PROFESSIONAL DISPLAY ---
        
        if not claim_text or not claim_url:
            st.error("❌ **Please enter both Claim Text and a Source URL to run the analysis.**")
            st.stop()
            
        # Validate media key
        if media_key is None:
             st.error("❌ **A media key could not be determined for analysis.**")
             st.stop()
            
        platform = load_platform()
        
        # Check platform initialization
        if platform is None:
             st.error("❌ **Analysis stopped. The AI platform failed to initialize. Check the error above and your terminal.**")
             st.stop() 

        # Run analysis with professional loading
        with st.spinner('🔍 Running comprehensive multi-modal analysis...'):
            report = platform.run_analysis(claim_url, claim_text, media_key)
        
        final_score = report['--- FINAL VERDICT ---']['score']
        verdict = report['--- FINAL VERDICT ---']['verdict']
        
        # Apply dynamic background color based on analysis result
        apply_ui_color(final_score)
        
        # --- 9. PROFESSIONAL VERDICT DISPLAY ---
        
        st.markdown("---")
        st.markdown("### 🎯 **Analysis Results**")
        
        # Determine verdict styling and messaging
        if final_score < 0.40:
            verdict_class = "verdict-warning"
            verdict_icon = "🚨"
            verdict_title = "HIGH RISK: MISINFORMATION DETECTED"
            toast_message = "Verdict: Misinformation Risk is HIGH!"
            toast_icon = "🚨"
            score_class = "score-low"
        elif final_score < misinformation_threshold:
            verdict_class = "verdict-caution"
            verdict_icon = "⚠️"
            verdict_title = "CAUTION: VERIFY BEFORE SHARING"
            toast_message = "Verdict: Caution Recommended."
            toast_icon = "⚠️"
            score_class = "score-medium"
        else:
            verdict_class = "verdict-trust"
            verdict_icon = "✅"
            verdict_title = "HIGH CREDIBILITY: LIKELY ACCURATE"
            toast_message = "Verdict: Credibility is High."
            toast_icon = "✅"
            score_class = "score-high"
        
        # Show toast notification
        st.toast(toast_message, icon=toast_icon)
        
        # Professional verdict container
        st.markdown(f"""
        <div class="verdict-container {verdict_class}">
            <h2 style="margin: 0; color: {COLORS['text_dark']};">
                {verdict_icon} {verdict_title}
            </h2>
            <p style="font-size: 1.2em; margin: 0.5rem 0;">
                <strong>Verdict:</strong> {verdict}
            </p>
            <p style="font-size: 1.1em; margin: 0;">
                <strong>Credibility Score:</strong> 
                <span class="{score_class}">{final_score:.1%}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

        # --- 10. DETAILED FINDINGS PANEL ---
        
        st.markdown("### 🔬 **Detailed Analysis Breakdown**")
        st.markdown("*Understanding the 'Why' behind our verdict*")
        
        raw_scores = report['Raw_Scores']
        findings = report['Detailed_Findings']
        
        # Create professional metric cards
        col1, col2, col3, col4 = st.columns(4)
        
        # Source Credibility Card
        with col1:
            source_score = raw_scores['source_credibility']
            source_color = "score-high" if source_score > 0.7 else "score-medium" if source_score > 0.4 else "score-low"
            source_icon = "🟢" if source_score > 0.7 else "🟠" if source_score > 0.4 else "🔴"
            
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="margin: 0; color: #ffffff;">{source_icon} Source Check</h4>
                <p style="font-size: 1.5em; margin: 0.5rem 0;">
                    <span class="{source_color}">{source_score:.2f}</span>
                </p>
                <p style="font-size: 0.9em; margin: 0; color: #ffffff;">
                    {findings['Source_Check']}
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Tone Analysis Card
        with col2:
            tone_score = raw_scores['text_tone']
            tone_color = "score-high" if tone_score > 0.7 else "score-medium" if tone_score > 0.4 else "score-low"
            tone_icon = "🟢" if tone_score > 0.7 else "🟠" if tone_score > 0.4 else "🔴"
            
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="margin: 0; color: #ffffff;">{tone_icon} Tone Analysis</h4>
                <p style="font-size: 1.5em; margin: 0.5rem 0;">
                    <span class="{tone_color}">{tone_score:.2f}</span>
                </p>
                <p style="font-size: 0.9em; margin: 0; color: #ffffff;">
                    {findings['Tone_Check']}
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Media Context Card
        with col3:
            media_score = raw_scores['image_context']
            media_color = "score-high" if media_score > 0.7 else "score-medium" if media_score > 0.4 else "score-low"
            media_icon = "🟢" if media_score > 0.7 else "🟠" if media_score > 0.4 else "🔴"
            
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="margin: 0; color: #ffffff;">{media_icon} Media Context</h4>
                <p style="font-size: 1.5em; margin: 0.5rem 0;">
                    <span class="{media_color}">{media_score:.2f}</span>
                </p>
                <p style="font-size: 0.9em; margin: 0; color: #ffffff;">
                    <strong>File:</strong> {media_key}<br>
                    {findings['Image_Context_Check']}
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Deepfake Detection Card
        with col4:
            deepfake_score = raw_scores['deepfake_authenticity']
            deepfake_color = "score-high" if deepfake_score > 0.7 else "score-medium" if deepfake_score > 0.4 else "score-low"
            deepfake_icon = "🟢" if deepfake_score > 0.7 else "🟠" if deepfake_score > 0.4 else "🔴"
            
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="margin: 0; color: #ffffff;">{deepfake_icon} Authenticity</h4>
                <p style="font-size: 1.5em; margin: 0.5rem 0;">
                    <span class="{deepfake_color}">{deepfake_score:.2f}</span>
                </p>
                <p style="font-size: 0.9em; margin: 0; color: #ffffff;">
                    {findings['Deepfake_Check']}
                </p>
            </div>
            """, unsafe_allow_html=True)

        # --- 11. PROFESSIONAL FOOTER ---
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; padding: 1rem;">
            <p><strong>CrediCheck AI</strong> - Advanced Multi-modal Misinformation Detection</p>
            <p style="font-size: 0.9em;">Powered by AI • Built for ANVESHAN-2025</p>
        </div>
        """, unsafe_allow_html=True)
