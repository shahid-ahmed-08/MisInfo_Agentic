"""
Example: Loading environment variables from .env file
This shows how to use python-dotenv to load API keys
"""

import os

# Option 1: Using python-dotenv (recommended)
try:
    from dotenv import load_dotenv
    
    # Load .env file from current directory
    load_dotenv()
    
    print("✓ Loaded .env file using python-dotenv")
    
except ImportError:
    print("⚠ python-dotenv not installed")
    print("  Install with: pip install python-dotenv")
    print("  For now, using manual loading...")
    
    # Option 2: Manual loading (fallback)
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        print("✓ Loaded .env file manually")

# Check if API key is loaded
serper_key = os.environ.get("SERPER_API_KEY")

print("\n=== Environment Status ===")
if serper_key and serper_key != "your_serper_api_key_here":
    print(f"✓ SERPER_API_KEY is set: {serper_key[:8]}...")
    print("  Ready to use Google Search via Serper API")
else:
    print("✗ SERPER_API_KEY is not set or using placeholder")
    print("  Will use DuckDuckGo fallback")
    print("\n  To fix:")
    print("  1. Edit .env file")
    print("  2. Replace 'your_serper_api_key_here' with your actual key")
    print("  3. Get key from: https://serper.dev")

# Test the search pipeline
print("\n=== Testing Search Pipeline ===")
from infra.search import run_search_pipeline, validate_pipeline

status = validate_pipeline()
print(f"Serper API Available: {status['serper']}")
print(f"DuckDuckGo Available: {status['duckduckgo']}")
print(f"Pipeline Status: {status['pipeline']}")

# Run a test search
print("\n=== Running Test Search ===")
result = run_search_pipeline("Scientists discover water on Mars")
print(f"Claim: {result['claim']}")
print(f"Search Source: {result['source']}")
print(f"Results Found: {result['score']['total']}")
print(f"Credibility: {result['credibility']}")

if result['source'] == 'serper':
    print("\n✓ SUCCESS! Using Serper API (Google Search)")
elif result['source'] == 'duckduckgo':
    print("\n⚠ Using DuckDuckGo fallback (Serper API not configured)")
else:
    print("\n✗ No search results (check network connection)")
