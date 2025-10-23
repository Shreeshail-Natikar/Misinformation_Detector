import os
import random
from typing import Dict, Any

class ReverseSearcher:
    """
    Simulates a Reverse Image Search to perform contextual verification.
    This component checks if an image is being used out of context 
    by comparing its alleged context (input_claim) with known historical 
    contexts (simulated_search_results).
    """
    
    # 🎯 Contextual Mismatch Keywords
    # If the simulated search finds dates/locations that contradict the claim, 
    # the score will be lower.
    CONTEXTUAL_KEYWORDS = {
        'flood_2010': '2010',
        '2024_election': '2020',
        'new_york_fire': 'chicago',
        'current_protest': '2022_archive'
    }

    def __init__(self):
        print("Reverse Search module initialized for contextual verification.")

    def simulate_search(self, image_path: str) -> Dict[str, Any]:
        """
        Simulates the results of a reverse image search based on the input image.
        In a real project, this would involve API calls or perceptual hashing.
        """
        
        # We use a simple hash of the file name (or just random choice) to simulate results
        # A more complex name simulates an older, oft-used image.
        is_reused = "old_news" in image_path.lower() or random.random() < 0.6
        
        results = {
            "image_id": os.path.basename(image_path),
            "is_reused_image": is_reused,
            "found_contexts": []
        }
        
        if is_reused:
            # Simulate finding the image in old or incorrect contexts
            results["found_contexts"] = [
                {"date": "June 2018", "source": "Old Newspaper Archive"},
                {"date": "May 2021", "source": "Foreign News Blog"},
                {"date": "May 2024", "source": "Current Claim Source"} # Included for comparison
            ]
        
        return results

    def verify_context(self, image_path: str, input_claim: str) -> Dict[str, Any]:
        """
        Compares the simulated search results with the current claim context.
        """
        search_results = self.simulate_search(image_path)
        
        final_score = 1.0  # Start high, lower if contradictions found
        reason = "Image context appears consistent with the claim."

        if search_results["is_reused_image"]:
            # Image is known to be reused, now check for contextual mismatch
            final_score -= 0.3 # Initial penalty for being a reused image
            
            # Check for strong contextual mismatch signals (e.g., conflicting dates/locations)
            
            # Simple simulation: If the image is reused and the claim mentions '2024', 
            # but the search finds contexts from '2018', there's a problem.
            
            if '2024' in input_claim and any('2018' in ctx['date'] for ctx in search_results["found_contexts"]):
                final_score -= 0.5
                reason = "Image is frequently reused and context history (2018) **strongly contradicts** the current claim (2024)."
            
            elif len(search_results["found_contexts"]) > 2:
                final_score -= 0.1
                reason = "Image is often reused. Contextual check suggests caution, but no direct contradiction found."
        
        # Ensure the score remains between 0.0 and 1.0
        final_score = max(0.0, min(1.0, final_score))

        return {
            "score": final_score,
            "is_reused": search_results["is_reused_image"],
            "reason": reason,
            "details": search_results["found_contexts"]
        }


# --- Example Usage ---
if __name__ == "__main__":
    searcher = ReverseSearcher()

    # Example 1: Old image used for a new, misleading claim
    image_1 = "old_news_fire_photo.jpg"
    claim_1 = "BREAKING: Massive fire sweeps through city center today, 2024!"

    # Example 2: New image, not widely reused (Simulated legitimate context)
    image_2 = "recent_weather_report.png"
    claim_2 = "Heavy rainfall predicted for tomorrow morning."

    print("\n--- Analyzing Image 1 (Reused/Out of Context) ---")
    analysis_1 = searcher.verify_context(image_1, claim_1)
    print(f"Image File: {image_1}")
    print(f"Claim: {claim_1[:40]}...")
    print(f"Contextual Score: {analysis_1['score']:.2f}")
    print(f"Verdict: {analysis_1['reason']}")

    print("\n--- Analyzing Image 2 (New/Consistent Context) ---")
    analysis_2 = searcher.verify_context(image_2, claim_2)
    print(f"Image File: {image_2}")
    print(f"Claim: {claim_2}")
    print(f"Contextual Score: {analysis_2['score']:.2f}")
    print(f"Verdict: {analysis_2['reason']}")