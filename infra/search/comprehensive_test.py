"""
Comprehensive Test Suite for Search Intelligence Layer
Tests various types of claims and scenarios
"""

from dotenv import load_dotenv
load_dotenv()

from infra.search import run_search_pipeline
import json

print("=" * 80)
print("COMPREHENSIVE SEARCH INTELLIGENCE TEST SUITE")
print("=" * 80)

# Test cases covering different types of misinformation
test_cases = [
    {
        "name": "Health Misinformation",
        "text": "Breaking: Drinking bleach cures COVID-19! #health",
        "expected": "Should find debunking articles with high contradictions"
    },
    {
        "name": "Political Claim",
        "text": "President announces new climate change policy today",
        "expected": "Should find news articles with moderate credibility"
    },
    {
        "name": "Scientific Discovery",
        "text": "NASA announces discovery of water on Mars",
        "expected": "Should find legitimate news sources"
    },
    {
        "name": "Celebrity Rumor",
        "text": "@TMZ OMG! Celebrity couple getting divorced! #gossip https://fake.com",
        "expected": "Mixed results, moderate credibility"
    },
    {
        "name": "Conspiracy Theory",
        "text": "5G towers are controlling our minds with radio waves!",
        "expected": "Should find debunking articles"
    },
    {
        "name": "Economic News",
        "text": "Stock market crashes by 50% in single day",
        "expected": "Should verify if true or exaggerated"
    },
    {
        "name": "Technology Claim",
        "text": "Apple releases iPhone 20 with holographic display",
        "expected": "Should check if announcement is real"
    },
    {
        "name": "Climate Claim",
        "text": "Scientists confirm global warming is a hoax",
        "expected": "High contradictions from scientific sources"
    },
]

results_summary = []

for i, test in enumerate(test_cases, 1):
    print(f"\n{'=' * 80}")
    print(f"TEST {i}/{len(test_cases)}: {test['name']}")
    print(f"{'=' * 80}")
    print(f"Input: {test['text']}")
    print(f"Expected: {test['expected']}")
    print(f"\nProcessing...")
    
    result = run_search_pipeline(test['text'])
    
    print(f"\n📊 RESULTS:")
    print(f"  Claim: {result['claim']}")
    print(f"  Query: {result['query']}")
    print(f"  Source: {result['source']}")
    print(f"  Results Found: {result['score']['total']}")
    print(f"  Matches: {result['score']['matches']}")
    print(f"  Contradictions: {result['score']['contradictions']}")
    print(f"  Credibility: {result['credibility']:.2f}")
    
    # Determine verdict
    if result['credibility'] < 0.3:
        verdict = "🚨 HIGHLY SUSPICIOUS"
    elif result['credibility'] < 0.5:
        verdict = "⚠️  QUESTIONABLE"
    elif result['credibility'] < 0.7:
        verdict = "⚖️  MIXED EVIDENCE"
    else:
        verdict = "✅ LIKELY CREDIBLE"
    
    print(f"\n  Verdict: {verdict}")
    
    if result['results']:
        print(f"\n  Top 2 Sources:")
        for j, item in enumerate(result['results'][:2], 1):
            print(f"    {j}. {item.get('title', 'No title')[:60]}...")
    else:
        print(f"\n  ⚠️  No search results found")
    
    # Store summary
    results_summary.append({
        "test": test['name'],
        "claim": result['claim'],
        "credibility": result['credibility'],
        "verdict": verdict,
        "results_count": result['score']['total']
    })

# Print summary
print(f"\n\n{'=' * 80}")
print("TEST SUMMARY")
print(f"{'=' * 80}")
print(f"\n{'Test':<25} {'Credibility':<15} {'Results':<10} {'Verdict':<20}")
print("-" * 80)

for summary in results_summary:
    print(f"{summary['test']:<25} {summary['credibility']:<15.2f} {summary['results_count']:<10} {summary['verdict']:<20}")

print(f"\n{'=' * 80}")
print("✓ ALL TESTS COMPLETE")
print(f"{'=' * 80}")
