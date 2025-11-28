"""
Claim Extractor Module
Extracts factual claims from raw tweet text.
"""

import re


def extract_claim(text: str) -> str:
    """
    Extract a clean factual claim from raw tweet text.
    
    Args:
        text: Raw tweet text
        
    Returns:
        Cleaned claim string
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    # Remove mentions (@username)
    text = re.sub(r'@\w+', '', text)
    
    # Remove hashtags (#tag)
    text = re.sub(r'#\w+', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    # Limit length to reasonable claim size (first sentence or 200 chars)
    sentences = re.split(r'[.!?]+', text)
    if sentences and sentences[0]:
        claim = sentences[0].strip()
    else:
        claim = text[:200].strip()
    
    return claim


def is_valid_claim(claim: str) -> bool:
    """
    Check if extracted claim is valid for search.
    
    Args:
        claim: Extracted claim text
        
    Returns:
        True if claim is valid, False otherwise
    """
    if not claim:
        return False
    
    # Must have at least 3 words
    words = claim.split()
    if len(words) < 3:
        return False
    
    # Must have some alphabetic content
    if not any(c.isalpha() for c in claim):
        return False
    
    return True
