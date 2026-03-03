"""
hello-mcp - MCP Server

A custom MCP server built with ChukMCPServer.

Features demonstrated:
- Tools: Actions Claude can perform
- Resources: Data Claude can read
- Prompts: Reusable prompt templates
- Async support: For I/O operations
- Context: Session and user tracking (optional)
- OAuth: Authentication support (optional)
"""

from chuk_mcp_server import tool, resource, prompt, run


# ============================================================================
# Tools - Actions Claude Can Perform
# ============================================================================

@tool
def hello(name: str = "World") -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"


@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@tool
def calculate(expression: str) -> str:
    """Safely evaluate a mathematical expression."""
    try:
        # Only allow safe operations
        allowed = {'+', '-', '*', '/', '(', ')', '.', ' '} | set('0123456789')
        if not all(c in allowed for c in expression):
            return "Error: Invalid characters in expression"

        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"


# Example async tool (commented out - uncomment to use)
# @tool
# async def fetch_data(url: str) -> dict:
#     """Fetch data from a URL asynchronously."""
#     import httpx
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url)
#         return {"status": response.status_code, "data": response.json()}


# ============================================================================
# Resources - Data Claude Can Read
# ============================================================================

@resource("config://info")
def server_info() -> dict:
    """Get server information."""
    return {
        "name": "hello-mcp",
        "version": "0.1.0",
        "description": "Custom MCP server built with ChukMCPServer"
    }


@resource("config://capabilities")
def server_capabilities() -> dict:
    """Get server capabilities and features."""
    return {
        "features": ["tools", "resources", "prompts"],
        "transport": "stdio/http",
        "async_support": True,
        "oauth_support": False,  # Set to True if using OAuth
    }


# ============================================================================
# Prompts - Reusable Prompt Templates
# ============================================================================

@prompt
def code_review(code: str, language: str = "python") -> str:
    """Generate a code review prompt."""
    return f"""Please review this {language} code:

```{language}
{code}
```

Provide feedback on:
1. Code quality and readability
2. Potential bugs or issues
3. Best practices
4. Performance improvements
5. Security considerations
"""


@prompt
def explain_code(code: str, language: str = "python") -> str:
    """Generate a prompt to explain code."""
    return f"""Please explain what this {language} code does:

```{language}
{code}
```

Include:
- Overall purpose
- Step-by-step breakdown
- Key concepts used
- Potential use cases
"""


# ============================================================================
# OAuth & Context Example (commented out - uncomment to use)
# ============================================================================

# from chuk_mcp_server import requires_auth, get_user_id
#
# @tool
# @requires_auth()
# async def create_user_resource(
#     name: str,
#     _external_access_token: str | None = None
# ) -> dict:
#     """Create a user-specific resource (requires OAuth)."""
#     # Get authenticated user ID
#     from chuk_mcp_server import require_user_id
#     user_id = require_user_id()
#
#     # Use the access token to call external API
#     # headers = {"Authorization": f"Bearer {_external_access_token}"}
#
#     return {
#         "created": name,
#         "owner": user_id,
#         "status": "success"
#     }


if __name__ == "__main__":
    import argparse
    import sys

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="hello-mcp - MCP Server")
    parser.add_argument("--stdio", action="store_true", help="Force STDIO transport mode")
    parser.add_argument("--http", action="store_true", help="Force HTTP transport mode")
    parser.add_argument("--port", type=int, default=None, help="Port for HTTP mode")
    parser.add_argument("--host", default=None, help="Host for HTTP mode")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument(
        "--log-level",
        default="warning",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Logging level (default: warning)",
    )
    parser.add_argument("--transport", choices=["stdio", "http"], help="Transport mode")

    args = parser.parse_args()

    # Determine transport mode
    if args.stdio or args.transport == "stdio":
        # Stdio mode
        run(transport="stdio", debug=args.debug, log_level=args.log_level)
    elif args.http or args.port or args.host or args.transport == "http":
        # HTTP mode
        run(
            transport="http",
            host=args.host,
            port=args.port,
            debug=args.debug,
            log_level=args.log_level,
        )
    else:
        # Default to stdio mode (best for Claude Desktop)
        run(transport="stdio", log_level=args.log_level)
