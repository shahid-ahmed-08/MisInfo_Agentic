# IMPORTANT: Load environment BEFORE any imports
from dotenv import load_dotenv
import os
load_dotenv()  # This must be called before importing infra.search

# Debug: Check if API key is loaded
api_key = os.getenv("SERPER_API_KEY")
print(f"DEBUG: API Key loaded: {'Yes (' + api_key[:10] + '...' + api_key[-4:] + ')' if api_key else 'NO'}")

# Now import after environment is loaded
from infra.search import run_search_pipeline
import json

print("=" * 70)
print("SEARCH INTELLIGENCE LAYER - TEST")
print("=" * 70)

result = run_search_pipeline("Breaking: Scientists discover aliens!")

print(f"\nExtracted Claim: {result['claim']}")
print(f"Search Query: {result['query']}")
print(f"Search Source: {result.get('source', 'unknown')}")
print(f"Total Results: {result['score']['total']}")
print(f"Matches: {result['score']['matches']}")
print(f"Contradictions: {result['score']['contradictions']}")
print(f"Credibility Score: {result['credibility']}")

if result['results']:
    print(f"\n{'─' * 70}")
    print(f"TOP 3 SEARCH RESULTS:")
    print(f"{'─' * 70}")
    for i, item in enumerate(result['results'][:3], 1):
        print(f"\n{i}. {item.get('title', 'No title')}")
        print(f"   {item.get('snippet', 'No snippet')[:150]}...")
else:
    print(f"\n⚠️  WARNING: No search results found!")
    if 'error' in result:
        print(f"   Error: {result['error']}")
    else:
        print(f"   Both Serper and DuckDuckGo searches failed.")
        print(f"   Check your internet connection and API key.")

print(f"\n{'=' * 70}")
print(f"FULL JSON OUTPUT:")
print(f"{'=' * 70}")
print(json.dumps(result, indent=2))
print(f"{'=' * 70}")