"""
Search Pipeline Module
Master orchestration for the search intelligence layer.
"""

from typing import Dict, List, Any
from .claim_extractor import extract_claim, is_valid_claim
from .query_builder import build_query
from .serper import search_serper, is_serper_available
from .duckduckgo import search_duckduckgo
from .scoring import score_evidence, calculate_credibility_score


def run_search_pipeline(text: str) -> Dict[str, Any]:
    """
    Run the complete search pipeline for misinformation detection.
    
    Args:
        text: Raw tweet text
        
    Returns:
        Dictionary containing:
        {
            "claim": str,
            "query": str,
            "score": {"matches": int, "contradictions": int, "total": int},
            "credibility": float,
            "results": [{"title": str, "snippet": str}, ...],
            "source": str
        }
    """
    # Step 1: Extract claim
    claim = extract_claim(text)
    
    if not is_valid_claim(claim):
        return {
            "claim": claim,
            "query": "",
            "score": {"matches": 0, "contradictions": 0, "total": 0},
            "credibility": 0.5,
            "results": [],
            "source": "none",
            "error": "Invalid or insufficient claim content"
        }
    
    # Step 2: Build search query
    query = build_query(claim)
    
    # Step 3: Search using Serper (primary)
    results = []
    source = "none"
    
    if is_serper_available():
        results = search_serper(query)
        if results:
            source = "serper"
    
    # Step 4: Fallback to DuckDuckGo if no results
    if not results:
        results = search_duckduckgo(query)
        if results:
            source = "duckduckgo"
    
    # Step 5: Score evidence
    evidence_score = score_evidence(claim, results)
    
    # Step 6: Calculate credibility
    credibility = calculate_credibility_score(evidence_score)
    
    # Return complete results
    return {
        "claim": claim,
        "query": query,
        "score": evidence_score,
        "credibility": credibility,
        "results": results,
        "source": source
    }


def run_batch_search(texts: List[str]) -> List[Dict[str, Any]]:
    """
    Run search pipeline on multiple texts.
    
    Args:
        texts: List of raw tweet texts
        
    Returns:
        List of pipeline results for each text
    """
    results = []
    
    for text in texts:
        result = run_search_pipeline(text)
        results.append(result)
    
    return results


def validate_pipeline() -> Dict[str, bool]:
    """
    Validate that all pipeline components are working.
    
    Returns:
        Dictionary with component status
    """
    status = {
        "claim_extractor": True,
        "query_builder": True,
        "serper": is_serper_available(),
        "duckduckgo": True,
        "scoring": True
    }
    
    # Test with sample text
    try:
        test_result = run_search_pipeline("Breaking news: Scientists discover new planet")
        status["pipeline"] = bool(test_result.get("claim"))
    except Exception:
        status["pipeline"] = False
    
    return status
