FROM python:3.11-slim

WORKDIR /app

COPY apps/workflows/requirements.txt /app/workflows-requirements.txt
COPY requirements-mcp.txt /app/requirements-mcp.txt

RUN pip install --no-cache-dir -r workflows-requirements.txt -r requirements-mcp.txt

COPY mcp_servers/ /app/mcp_servers/
COPY apps/workflows/ /app/apps/workflows/

ENV PYTHONPATH=/app
CMD ["prefect", "worker", "start", "--pool", "bioplatform-pool"]
