"""
Batch Testing Tool
Test multiple tweets from a file or list
"""

from dotenv import load_dotenv
load_dotenv()

from infra.search import run_batch_search, run_search_pipeline
import json
import csv
from datetime import datetime

# Sample tweet dataset
SAMPLE_TWEETS = [
    "Breaking: Drinking bleach cures coronavirus! #health #COVID19",
    "NASA announces discovery of Earth-like planet 100 light years away",
    "New study shows coffee reduces risk of heart disease by 30%",
    "FAKE NEWS: Election was rigged by voting machines!",
    "Scientists confirm 5G towers are safe and don't cause health issues",
    "President Biden announces new climate change initiative today",
    "Elon Musk acquires Twitter for $44 billion dollars",
    "Vaccines cause autism says discredited study from 1998",
    "Apple releases iPhone 15 with revolutionary new battery technology",
    "Global warming is a hoax created by China says conspiracy theorist",
]

def batch_test_basic():
    """Run basic batch test."""
    print("=" * 80)
    print("BATCH TESTING - BASIC")
    print("=" * 80)
    
    print(f"\nTesting {len(SAMPLE_TWEETS)} sample tweets...\n")
    
    results = run_batch_search(SAMPLE_TWEETS)
    
    suspicious_count = 0
    credible_count = 0
    
    for i, result in enumerate(results, 1):
        cred = result['credibility']
        
        if cred < 0.3:
            verdict = "🚨 SUSPICIOUS"
            suspicious_count += 1
        elif cred < 0.5:
            verdict = "⚠️  QUESTIONABLE"
        elif cred < 0.7:
            verdict = "⚖️  MIXED"
        else:
            verdict = "✅ CREDIBLE"
            credible_count += 1
        
        print(f"{i:2}. {verdict:<15} (Cred: {cred:.2f}) - {result['claim'][:50]}...")
    
    print(f"\n{'=' * 80}")
    print(f"Summary: {suspicious_count} suspicious, {credible_count} credible")
    print(f"{'=' * 80}")

def batch_test_detailed():
    """Run detailed batch test with full output."""
    print("\n\n" + "=" * 80)
    print("BATCH TESTING - DETAILED")
    print("=" * 80)
    
    results = run_batch_search(SAMPLE_TWEETS[:3])  # Test first 3 for detail
    
    for i, result in enumerate(results, 1):
        print(f"\n{'-' * 80}")
        print(f"TWEET {i}")
        print(f"{'-' * 80}")
        print(f"Original: {SAMPLE_TWEETS[i-1]}")
        print(f"\nClaim: {result['claim']}")
        print(f"Query: {result['query']}")
        print(f"Source: {result['source']}")
        print(f"Results: {result['score']['total']}")
        print(f"Matches: {result['score']['matches']}")
        print(f"Contradictions: {result['score']['contradictions']}")
        print(f"Credibility: {result['credibility']:.2f}")
        
        if result['results']:
            print(f"\nTop Result:")
            print(f"  {result['results'][0].get('title', 'No title')[:60]}")

def export_results_to_json():
    """Export batch results to JSON file."""
    print("\n\n" + "=" * 80)
    print("EXPORTING RESULTS TO JSON")
    print("=" * 80)
    
    results = run_batch_search(SAMPLE_TWEETS)
    
    output_data = {
        "timestamp": datetime.now().isoformat(),
        "total_tweets": len(SAMPLE_TWEETS),
        "results": []
    }
    
    for tweet, result in zip(SAMPLE_TWEETS, results):
        output_data["results"].append({
            "original_tweet": tweet,
            "claim": result['claim'],
            "credibility": result['credibility'],
            "matches": result['score']['matches'],
            "contradictions": result['score']['contradictions'],
            "total_results": result['score']['total'],
            "source": result['source']
        })
    
    filename = f"batch_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\n✓ Results exported to: {filename}")
    print(f"  Total tweets analyzed: {len(SAMPLE_TWEETS)}")

def export_results_to_csv():
    """Export batch results to CSV file."""
    print("\n\n" + "=" * 80)
    print("EXPORTING RESULTS TO CSV")
    print("=" * 80)
    
    results = run_batch_search(SAMPLE_TWEETS)
    
    filename = f"batch_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "Original Tweet", 
            "Extracted Claim", 
            "Credibility", 
            "Matches", 
            "Contradictions", 
            "Total Results", 
            "Source",
            "Verdict"
        ])
        
        for tweet, result in zip(SAMPLE_TWEETS, results):
            cred = result['credibility']
            if cred < 0.3:
                verdict = "SUSPICIOUS"
            elif cred < 0.5:
                verdict = "QUESTIONABLE"
            elif cred < 0.7:
                verdict = "MIXED"
            else:
                verdict = "CREDIBLE"
            
            writer.writerow([
                tweet,
                result['claim'],
                f"{cred:.2f}",
                result['score']['matches'],
                result['score']['contradictions'],
                result['score']['total'],
                result['source'],
                verdict
            ])
    
    print(f"\n✓ Results exported to: {filename}")
    print(f"  Total tweets analyzed: {len(SAMPLE_TWEETS)}")

def main():
    """Run all batch tests."""
    batch_test_basic()
    batch_test_detailed()
    export_results_to_json()
    export_results_to_csv()
    
    print("\n\n" + "=" * 80)
    print("✓ ALL BATCH TESTS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
