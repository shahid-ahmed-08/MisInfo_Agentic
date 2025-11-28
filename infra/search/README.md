# Search Intelligence Layer

Complete evidence-based verification system for misinformation detection.

## Overview

This module provides a robust search-based evidence engine that extracts claims from social media text, searches multiple sources for verification, and scores the credibility of claims.

## Architecture

```
infra/search/
├── __init__.py          # Main exports
├── claim_extractor.py   # Extract claims from raw text
├── query_builder.py     # Build search queries
├── serper.py           # Primary search via Serper API
├── duckduckgo.py       # Fallback search via DuckDuckGo
├── scoring.py          # Evidence scoring and credibility
└── pipeline.py         # Master orchestration
```

## Features

### 1. Claim Extraction
- Removes URLs, mentions, hashtags
- Extracts clean factual claims
- Validates claim quality

### 2. Multi-Source Search
- **Primary**: Serper API (Google Search API)
- **Fallback**: DuckDuckGo HTML parser
- Automatic failover

### 3. Evidence Scoring
- Match counting (claim keywords in results)
- Contradiction detection (false, fake, hoax, etc.)
- Credibility score (0-1 scale)

### 4. Complete Pipeline
- End-to-end claim verification
- Batch processing support
- Safe fallbacks for all errors

## Usage

### Basic Usage

```python
from infra.search import run_search_pipeline

# Analyze a tweet
result = run_search_pipeline("Breaking: Scientists discover cure for all diseases!")

print(result)
# {
#     "claim": "Breaking: Scientists discover cure for all diseases",
#     "query": "Breaking: Scientists discover cure for all diseases news verification",
#     "score": {
#         "matches": 5,
#         "contradictions": 3,
#         "total": 10
#     },
#     "credibility": 0.4,
#     "results": [
#         {"title": "...", "snippet": "..."},
#         ...
#     ],
#     "source": "serper"
# }
```

### Batch Processing

```python
from infra.search import run_batch_search

tweets = [
    "Breaking news: Major political scandal revealed",
    "Scientists warn about climate change impacts",
    "Celebrity announced retirement from acting"
]

results = run_batch_search(tweets)
for result in results:
    print(f"Claim: {result['claim']}")
    print(f"Credibility: {result['credibility']}")
```

### Individual Components

```python
from infra.search import extract_claim, build_query, search_serper, score_evidence

# Step 1: Extract claim
text = "OMG! @user Check this out! #viral https://example.com Scientists find aliens!"
claim = extract_claim(text)
# "Scientists find aliens"

# Step 2: Build query
query = build_query(claim)
# "Scientists find aliens news verification"

# Step 3: Search
results = search_serper(query)
# [{"title": "...", "snippet": "..."}, ...]

# Step 4: Score
score = score_evidence(claim, results)
# {"matches": 2, "contradictions": 1, "total": 10}
```

## Configuration

### Environment Variables

**Option 1: Using .env file (Recommended)**

1. Create a `.env` file in `infra/search/`:
```bash
SERPER_API_KEY=your_api_key_here
```

2. Load it in your code:
```python
from dotenv import load_dotenv
load_dotenv()

from infra.search import run_search_pipeline
```

**Option 2: Using environment variables**

```bash
# Windows PowerShell
$env:SERPER_API_KEY="your_api_key_here"

# Linux/Mac
export SERPER_API_KEY="your_api_key_here"
```

**Get your free API key at:** https://serper.dev (2,500 searches/month free)

If `SERPER_API_KEY` is not set, the system automatically falls back to DuckDuckGo.

### Validation

```python
from infra.search import validate_pipeline

status = validate_pipeline()
print(status)
# {
#     "claim_extractor": True,
#     "query_builder": True,
#     "serper": True,  # False if API key not set
#     "duckduckgo": True,
#     "scoring": True,
#     "pipeline": True
# }
```

## API Reference

### `run_search_pipeline(text: str) -> dict`

Master function that runs the complete pipeline.

**Parameters:**
- `text` (str): Raw tweet or social media text

**Returns:**
```python
{
    "claim": str,              # Extracted claim
    "query": str,              # Search query used
    "score": {
        "matches": int,        # Results matching claim
        "contradictions": int, # Results contradicting claim
        "total": int          # Total results found
    },
    "credibility": float,      # 0-1 credibility score
    "results": [               # Search results
        {"title": str, "snippet": str},
        ...
    ],
    "source": str             # "serper", "duckduckgo", or "none"
}
```

### `extract_claim(text: str) -> str`

Extract clean claim from raw text.

### `build_query(claim: str) -> str`

Convert claim to search query.

### `search_serper(query: str) -> list`

Search using Serper API (requires `SERPER_API_KEY`).

### `search_duckduckgo(query: str) -> list`

Search using DuckDuckGo HTML parser (no API key needed).

### `score_evidence(claim: str, results: list) -> dict`

Score search results for verification.

### `calculate_credibility_score(score: dict) -> float`

Calculate credibility score (0-1) from evidence score.

## Error Handling

All functions are designed to fail gracefully:
- Network errors return empty results
- Missing API keys trigger fallback
- Invalid input returns safe defaults
- No exceptions propagate to caller

## Dependencies

- Python 3.10+
- `requests` - HTTP requests
- `python-dotenv` - Load .env files
- `re` - Regular expressions (built-in)
- `os` - Environment variables (built-in)

Install dependencies:
```bash
pip install -r requirements.txt
# or
pip install requests python-dotenv
```

## Testing

```python
# Quick test
from infra.search import run_search_pipeline

test_text = "Breaking: Scientists discover water on Mars #space"
result = run_search_pipeline(test_text)

assert result["claim"]
assert result["query"]
assert "score" in result
assert "credibility" in result
print("✓ All tests passed!")
```

## Integration Example

```python
# Backend integration
from infra.search import run_search_pipeline

def analyze_tweet(tweet_data):
    """Analyze tweet for misinformation."""
    text = tweet_data.get("text", "")
    
    # Run search pipeline
    search_result = run_search_pipeline(text)
    
    # Make decision
    credibility = search_result["credibility"]
    contradictions = search_result["score"]["contradictions"]
    
    if credibility < 0.3 or contradictions > 3:
        return {
            "flagged": True,
            "reason": "Low credibility or high contradictions",
            "evidence": search_result
        }
    
    return {
        "flagged": False,
        "evidence": search_result
    }
```

## Performance

- **Average latency**: 1-3 seconds per query
- **Serper**: ~500ms (with API)
- **DuckDuckGo**: ~2s (HTML parsing)
- **Batch processing**: Sequential (can be parallelized)

## Limitations

1. Depends on search engine availability
2. Serper API requires paid subscription
3. DuckDuckGo may rate-limit heavy usage
4. Credibility scoring is heuristic-based
5. Does not perform deep fact-checking

## Future Enhancements

- [ ] Parallel batch processing
- [ ] Additional search sources (Bing, etc.)
- [ ] ML-based credibility scoring
- [ ] Result caching
- [ ] Advanced NLP for claim extraction
- [ ] Multi-language support

## License

Part of Mumbai-Hacks misinformation detection project.

## Support

For issues or questions, refer to the main project documentation.
