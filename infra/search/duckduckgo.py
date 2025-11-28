"""
DuckDuckGo Search Module
Fallback search engine using DuckDuckGo HTML parser.
"""

import re
import requests
from typing import List, Dict
from urllib.parse import quote_plus


DDG_HTML_URL = "https://duckduckgo.com/html/"


def search_duckduckgo(query: str) -> List[Dict[str, str]]:
    """
    Search using DuckDuckGo HTML interface.
    
    Args:
        query: Search query string
        
    Returns:
        List of search results with title and snippet
        Format: [{"title": "...", "snippet": "..."}, ...]
    """
    if not query:
        return []
    
    # Encode query for URL
    encoded_query = quote_plus(query)
    url = f"{DDG_HTML_URL}?q={encoded_query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return []
        
        html = response.text
        
        # Parse results using regex
        results = parse_ddg_html(html)
        
        return results
        
    except requests.RequestException:
        # Network error or timeout
        return []
    except Exception:
        # Any other error
        return []


def parse_ddg_html(html: str) -> List[Dict[str, str]]:
    """
    Parse DuckDuckGo HTML results.
    
    Args:
        html: Raw HTML content from DuckDuckGo
        
    Returns:
        List of parsed results
    """
    results = []
    
    # Pattern to match result blocks
    # DuckDuckGo HTML structure: <div class="result">
    result_pattern = r'<div class="result[^"]*"[^>]*>(.*?)</div>\s*</div>'
    result_blocks = re.findall(result_pattern, html, re.DOTALL)
    
    for block in result_blocks[:10]:  # Limit to first 10 results
        # Extract title
        title_match = re.search(r'class="result__title"[^>]*>.*?<a[^>]*>(.*?)</a>', block, re.DOTALL)
        title = ""
        if title_match:
            title = clean_html(title_match.group(1))
        
        # Extract snippet
        snippet_match = re.search(r'class="result__snippet"[^>]*>(.*?)</a>', block, re.DOTALL)
        snippet = ""
        if snippet_match:
            snippet = clean_html(snippet_match.group(1))
        
        if title or snippet:
            results.append({
                "title": title,
                "snippet": snippet
            })
    
    return results


def clean_html(text: str) -> str:
    """
    Remove HTML tags and clean text.
    
    Args:
        text: HTML text
        
    Returns:
        Cleaned plain text
    """
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Decode HTML entities
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    text = text.replace('&nbsp;', ' ')
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()
