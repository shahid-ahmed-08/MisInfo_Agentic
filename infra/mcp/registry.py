import logging
from typing import Any, Dict

logger = logging.getLogger("mcp_registry")

# canonical shared registry for MCP tools
TOOL_REGISTRY: Dict[str, Dict[str, Any]] = {}


def register_tool(name: str, description: str = ""):
    def decorator(fn):
        TOOL_REGISTRY[name] = {"func": fn, "description": description}
        logger.info(f"[registry] Registered tool: {name}")
        return fn

    return decorator


def list_tools():
    return {name: {"description": TOOL_REGISTRY[name]["description"]} for name in TOOL_REGISTRY}

