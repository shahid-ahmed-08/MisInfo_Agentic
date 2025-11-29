import os
import requests
from typing import List, Dict, Any
from mcp.server.fastmcp import FastMCP, Tool

SERPER_KEY = os.getenv("SERPER_API_KEY")

mcp = FastMCP()

@mcp.tool()
def search_run(query: str) -> List[Dict[str, Any]]:
    """
    MCP tool for searching the web using Serper.
    """
    if not SERPER_KEY:
        return []

    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_KEY, "Content-Type": "application/json"}

    try:
        response = requests.post(url, json={"q": query}, headers=headers, timeout=6)
        data = response.json()
    except Exception:
        return []

    results = []
    for item in data.get("organic", [])[:3]:
        results.append({
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet")
        })

    return results

if __name__ == "__main__":
    mcp.run()

