"""Example client for Jina AI Search MCP Server using mcp[cli]."""
import asyncio
import os
from typing import Any, Dict, Optional

from mcp import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "https://jina-mcp.onrender.com")
JINA_API_KEY = os.getenv("JINA_API_KEY")


async def main():
    """Run the example client."""
    if not JINA_API_KEY:
        print("Error: JINA_API_KEY environment variable is not set")
        return

    # Initialize the MCP client
    async with Client(
        base_url=MCP_SERVER_URL,
        headers={"Authorization": f"Bearer {JINA_API_KEY}"}
    ) as client:
        # List available tools
        print("\nListing available tools...")
        tools = await client.list_tools()
        print("Available tools:")
        for tool in tools:
            print(f"- {tool['name']}: {tool['description']}")

        # Test the reader tool
        print("\nTesting URL reader...")
        reader_result = await client.execute_tool(
            "jina_reader",
            {
                "url": "https://jina.ai",
                "x_with_links_summary": True,
                "x_with_highlight": True,
            }
        )
        print(f"Reader result: {reader_result}")

        # Test the search tool
        print("\nTesting search...")
        search_result = await client.execute_tool(
            "jina_search",
            {
                "q": "Jina AI",
                "limit": 3,
                "x_with_images": True,
            }
        )
        print(f"Search result: {search_result}")

        # Test streaming (if supported)
        print("\nTesting streaming search...")
        try:
            async for chunk in client.stream_tool(
                "jina_search",
                {
                    "q": "Jina AI",
                    "limit": 2,
                }
            ):
                print(f"Received chunk: {chunk}")
        except Exception as e:
            print(f"Streaming not supported or error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
