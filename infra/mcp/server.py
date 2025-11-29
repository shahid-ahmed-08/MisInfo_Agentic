import os
import sys
import logging
import importlib
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Resolve project root and ensure backend is on path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
BACKEND_PATH = os.path.join(PROJECT_ROOT, "backend")
if BACKEND_PATH not in sys.path:
    sys.path.insert(0, BACKEND_PATH)

# internal imports
from infra.mcp import registry

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("mcp_server")

API_KEY = os.getenv("MCP_API_KEY", "")

app = FastAPI(title="Local MCP Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ToolCall(BaseModel):
    args: List[Any] = []
    kwargs: Dict[str, Any] = {}


# auto-load local tools (import module to trigger registration into registry.TOOL_REGISTRY)
def load_local_tools():
    try:
        importlib.import_module("infra.mcp.tools.search_tool")
        logger.info("Auto-imported infra.mcp.tools.search_tool")
    except Exception as e:
        logger.exception("Failed to auto-import infra.mcp.tools.search_tool: %s", e)


# endpoints
@app.get("/tools")
def list_tools():
    return registry.list_tools()


@app.post("/tools/{tool_name}/call")
async def call_tool(tool_name: str, payload: ToolCall, request: Request, x_api_key: str | None = Header(None)):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid MCP API KEY")

    entry = registry.TOOL_REGISTRY.get(tool_name)
    if not entry:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

    fn = entry["func"]

    try:
        result = fn(*payload.args, **payload.kwargs)
        if hasattr(result, "__await__"):
            result = await result
    except Exception as e:
        logger.exception("Tool execution error")
        raise HTTPException(status_code=500, detail=str(e))

    return {"tool": tool_name, "result": result}


@app.get("/health")
def health():
    return {"status": "ok", "tools": list(registry.TOOL_REGISTRY.keys())}


# startup: ensure tools are loaded and print routes and registry
@app.on_event("startup")
def startup_event():
    logger.info("Starting MCP server. Loading tools...")
    load_local_tools()
    logger.info("TOOL_REGISTRY contains: %s", list(registry.TOOL_REGISTRY.keys()))
    # debug: print routes after server initialization (will also print on reload)
    for route in app.routes:
        try:
            logger.info("ROUTE: %s → %s", route.path, route.methods)
        except Exception:
            pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8001)

