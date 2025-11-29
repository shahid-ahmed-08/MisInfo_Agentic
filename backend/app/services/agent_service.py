def extract_claim(text: str) -> str:
    """
    Minimal claim extraction:
    - Remove URLs
    - Take first sentence or first line
    - Strip whitespace
    """
    parts = text.split("http")[0]
    claim = parts.split(".")[0]
    claim = claim.split("\n")[0]
    claim = claim.strip()
    return claim


def generate_queries(claim: str):
    """
    Generate simple search queries (non-LLM).
    Will upgrade later.
    """
    q1 = claim
    q2 = claim + " news"
    q3 = " ".join(claim.split()[:6])
    return [q1, q2, q3]


def score_sources(sources, claim_tokens):
    """
    Score each source by matching claim tokens against its title/snippet.
    Produces a normalized score 0–1.
    """
    scored = []
    for s in sources:
        text = (s.get("title") or "") + " " + (s.get("snippet") or "")
        score = 0
        for tok in claim_tokens:
            if tok.lower() in text.lower():
                score += 1
        s["score"] = score / max(1, len(claim_tokens))  # normalize
        scored.append(s)
    return scored


def determine_verdict(scored_sources):
    """
    Simple rule-based verdict:
    - score > 0.60 → accurate
    - score > 0.35 → unverified
    - else → contradicted
    """
    if not scored_sources or len(scored_sources) == 0:
        return "unverified", 0.10

    max_score = max(s["score"] for s in scored_sources)

    if max_score > 0.60:
        return "accurate", max_score
    elif max_score > 0.35:
        return "unverified", max_score
    else:
        return "contradicted", 1.0 - max_score

