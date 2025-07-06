"""Jina AI MCP Server with SSE support."""
import asyncio
import json
import logging
import uuid
from typing import Any, Dict, List, Optional, AsyncGenerator

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse
from fastapi import Request, Response, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings, DOCS_HTML
from .client import JinaClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store connected SSE clients
sse_clients = set()

# Initialize Jina client
jina_client = JinaClient()

# Initialize MCP
mcp = FastMCP(
    "jina-ai-search",
    dependencies=["mcp[cli]>=1.9.3"],
    cors_origins=["*"],
    host=settings.host,
    port=settings.port,
    debug=settings.debug,
    log_level=settings.log_level  # Already in uppercase from config
)

# Create FastAPI app
app = FastAPI(
    title="Jina MCP Server",
    description="Jina AI Model Context Protocol server with SSE support",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the SSE transport for MCP at '/sse/'
app.mount("/sse", mcp.sse_app())

# Tool Definitions

@mcp.tool(
    name="jina_reader",
    description="Read content from a URL using Jina's Reader API"
)
async def read_url(
    url: str
) -> Dict[str, Any]:
    """Read content from a URL using Jina's Reader API."""
    try:
        response = await jina_client.read_url(url)
        return {"result": {"content": response}}
    except Exception as e:
        error_msg = f"Error reading URL {url}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise e

@mcp.tool(
    name="jina_search",
    description="Search using Jina's Search API"
)
async def search(
    q: str
) -> dict:
    """Search using Jina's Search API."""
    try:
        result = await jina_client.search(q)
        return {"result": result}
    except Exception as e:
        error_msg = f"Search failed: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise ToolError(error_msg)

# Tools are registered with the @mcp.tool decorator

# SSE Event Generator
async def event_generator(request: Request) -> AsyncGenerator[Dict[str, str], None]:
    """Generate server-sent events."""
    client_id = str(uuid.uuid4())
    queue = asyncio.Queue()
    sse_clients.add(queue)
    
    try:
        # Send initial connection event
        yield {
            "event": "connection",
            "data": json.dumps({"client_id": client_id, "status": "connected"})
        }
        
        # Keep connection alive
        while True:
            if await request.is_disconnected():
                logger.info(f"Client {client_id} disconnected")
                break
                
            try:
                # Wait for a message with timeout
                message = await asyncio.wait_for(queue.get(), timeout=30)
                yield message
            except asyncio.TimeoutError:
                # Send a keep-alive ping
                yield {"event": "ping", "data": ""}
                
    except asyncio.CancelledError:
        logger.info(f"Client {client_id} connection cancelled")
    finally:
        sse_clients.remove(queue)

# Broadcast message to all connected clients
async def broadcast_message(event: str, data: Dict[str, Any]):
    """Broadcast a message to all connected SSE clients."""
    message = {
        "event": event,
        "data": json.dumps(data),
        "id": str(uuid.uuid4()),
        "retry": 30000  # 30 seconds
    }
    
    for queue in list(sse_clients):
        await queue.put(message)

# SSE endpoint
@app.get("/sse")
async def sse_endpoint(request: Request):
    """SSE endpoint for real-time updates."""
    return EventSourceResponse(event_generator(request))

# Root endpoint for documentation
@app.get("/", response_class=Response)
async def root():
    """Serve the HTML documentation page."""
    return Response(content=DOCS_HTML, media_type="text/html")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "jina-mcp"}

# MCP discovery endpoint
@app.get("/.well-known/mcp.json")
async def mcp_discovery() -> Dict[str, Any]:
    """MCP discovery endpoint with SSE support."""
    return mcp.discovery_document()

def run_server():
    """Run the MCP server with SSE support."""
    logger.info(f"Starting Jina MCP Server with SSE on {settings.host}:{settings.port}")
    logger.info(f"API Base URL: {settings.jina_api_base}")
    logger.info(f"Debug Mode: {settings.debug}")
    logger.info(f"SSE Endpoint: http://{settings.host}:{settings.port}/sse")
    logger.info(f"MCP Endpoint: http://{settings.host}:{settings.port}/mcp")
    
    # Run the MCP server
    mcp.run(transport="sse")

if __name__ == "__main__":
    run_server()
