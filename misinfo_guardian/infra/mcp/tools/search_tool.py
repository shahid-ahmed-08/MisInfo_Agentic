import os, sys

# ----- Fix Python import path for backend -----
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

BACKEND_PATH = os.path.join(PROJECT_ROOT, "backend")
if BACKEND_PATH not in sys.path:
    sys.path.insert(0, BACKEND_PATH)

# ----- Import canonical MCP tool registry -----
from infra.mcp.registry import register_tool

# ----- Import the resilient search_manager from backend -----
from backend.tools.search_manager import search_manager


@register_tool("search", description="Search web using resilient search_manager")
def search_tool(query: str):
    """
    MCP search wrapper.
    Calls resilient backend.tools.search_manager(query).
    ALWAYS returns a list.
    NEVER raises exceptions.
    """
    try:
        results = search_manager(query)
        return results or []
    except Exception as e:
        print("search_tool error:", e)
        return []
