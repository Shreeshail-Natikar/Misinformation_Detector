# src/nlp_module/tone_analyzer.py

from typing import Dict, Any
# 1. Import the necessary VADER components
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class TextAnalyzer:
    """
    Analyzes the tone and emotional charge of the text to detect sensationalism.
    Uses VADER (Valence Aware Dictionary and sEntiment Reasoner) for rapid sentiment analysis.
    """
    def __init__(self):
        # 2. Initialize the VADER analyzer
        self.analyzer = SentimentIntensityAnalyzer()
        print("NLP: Tone Analyzer initialized (using VADER).")

    def analyze_tone(self, text: str) -> Dict[str, Any]:
        """
        Calculates the sensationalism score.
        A score of 1.0 means high sensationalism (often negative or urgent) -> Low Credibility.
        A score of 0.0 means neutral/objective tone -> High Credibility.
        
        The result dict returns the sensationalism score. The main app (main_app.py) 
        will calculate the credibility score as: 1.0 - sensationalism_score.
        """
        
        # 3. Get the sentiment scores
        vs = self.analyzer.polarity_scores(text)
        
        # VADER's compound score is normalized between -1 (Extreme Negative) and +1 (Extreme Positive).
        compound_score = vs['compound']
        
        # We define a simple sensationalism metric based on how far the score is from 0 (Neutral).
        # We use the absolute value: abs(-0.8) = 0.8, abs(0.8) = 0.8.
        # This means highly positive AND highly negative text is considered sensational.
        sensationalism_score = abs(compound_score)
        
        # Map the sensationalism score to a detailed finding
        if sensationalism_score > 0.8:
            reason = "Tone is EXTREMELY HIGHLY POLARIZED. This often suggests sensationalism or strong bias."
        elif sensationalism_score > 0.5:
            reason = "Tone is strongly opinionated (polarized). Caution advised regarding emotional appeals."
        elif sensationalism_score > 0.2:
            reason = "Tone shows mild polarity, but remains largely objective."
        else:
            reason = "Tone is highly NEUTRAL and OBJECTIVE. No significant sensationalism detected."

        return {
            # This is the sensationalism score (1.0 = highly sensational/polarised)
            "score": sensationalism_score, 
            "reason": reason,
            "raw_vader_scores": vs # Include raw scores for debugging
        }

# Example execution for testing (optional)
if __name__ == "__main__":
    analyzer = TextAnalyzer()
    
    claim_1 = "SHOCKING NEW VIDEO shows government cover-up of alien contact! MUST WATCH!"
    report_1 = analyzer.analyze_tone(claim_1)
    print(f"\nClaim 1: '{claim_1}'")
    print(f"Sensationalism Score: {report_1['score']:.4f}")
    print(f"Finding: {report_1['reason']}")
    
    claim_2 = "The committee released its quarterly economic report, noting a 3% growth in regional consumer spending."
    report_2 = analyzer.analyze_tone(claim_2)
    print(f"\nClaim 2: '{claim_2}'")
    print(f"Sensationalism Score: {report_2['score']:.4f}")
    print(f"Finding: {report_2['reason']}")