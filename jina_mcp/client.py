"""Jina API client implementation with MCP support."""
import asyncio
import json
import logging
import os
from typing import Any, AsyncGenerator, Dict, List, Optional, Union

import httpx
from pydantic import BaseModel, Field, ConfigDict

from .config import JINA_READER_ENDPOINT, JINA_SEARCH_ENDPOINT, settings

# Configure logging
logger = logging.getLogger(__name__)

class MCPStreamEvent(BaseModel):
    """MCP stream event model."""
    event: str
    data: Dict[str, Any]
    
    model_config = ConfigDict(extra='allow')

class MCPStreamHandler:
    """Handler for MCP streaming responses."""
    
    def __init__(self, response: httpx.Response):
        """Initialize with an HTTPX response object."""
        self.response = response
        self.encoding = response.encoding or "utf-8"
    
    async def __aiter__(self) -> AsyncGenerator[MCPStreamEvent, None]:
        """Iterate over SSE events."""
        buffer = b""
        async for chunk in self.response.aiter_bytes():
            buffer += chunk
            while b"\n\n" in buffer:
                event_data, buffer = buffer.split(b"\n\n", 1)
                if not event_data.strip():
                    continue
                    
                event = self._parse_event(event_data)
                if event:
                    yield event
    
    def _parse_event(self, event_data: bytes) -> Optional[MCPStreamEvent]:
        """Parse a single SSE event."""
        try:
            lines = event_data.decode(self.encoding).split("\n")
            event = {"event": "message", "data": {}}
            
            for line in lines:
                if ":" not in line:
                    continue
                    
                field, value = line.split(":", 1)
                field = field.strip()
                value = value.strip()
                
                if field == "event":
                    event["event"] = value
                elif field == "data":
                    try:
                        event["data"] = json.loads(value) if value else {}
                    except json.JSONDecodeError:
                        event["data"] = {"raw": value}
            
            return MCPStreamEvent(**event)
        except Exception as e:
            logger.error(f"Error parsing SSE event: {str(e)}")
            return None


class JinaClient:
    """Client for interacting with Jina AI Search APIs."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize the JinaClient.
        Get your Jina AI API key for free: https://jina.ai/?sui=apikey
        Args:
            api_key: Jina API key. If not provided, will use JINA_API_KEY from environment.
            base_url: (Unused for official APIs)
        """
        self.api_key = api_key or os.environ.get("JINA_API_KEY")
        if not self.api_key:
            raise ValueError("Jina API key is required. Set JINA_API_KEY environment variable.")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.timeout = 60.0

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    async def _make_request(
        self, method: str, path: str, **kwargs
    ) -> Dict[str, Any]:
        """Make an HTTP request to the Jina API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            **kwargs: Additional arguments to pass to the request
            
        Returns:
            Dict containing the JSON response
            
        Raises:
            httpx.HTTPStatusError: If the request fails
        """
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        logger.debug(f"Making {method} request to {url}")
        
        try:
            response = await self.client.request(method, path, **kwargs)
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '')
            if 'application/json' in content_type:
                return response.json()
            else:
                return {"content": response.text}
                
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP error {e.response.status_code}"
            try:
                error_data = e.response.json()
                error_msg = f"{error_msg}: {error_data.get('detail', error_data)}"
            except:
                error_msg = f"{error_msg}: {e.response.text}"
                
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e
        
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            raise

    async def read_url(
        self,
        url: str,
        x_with_links_summary: Optional[bool] = None,
        x_with_metadata: Optional[bool] = None,
        x_with_highlight: Optional[bool] = None,
        x_with_shadow_dom: Optional[bool] = None,
    ) -> str:
        """
        Read content from a URL using Jina's Reader API. Always returns markdown text from response['data']['content'].
        """
        endpoint = "https://r.jina.ai/"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {"url": url}
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(endpoint, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("data", {}).get("content", "")
        except Exception as e:
            logger.error(f"Error calling Jina Reader API: {e}")
            raise

    async def search(
        self,
        q: str,
        limit: int = 5,
        x_with_images: Optional[bool] = None,
        x_with_favicons: Optional[bool] = None,
        x_locale: Optional[str] = None,
    ) -> list:
        """
        Search using Jina's Search API. Always returns a list of results from response['data'].
        """
        endpoint = "https://s.jina.ai/"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {"q": q, "num": limit}
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(endpoint, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("data", [])
        except Exception as e:
            logger.error(f"Error calling Jina Search API: {e}")
            raise

    async def process_mcp_request(
        self, 
        method: str, 
        params: Dict[str, Any], 
        stream: bool = False
    ) -> Union[Dict[str, Any], AsyncGenerator[Dict[str, Any], None]]:
        """
        Process an MCP request by routing to the appropriate method.

        Args:
            method: The MCP method to call
            params: Parameters for the method
            stream: Whether to stream the response

        Returns:
            Dict containing the response data or a stream of chunks
        """
        # Handle MCP protocol methods
        if method == "mcp.discover":
            return {
                "name": "jina-ai-search-mcp",
                "version": "0.1.0",
                "capabilities": ["tools/list", "tools/execute", "stream"],
            }
            
        # Handle Jina API methods
        elif method == "jina_reader":
            return await self.read_url(stream=stream, **params)
            
        elif method == "jina_search":
            return await self.search(stream=stream, **params)
            
        else:
            raise ValueError(f"Unknown MCP method: {method}")
    
    # Context manager support
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
