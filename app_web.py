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
    
    - Misinformation (score < 0.5): Light Purple background, Black text.
    - Credible (score >= 0.5): Light Purple background, Black text.
    """
    if score < THRESHOLD:
        color_hex = COLOR_MISINFORMATION_RED
        text_color = 'black'  # Black text on light purple background
    else:
        # Credible result: Light purple background
        color_hex = COLOR_NEUTRAL_BG 
        text_color = 'black'  # Black text on light purple background

    # --- INJECT CUSTOM CSS ---
    st.markdown(
        f"""
        <style>
        /* 1. Target the overall Streamlit app container for background color */
        .stApp {{
            background-color: {color_hex};
            transition: background-color 0.5s ease; /* Smooth transition */
        }}

        /* 2. Set ALL text elements to the calculated color for readability */
        .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label, 
        .stApp div[data-testid*="stText"], 
        .stApp div[data-testid*="stHeader"],
        .stApp .stMarkdown,
        .stApp .stWrite {{
            color: {text_color} !important; 
        }}
        
        /* 3. Ensure sidebar text is white for better visibility */
        .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar p, .stSidebar label,
        .stSidebar .stMarkdown,
        .stSidebar .stWrite,
        .stSidebar div[data-testid*="stText"],
        .stSidebar div[data-testid*="stHeader"] {{
            color: white !important; 
        }}
        
        /* 4. Ensure input boxes and buttons remain functional and visible */
        /* This keeps elements like text_area and file_uploader backgrounds functional */
        div[data-testid="stTextInput"] > div, 
        div[data-testid="stFileUploader"] > div,
        div[data-testid="stTextArea"] > div {{
            background-color: white !important;
            color: black !important;
        }}
        
        /* 5. Ensure buttons remain visible and functional */
        .stButton > button {{
            background-color: {COLORS['primary_blue']} !important;
            color: white !important;
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

# Custom CSS for professional styling
st.markdown(f"""
<style>
    .main {{
        background-color: {COLORS['background_gray']};
    }}
    .stApp {{
        background-color: {COLORS['background_gray']};
    }}
    .credicheck-header {{
        background: linear-gradient(135deg, {COLORS['primary_blue']}, {COLORS['trust_green']});
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    .verdict-container {{
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    .verdict-trust {{
        background-color: #E8F5E8;
        border-left: 5px solid {COLORS['trust_green']};
    }}
    .verdict-warning {{
        background-color: #FFEBEE;
        border-left: 5px solid {COLORS['warning_red']};
    }}
    .verdict-caution {{
        background-color: #FFF3E0;
        border-left: 5px solid #FF9800;
    }}
    .metric-card {{
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }}
    .score-high {{ color: {COLORS['trust_green']}; font-weight: bold; }}
    .score-medium {{ color: #FF9800; font-weight: bold; }}
    .score-low {{ color: {COLORS['warning_red']}; font-weight: bold; }}
</style>
""", unsafe_allow_html=True)

# --- 5. INITIAL BACKGROUND SETUP ---

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

st.sidebar.title("⚙️ Analysis Settings")
st.sidebar.markdown("---")

# Risk Threshold Configuration
st.sidebar.subheader("🎯 Risk Assessment")
misinformation_threshold = st.sidebar.slider(
    'Credibility Threshold',
    min_value=0.20,
    max_value=0.80,
    value=0.60,
    step=0.05,
    help="Scores below this value trigger 'High Risk' warnings"
)

# Advanced Settings
with st.sidebar.expander("🔧 Advanced Settings"):
    st.info("🔬 **Development Mode** - Adjust mock components for testing")
    mock_deepfake_score = st.slider(
        'Deepfake Mock Score',
        min_value=0.0,
        max_value=1.0,
        value=0.90, 
        step=0.01,
        help="Mock score for deepfake detection testing"
    )

st.sidebar.markdown("---")
st.sidebar.markdown("**🚀 Powered by:**")
st.sidebar.markdown("• **NLP Analysis** (VADER)")
st.sidebar.markdown("• **Computer Vision** (BLIP)")
st.sidebar.markdown("• **Source Verification**")
st.sidebar.markdown("• **Fusion AI Engine**")

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
                <h4 style="margin: 0; color: {COLORS['text_dark']};">{source_icon} Source Check</h4>
                <p style="font-size: 1.5em; margin: 0.5rem 0;">
                    <span class="{source_color}">{source_score:.2f}</span>
                </p>
                <p style="font-size: 0.9em; margin: 0; color: #666;">
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
                <h4 style="margin: 0; color: {COLORS['text_dark']};">{tone_icon} Tone Analysis</h4>
                <p style="font-size: 1.5em; margin: 0.5rem 0;">
                    <span class="{tone_color}">{tone_score:.2f}</span>
                </p>
                <p style="font-size: 0.9em; margin: 0; color: #666;">
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
                <h4 style="margin: 0; color: {COLORS['text_dark']};">{media_icon} Media Context</h4>
                <p style="font-size: 1.5em; margin: 0.5rem 0;">
                    <span class="{media_color}">{media_score:.2f}</span>
                </p>
                <p style="font-size: 0.9em; margin: 0; color: #666;">
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
                <h4 style="margin: 0; color: {COLORS['text_dark']};">{deepfake_icon} Authenticity</h4>
                <p style="font-size: 1.5em; margin: 0.5rem 0;">
                    <span class="{deepfake_color}">{deepfake_score:.2f}</span>
                </p>
                <p style="font-size: 0.9em; margin: 0; color: #666;">
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
