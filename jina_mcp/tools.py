"""MCP Tools implementation for Jina AI Search."""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .client import JinaClient


class ToolParameter(BaseModel):
    """Parameter definition for MCP tools."""
    name: str
    type: str
    description: str
    required: bool = False
    default: Any = None


class ToolDefinition(BaseModel):
    """MCP tool definition."""
    name: str
    description: str
    parameters: List[ToolParameter]
    required: List[str] = []
    returns: Dict[str, str] = {"type": "object", "description": "Tool execution result"}


class JinaTools:
    """Jina AI Tools implementation for MCP."""

    def __init__(self, client: JinaClient):
        """Initialize with a JinaClient instance."""
        self.client = client
        self._tools = self._get_tools()

    def _get_tools(self) -> Dict[str, ToolDefinition]:
        """Get all available tools."""
        return {
            "jina.reader": self._get_reader_tool(),
            "jina.search": self._get_search_tool(),
        }

    def _get_reader_tool(self) -> ToolDefinition:
        """Get the reader tool definition."""
        return ToolDefinition(
            name="jina.reader",
            description="Read content from a URL using Jina's Reader API",
            parameters=[
                ToolParameter(
                    name="url",
                    type="string",
                    description="The URL to read content from",
                    required=True,
                ),
            ],
            required=["url"],
        )

    def _get_search_tool(self) -> ToolDefinition:
        """Get the search tool definition."""
        return ToolDefinition(
            name="jina.search",
            description="Search using Jina's Search API",
            parameters=[
                ToolParameter(
                    name="q",
                    type="string",
                    description="The search query",
                    required=True,
                ),
            ],
            required=["q"],
        )

    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools."""
        return [tool.dict() for tool in self._tools.values()]

    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        """Get a specific tool by name."""
        return self._tools.get(name)

    async def execute_tool(
        self, name: str, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a tool with the given parameters.

        Args:
            name: Name of the tool to execute
            parameters: Parameters for the tool

        Returns:
            Tool execution result
        """
        if name == "jina.reader":
            return await self.client.read_url(**parameters)
        elif name == "jina.search":
            return await self.client.search(**parameters)
        else:
            raise ValueError(f"Unknown tool: {name}")
