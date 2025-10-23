# app_web.py - Final Streamlit Web Interface for Misinformation Detector

import streamlit as st
import os
import sys

# --- 1. SETUP & IMPORTS ---

# Add the src directory to the path to allow importing modules (e.g., FusionEngine)
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import the core analysis class
try:
    from main_app import MisinformationPlatform
except ImportError:
    st.error("Error: Could not import MisinformationPlatform. Check your file structure.")
    st.stop()


# --- 2. STREAMLIT CACHING (Performance Optimization) ---

@st.cache_resource
def load_platform():
    """Loads the core analysis modules only once for efficient execution."""
    try:
        # Initialize the platform. It will load all mock ML components.
        platform = MisinformationPlatform()
        return platform
    except Exception as e:
        st.error(f"Failed to load AI platform components: {e}")
        st.stop()

# --- 3. UI DEFINITION & LAYOUT ---

st.set_page_config(
    page_title="Multi-modal Misinformation Detector",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛡️ Multi-modal Misinformation Detector")
st.markdown(
    """
    Analyze a claim based on its **Source**, **Text Tone**, **Image Context**, and **Deepfake Integrity**.
    """
)

# Input fields container
with st.container(border=True):
    st.subheader("1. Enter Claim Details")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # User input for the main text
        claim_text = st.text_area(
            "Enter the Claim Text (e.g., the headline or a short excerpt):",
            "SHOCKING NEW VIDEO shows government cover-up of alien contact! MUST WATCH!",
            height=120
        )
        # User input for the source URL
        claim_url = st.text_input(
            "Enter the Source URL:",
            "http://bunkerville.com/secret-file-exposed"
        )
        
    with col2:
        st.markdown("**Upload Media (Image/Video) for CV Analysis:**")
        # --- File Uploader Widget ---
        uploaded_file = st.file_uploader(
            " ", # Label is intentionally a space to make the widget look like a button/plus icon is desired
            type=['png', 'jpg', 'jpeg', 'mp4', 'mov', 'avi'], # Accepts common image and video formats
            accept_multiple_files=False,
            # The 'help' provides a custom message resembling a 'plus' button hint
            help="Click 'Browse files' or drag-and-drop an image/video file (Max 200MB)"
        )
        
        # Display a preview of the uploaded media
        media_key = "old_news_fire_photo.jpg" # Default mock key for analysis
        
        if uploaded_file is not None:
            file_type = uploaded_file.type
            st.success(f"File uploaded: {uploaded_file.name}")
            
            # Update the analysis key to the actual uploaded file name
            media_key = uploaded_file.name 
            
            # --- MAKE PREVIEW SMALLER ---
            if 'image' in file_type:
                st.image(uploaded_file, caption='Uploaded Image Preview', width=200) # Set a fixed width
            elif 'video' in file_type:
                st.video(uploaded_file, format=file_type, start_time=0, height=150) # Set a fixed height
            
        else:
            # If no file is uploaded, show a placeholder or information about the default mock analysis
            st.info("No file uploaded. Analysis will use a **mock file** for Media Context and Deepfake checks.")
    
    # Analysis button
    if st.button("Analyze Claim", type="primary", use_container_width=True):
        
        # --- 4. EXECUTION & DISPLAY ---
        
        # Check for minimum required inputs before running
        if not claim_text or not claim_url:
            st.error("Please enter both Claim Text and a Source URL to run the analysis.")
            st.stop()
            
        # Load the platform (retrieved instantly from cache)
        platform = load_platform()
        
        with st.spinner('Running Multi-modal Analysis...'):
            # Pass the actual media_key (either uploaded file name or the mock file name)
            report = platform.run_analysis(claim_url, claim_text, media_key)
        
        final_score = report['--- FINAL VERDICT (Based on Source, Context, Tone) ---']['score']
        verdict = report['--- FINAL VERDICT (Based on Source, Context, Tone) ---']['verdict']
        
        st.subheader("2. Final Fusion Verdict")

        # Dynamic display based on the final score
        col_v, col_s = st.columns([2, 1])
        
        if final_score < 0.40:
            st.toast("Verdict: Misinformation Risk is HIGH!", icon="🚨")
            col_v.error(f"## 🚨 {verdict}")
        elif final_score < 0.60:
            st.toast("Verdict: Caution Recommended.", icon="⚠️")
            col_v.warning(f"## ⚠️ {verdict}")
        else:
            st.toast("Verdict: Credibility is High.", icon="✅")
            col_v.success(f"## ✅ {verdict}")
            
        col_s.metric(label="Fusion Credibility Score", value=f"{final_score:.4f}", help="Weighted average of all analysis components.")

        st.divider()

        # --- 5. COMPONENT BREAKDOWN DISPLAY ---

        st.subheader("3. 🔬 Component Breakdown (Raw Scores and Findings)")
        
        raw_scores = report['Raw_Scores']
        findings = report['Detailed_Findings']
        
        # Use four columns to display the four input components side-by-side
        cols_score = st.columns(4)
        
        # Source Check
        cols_score[0].metric(
            "Source Credibility", 
            f"{raw_scores['source_credibility']:.2f}",
            help="Score based on the domain's known reliability (out of 1.0)."
        )
        cols_score[0].caption(f"**Finding:** {findings['Source_Check']}")

        # Tone Check (Note: raw_scores['text_tone'] is an inverted score)
        cols_score[1].metric(
            "Text Tone Credibility", 
            f"{raw_scores['text_tone']:.2f}",
            help="Credibility based on text tone (Lower sensationalism = Higher score)."
        )
        cols_score[1].caption(f"**Finding:** {findings['Tone_Check']}")
        
        # Media Context
        cols_score[2].metric(
            "Media Context Score", 
            f"{raw_scores['image_context']:.2f}",
            help="Score from reverse image search and contextual analysis."
        )
        cols_score[2].caption(f"**Media Used:** *{media_key}*")
        cols_score[2].caption(f"**Finding:** {findings['Image_Context_Check']}")

        # Deepfake Check
        cols_score[3].metric(
            "Deepfake Authenticity", 
            f"{raw_scores['deepfake_authenticity']:.2f}",
            help="Probability of the media being authentic (not a deepfake or manipulation)."
        )
        cols_score[3].caption(f"**Finding:** {findings['Deepfake_Check']}")# app_web.py - Final Streamlit Web Interface for Misinformation Detector

import streamlit as st
import os
import sys

# --- 1. SETUP & IMPORTS ---

# Add the src directory to the path to allow importing modules (e.g., FusionEngine)
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import the core analysis class
try:
    from main_app import MisinformationPlatform
except ImportError:
    st.error("Error: Could not import MisinformationPlatform. Check your file structure.")
    st.stop()


# --- 2. STREAMLIT CACHING (Performance Optimization) ---

@st.cache_resource
def load_platform():
    """Loads the core analysis modules only once for efficient execution."""
    try:
        # Initialize the platform. It will load all mock ML components.
        platform = MisinformationPlatform()
        return platform
    except Exception as e:
        st.error(f"Failed to load AI platform components: {e}")
        st.stop()

# --- 3. UI DEFINITION & LAYOUT ---

st.set_page_config(
    page_title="Multi-modal Misinformation Detector",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛡️ Multi-modal Misinformation Detector")
st.markdown(
    """
    Analyze a claim based on its **Source**, **Text Tone**, **Image Context**, and **Deepfake Integrity**.
    """
)

# Input fields container
with st.container(border=True):
    st.subheader("1. Enter Claim Details")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # User input for the main text
        claim_text = st.text_area(
            "Enter the Claim Text (e.g., the headline or a short excerpt):",
            "SHOCKING NEW VIDEO shows government cover-up of alien contact! MUST WATCH!",
            height=120
        )
        # User input for the source URL
        claim_url = st.text_input(
            "Enter the Source URL:",
            "http://bunkerville.com/secret-file-exposed"
        )
        
    with col2:
        st.markdown("**Upload Media (Image/Video) for CV Analysis:**")
        # --- File Uploader Widget ---
        uploaded_file = st.file_uploader(
            " ", # Label is intentionally a space to make the widget look like a button/plus icon is desired
            type=['png', 'jpg', 'jpeg', 'mp4', 'mov', 'avi'], # Accepts common image and video formats
            accept_multiple_files=False,
            # The 'help' provides a custom message resembling a 'plus' button hint
            help="Click 'Browse files' or drag-and-drop an image/video file (Max 200MB)"
        )
        
        # Display a preview of the uploaded media
        media_key = "old_news_fire_photo.jpg" # Default mock key for analysis
        
        if uploaded_file is not None:
            file_type = uploaded_file.type
            st.success(f"File uploaded: {uploaded_file.name}")
            
            # Update the analysis key to the actual uploaded file name
            media_key = uploaded_file.name 
            
            # --- MAKE PREVIEW SMALLER ---
            if 'image' in file_type:
                st.image(uploaded_file, caption='Uploaded Image Preview', width=200) # Set a fixed width
            elif 'video' in file_type:
                st.video(uploaded_file, format=file_type, start_time=0, height=150) # Set a fixed height
            
        else:
            # If no file is uploaded, show a placeholder or information about the default mock analysis
            st.info("No file uploaded. Analysis will use a **mock file** for Media Context and Deepfake checks.")
    
    # Analysis button
    if st.button("Analyze Claim", type="primary", use_container_width=True):
        
        # --- 4. EXECUTION & DISPLAY ---
        
        # Check for minimum required inputs before running
        if not claim_text or not claim_url:
            st.error("Please enter both Claim Text and a Source URL to run the analysis.")
            st.stop()
            
        # Load the platform (retrieved instantly from cache)
        platform = load_platform()
        
        with st.spinner('Running Multi-modal Analysis...'):
            # Pass the actual media_key (either uploaded file name or the mock file name)
            report = platform.run_analysis(claim_url, claim_text, media_key)
        
        final_score = report['--- FINAL VERDICT (Based on Source, Context, Tone) ---']['score']
        verdict = report['--- FINAL VERDICT (Based on Source, Context, Tone) ---']['verdict']
        
        st.subheader("2. Final Fusion Verdict")

        # Dynamic display based on the final score
        col_v, col_s = st.columns([2, 1])
        
        if final_score < 0.40:
            st.toast("Verdict: Misinformation Risk is HIGH!", icon="🚨")
            col_v.error(f"## 🚨 {verdict}")
        elif final_score < 0.60:
            st.toast("Verdict: Caution Recommended.", icon="⚠️")
            col_v.warning(f"## ⚠️ {verdict}")
        else:
            st.toast("Verdict: Credibility is High.", icon="✅")
            col_v.success(f"## ✅ {verdict}")
            
        col_s.metric(label="Fusion Credibility Score", value=f"{final_score:.4f}", help="Weighted average of all analysis components.")

        st.divider()

        # --- 5. COMPONENT BREAKDOWN DISPLAY ---

        st.subheader("3. 🔬 Component Breakdown (Raw Scores and Findings)")
        
        raw_scores = report['Raw_Scores']
        findings = report['Detailed_Findings']
        
        # Use four columns to display the four input components side-by-side
        cols_score = st.columns(4)
        
        # Source Check
        cols_score[0].metric(
            "Source Credibility", 
            f"{raw_scores['source_credibility']:.2f}",
            help="Score based on the domain's known reliability (out of 1.0)."
        )
        cols_score[0].caption(f"**Finding:** {findings['Source_Check']}")

        # Tone Check (Note: raw_scores['text_tone'] is an inverted score)
        cols_score[1].metric(
            "Text Tone Credibility", 
            f"{raw_scores['text_tone']:.2f}",
            help="Credibility based on text tone (Lower sensationalism = Higher score)."
        )
        cols_score[1].caption(f"**Finding:** {findings['Tone_Check']}")
        
        # Media Context
        cols_score[2].metric(
            "Media Context Score", 
            f"{raw_scores['image_context']:.2f}",
            help="Score from reverse image search and contextual analysis."
        )
        cols_score[2].caption(f"**Media Used:** *{media_key}*")
        cols_score[2].caption(f"**Finding:** {findings['Image_Context_Check']}")

        # Deepfake Check
        cols_score[3].metric(
            "Deepfake Authenticity", 
            f"{raw_scores['deepfake_authenticity']:.2f}",
            help="Probability of the media being authentic (not a deepfake or manipulation)."
        )
        cols_score[3].caption(f"**Finding:** {findings['Deepfake_Check']}")
