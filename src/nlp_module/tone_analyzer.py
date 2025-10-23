# src/nlp_module/tone_analyzer.py

import re
import random
from typing import Dict, Any

class TextAnalyzer:
    """
    Handles text preprocessing and tone/sensationalism analysis.
    In a real system, this would use a pre-trained sentiment or clickbait NLP model.
    """
    def __init__(self):
        # Simulate loading a large NLP model
        print("NLP: Tone Analyzer initialized (using mock model).")
        
        # Keywords that indicate highly emotional/sensational language
        self.sensational_keywords = [
            'BREAKING', 'SHOCKING', 'BELIEVE', 'SECRET', 'WARNING', 'HIDDEN', 'MUST WATCH'
        ]

    def preprocess_text(self, text: str) -> str:
        """
        Cleans the input text for analysis.
        """
        # Remove URLs, special chars, etc. (Simplified)
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(' +', ' ', text).strip()
        return text

    def analyze_tone(self, claim: str) -> Dict[str, Any]:
        """
        Analyzes the tone (sentiment/emotion/sensationalism) of a text claim.
        Returns a score (1.0 for high emotion/sensationalism, 0.0 for low) 
        and a 'label' (POSITIVE, NEGATIVE, or NEUTRAL).
        """
        cleaned_text = self.preprocess_text(claim)
        
        if not cleaned_text:
            return {"label": "N/A", "score": 0.5, "reason": "Empty text after cleaning."}
        
        # --- MOCK LOGIC ---
        # 1. Check for sensational keywords (strong indicator)
        sensational_count = sum(1 for keyword in self.sensational_keywords if keyword in cleaned_text.upper())
        sensational_score = min(1.0, sensational_count * 0.25)
        
        # 2. Estimate sentiment (Mock: based on capital letters and exclamation marks)
        caps_ratio = sum(1 for c in cleaned_text if c.isupper()) / len(cleaned_text) if len(cleaned_text) > 0 else 0
        excl_count = claim.count('!')
        
        # Score where higher is more emotional/sensational (misinformation proxy)
        emotional_score = (sensational_score * 0.5) + (caps_ratio * 0.3) + (min(3, excl_count) * 0.1)
        emotional_score = max(0.0, min(1.0, emotional_score))
        
        # Determine label for display
        if emotional_score > 0.7:
            label = "HIGHLY EMOTIONAL/SENSATIONAL"
        elif emotional_score > 0.4:
            label = "MODERATE EMOTION"
        else:
            label = "NEUTRAL/OBJECTIVE"
            
        # The score returned is the probability of the text being HIGHLY sensational (1.0 = highly sensational)
        return {
            "label": label,
            "score": emotional_score, 
            "reason": f"Text exhibits {label} tone (Sensationalism Score: {emotional_score:.2f})."
        }

# --- Example Usage (Optional, but good for testing) ---
if __name__ == "__main__":
    analyzer = TextAnalyzer()
    
    claim_1 = "BREAKING! You won't BELIEVE what they are hiding from you! WATCH NOW!"
    claim_2 = "The local government released a report detailing budget adjustments for the next fiscal quarter."

    print(analyzer.analyze_tone(claim_1))
    print(analyzer.analyze_tone(claim_2))