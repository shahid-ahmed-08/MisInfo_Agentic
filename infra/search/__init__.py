"""
Search Intelligence Layer
Complete evidence-based verification system for misinformation detection.
"""

from .pipeline import run_search_pipeline, run_batch_search, validate_pipeline
from .claim_extractor import extract_claim, is_valid_claim
from .query_builder import build_query
from .serper import search_serper, is_serper_available
from .duckduckgo import search_duckduckgo
from .scoring import score_evidence, calculate_credibility_score

__all__ = [
    # Main pipeline
    "run_search_pipeline",
    "run_batch_search",
    "validate_pipeline",
    
    # Individual components
    "extract_claim",
    "is_valid_claim",
    "build_query",
    "search_serper",
    "is_serper_available",
    "search_duckduckgo",
    "score_evidence",
    "calculate_credibility_score",
]

__version__ = "1.0.0"

