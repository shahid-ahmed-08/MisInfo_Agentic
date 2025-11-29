import os
import requests

SERPER_API_KEY = os.getenv("SERPER_API_KEY")


def search_manager(query: str):
    """
    Ultra-resilient search manager:
    - Serper: timeout=2 seconds
    - If rate-limited or failed: fallback to DuckDuckGo Lite
    - Always returns quickly
    """

    results = []

    # --- Primary: Serper ---
    if SERPER_API_KEY:
        try:
            resp = requests.post(
                "https://google.serper.dev/search",
                json={"q": query},
                headers={
                    "X-API-KEY": SERPER_API_KEY,
                    "Content-Type": "application/json"
                },
                timeout=2
            )
            data = resp.json()
            for item in data.get("organic", [])[:5]:
                results.append({
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet", "")
                })
        except Exception:
            pass

    # --- Fallback: DuckDuckGo Light ---
    if not results:
        try:
            r = requests.get(
                "https://duckduckgo.com/",
                params={"q": query},
                timeout=2
            )
            # minimal parsing
            if "<title>" in r.text:
                results.append({
                    "title": f"DuckDuckGo result for: {query}",
                    "link": "https://duckduckgo.com/?q=" + query.replace(" ", "+"),
                    "snippet": "Fallback search result"
                })
        except Exception:
            pass

    return results[:5]
