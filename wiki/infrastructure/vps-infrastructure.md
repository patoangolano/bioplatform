---
title: Infraestrutura VPS
slug: vps-infrastructure
type: infrastructure
status: active
created: 2026-06-24
updated: 2026-06-24
tags: [vps, hostinger, docker, caddy, deploy]
related_pages: [[project-status]] [[project-architecture]] [[mcp-server-ecosystem]] [[docker-and-reproducibility]]
---

# Infraestrutura VPS

Infraestrutura de produção na Hostinger.

## VPS

| Propriedade | Valor |
|-------------|-------|
| Modelo | KVM 4 |
| vCPUs | 4 |
| RAM | 16 GB |
| Disco | 200 GB NVMe |
| SO | Ubuntu 24.04 com Docker e Traefik (template) |
| IP | 187.77.232.5 |
| Hostname | srv1768048.hstgr.cloud |
| Domínio | bio.quackai.com.br |
| Firewall | Portas 22, 80, 443, 3000, 11434 |
| Acesso SSH | Chave ED25519 `cursor-devops-vps` |

## Containers em produção (21)

### bioplatform (5 containers)
| Container | Imagem | Porta |
|-----------|--------|-------|
| bioplatform-caddy-1 | caddy:2-alpine | 80, 443 |
| bioplatform-api-1 | bioplatform-api | 8000 (interno) |
| bioplatform-worker-1 | bioplatform-worker | — |
| bioplatform-postgres-1 | postgres:16-alpine | 5432 (interno) |
| bioplatform-redis-1 | redis:7-alpine | 6379 (interno) |

### PostgreSQL externo (1)
| Container | Imagem | Porta |
|-----------|--------|-------|
| postgres | postgres:16-alpine | 5432 |

### MCP servers (15)
Ver [[mcp-server-ecosystem]].

## Rede

- Rede Docker `bioplatform_bionet` (bridge) — conecta Caddy, API, worker, Postgres, Redis e todos os containers MCP
- Volume `mcp-data` — compartilhado entre containers MCP para `/tmp/mcp-work`
- Caddy reverse proxy com 15 rotas `handle_path` para servidores MCP

## Deploy

- **Método:** GitHub Actions → SSH deploy → `docker compose up -d`
- **Compose files:**
  - `/opt/bioplatform/docker-compose.yml` — bioplatform (API, worker, DB, Redis, Caddy)
  - `/opt/mcp-bio/docker-compose.yml` — servidores MCP
- **Caddyfile:** `/opt/bioplatform/infra/caddy/Caddyfile`

## Uso de recursos

| Recurso | Uso |
|---------|-----|
| RAM | ~2 GB / 16 GB (12%) |
| CPU | ~2% ocioso |
| Disco | ~8 GB / 200 GB (4%) |
