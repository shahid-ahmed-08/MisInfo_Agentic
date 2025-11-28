"""
Test Script for Search Intelligence Layer
Demonstrates all functionality and validates the implementation.
"""

import os
from infra.search import (
    run_search_pipeline,
    run_batch_search,
    validate_pipeline,
    extract_claim,
    build_query,
    is_valid_claim,
    calculate_credibility_score
)


def test_claim_extraction():
    """Test claim extraction functionality."""
    print("\n=== Testing Claim Extraction ===")
    
    test_cases = [
        "Breaking news! @user Scientists discover cure for cancer #medical https://example.com",
        "OMG did you hear about the earthquake in California?? So scary!",
        "@mention1 @mention2 Check this out #trending #viral",
        "The president announced new economic policies today."
    ]
    
    for text in test_cases:
        claim = extract_claim(text)
        valid = is_valid_claim(claim)
        print(f"Input: {text[:50]}...")
        print(f"Claim: {claim}")
        print(f"Valid: {valid}")
        print()


def test_query_building():
    """Test query building functionality."""
    print("\n=== Testing Query Building ===")
    
    claims = [
        "Scientists discover cure for cancer",
        "Major earthquake hits California",
        "New economic policies announced"
    ]
    
    for claim in claims:
        query = build_query(claim)
        print(f"Claim: {claim}")
        print(f"Query: {query}")
        print()


def test_credibility_scoring():
    """Test credibility scoring logic."""
    print("\n=== Testing Credibility Scoring ===")
    
    test_scores = [
        {"matches": 8, "contradictions": 1, "total": 10},
        {"matches": 3, "contradictions": 5, "total": 10},
        {"matches": 5, "contradictions": 2, "total": 10},
        {"matches": 0, "contradictions": 0, "total": 0},
    ]
    
    for score in test_scores:
        credibility = calculate_credibility_score(score)
        print(f"Score: {score}")
        print(f"Credibility: {credibility}")
        print()


def test_pipeline_validation():
    """Test pipeline validation."""
    print("\n=== Testing Pipeline Validation ===")
    
    status = validate_pipeline()
    print("Component Status:")
    for component, is_working in status.items():
        status_str = "✓" if is_working else "✗"
        print(f"  {status_str} {component}: {is_working}")
    
    if not status.get("serper"):
        print("\nNote: Serper API not configured (SERPER_API_KEY not set)")
        print("Pipeline will use DuckDuckGo as fallback")


def test_full_pipeline():
    """Test complete search pipeline."""
    print("\n=== Testing Full Pipeline ===")
    
    test_tweets = [
        "Breaking: Scientists discover water on Mars! #space #nasa",
        "FAKE NEWS: The moon landing was staged in Hollywood!",
        "New study shows coffee is actually good for health"
    ]
    
    for i, tweet in enumerate(test_tweets, 1):
        print(f"\nTest {i}: {tweet}")
        print("-" * 60)
        
        result = run_search_pipeline(tweet)
        
        print(f"Claim: {result['claim']}")
        print(f"Query: {result['query']}")
        print(f"Source: {result['source']}")
        print(f"Results found: {result['score']['total']}")
        print(f"Matches: {result['score']['matches']}")
        print(f"Contradictions: {result['score']['contradictions']}")
        print(f"Credibility: {result['credibility']:.2f}")
        
        if result['results']:
            print(f"\nTop Result:")
            top = result['results'][0]
            print(f"  Title: {top['title'][:70]}...")
            print(f"  Snippet: {top['snippet'][:100]}...")


def test_batch_processing():
    """Test batch processing functionality."""
    print("\n=== Testing Batch Processing ===")
    
    tweets = [
        "Scientists announce breakthrough in quantum computing",
        "Celebrity couple announces surprise wedding",
        "Major tech company releases new smartphone"
    ]
    
    print(f"Processing {len(tweets)} tweets...")
    results = run_batch_search(tweets)
    
    print(f"\nResults Summary:")
    for i, result in enumerate(results, 1):
        print(f"{i}. Claim: {result['claim'][:50]}...")
        print(f"   Credibility: {result['credibility']:.2f}")
        print(f"   Source: {result['source']}")


def display_api_info():
    """Display API configuration info."""
    print("\n" + "=" * 60)
    print("SEARCH INTELLIGENCE LAYER - TEST SUITE")
    print("=" * 60)
    
    serper_key = os.environ.get("SERPER_API_KEY")
    if serper_key:
        print(f"✓ Serper API: Configured (key: {serper_key[:8]}...)")
    else:
        print("○ Serper API: Not configured (will use DuckDuckGo fallback)")
    
    print("✓ DuckDuckGo: Always available (no API key required)")
    print()


def main():
    """Run all tests."""
    try:
        display_api_info()
        
        # Run tests
        test_claim_extraction()
        test_query_building()
        test_credibility_scoring()
        test_pipeline_validation()
        test_full_pipeline()
        test_batch_processing()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS COMPLETED")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
