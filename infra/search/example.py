"""
Quick Start Example
Demonstrates basic usage of the Search Intelligence Layer
"""

import os
from infra.search import run_search_pipeline

# Example 1: Basic usage
print("=== Example 1: Basic Tweet Analysis ===\n")

tweet = "Breaking: Scientists announce major breakthrough in cancer research! #medical #health"

result = run_search_pipeline(tweet)

print(f"Original Tweet: {tweet}")
print(f"\nExtracted Claim: {result['claim']}")
print(f"Search Query: {result['query']}")
print(f"Search Source: {result['source']}")
print(f"Total Results: {result['score']['total']}")
print(f"Matches: {result['score']['matches']}")
print(f"Contradictions: {result['score']['contradictions']}")
print(f"Credibility Score: {result['credibility']:.2f}")

if result['results']:
    print(f"\nTop Result:")
    print(f"  Title: {result['results'][0]['title']}")
    print(f"  Snippet: {result['results'][0]['snippet'][:100]}...")

# Example 2: Batch processing
print("\n\n=== Example 2: Batch Processing ===\n")

from infra.search import run_batch_search

tweets = [
    "BREAKING: Aliens spotted in New York City!",
    "New study shows chocolate is good for heart health",
    "President announces new economic stimulus package"
]

results = run_batch_search(tweets)

for i, result in enumerate(results, 1):
    print(f"{i}. {result['claim'][:50]}...")
    print(f"   Credibility: {result['credibility']:.2f} | Results: {result['score']['total']}")

# Example 3: Decision making
print("\n\n=== Example 3: Flagging Misinformation ===\n")

def should_flag_content(text):
    """Determine if content should be flagged."""
    result = run_search_pipeline(text)
    
    credibility = result['credibility']
    contradictions = result['score']['contradictions']
    total_results = result['score']['total']
    
    # Flag if low credibility or high contradictions
    if credibility < 0.3:
        return True, "Very low credibility score"
    
    if total_results > 0 and contradictions / total_results > 0.4:
        return True, "High contradiction rate"
    
    return False, "Content appears credible"

test_content = "5G towers are causing coronavirus spread!"
should_flag, reason = should_flag_content(test_content)

print(f"Content: {test_content}")
print(f"Should Flag: {should_flag}")
print(f"Reason: {reason}")

# Example 4: Using individual components
print("\n\n=== Example 4: Component-Level Usage ===\n")

from infra.search import extract_claim, build_query, score_evidence

text = "@user OMG! https://fake-news.com Scientists find cure for aging! #viral"

# Step by step
claim = extract_claim(text)
print(f"1. Extracted Claim: {claim}")

query = build_query(claim)
print(f"2. Built Query: {query}")

# Simulate results
fake_results = [
    {"title": "Debunked: No cure for aging", "snippet": "This false claim has been debunked by experts"},
    {"title": "Aging research continues", "snippet": "Scientists are still researching aging"}
]

score = score_evidence(claim, fake_results)
print(f"3. Evidence Score: {score}")

# API Configuration Info
print("\n\n=== API Configuration ===\n")

serper_key = os.environ.get("SERPER_API_KEY")
if serper_key:
    print(f"✓ Serper API is configured")
    print(f"  Primary search will use Google Search via Serper")
else:
    print(f"○ Serper API is NOT configured")
    print(f"  To enable: Set environment variable SERPER_API_KEY")
    print(f"  Get API key: https://serper.dev")
    print(f"  Fallback: DuckDuckGo will be used automatically")

print("\n✓ Search Intelligence Layer is ready!")
