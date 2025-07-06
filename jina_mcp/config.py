"""Configuration settings for the Jina MCP server."""
import os
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Jina API Configuration
    jina_api_key: str = Field(..., env="JINA_API_KEY")
    jina_api_base: str = Field(
        "https://api.jina.ai",  # Hardcoded Jina API base URL
        description="Base URL for Jina API",
    )

    # Server Configuration
    host: str = Field("0.0.0.0", description="Host to bind the server to")
    port: int = Field(8000, description="Port to bind the server to")
    debug: bool = Field(False, description="Enable debug mode")
    log_level: str = Field(
        "INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
        pattern=r'^(?i)(debug|info|warning|error|critical)$',
        to_upper=True
    )
    
    # MCP Server Configuration
    mcp_server_url: str = Field(
        "http://localhost:8000",
        description="Base URL for the MCP server"
    )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }


# Global settings instance
settings = Settings()

# Jina API endpoints
JINA_READER_ENDPOINT = f"{settings.jina_api_base}/v1/reader"
JINA_SEARCH_ENDPOINT = f"{settings.jina_api_base}/v1/search"

# Server configuration
SERVER_CONFIG = {
    "host": settings.host,
    "port": settings.port,
    "debug": settings.debug,
    "log_level": settings.log_level
}

# MCP Server Info
MCP_SERVER_INFO = {
    "name": "jina-ai-search-mcp",
    "version": "0.1.0",
    "capabilities": ["reader", "search"],
}

# Documentation
DOCS_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jina AI MCP Server</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        h1, h2 {
            color: #2c3e50;
        }
        pre {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        code {
            background: #f5f5f5;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 0.9em;
        }
        .section {
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
        }
        .endpoint {
            background: #f9f9f9;
            padding: 15px;
            border-left: 4px solid #3498db;
            margin: 15px 0;
        }
    </style>
</head>
<body>
    <h1>Jina AI MCP Server</h1>
    
    <div class="section">
        <h2>About</h2>
        <p>This is a Model Context Protocol (MCP) server that provides access to Jina AI's search and reader APIs.</p>
    </div>

    <div class="section">
        <h2>Endpoints</h2>
        
        <div class="endpoint">
            <h3>SSE Stream</h3>
            <p><code>GET /sse</code> - Server-Sent Events stream for real-time updates</p>
            <p>Example usage with JavaScript:</p>
            <pre><code>const eventSource = new EventSource('http://localhost:8000/sse');
eventSource.onmessage = (event) => {
    console.log('New event:', JSON.parse(event.data));
};</code></pre>
        </div>

        <div class="endpoint">
            <h3>Search</h3>
            <p><code>POST /search</code> - Perform a search query</p>
            <p>Example request:</p>
            <pre><code>{
    "method": "jina.search",
    "params": {
        "q": "your search query",
        "limit": 5
    }
}</code></pre>
        </div>

        <div class="endpoint">
            <h3>Read URL</h3>
            <p><code>POST /read</code> - Read content from a URL</p>
            <p>Example request:</p>
            <pre><code>{
    "method": "jina.reader",
    "params": {
        "url": "https://example.com"
    }
}</code></pre>
        </div>
    </div>

    <div class="section">
        <h2>Integration with Claude Desktop/IDE</h2>
        <p>To use this MCP server with Claude Desktop or your IDE:</p>
        <ol>
            <li>Make sure the server is running</li>
            <li>In your Claude Desktop/IDE settings, add a new MCP server with URL: <code>http://localhost:8000</code></li>
            <li>Ensure your <code>JINA_API_KEY</code> is set in the environment variables</li>
        </ol>
    </div>

    <div class="section">
        <h2>Available Tools</h2>
        <ul>
            <li><strong>jina.search</strong>: Search the web using Jina AI</li>
            <li><strong>jina.reader</strong>: Read content from a URL using Jina's reader</li>
        </ul>
    </div>
</body>
</html>
"""
