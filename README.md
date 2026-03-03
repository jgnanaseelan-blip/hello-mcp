# hello-mcp

MCP server built with [ChukMCPServer](https://github.com/chrishayuk/chuk-mcp-server).

## Transport Modes

This server supports two transport modes:

- **STDIO (default)**: For Claude Desktop and MCP clients. Communication via stdin/stdout.
- **HTTP**: For web applications, APIs, and cloud deployment. RESTful endpoints with streaming support.

## Quick Start

### Option 1: Claude Desktop (STDIO mode)

#### 1. Install dependencies
```bash
# Install globally
uv pip install --system chuk-mcp-server

# Or in a virtual environment (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install chuk-mcp-server
```

#### 2. Test the server
```bash
# Default mode is stdio - perfect for Claude Desktop
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python server.py
```

#### 3. Configure Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "hello-mcp": {
      "command": "uv",
      "args": ["--directory", "C:\Users\Administrator\Downloads\mcpserver\hello-mcp", "run", "server.py"]
    }
  }
}
```

Restart Claude Desktop and your server will be available!

### Option 2: Web/API (HTTP mode)

Perfect for web applications and cloud deployment.

```bash
# Start HTTP server on port 8000
python server.py --http

# Or specify custom port/host
python server.py --port 8000 --host 0.0.0.0
```

Test with curl:
```bash
curl http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

### Option 3: Docker (Production Deployment)

Docker automatically runs the server in HTTP mode, suitable for containerized deployments.

#### Using docker-compose (easiest)
```bash
docker-compose up
```

#### Or build manually
```bash
# Build the image
docker build -t hello-mcp .

# Run the container
docker run -p 8000:8000 hello-mcp
```

#### Test the deployment
```bash
curl http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

You should see:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {"name": "hello", "description": "Say hello to someone."},
      {"name": "add_numbers", "description": "Add two numbers together."},
      {"name": "calculate", "description": "Safely evaluate a mathematical expression."}
    ]
  }
}
```

Perfect for deploying to cloud platforms like AWS, GCP, Azure, or Kubernetes!

## Available Tools

- **hello**: Say hello to someone
- **add_numbers**: Add two numbers together
- **calculate**: Safely evaluate a mathematical expression

## Available Resources

- **config://info**: Get server information
- **config://capabilities**: Get server capabilities and features

## Available Prompts

- **code_review**: Generate a code review prompt for any language
- **explain_code**: Generate a prompt to explain code

## Features

This scaffolded server demonstrates:

- **Tools**: Sync and async functions Claude can call
- **Resources**: Static and dynamic data Claude can read
- **Prompts**: Reusable prompt templates
- **Type Safety**: Automatic schema generation from type hints
- **Dual Transport**: STDIO for Claude Desktop, HTTP for web/APIs
- **OAuth** (commented): Authentication example included (uncomment to use)
- **Context** (commented): Session and user tracking example (uncomment to use)

### Adding OAuth Authentication

To add OAuth support:

1. Uncomment the OAuth example in `server.py`
2. Implement your OAuth provider (see [OAuth docs](https://github.com/chrishayuk/chuk-mcp-server/blob/main/docs/OAUTH.md))
3. Update `server_capabilities()` to set `"oauth_support": True`

### Using Context Management

To use context management (sessions, user tracking):

1. Uncomment the context example in `server.py`
2. Use `get_user_id()` to check authentication (optional)
3. Use `require_user_id()` to enforce authentication (raises error if not authenticated)
4. Use `get_session_id()` to track MCP sessions

## Development

### Run tests
```bash
uv run pytest
```

### Type checking
```bash
uv run mypy server.py
```

### Linting
```bash
uv run ruff check .
```

## Command-Line Options

The server automatically detects the best transport mode, but you can override:

```bash
# Force STDIO mode (default)
python server.py --stdio
python server.py --transport=stdio

# Force HTTP mode
python server.py --http
python server.py --port 8000
python server.py --host 0.0.0.0
python server.py --transport=http
```

## Customization

Edit `server.py` to add your own tools, resources, and prompts:

```python
from chuk_mcp_server import tool, resource, prompt, run

# Add your custom tool
@tool
def my_custom_tool(param: str) -> str:
    """Your custom tool description."""
    return f"Result: {param}"

# Add your custom resource
@resource("custom://data")
def my_resource() -> dict:
    """Your custom resource."""
    return {"data": "value"}

# Add your custom prompt
@prompt
def my_prompt_template(topic: str) -> str:
    """Custom prompt template."""
    return f"Please write about: {topic}"

# Add async tools for I/O operations
@tool
async def fetch_api(url: str) -> dict:
    """Fetch data from API asynchronously."""
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

if __name__ == "__main__":
    run(transport="stdio")  # or just run() for auto-detection
```

### Advanced Features

For OAuth authentication, context management, and more advanced features, see:

- [ChukMCPServer Documentation](https://github.com/chrishayuk/chuk-mcp-server)
- [OAuth Guide](https://github.com/chrishayuk/chuk-mcp-server/blob/main/docs/OAUTH.md)
- [Context Architecture](https://github.com/chrishayuk/chuk-mcp-server/blob/main/docs/CONTEXT_ARCHITECTURE.md)
- [Example: LinkedIn OAuth Integration](https://github.com/chrishayuk/chuk-mcp-linkedin)
