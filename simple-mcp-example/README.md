# Simple MCP Example

This repository demonstrates how to implement a Model Context Protocol (MCP) server and client using FastAPI and Pydantic AI. It provides a practical example of building an extensible MCP solution that can be integrated into various AI workflows.

## What is MCP?

The Model Context Protocol (MCP) provides a standardized way to define how an LLM interacts with tools. Instead of defining tools on a one-off basis in LLM applications, we can utilize prebuilt or custom servers that expose tools. This allows for both reusability for servers we may build ourselves or plugging into various vendor or open source MCP servers - preventing us from reinventing the wheel when we want to use a new tool.

For more information, check out:
- [Anthropic's release post](https://www.anthropic.com/news/model-context-protocol)
- [The model context protocol site](https://modelcontextprotocol.io/introduction)
- [Python SDK GitHub repo](https://github.com/modelcontextprotocol/python-sdk)

## Features

- FastAPI-based MCP server implementation
- Server-Sent Events (SSE) transport for streaming
- Tool integration and handling
- Pydantic AI integration
- Simple client implementation for testing

## Prerequisites

- Python 3.11+
- FastAPI and related dependencies
- MCP SDK

## Installation

1. Clone the repository and cd into simple-mcp-example:
```bash
git clone https://github.com/bstuddard/python-examples.git
cd simple-mcp-example
```

2. Create a virtual environment and activate it (venv, conda, etc)

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure
- src/
   - build_mcp/
      - create_mcp.py # MCP server creation and tool definitions
   - startup/
      - app.py # FastAPI application setup
      - routes.py # API routes
      - mcp.py # MCP server integration with FastAPI
   - test_mcp/
      - client.py # Simple MCP client for testing
      - pydantic_stream_example.py # Pydantic AI integration example
   - main.py # Application entry point
   - load_config.py # Configuration loading
- requirements.txt # Project dependencies

## Key Components

The project includes several key components:

1. **MCP Server** (`build_mcp/create_mcp.py`)
   - Tool definitions and server setup
   - Example tool implementation (get_user_name)
   - Uses FastMCP class for server creation

2. **FastAPI Integration** (`startup/mcp.py`)
   - SSE transport setup
   - MCP server mounting to FastAPI as a sub-application
   - Endpoint setup for SSE connections

3. **MCP Client** (`test_mcp/client.py`)
   - Simple client implementation for testing
   - Tool calling demonstration
   - Connection to SSE endpoint

4. **Pydantic AI Integration** (`test_mcp/pydantic_stream_example.py`)
   - Event handling and streaming
   - Structured message parsing
   - Integration with LLM APIs

## Dependencies

Key dependencies include:
- fastapi
- uvicorn[standard]
- mcp[cli]
- pydantic-ai[logfire]
- anthropic

See `requirements.txt` for a complete list of dependencies.

## Usage

1. Start the FastAPI server:
```bash
uvicorn src.main:app --reload --host 127.0.0.1
```

2. In a separate terminal, run the MCP client to test:
```bash
python src/test_mcp/client.py
```

3. To use with Pydantic AI, initialize the agent with MCP servers:
```python
from pydantic_ai.mcp import MCPServerHTTP

# Setup mcp server objects for pydantic
pydantic_mcp_server = MCPServerHTTP(url='http://127.0.0.1:8000/sse')
pydantic_mcp_servers = [pydantic_mcp_server]

agent = Agent(  
    'anthropic:claude-3-5-sonnet-20241022',
    system_prompt=(
        "You are a helpful assistant that can answer questions and help with tasks. Greet the user by name first before answering any questions."
    ),
    mcp_servers=pydantic_mcp_servers
)
```

## Additional Resources

- [MCP Documentation](https://github.com/modelcontextprotocol/spec)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic AI Documentation](https://ai.pydantic.dev/)
- [Blog Post: MCP with Pydantic AI](https://datastud.dev/posts/pydantic-ai-mcp) 