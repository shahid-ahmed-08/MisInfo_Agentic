"""
Direct API test to isolate the issue
"""
from dotenv import load_dotenv
import os
load_dotenv()

import requests

api_key = os.environ.get("SERPER_API_KEY")
print(f"API Key: {api_key[:10]}...{api_key[-4:]}")

url = "https://google.serper.dev/search"
headers = {
    "X-API-KEY": api_key,
    "Content-Type": "application/json"
}
payload = {"q": "Breaking Scientists discover aliens news verification"}

print(f"\nMaking request...")
response = requests.post(url, json=payload, headers=headers, timeout=10)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    organic = data.get("organic", [])
    print(f"Results: {len(organic)}")
    if organic:
        print(f"\nFirst result:")
        print(f"  Title: {organic[0].get('title')}")
        print(f"  Snippet: {organic[0].get('snippet')[:100]}...")
else:
    print(f"Error: {response.text}")
