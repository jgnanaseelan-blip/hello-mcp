FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml ./
COPY server.py ./

# Install dependencies using uv
RUN uv pip install --system --no-cache chuk-mcp-server>=0.4.4

# Expose HTTP port
EXPOSE 8000

# Run server in HTTP mode for web/API access
CMD ["python", "server.py", "--port", "8000", "--host", "0.0.0.0", "http" ]
