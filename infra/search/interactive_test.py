"""
Interactive Testing Tool
Test the search pipeline with your own queries
"""

from dotenv import load_dotenv
load_dotenv()

from infra.search import run_search_pipeline
import json

def test_claim(text):
    """Test a single claim and display results."""
    print("\n" + "=" * 70)
    print("ANALYZING...")
    print("=" * 70)
    
    result = run_search_pipeline(text)
    
    print(f"\n📝 Input: {text}")
    print(f"\n🔍 Extracted Claim: {result['claim']}")
    print(f"🔎 Search Query: {result['query']}")
    print(f"📡 Source: {result['source']}")
    
    print(f"\n📊 Evidence Scoring:")
    print(f"  • Total Results: {result['score']['total']}")
    print(f"  • Matching Results: {result['score']['matches']}")
    print(f"  • Contradicting Results: {result['score']['contradictions']}")
    print(f"  • Credibility Score: {result['credibility']:.2f}/1.0")
    
    # Interpretation
    cred = result['credibility']
    if cred >= 0.8:
        interpretation = "✅ HIGHLY CREDIBLE - Strong supporting evidence"
    elif cred >= 0.6:
        interpretation = "✓ CREDIBLE - Good supporting evidence"
    elif cred >= 0.4:
        interpretation = "⚖️  MIXED - Conflicting evidence found"
    elif cred >= 0.2:
        interpretation = "⚠️  QUESTIONABLE - Multiple debunking sources"
    else:
        interpretation = "🚨 HIGHLY SUSPICIOUS - Strong contradictory evidence"
    
    print(f"\n💡 Interpretation: {interpretation}")
    
    if result['results']:
        print(f"\n📰 Top 3 Evidence Sources:")
        for i, item in enumerate(result['results'][:3], 1):
            print(f"\n  {i}. {item.get('title', 'No title')}")
            snippet = item.get('snippet', 'No snippet')
            # Wrap snippet at 65 chars
            words = snippet.split()
            line = "     "
            for word in words:
                if len(line) + len(word) > 65:
                    print(line)
                    line = "     " + word + " "
                else:
                    line += word + " "
            if line.strip():
                print(line)
    else:
        print(f"\n⚠️  No search results found")
    
    print("\n" + "=" * 70)
    
    # Ask if user wants JSON
    choice = input("\nShow full JSON output? (y/n): ").lower()
    if choice == 'y':
        print("\n" + json.dumps(result, indent=2))

def main():
    """Main interactive loop."""
    print("=" * 70)
    print("INTERACTIVE SEARCH INTELLIGENCE TESTER")
    print("=" * 70)
    print("\nTest any claim for misinformation detection!")
    print("Type 'quit' or 'exit' to stop.\n")
    
    # Example claims
    examples = [
        "Drinking bleach cures COVID-19",
        "NASA discovers alien life on Mars",
        "5G towers cause coronavirus",
        "President announces new policy",
    ]
    
    print("📋 Example claims you can test:")
    for i, example in enumerate(examples, 1):
        print(f"  {i}. {example}")
    
    while True:
        print("\n" + "-" * 70)
        user_input = input("\n✍️  Enter a claim to test (or 'quit' to exit): ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Thanks for testing! Goodbye.")
            break
        
        if not user_input:
            print("⚠️  Please enter a valid claim.")
            continue
        
        try:
            test_claim(user_input)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
        
        # Ask to continue
        choice = input("\n🔄 Test another claim? (y/n): ").lower()
        if choice != 'y':
            print("\n👋 Thanks for testing! Goodbye.")
            break

if __name__ == "__main__":
    main()
