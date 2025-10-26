# src/nlp_module/source_checker.py

import json
import os
from typing import Tuple, Dict, Any
from urllib.parse import urlparse

try:
    # This requires 'pip install pysafebrowsing'
    from pysafebrowsing import SafeBrowsing
except ImportError:
    print("WARNING: pysafebrowsing not installed. Safe Browsing checks will be skipped.")
    SafeBrowsing = None

class SourceChecker:
    """
    Checks the credibility of the source URL using two methods:
    1. A local credibility database (for known bias).
    2. Google Safe Browsing API (for malware/phishing).
    """
    def __init__(self):
        self.db = {}
        self.db_path = os.path.join(os.path.dirname(__file__), '../../data/credibility_db.json')
        self._load_credibility_db()
        self.sb_key = os.environ.get("SAFEBROWSING_API_KEY")
        
        if self.sb_key and SafeBrowsing:
            self.sb = SafeBrowsing(self.sb_key)
            print("SourceChecker: Google Safe Browsing API loaded.")
        else:
            self.sb = None
            print("SourceChecker: Safe Browsing API KEY missing or library not available. Using DB only.")


    def _load_credibility_db(self):
        """Loads known domain scores from the local JSON file."""
        try:
            with open(self.db_path, 'r') as f:
                self.db = json.load(f)
            print(f"Source Checker loaded {len(self.db)} domains from DB.")
        except json.JSONDecodeError:
            print(f"ERROR: Could not decode JSON from {self.db_path}")
        except FileNotFoundError:
            print(f"ERROR: Credibility DB file not found at {self.db_path}")

    
    def get_credibility_score(self, url: str) -> Tuple[float, str]:
        """
        Calculates a source credibility score (1.0 = highly credible).
        
        Returns: A tuple (score, reason_string)
        """
        # Default scores
        base_score = 0.5 
        reason = "Source check performed."

        # 1. Check local credibility database
        try:
            netloc = urlparse(url).netloc.lstrip('www.')
        except ValueError:
            return 0.1, "Error: Invalid URL format."
        
        if netloc in self.db:
            db_entry = self.db[netloc]
            # Use the score from the DB, and update the reason
            base_score = db_entry.get('score', base_score)
            reason = f"Domain found in DB. Score: {base_score:.2f}. Reason: {db_entry.get('reason', 'N/A')}"
        
        # 2. Check Google Safe Browsing API for immediate threats
        if self.sb:
            try:
                # Check the URL against Google's threat lists
                response = self.sb.lookup_urls([url])
                
                if response:
                    threats = response.get(url, [])
                    if threats:
                        # If a threat is found, drop the score significantly
                        threat_type = threats[0].get('threatType', 'Unknown Threat')
                        base_score = min(base_score, 0.1) 
                        reason = f"DANGER! Google Safe Browsing flagged URL as: {threat_type}. Credibility set to 0.1."
                    else:
                        reason += " Google Safe Browsing found no immediate threats."
                
            except Exception as e:
                # Log the API error but don't crash the app. Fall back to DB score.
                print(f"SourceChecker API Error: {e}. Falling back to DB score.")
        
        # Final safety check: if the score is still default (0.5) and not in DB, 
        # let's assume unknown/low-traffic sites are neutral.
        
        # NOTE: We return a TUPLE (score, reason) to be compatible with main_app.py's
        # fix: source_analysis[0] and source_analysis[1].
        return base_score, reason

# You will need to make sure your credibility_db.json is a valid JSON file!