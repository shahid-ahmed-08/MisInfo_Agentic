"""
Query Builder Module
Converts extracted claims into search queries.
"""


def build_query(claim: str) -> str:
    """
    Convert extracted claim into a Google-style search query.
    
    Args:
        claim: Extracted factual claim
        
    Returns:
        Search query string formatted for verification
    """
    if not claim:
        return ""
    
    # Clean up the claim
    claim = claim.strip()
    
    # Don't use strict quotes - they're too restrictive
    # Just add verification keywords
    query = f'{claim} news verification'
    
    return query


def build_alternative_query(claim: str) -> str:
    """
    Build an alternative query for fallback searches.
    
    Args:
        claim: Extracted factual claim
        
    Returns:
        Alternative search query
    """
    if not claim:
        return ""
    
    claim = claim.strip()
    query = f"{claim} fact check"
    
    return query
