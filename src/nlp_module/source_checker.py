# src/nlp_module/source_checker.py

import re
import json
import os
from urllib.parse import urlparse
from typing import Dict, Any

class SourceChecker:
    """
    Handles extraction of the source domain from a URL and checks 
    its credibility against a database loaded from a JSON file.
    """
    
    # Define the path to the JSON database file
    DB_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'credibility_db.json')
    
    def __init__(self):
        self.credibility_db = self._load_credibility_db()
        print(f"Source Checker loaded {len(self.credibility_db)} domains from DB.")

    def _load_credibility_db(self) -> Dict[str, float]:
        """
        Loads the credibility scores from the external JSON file.
        """
        try:
            with open(self.DB_FILE_PATH, 'r') as f:
                # The JSON should map domain names to a credibility score (0.0 to 1.0)
                return json.load(f)
        except FileNotFoundError:
            print(f"WARNING: Credibility database not found at {self.DB_FILE_PATH}")
            # Return a small default database if the file is missing
            return {
                'nytimes.com': 1.0,
                'reuters.com': 1.0,
                'fake-news-alert.net': 0.0,
                'low-info-blog.com': 0.2
            }
        except json.JSONDecodeError:
            print(f"ERROR: Could not decode JSON from {self.DB_FILE_PATH}")
            return {}

    def extract_domain(self, url: str) -> str:
        """
        Extracts the root domain (e.g., 'example.com') from a full URL.
        """
        try:
            # 1. Parse the URL
            parsed_url = urlparse(url)
            netloc = parsed_url.netloc
            
            # 2. Remove 'www.' prefix
            if netloc.startswith('www.'):
                netloc = netloc[4:]
            
            # 3. Remove port number if present
            if ':' in netloc:
                netloc = netloc.split(':')[0]
                
            return netloc.lower()
        
        except Exception:
            # Return an empty string if the URL is invalid
            return ""

    def get_credibility_score(self, url: str) -> Dict[str, Any]:
        """
        Analyzes the source credibility based on the URL against the loaded database.
        """
        domain = self.extract_domain(url)
        
        # Default score for unknown domains
        DEFAULT_SCORE = 0.5 

        if not domain:
            return {
                "score": DEFAULT_SCORE,
                "reason": "Invalid or missing URL/Domain. Credibility check skipped.",
                "domain": "N/A"
            }

        # Look up the score, use DEFAULT_SCORE (0.5) if unknown
        score = self.credibility_db.get(domain, DEFAULT_SCORE)
        
        reason = ""
        if score == 1.0:
            reason = f"Source '{domain}' is HIGHLY RELIABLE (Verified Fact-Checker/Major News)."
        elif score >= 0.7:
            reason = f"Source '{domain}' is Generally Reliable (Medium Risk)."
        elif score <= 0.2:
            reason = f"Source '{domain}' is LOW CREDIBILITY/KNOWN MISINFORMATION SPREADER."
        else:
            reason = f"Source '{domain}' is Unknown/Neutral. Further content analysis is crucial."
            
        return {
            "score": score,
            "domain": domain,
            "reason": reason
        }

# --- Example Usage ---
if __name__ == "__main__":
    
    # --- STEP 0: Create the mock JSON file for testing ---
    # In your project, you should place this content into data/credibility_db.json
    mock_db_content = {
        'bbc.com': 1.0,
        'thehindu.com': 0.9,
        'cnnfakenews.org': 0.1,
        'bunkerville.com': 0.2,
        'localreporter.co.in': 0.6
    }
    
    # Ensure the 'data' directory exists for this test to run successfully
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    try:
        with open(SourceChecker.DB_FILE_PATH, 'w') as f:
            json.dump(mock_db_content, f, indent=4)
        print("Mock database created successfully for testing.")
    except Exception as e:
        print(f"Could not create mock DB file for testing: {e}")
        
    # --- STEP 1: Run the Checker ---
    checker = SourceChecker()

    url_reliable = "https://www.bbc.com/news/world/india-elections"
    url_low_cred = "http://cnnfakenews.org:8080/shocker-aliens-found-today"
    url_unknown = "https://new-startup-blog.io/article"

    print("\n--- Analyzing Reliable Source ---")
    analysis_1 = checker.get_credibility_score(url_reliable)
    print(f"Score: {analysis_1['score']:.2f} | Hint: {analysis_1['reason']}")

    print("\n--- Analyzing Low Credibility Source ---")
    analysis_2 = checker.get_credibility_score(url_low_cred)
    print(f"Score: {analysis_2['score']:.2f} | Hint: {analysis_2['reason']}")

    print("\n--- Analyzing Unknown Source ---")
    analysis_3 = checker.get_credibility_score(url_unknown)
    print(f"Score: {analysis_3['score']:.2f} | Hint: {analysis_3['reason']}")