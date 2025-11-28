"""
Evidence Scoring Module
Scores search results for claim verification.
"""

import re
from typing import List, Dict


# Keywords that indicate debunking or contradiction
CONTRADICTION_KEYWORDS = [
    "false", "fake", "hoax", "debunked", "myth", "misleading",
    "misinformation", "disinformation", "untrue", "incorrect",
    "fabricated", "bogus", "conspiracy", "rumor", "unverified"
]


def score_evidence(claim: str, results: List[Dict[str, str]]) -> Dict[str, int]:
    """
    Score search results based on claim verification.
    
    Args:
        claim: Original claim text
        results: List of search results with title and snippet
        
    Returns:
        Dictionary with match, contradiction, and total counts
        Format: {"matches": int, "contradictions": int, "total": int}
    """
    if not results:
        return {
            "matches": 0,
            "contradictions": 0,
            "total": 0
        }
    
    # Extract keywords from claim
    claim_keywords = extract_keywords(claim)
    
    match_count = 0
    contradiction_count = 0
    
    for result in results:
        title = result.get("title", "").lower()
        snippet = result.get("snippet", "").lower()
        combined = f"{title} {snippet}"
        
        # Check for matches
        if has_keyword_match(combined, claim_keywords):
            match_count += 1
        
        # Check for contradictions
        if has_contradiction(combined):
            contradiction_count += 1
    
    return {
        "matches": match_count,
        "contradictions": contradiction_count,
        "total": len(results)
    }


def extract_keywords(text: str) -> List[str]:
    """
    Extract meaningful keywords from text.
    
    Args:
        text: Input text
        
    Returns:
        List of keywords
    """
    if not text:
        return []
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Split into words
    words = text.split()
    
    # Filter out common stop words
    stop_words = {
        "a", "an", "and", "are", "as", "at", "be", "by", "for",
        "from", "has", "he", "in", "is", "it", "its", "of", "on",
        "that", "the", "to", "was", "will", "with", "this", "but",
        "they", "have", "had", "what", "when", "where", "who", "which",
        "their", "said", "been", "has", "were", "more", "some", "can"
    }
    
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    
    return keywords


def has_keyword_match(text: str, keywords: List[str]) -> bool:
    """
    Check if text contains any of the keywords.
    
    Args:
        text: Text to search in
        keywords: List of keywords to search for
        
    Returns:
        True if at least one keyword is found
    """
    if not keywords:
        return False
    
    # Check if at least 30% of keywords are present
    found_count = sum(1 for keyword in keywords if keyword in text)
    threshold = max(1, len(keywords) * 0.3)
    
    return found_count >= threshold


def has_contradiction(text: str) -> bool:
    """
    Check if text contains contradiction keywords.
    
    Args:
        text: Text to search in
        
    Returns:
        True if contradiction keywords are found
    """
    for keyword in CONTRADICTION_KEYWORDS:
        if keyword in text:
            return True
    
    return False


def calculate_credibility_score(score: Dict[str, int]) -> float:
    """
    Calculate a credibility score (0-1) based on evidence.
    
    Args:
        score: Evidence score dictionary
        
    Returns:
        Credibility score between 0 and 1
    """
    total = score.get("total", 0)
    if total == 0:
        return 0.5  # Neutral when no evidence
    
    matches = score.get("matches", 0)
    contradictions = score.get("contradictions", 0)
    
    # If contradictions are high, credibility is low
    if contradictions > total * 0.5:
        return 0.2
    elif contradictions > total * 0.3:
        return 0.4
    
    # If matches are high, credibility is higher
    if matches > total * 0.7:
        return 0.8
    elif matches > total * 0.5:
        return 0.6
    
    # Default moderate credibility
    return 0.5
