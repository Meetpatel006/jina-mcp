"""Pydantic models for MCP protocol and Jina API."""
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class MCPError(BaseModel):
    """MCP error object."""

    code: int
    message: str
    data: Optional[Dict[str, Any]] = None


class MCPRequest(BaseModel):
    """MCP request model."""

    jsonrpc: str = "2.0"
    method: str
    params: Optional[Union[Dict[str, Any], List[Any]]] = None
    id: Optional[Union[str, int, float]] = None


class MCPResult(BaseModel):
    """MCP result model."""

    result: Any
    id: Union[str, int, float, None]
    jsonrpc: str = "2.0"


class MCPErrorResponse(BaseModel):
    """MCP error response model."""

    error: MCPError
    id: Union[str, int, float, None]
    jsonrpc: str = "2.0"


class MCPStreamResponse(BaseModel):
    """MCP stream response model."""

    event: str
    data: Dict[str, Any]


class ReaderRequest(BaseModel):
    """Jina Reader API request model."""

    url: str
    x_with_links_summary: Optional[bool] = Field(
        None, alias="X-With-Links-Summary"
    )
    x_with_metadata: Optional[bool] = Field(
        None, alias="X-With-Metadata"
    )
    x_with_highlight: Optional[bool] = Field(
        None, alias="X-With-Highlight"
    )
    x_with_shadow_dom: Optional[bool] = Field(
        None, alias="X-With-Shadow-Dom"
    )


class SearchRequest(BaseModel):
    """Jina Search API request model."""

    q: str
    limit: int = 5
    x_with_images: Optional[bool] = Field(
        None, alias="X-With-Images"
    )
    x_with_favicons: Optional[bool] = Field(
        None, alias="X-With-Favicons"
    )
    x_timeout: Optional[int] = Field(
        None, alias="X-Timeout"
    )
    x_locale: Optional[str] = Field(
        None, alias="X-Locale"
    )


class SearchResult(BaseModel):
    """Jina Search API result model."""

    title: str
    url: str
    snippet: Optional[str] = None
    favicon: Optional[str] = None
    image: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class SearchResponse(BaseModel):
    """Jina Search API response model."""

    results: List[SearchResult]
    query: str
    total_results: int
    search_time: float
