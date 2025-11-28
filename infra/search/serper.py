"""
Serper API Module
Primary search engine using Google Serper API.
"""

import os
import requests
from typing import List, Dict, Optional


SERPER_API_URL = "https://google.serper.dev/search"


def search_serper(query: str) -> List[Dict[str, str]]:
    """
    Search using Serper API.
    
    Args:
        query: Search query string
        
    Returns:
        List of search results with title and snippet
        Format: [{"title": "...", "snippet": "..."}, ...]
    """
    api_key = os.environ.get("SERPER_API_KEY")
    
    if not api_key:
        # No API key available, return empty results
        return []
    
    if not query:
        return []
    
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "q": query
    }
    
    try:
        response = requests.post(
            SERPER_API_URL,
            json=payload,
            headers=headers,
            timeout=10
        )
        
        if response.status_code != 200:
            return []
        
        data = response.json()
        
        # Extract organic results
        organic = data.get("organic", [])
        
        results = []
        for item in organic:
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            
            if title or snippet:
                results.append({
                    "title": title,
                    "snippet": snippet
                })
        
        return results
        
    except requests.RequestException:
        # Network error or timeout
        return []
    except (KeyError, ValueError):
        # JSON parsing error
        return []
    except Exception:
        # Any other error
        return []


def is_serper_available() -> bool:
    """
    Check if Serper API key is configured.
    
    Returns:
        True if API key is available, False otherwise
    """
    return bool(os.environ.get("SERPER_API_KEY"))
