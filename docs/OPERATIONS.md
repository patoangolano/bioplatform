# Guia de Operações — bioplatform

## Pré-requisitos

- Docker Engine 24+ e Docker Compose v2
- Git
- Acesso SSH à VPS (para deploy remoto)

## Setup Local

```bash
git clone <repo-url> bioplatform
cd bioplatform
cp .env.example .env
# Edite .env com suas credenciais locais
docker compose up -d
```

Acesse: http://localhost:8000/health

## Deploy na VPS Hostinger

1. Provisionar a VPS (Ubuntu 22.04+):
```bash
scp infra/scripts/bootstrap-vps.sh root@<IP>:/tmp/
ssh root@<IP> bash /tmp/bootstrap-vps.sh
```

2. Configurar ambiente:
```bash
ssh bioplatform@<IP>
cp .env.example /opt/bioplatform/.env
# Edite /opt/bioplatform/.env com credenciais de produção
```

3. Deploy:
```bash
cd /opt/bioplatform
bash infra/scripts/deploy.sh
```

## Rollback

```bash
bash infra/scripts/rollback.sh --list     # ver versões disponíveis
bash infra/scripts/rollback.sh <tag>       # reverter para versão específica
```

## Portas

| Serviço  | Porta | Exposição      |
|----------|-------|----------------|
| Caddy    | 80/443| Pública        |
| API      | 8000  | Interna (rede Docker) |
| Postgres | 5432  | localhost only  |
| Redis    | 6379  | localhost only  |

## Volumes Persistentes

- `pgdata` — dados PostgreSQL
- `redisdata` — dados Redis
- `caddy_data` — certificados TLS
- `caddy_config` — config Caddy

## Comandos Úteis

```bash
# Logs em tempo real
docker compose logs -f api

# Health check
curl -s localhost:8000/health | jq

# Backup do banco
docker exec bioplatform-postgres-1 pg_dump -U bio biodb > backup_$(date +%F).sql

# Reiniciar um serviço
docker compose restart api
```
