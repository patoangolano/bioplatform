# bioplatform

Plataforma de orquestração translacional bioinformática.

## Princípios

1. **Proveniência obrigatória** — todo resultado deve rastrear origem (ferramenta, versão, parâmetros, timestamp)
2. **Separação epistêmica** — distinguir observação, inferência e hipótese
3. **Modularidade** — adapters, services, workflows isolados
4. **Biossegurança** — sandboxing de operações com organismos, classificação de risco
5. **Reprodutibilidade** — workflows devem ser repetíveis com mesmos inputs
6. **Segurança operacional** — secrets nunca em código versionado, mínimo de portas expostas
7. **Deploy-first** — infraestrutura e aplicação pensadas juntas desde o início

## Arquitetura

```
apps/api/          — backend FastAPI
apps/web/          — frontend (futuro)
apps/worker/       — processamento assíncrono
services/          — módulos de domínio:
                     provenance, literature, annotation,
                     taxonomy, biosafety, regulatory_assist
mcp_servers/       — MCP servers para Claude Code
infra/             — scripts de deploy, Docker, proxy
```

## Stack

- Python 3.11+, FastAPI, PostgreSQL, Redis
- Docker Compose, Caddy (reverse proxy)
- Prefect (futuro — orquestração de workflows)

## Deploy

- Target: VPS Hostinger KVM8 (Ubuntu)
- Proxy: Caddy com HTTPS automático
- Containers: Docker Compose em produção

## MCP Servers disponíveis

- hostinger-api — gerenciamento VPS
- scientific-bio — ferramentas bioinformáticas
- github — repositórios e CI
- filesystem — operações locais de arquivo
- postgres — queries e migrações
- docker — gerenciamento de containers

## Regras de commits

- Conventional commits em português: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
- Mensagens descritivas no imperativo: "adiciona endpoint de anotação"
- Um commit por mudança lógica

## Regras de secrets

- Usar `.env` para variáveis sensíveis (nunca commitar)
- `.env` deve estar no `.gitignore`
- Em produção, injetar via Docker secrets ou variáveis de ambiente do host
- Nunca logar tokens, senhas ou chaves de API
