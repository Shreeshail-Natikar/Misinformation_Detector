# src/fusion_module/fusion_logic.py

from typing import Dict, Any

class FusionEngine:
    """
    Combines credibility scores from multiple modules using a weighted average.
    All scores should be normalized (0.0 to 1.0).
    """
    def __init__(self):
        # Adjusted weights for FOUR inputs (Source, Image Context, Tone, Deepfake)
        # Total weights must sum to 1.0 (or 100%)
        self.WEIGHTS = {
            "source_credibility": 0.35,          # High weight for journalistic reputation
            "image_context": 0.25,               # Medium weight for image relevance
            "text_tone": 0.20,                   # Medium weight for sensationalism
            "deepfake_authenticity": 0.20        # Medium weight for media integrity (NEW)
        }
        print("Fusion Engine initialized. Weights are balanced for 4 inputs.")

    def calculate_final_score(self, scores: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculates the final weighted score and determines the verdict.
        """
        total_score = 0
        total_weight = 0

        # Calculate the weighted score
        for key, score in scores.items():
            if key in self.WEIGHTS:
                weight = self.WEIGHTS[key]
                total_score += score * weight
                total_weight += weight
        
        # Ensure weights sum to 1 (should be 1.0 if all expected keys are present)
        if total_weight == 0:
            final_score = 0.5
        else:
            final_score = total_score / total_weight

        # Determine the verdict based on thresholds
        if final_score >= 0.80:
            verdict = "Highly Credible (TRUE)"
        elif final_score >= 0.60:
            verdict = "Medium Credibility (Watchful)"
        elif final_score >= 0.40:
            verdict = "Low Credibility (Suspect)"
        else:
            verdict = "High Probability of MISINFORMATION (FALSE)"
            
        return {
            "score": final_score,
            "verdict": verdict
        }