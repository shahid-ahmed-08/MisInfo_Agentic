import requests
import os
import socket

MCP_BASE = "http://localhost:8001"
MCP_URL = f"{MCP_BASE}/tools/search/call"
MCP_KEY = os.getenv("MCP_API_KEY", "")

print("Using MCP client connecting to:", MCP_BASE, "(", socket.gethostbyname('localhost'), ")")


def mcp_search(query: str, top_k: int = 3):
    """
    Calls the MCP search tool and returns list of results.
    """
    payload = {
        "args": [query],
        "kwargs": {},
    }

    headers = {"Content-Type": "application/json"}
    if MCP_KEY:
        headers["X-API-KEY"] = MCP_KEY

    try:
        resp = requests.post(MCP_URL, json=payload, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, dict):
            return []
        return data.get("result", [])
    except Exception as e:
        print("MCP search error:", e)
        return []

