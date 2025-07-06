"""Configuration settings for the Jina MCP server."""
import os
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Jina API Configuration
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