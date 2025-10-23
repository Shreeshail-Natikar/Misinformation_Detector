# app_web.py - Streamlit Web Interface

import streamlit as st
import os
import sys

# --- 1. SETUP & IMPORTS ---
# Add the src directory to the path to allow importing modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import the core analysis class
try:
    from main_app import MisinformationPlatform
except ImportError:
    st.error("Error: Could not import MisinformationPlatform. Check your file structure.")
    st.stop()


# --- 2. STREAMLIT APP LOGIC ---

# Initialize the platform (using Streamlit's cache for efficiency)
@st.cache_resource
def load_platform():
    """Loads the core analysis modules only once."""
    try:
        # NOTE: We assume the updated FusionEngine (4-score weights) is in use
        platform = MisinformationPlatform()
        return platform
    except Exception as e:
        st.error(f"Failed to load AI platform components: {e}")
        st.stop()

# --- 3. UI DEFINITION ---

st.set_page_config(
    page_title="Multi-modal Misinformation Detector",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛡️ Multi-modal Misinformation Detector")
st.markdown("Analyze a claim based on its **Source**, **Text Tone**, **Image Context**, and **Deepfake Integrity**.")

# Input fields
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        claim_text = st.text_area(
            "Enter the Claim Text (e.g., the headline):",
            "SHOCKING NEW VIDEO shows government cover-up of alien contact! MUST WATCH!",
            height=100
        )
    with col2:
        claim_url = st.text_input(
            "Enter the Source URL (e.g., the website):",
            "http://bunkerville.com/secret-file-exposed"
        )
        # Mock image input (since we don't handle file uploads for mock logic)
        image_file_mock = st.selectbox(
            "Select Mock Image/Video File for CV Analysis:",
            ("old_news_fire_photo.jpg", "official_video_clean_shot.mp4"),
            index=0
        )
    
    if st.button("Analyze Claim", type="primary", use_container_width=True):
        
        # --- 4. EXECUTION & DISPLAY ---
        
        # Load the platform
        platform = load_platform()
        
        with st.spinner('Running Multi-modal Analysis...'):
            # Run the core analysis using the existing class
            report = platform.run_analysis(claim_url, claim_text, image_file_mock)
        
        final_score = report['--- FINAL VERDICT (Based on Source, Context, Tone) ---']['score']
        verdict = report['--- FINAL VERDICT (Based on Source, Context, Tone) ---']['verdict']
        
        st.subheader("Final Fusion Verdict")

        # Display the result using Streamlit metrics/indicators
        col_v, col_s = st.columns([2, 1])
        
        if final_score < 0.40:
            st.toast("Verdict: Misinformation Risk is HIGH!", icon="🚨")
            col_v.error(f"## {verdict}")
        elif final_score < 0.60:
            st.toast("Verdict: Caution Recommended.", icon="⚠️")
            col_v.warning(f"## {verdict}")
        else:
            st.toast("Verdict: Credibility is High.", icon="✅")
            col_v.success(f"## {verdict}")
            
        col_s.metric(label="Fusion Credibility Score", value=f"{final_score:.4f}", help="Weighted average of all analysis components.")

        st.divider()

        st.subheader("🔬 Component Breakdown")
        
        # Display the raw scores and findings side-by-side
        cols_score = st.columns(4)
        raw_scores = report['Raw_Scores']
        findings = report['Detailed_Findings']
        
        # Source Check
        cols_score[0].metric("Source Credibility", f"{raw_scores['source_credibility']:.2f}")
        cols_score[0].caption(f"**Finding:** {findings['Source_Check']}")

        # Tone Check (Inverted Score)
        cols_score[1].metric("Text Tone Credibility", f"{raw_scores['text_tone']:.2f}")
        cols_score[1].caption(f"**Finding:** {findings['Tone_Check']}")
        
        # Image Context
        cols_score[2].metric("Image Context Score", f"{raw_scores['image_context']:.2f}")
        cols_score[2].caption(f"**Finding:** {findings['Image_Context_Check']}")

        # Deepfake Check
        cols_score[3].metric("Deepfake Authenticity", f"{raw_scores['deepfake_authenticity']:.2f}")
        cols_score[3].caption(f"**Finding:** {findings['Deepfake_Check']}")