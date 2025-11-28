"""
Debug script to identify search issues
"""
from dotenv import load_dotenv
import os
load_dotenv()

print("=" * 70)
print("SEARCH DEBUG - DETAILED DIAGNOSTICS")
print("=" * 70)

# 1. Check environment
print("\n1. ENVIRONMENT CHECK")
api_key = os.getenv("SERPER_API_KEY")
if api_key:
    print(f"   ✓ API Key found: {api_key[:10]}...{api_key[-4:]}")
else:
    print(f"   ✗ API Key NOT found")
print()

# 2. Test Serper API directly
print("2. TESTING SERPER API")
try:
    import requests
    
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    payload = {"q": "test query"}
    
    print(f"   Making request to: {url}")
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        organic = data.get("organic", [])
        print(f"   ✓ SUCCESS! Got {len(organic)} results")
        if organic:
            print(f"   First result: {organic[0].get('title', 'N/A')[:50]}...")
    else:
        print(f"   ✗ FAILED: {response.text}")
        
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
print()

# 3. Test DuckDuckGo
print("3. TESTING DUCKDUCKGO")
try:
    import requests
    from urllib.parse import quote_plus
    
    query = "test query"
    encoded_query = quote_plus(query)
    url = f"https://duckduckgo.com/html/?q={encoded_query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    print(f"   Making request to: {url[:50]}...")
    response = requests.get(url, headers=headers, timeout=10)
    print(f"   Status Code: {response.status_code}")
    print(f"   Content Length: {len(response.text)} bytes")
    
    if response.status_code == 200:
        html = response.text
        # Quick check for results
        if 'result__title' in html or 'results' in html.lower():
            print(f"   ✓ SUCCESS! Found search results in HTML")
        else:
            print(f"   ⚠ WARNING: Got response but no results found")
            print(f"   First 500 chars: {html[:500]}")
    else:
        print(f"   ✗ FAILED")
        
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
print()

# 4. Test using search modules
print("4. TESTING SEARCH MODULES")
try:
    from infra.search.serper import search_serper
    print("   Testing search_serper()...")
    results = search_serper("covid vaccine")
    print(f"   Results: {len(results)} items")
    if results:
        print(f"   ✓ First result: {results[0].get('title', 'N/A')[:50]}...")
    else:
        print(f"   ✗ No results returned")
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
print()

try:
    from infra.search.duckduckgo import search_duckduckgo
    print("   Testing search_duckduckgo()...")
    results = search_duckduckgo("covid vaccine")
    print(f"   Results: {len(results)} items")
    if results:
        print(f"   ✓ First result: {results[0].get('title', 'N/A')[:50]}...")
    else:
        print(f"   ✗ No results returned")
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
print()

# 5. Test full pipeline
print("5. TESTING FULL PIPELINE")
try:
    from infra.search import run_search_pipeline
    result = run_search_pipeline("Scientists discover aliens")
    print(f"   Claim: {result['claim']}")
    print(f"   Source: {result.get('source', 'none')}")
    print(f"   Results: {len(result['results'])}")
    
    if result['results']:
        print(f"   ✓ SUCCESS!")
    else:
        print(f"   ✗ No results")
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 70)
print("DIAGNOSIS COMPLETE")
print("=" * 70)
