# src/cv_module/reverse_search.py

from typing import Dict, Any
import os
from PIL import Image

# Import the necessary Hugging Face components
try:
    from transformers import BlipProcessor, BlipForQuestionAnswering
    import torch
    
    # We will set the target device inside the __init__ for more control
    
except ImportError:
    print("CV: BLIP model dependencies (transformers/torch) are missing. Using mock scores.")
    BlipProcessor = None

class ReverseSearcher:
    """
    Analyzes the context of an uploaded image/video (simulated) by generating a caption
    using the BLIP VQA model and checking its relevance to the text claim.
    """
    def __init__(self):
        self.processor = None
        self.model = None
        
        if BlipProcessor:
            try:
                # FIX: Explicitly set device to CPU for stability during initialization
                DEVICE = "cpu"
                model_name = "Salesforce/blip-vqa-base"
                self.processor = BlipProcessor.from_pretrained(model_name)
                # FIX: Load the model and ensure it's on the chosen device
                self.model = BlipForQuestionAnswering.from_pretrained(model_name).to(DEVICE)
                print(f"CV: BLIP VQA model successfully loaded on {DEVICE}.")
            except Exception as e:
                # This error catches download or memory issues
                print(f"CV: ERROR loading BLIP model: {e}. Falling back to mock scores.")

    def _calculate_mismatch_score(self, claim_text: str, ai_caption: str) -> float:
        """
        Calculates a simple score based on the perceived mismatch between the claim and the caption.
        In a real hackathon setting, this would be a full semantic similarity check.
        """
        # A very basic check: does the claim contain strong positive/negative words 
        # that are NOT present in the neutral AI caption?
        claim_words = set(claim_text.lower().split())
        caption_words = set(ai_caption.lower().split())
        
        # Keywords suggesting sensationalism/emotion often used in misinformation
        sensational_keywords = {"shocking", "cover-up", "secret", "exposed", "truth", "must"}
        
        # Find sensational words in the claim that are NOT in the AI's neutral description
        unsupported_sensationalism = claim_words.intersection(sensational_keywords) - caption_words
        
        # The logic: High unsupported sensationalism -> Low score (High mismatch)
        if len(unsupported_sensationalism) >= 2:
            return 0.2  # High Mismatch/Low Credibility
        elif len(unsupported_sensationalism) == 1:
            return 0.5  # Moderate Mismatch
        else:
            return 0.85 # Low Mismatch/High Credibility

    def verify_context(self, media_key: str, claim_text: str) -> Dict[str, Any]:
        """
        Analyzes the image context.
        """
        score = 0.5
        reason = "Media context analysis performed."
        ai_caption = "N/A"
        
        # Define a mock path where the app expects to find placeholder images
        mock_image_path = os.path.join(os.path.dirname(__file__), '../../data/images', media_key)

        # Re-check device here for the execution step (must use the device set in __init__)
        device_used = self.model.device if self.model else "cpu"

        if self.processor and self.model:
            try:
                if not os.path.exists(mock_image_path):
                    reason = f"Image file '{media_key}' not found at mock path. Cannot run VQA. Using default score."
                    return {"score": score, "reason": reason}
                    
                raw_image = Image.open(mock_image_path).convert('RGB')
                
                # Use BLIP to generate a descriptive caption
                question = "describe the main content of the image in a concise sentence"
                
                # Ensure inputs tensor is moved to the correct device
                inputs = self.processor(raw_image, question, return_tensors="pt").to(device_used)
                out = self.model.generate(**inputs, max_length=20) # Max 20 words for conciseness
                ai_caption = self.processor.decode(out[0], skip_special_tokens=True)
                
                # Calculate the score based on mismatch
                score = self._calculate_mismatch_score(claim_text, ai_caption)

                if score < 0.5:
                    reason = f"VQA found high content mismatch. AI Caption: '{ai_caption}'."
                elif score < 0.8:
                    reason = f"VQA found moderate mismatch. AI Caption: '{ai_caption}'."
                else:
                    reason = f"VQA content appears relevant. AI Caption: '{ai_caption}'."
                    
            except Exception as e:
                # Catch any runtime issues during model execution
                reason = f"VQA Model Runtime Error: {e}. Using default score."
        
        else:
            reason = f"VQA Model not loaded or dependencies missing. Using mock score."

        return {
            "score": score,
            "reason": reason
        }

# Example execution block (optional for testing)
if __name__ == "__main__":
    # Create a mock image file for testing the logic
    # You MUST have a dummy file at this path for the test below to work:
    # data/images/test_image.jpg (or similar)
    if not os.path.exists('../../data/images/test_image.jpg'):
        print("\nNOTE: Please create a dummy image at 'data/images/test_image.jpg' to run the test.")
    
    analyzer = ReverseSearcher()
    
    # SCENARIO 1: High Mismatch (Image of a cat, but claim is about a government secret)
    claim_1 = "SHOCKING NEW VIDEO shows government cover-up of alien contact! MUST WATCH!"
    report_1 = analyzer.verify_context("test_image.jpg", claim_1)
    print(f"\nClaim 1: '{claim_1}'")
    print(f"Context Score: {report_1['score']:.4f}")
    print(f"Finding: {report_1['reason']}")