# Jina AI Search MCP Server

A Model Context Protocol (MCP) server implementation for Jina AI Search Foundation API, providing a standardized interface for interacting with Jina's AI capabilities.

## Features

- MCP-compliant server implementation
- Support for Jina's Reader and Search APIs
- Clean, modular codebase
- Comprehensive documentation
- Easy setup with virtual environment

## Prerequisites

- Python 3.8+
- pip
- Jina AI API Key (Get yours at [Jina AI](https://jina.ai/?sui=apikey))

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/jina-mcp.git
   cd jina-mcp
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the project root:
   ```
   JINA_API_KEY=your_jina_api_key_here
   ```

## Running the Server

```bash
python -m jina_mcp.server
```

## API Documentation

See [API Documentation](docs/API.md) for detailed API reference.

## Development

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Run tests:
   ```bash
   pytest
   ```

## License

MIT
