# infra/ — Infraestrutura e Reprodutibilidade

Scaffolding de infraestrutura para execução reprodutível.

## Conteúdo atual

| Caminho | Propósito |
|---------|-----------|
| `caddy/` | Configuração do Caddy reverse proxy (HTTPS automático) |
| `db/` | Migrações e inicialização do PostgreSQL |
| `scripts/` | Scripts auxiliares de deploy e manutenção |
| `docker/` | Dockerfiles auxiliares (futuro) |
| `compose/` | Docker Compose sobrepostos (futuro) |
| `postgres/` | Configurações específicas do PostgreSQL (futuro) |

## Assets futuros

- Docker Compose sobrepostos para ambientes (dev, staging, prod)
- Scripts de inicialização de banco de dados
- Templates de container para ferramentas bioinformáticas
- Notas de deploy e referências de VPS
- Configurações de CI/CD
