# Observabilidade — Prometheus + Grafana

Stack de monitoramento da bioplatform, separado do compose principal para nunca
arriscar o deploy de produção. Coleta métricas de host (node-exporter) e de
containers (cAdvisor), armazena no Prometheus e visualiza no Grafana.

## Subir na VPS

Depois que o stack principal estiver rodando (`/opt/bioplatform`):

```bash
cd /opt/bioplatform
docker compose -f infra/monitoring/docker-compose.monitoring.yml --env-file .env up -d
```

A rede `bioplatform_bionet` (criada pelo compose principal) é reutilizada como
`external`, então o Prometheus enxerga os containers da aplicação pelo nome.

## Acesso (seguro — sem expor portas novas à internet)

Grafana e Prometheus escutam apenas em `127.0.0.1`. Acesse via túnel SSH:

```bash
ssh -L 3000:127.0.0.1:3000 -L 9090:127.0.0.1:9090 root@187.77.232.5
```

- Grafana:    http://localhost:3000  (admin / `GRAFANA_ADMIN_PASSWORD` do `.env`)
- Prometheus: http://localhost:9090

> Princípio de secops do projeto: mínimo de portas expostas. Para publicar o
> Grafana com TLS, adicione um subdomínio (ex.: `grafana.quackai.com.br`) e uma
> rota no Caddy — não abra a porta 3000 ao mundo sem autenticação + HTTPS.

## Dashboards

O datasource Prometheus já vem provisionado. Importe os dashboards da comunidade
em **Dashboards → New → Import**:

| ID    | Dashboard                          |
|-------|------------------------------------|
| 1860  | Node Exporter Full (host)          |
| 19792 | cAdvisor / Docker containers       |

## Métricas de aplicação (follow-up)

O FastAPI ainda não expõe `/metrics`. Para métricas de aplicação (latência,
throughput, erros por rota), adicionar `prometheus-fastapi-instrumentator` à API
e um job de scrape para `api:8000` no `prometheus/prometheus.yml`.
