"""
Test with exact query format from query_builder
"""
from dotenv import load_dotenv
import os
load_dotenv()

import requests

api_key = os.environ.get("SERPER_API_KEY")

url = "https://google.serper.dev/search"
headers = {
    "X-API-KEY": api_key,
    "Content-Type": "application/json"
}

# This is the EXACT format from query_builder
query_with_quotes = '"Breaking Scientists discover aliens" news verification'
payload = {"q": query_with_quotes}

print(f"Testing query: {query_with_quotes}")
print(f"\nMaking request...")
response = requests.post(url, json=payload, headers=headers, timeout=10)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    organic = data.get("organic", [])
    print(f"✓ SUCCESS! Results: {len(organic)}")
    if organic:
        print(f"\nFirst result:")
        print(f"  Title: {organic[0].get('title')}")
else:
    print(f"✗ FAILED: {response.text}")
