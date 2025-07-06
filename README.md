# Jina AI Search MCP Server

[![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-blue)](https://modelcontextprotocol.io/)
[![Deployment](https://img.shields.io/badge/Deployment-Render-46e3b7?style=flat-square&logo=render)](https://jina-mcp.onrender.com)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/Meetpatel006/jina-mcp)


> 🚀 **Quick Start**: Try it instantly with Claude Desktop using our hosted endpoint: `https://jina-mcp.onrender.com/sse`

A powerful **Model Context Protocol (MCP)** server implementation that provides seamless access to **Jina AI's Search Foundation API**. This server enables AI assistants and applications to leverage Jina's advanced search, reading, and knowledge retrieval capabilities through a standardized MCP interface.

## 📋 Table of Contents
- [✨ Features](#features)
- [🔧 How it Works](#how-it-works)
- [⚡ Quick Start](#quick-start)
- [📦 Installation](#installation)
- [⚙️ Configuration](#configuration)
- [🔌 MCP Server Setup](#mcp-server-setup)
- [💡 Usage Examples](#usage-examples)
- [📚 API Documentation](#api-documentation)
- [🛠️ Development](#development)
- [🤝 Contributing](#contributing)
- [💬 Support](#support)
- [📄 License](#license)

## ✨ Features

- 🚀 **MCP-compliant server implementation** - Full compatibility with Model Context Protocol
- 🔍 **Jina AI Search & Reader APIs** - Access to powerful AI search and content reading capabilities
- 📚 **DeepWiki Integration** - Enhanced Wikipedia access with AI understanding
- 🏗️ **Clean, modular codebase** - Well-structured and maintainable architecture
- 📖 **Comprehensive documentation** - Detailed guides and API references
- ⚡ **Easy setup** - Simple installation with virtual environment support
- 🔐 **Secure authentication** - OAuth2 Bearer token support
- 🌐 **Real-time processing** - Server-Sent Events (SSE) for live communication

## 🔧 How it Works

The Jina MCP server provides seamless integration with Jina AI's powerful search and reading capabilities through the Model Context Protocol. Here's how you can leverage its features:

### 🔍 **Search with Jina AI**
Ask questions and get comprehensive search results from across the web:
```
"Search for the latest developments in artificial intelligence"
"Find information about sustainable energy solutions"
"What are the recent breakthroughs in quantum computing?"
```

### 🎯 **Use Cases**
- **Research assistance** - Get comprehensive information on any topic
- **Content analysis** - Read and analyze web pages
- **Knowledge discovery** - Explore Wikipedia with AI-enhanced understanding
- **AI assistant integration** - Seamlessly integrate with Claude Desktop and other MCP clients

## ⚡ Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- Jina AI API Key ([Get yours here](https://jina.ai/?sui=apikey))

### Instant Setup with Claude Desktop
Add this configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "jina": {
      "command": "cmd",
      "args": [
        "/c",
        "npx",
        "-y",
        "supergateway",
        "--sse",
        "https://jina-mcp.onrender.com/sse",
        "--oauth2Bearer=your-jina-api-key"
      ]
    }
  }
}
```

**Replace `your-jina-api-key`** with your actual Jina AI API key and restart Claude Desktop!

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Meetpatel006/jina-mcp.git
cd jina-mcp
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Environment Setup
Create a `.env` file in the project root:
```env
JINA_API_KEY=your_jina_api_key_here
```

### Running the Server Locally
```bash
python -m jina_mcp.server
```

## 🔌 MCP Server Setup

### For Claude Desktop (Recommended)
Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "jina": {
      "command": "cmd",
      "args": [
        "/c",
        "npx",
        "-y",
        "supergateway",
        "--sse",
        "https://jina-mcp.onrender.com/sse",
        "--oauth2Bearer=your-jina-api-key"
      ]
    }
  }
}
```

### Local Development Setup
For local development:

```json
{
  "mcpServers": {
    "jina": {
      "command": "python",
      "args": ["-m", "jina_mcp.server"],
      "cwd": "/path/to/jina-mcp",
      "env": {
        "JINA_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Configuration Steps
1. **For Claude Desktop**: Add the configuration to your `claude_desktop_config.json` file
2. **Replace API Key**: Use your actual Jina AI API key
3. **Restart Client**: Restart your MCP client to load the new server

## 💡 Usage Examples

### Basic Search
```python
# Search for information
"Search for Python best practices"
"Find the latest news about AI development"
```

### DeepWiki Queries
```python
# Ask deepwiki for detailed information
"Ask deepwiki about machine learning"
"Ask deepwiki to explain neural networks"
"Ask deepwiki about the Python programming language"
```

### Web Content Analysis
```python
# Read and analyze web content
"Read https://example.com/blog-post"
"Summarize the content from https://research-paper-url.com"
```

## 📚 API Documentation

### Documentation Resources
- [📖 API Documentation](docs/API.md) - Complete API reference
- [🔧 MCP Protocol Documentation](docs/mcp.md) - MCP implementation details
- [🐍 Python SDK Documentation](docs/python-sdk.md) - Python SDK usage
- [🔍 Jina API Documentation](docs/jina-api-docs.md) - Jina AI API reference

### Code Examples
Explore the [examples](examples/) directory:
- [🔧 Client Example](examples/client_example.py) - Basic client implementation
- More examples coming soon!

## 🛠️ Development

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Code formatting
black .

# Linting
flake8 .
```

### Project Structure
```
jina-mcp/
├── jina_mcp/           # Main package
│   ├── __init__.py
│   ├── server.py       # MCP server implementation
│   ├── client.py       # Jina API client
│   ├── config.py       # Configuration management
│   ├── models.py       # Data models
│   └── tools.py        # MCP tools
├── docs/               # Documentation
├── examples/           # Usage examples
├── requirements.txt    # Dependencies
└── README.md          # This file
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### How to Contribute
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add some amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Contribution Guidelines
- Follow the existing code style (use `black` for formatting)
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## 💬 Support

### Get Help
- 📖 [Documentation](docs/) - Comprehensive guides and references
- 🐛 [Issue Tracker](https://github.com/Meetpatel006/jina-mcp/issues) - Report bugs or request features
- 💬 [Discussions](https://github.com/Meetpatel006/jina-mcp/discussions) - Community discussions
- 📧 Contact: [Create an issue](https://github.com/Meetpatel006/jina-mcp/issues/new) for support

### Useful Links
- [🌐 Jina AI Website](https://jina.ai)
- [📋 Model Context Protocol](https://modelcontextprotocol.io/)
- [🖥️ Claude Desktop](https://claude.ai/desktop)

---

<div align="center">

**Made with ❤️ by [Meet Patel](https://github.com/Meetpatel006)**

⭐ Star this repo if you find it helpful! ⭐

</div>
