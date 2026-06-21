FROM python:3.11-slim AS builder

WORKDIR /app

COPY apps/worker/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

COPY --from=builder /install /usr/local
COPY apps/worker/ .
COPY mcp_servers/ /app/mcp_servers/

RUN chown -R appuser:appgroup /app

USER appuser

CMD ["python", "-m", "arq", "main.WorkerSettings"]
