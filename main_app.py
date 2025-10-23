# main_app.py

import os
import sys
from typing import Dict, Any

# Add the src directory to the path to allow importing modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# 1. Import all core analysis modules
try:
    from nlp_module.tone_analyzer import TextAnalyzer
    from nlp_module.source_checker import SourceChecker
    from cv_module.reverse_search import ReverseSearcher
    from cv_module.deepfake_detector import DeepfakeDetector  # <-- NEW
    from fusion_module.fusion_logic import FusionEngine
except ImportError as e:
    print(f"ERROR: Could not import necessary modules. Check your file structure and run 'pip install -r requirements.txt'.")
    print(f"Details: {e}")
    sys.exit(1)


class MisinformationPlatform:
    """
    The central platform that orchestrates the multi-modal analysis pipeline.
    """
    def __init__(self):
        print("--- Initializing Multi-modal AI Platform ---")
        self.text_analyzer = TextAnalyzer()
        self.source_checker = SourceChecker()
        self.reverse_searcher = ReverseSearcher()
        self.deepfake_detector = DeepfakeDetector() # <-- NEW
        self.fusion_engine = FusionEngine()
        print("All core analysis engines loaded and ready.")

    def run_analysis(self, claim_url: str, claim_text: str, image_file_mock: str) -> Dict[str, Any]:
        """
        Runs the full analysis pipeline on a given claim.
        """
        
        # --- PHASE 1: Text Analysis ---
        print("\n[PHASE 1] Starting Text (NLP) Analysis...")
        
        # Tone/Sensationalism Check
        tone_analysis = self.text_analyzer.analyze_tone(claim_text)
        # The Tone Analyzer returns a score (0 to 1) for sensationalism. 
        # We invert this for fusion: (1 - score) = Credibility Score.
        tone_credibility_score = 1.0 - tone_analysis['score'] 
        
        # Source Credibility Check
        source_analysis = self.source_checker.get_credibility_score(claim_url)
        
        # --- PHASE 2: Computer Vision (CV) Analysis ---
        print("[PHASE 2] Starting Computer Vision (CV) Analysis...")
        
        # Contextual Verification (Reverse Search)
        image_context_analysis = self.reverse_searcher.verify_context(image_file_mock, claim_text)

        # Deepfake/Manipulation Check
        deepfake_analysis = self.deepfake_detector.analyze_manipulation(image_file_mock)
        
        # --- PHASE 3: Multi-modal Fusion ---
        print("[PHASE 3] Starting Fusion Engine...")
        
        # Collect all credibility scores (1.0 = High Credibility/Authenticity)
        raw_scores = {
            "source_credibility": source_analysis['score'],
            "image_context": image_context_analysis['score'],
            "text_tone": tone_credibility_score,  # Uses the inverted score (High Credibility = Low Sensationalism)
            # NOTE: Deepfake score needs to be integrated into the FusionEngine's weights to be fully used.
            # For this demo, we'll include it in the report, but use the original 3-score weights.
            "deepfake_authenticity": deepfake_analysis['score'] 
        }
        
        # **IMPORTANT:** If you want to include deepfake, you must update the WEIGHTS in fusion_logic.py
        # For now, we use the original 3 scores for the final Fusion Score calculation.
        fusion_input_scores = {k: v for k, v in raw_scores.items() if k in self.fusion_engine.WEIGHTS}
        final_report = self.fusion_engine.calculate_final_score(fusion_input_scores)
        
        # --- PHASE 4: Final Report Compilation ---
        full_report = {
            "Input_Claim": claim_text,
            "Input_Source": claim_url,
            "--- FINAL VERDICT (Based on Source, Context, Tone) ---": final_report,
            "Raw_Scores": raw_scores,
            "Detailed_Findings": {
                "Source_Check": source_analysis['reason'],
                "Tone_Check": tone_analysis['reason'],
                "Image_Context_Check": image_context_analysis['reason'],
                "Deepfake_Check": deepfake_analysis['verdict'] # New detail
            }
        }
        
        return full_report


# --- Example Execution (The Demonstration) ---
if __name__ == "__main__":
    platform = MisinformationPlatform()

    # 1. SCENARIO 1: High Probability of MISINFORMATION (All red flags)
    misleading_url = "http://bunkerville.com/secret-file-exposed"
    misleading_text = "SHOCKING NEW VIDEO shows government cover-up of alien contact! They are lying to us! MUST WATCH!"
    misleading_image = "old_news_fire_photo.jpg" # Mocks a reused/low-quality image

    print("\n========================================================")
    print("ANALYSIS SCENARIO 1: High Misinformation Risk (LOW CREDIBILITY)")
    print("========================================================")
    report_1 = platform.run_analysis(misleading_url, misleading_text, misleading_image)
    
    # Print the final summary
    print("\n--- FINAL MISINFORMATION REPORT ---")
    print(f"Verdict: {report_1['--- FINAL VERDICT (Based on Source, Context, Tone) ---']['verdict']}")
    print(f"Fusion Score: {report_1['--- FINAL VERDICT (Based on Source, Context, Tone) ---']['score']:.4f}")
    print("\n--- Detailed Findings ---")
    for key, value in report_1['Detailed_Findings'].items():
        print(f"{key}: {value}")

    print("\n\n========================================================")
    print("ANALYSIS SCENARIO 2: High Credibility Risk (TRUE NEWS)")
    print("========================================================")
    
    # 2. SCENARIO 2: High Probability of CREDIBILITY (Legitimate News)
    credible_url = "https://www.reuters.com/latest-market-update-report"
    credible_text = "The Federal Reserve released its quarterly economic report, noting a 3% growth in regional consumer spending."
    credible_image = "official_video_clean_shot.mp4" # Mocks a high-quality, official image

    report_2 = platform.run_analysis(credible_url, credible_text, credible_image)

    # Print the final summary
    print("\n--- FINAL MISINFORMATION REPORT ---")
    print(f"Verdict: {report_2['--- FINAL VERDICT (Based on Source, Context, Tone) ---']['verdict']}")
    print(f"Fusion Score: {report_2['--- FINAL VERDICT (Based on Source, Context, Tone) ---']['score']:.4f}")
    print("\n--- Detailed Findings ---")
    for key, value in report_2['Detailed_Findings'].items():
        print(f"{key}: {value}")