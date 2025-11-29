import logging

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.agent_service import (
    extract_claim,
    generate_queries,
    score_sources,
    determine_verdict
)
from tools.search_manager import cached_search

logger = logging.getLogger("misinfo_guardian")

router = APIRouter()

class VerifyRequest(BaseModel):
    id: str | None = None
    text: str

@router.post("/verify")
def verify(payload: VerifyRequest):
    try:
        claim = extract_claim(payload.text)
        queries = generate_queries(claim)

        all_sources = []
        for q in queries:
            results = cached_search(q)
            all_sources.extend(results)

        seen = set()
        unique_sources = []
        for src in all_sources:
            key = src.get("link") or src.get("title")
            if key not in seen:
                seen.add(key)
                unique_sources.append(src)

        unique_sources = unique_sources[:5]  # speed limit

        claim_tokens = claim.split()[:8]
        scored = score_sources(unique_sources, claim_tokens)

        verdict, confidence = determine_verdict(scored)

        return {
            "verdict": verdict,
            "confidence": float(confidence),
            "claim": claim,
            "search_queries": queries,
            "top_sources": scored[:3],
            "reasoning": [
                "Claim extracted",
                "Queries generated",
                f"Found {len(scored)} evidence sources",
                f"Max score {max((s['score'] for s in scored), default=0):.2f}",
                f"Final verdict: {verdict}"
            ]
        }

    except Exception as e:
        logger.error(f"Verification error: {str(e)}")
        return {
            "verdict": "unverified",
            "confidence": 0.10,
            "claim": payload.text,
            "search_queries": [],
            "top_sources": [],
            "reasoning": ["Internal error — safe fallback applied."]
        }
