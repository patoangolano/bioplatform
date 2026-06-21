FROM python:3.11-slim AS builder

WORKDIR /app

COPY apps/api/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

COPY --from=builder /install /usr/local

# Código da API
COPY apps/api/ .

# Módulos compartilhados (adapters bioinformáticos)
COPY mcp_servers/ /app/mcp_servers/
COPY services/ /app/services/

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
