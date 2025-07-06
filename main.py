from jina_mcp.server import app
if __name__ == "__main__":
    from jina_mcp import server
    print("Starting Jina MCP server with SSE transport...")
    server.mcp.run(transport="sse") 