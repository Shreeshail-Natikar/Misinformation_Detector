# src/cv_module/deepfake_detector.py

import os
import random
from typing import Dict, Any

class DeepfakeDetector:
    """
    Analyzes media files for signs of deepfake manipulation.
    Currently uses mock logic based on filename patterns.
    """
    def __init__(self):
        print("CV: Deepfake Detector initialized (mock mode).")

    def analyze_manipulation(self, file_path: str) -> Dict[str, Any]:
        """
        Analyzes the file for signs of synthetic manipulation (deepfake).
        Returns a score (0.0 = Likely Deepfake, 1.0 = Authentic).
        """
        
        # --- IMPROVED MOCK LOGIC ---
        file_name = os.path.basename(file_path).lower()
        
        # Scenario 1: Highly Manipulated (Low Score)
        if 'manipulated' in file_name or 'deepfake' in file_name or 'shocking' in file_name:
            score = random.uniform(0.1, 0.3) 
            reason = "High probability of deepfake/synthetic manipulation based on visual artifacts."
            
        # Scenario 2: Highly Authentic (High Score)
        elif 'clean' in file_name or 'official' in file_name or 'rbi' in file_name:
            score = random.uniform(0.9, 0.98) 
            reason = "High probability of authenticity (no manipulation detected)."
            
        # Scenario 3: Default/Inconclusive
        else:
            score = random.uniform(0.65, 0.75) 
            reason = "Manipulation status is inconclusive; proceeding with standard score."
            
        return {
            "score": score,
            "verdict": reason,
            "details": f"Mock analysis of {file_name}"
        }