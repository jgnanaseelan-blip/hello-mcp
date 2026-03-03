FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml ./
COPY server.py ./

RUN uv pip install --system --no-cache chuk-mcp-server>=0.4.4

EXPOSE 8080

CMD ["python", "server.py", "--http", "--host", "0.0.0.0", "--port", "8080"]