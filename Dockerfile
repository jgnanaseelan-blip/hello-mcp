FROM python:3.11-slim

WORKDIR /app

# Ensure logs and streams are sent straight to terminal without buffering
ENV PYTHONUNBUFFERED=1

RUN pip install uv

COPY pyproject.toml ./
COPY server.py ./

# Ensure we have a version supporting SSE
RUN uv pip install --system --no-cache chuk-mcp-server>=0.4.4

# Standard port for MCP SSE/HTTP
EXPOSE 8080

# Updated CMD to use the --sse flag we added to server.py
CMD ["python", "server.py", "--sse", "--host", "0.0.0.0", "--port", "8080"]
