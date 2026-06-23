# 🧬 QuackAI BioLab

[![CI/CD](https://github.com/patoangolano/bioplatform/actions/workflows/deploy.yml/badge.svg)](https://github.com/patoangolano/bioplatform/actions)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL 16](https://img.shields.io/badge/PostgreSQL-16-336791.svg)](https://www.postgresql.org/)
[![Redis 7](https://img.shields.io/badge/Redis-7-DC382D.svg)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://docs.docker.com/compose/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Plataforma de orquestração translacional bioinformática**

> Análise de sequências biológicas com proveniência completa, busca BLAST assíncrona, integração com bancos públicos (UniProt, PubMed, InterPro, AlphaFold, STRING), screening de biossegurança, geração de documentos regulatórios GxP e deploy automatizado.

🔗 **Live:** [bio.quackai.com.br](https://bio.quackai.com.br)  
📖 **API Docs:** [bio.quackai.com.br/docs](https://bio.quackai.com.br/docs)  
🖥️ **Frontend:** [Hostinger Horizons](https://bio.quackai.com.br)

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    Caddy (HTTPS/LE)                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────┐   ┌──────────┐   ┌──────────────────┐   │
│  │ FastAPI  │   │  Worker  │   │   PostgreSQL     │   │
│  │  (API)   │◄──┤  (BLAST) │──►│   (biodb)        │   │
│  └────┬─────┘   └──────────┘   └──────────────────┘   │
│       │                                                 │
│       ▼                                                 │
│  ┌──────────────────────────────────────────────┐      │
│  │        External APIs (async)                  │      │
│  │  UniProt · PubMed · InterPro · AlphaFold     │      │
│  │  STRING · NCBI BLAST                          │      │
│  └──────────────────────────────────────────────┘      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Features

| Feature | Descrição |
|---------|-----------|
| 🔐 Auth JWT | Registro, login, tokens 24h |
| 🧬 Sequences CRUD | Submissão de DNA/RNA/proteína com análise inline |
| 🔍 BLAST Assíncrono | Submit → poll → resultados via NCBI BLAST |
| 📊 Análise Inline | UniProt + PubMed + InterPro + AlphaFold + STRING |
| 📜 Proveniência | Rastreio completo: ferramenta, versão, hash, timestamp |
| 👑 Admin Panel | Gestão de usuários, estatísticas, sequências, jobs |
| 🛡️ Biossegurança | Screening de sequências contra Select Agents (CDC/USDA) |
| 📋 Regulatório GxP | Geração de documentos (protocolo, SAP, TCLE) — Anvisa/ICH |
| 🧪 ESM3 Adapter | Predição de estrutura e mutações via modelos de proteínas |
| 🚀 CI/CD | GitHub Actions → lint → deploy automático |
| 🔒 HTTPS | Certificado Let's Encrypt via Caddy |

## Stack Tecnológico

| Camada | Tecnologia |
|--------|------------|
| Backend | Python 3.11, FastAPI, SQLAlchemy 2.0 (async) |
| Database | PostgreSQL 16 |
| Cache | Redis 7 (TTL por adapter: 2h–7d) |
| Auth | JWT (python-jose), bcrypt |
| Worker | arq (Redis queue) + NCBI BLAST REST |
| Workflows | Prefect 3.x (multi-step pipelines) |
| Proxy | Caddy 2 (auto-HTTPS via Let's Encrypt) |
| Deploy | Docker Compose, GitHub Actions CI/CD |
| VPS | Ubuntu 24.04, KVM 4CPU/16GB |
| MCP | JSON-RPC 2.0 stdio (Claude Code integration) |

## Endpoints da API

### Auth
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/v1/auth/register` | Criar conta |
| POST | `/api/v1/auth/login` | Login (form-urlencoded) |
| GET | `/api/v1/auth/me` | Perfil do usuário autenticado |

### Sequences
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/v1/sequences` | Submeter sequência (+ análise inline) |
| GET | `/api/v1/sequences` | Listar sequências |
| GET | `/api/v1/sequences/{id}` | Detalhes de uma sequência |

### BLAST
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/v1/blast/submit` | Submeter job BLAST |
| GET | `/api/v1/blast/jobs` | Listar jobs |
| GET | `/api/v1/blast/jobs/{id}` | Status + resultados |

### Admin (requer `is_admin=true`)
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/v1/admin/stats` | Estatísticas da plataforma |
| GET | `/api/v1/admin/users` | Listar usuários |
| PATCH | `/api/v1/admin/users/{id}` | Atualizar usuário |
| DELETE | `/api/v1/admin/users/{id}` | Remover usuário |
| GET | `/api/v1/admin/sequences` | Todas as sequências |
| GET | `/api/v1/admin/jobs` | Todos os jobs |

### Regulatory (requer autenticação)
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/v1/regulatory/templates` | Templates disponíveis |
| POST | `/api/v1/regulatory/generate` | Gerar documento regulatório |

## Quick Start (Local)

```bash
# Clonar
git clone https://github.com/patoangolano/bioplatform.git
cd bioplatform

# Ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\Activate.ps1  # Windows

# Dependências
pip install -r apps/api/requirements.txt

# Variáveis de ambiente
cp .env.example .env
# Editar .env com suas credenciais

# Subir com Docker
docker compose up -d
```

## Deploy (Produção)

O deploy é automático via GitHub Actions em cada push na `main`:

1. **Lint** — ruff check em `apps/api/` e `mcp_servers/`
2. **SSH Deploy** — pull + migrate + build + up
3. **Health Check** — `curl http://localhost:8000/health`

```yaml
# .github/workflows/deploy.yml
on:
  push:
    branches: [main]
```

## Estrutura do Projeto

```
bioplatform/
├── apps/
│   ├── api/              # FastAPI backend
│   │   ├── main.py       # App + middleware + lifespan
│   │   ├── models.py     # SQLAlchemy models (Sequence, Job, Result, Provenance)
│   │   ├── schemas.py    # Pydantic schemas (request/response)
│   │   ├── auth.py       # JWT + bcrypt + dependencies
│   │   ├── database.py   # Async engine (pool_size=5, max_overflow=10)
│   │   ├── config.py     # Settings via pydantic-settings
│   │   └── routers/      # auth, sequences, blast, admin, regulatory
│   ├── worker/           # arq BLAST async processor
│   └── workflows/        # Prefect flows + tasks
│       ├── flows/        # protein_report (multi-step pipeline)
│       └── tasks/        # blast, annotation, literature, report
├── mcp_servers/          # MCP servers para Claude Code
│   ├── bio_science_mcp.py  # JSON-RPC 2.0 dispatcher
│   ├── cache.py          # Redis caching layer (@cached decorator)
│   └── adapters/         # pubmed, uniprot, interpro, alphafold, string, blast, esm
├── services/
│   ├── biosafety/        # Select Agents screening (CDC/USDA)
│   └── regulatory_assist/ # Geração de documentos GxP (ICH/Anvisa)
├── skills/               # Protocolos institucionais para Claude Code
│   ├── protocols/        # BLAST, caracterização, literatura
│   ├── thresholds/       # e-value, pLDDT, STRING scores (YAML)
│   └── templates/        # Formato de relatório com proveniência
├── infra/
│   ├── docker-compose.yml
│   ├── Caddyfile
│   └── db/migrations/
└── .github/workflows/    # CI/CD (ruff lint → SSH deploy)
```

## Princípios de Design

1. **Proveniência obrigatória** — todo resultado rastreia origem
2. **Separação epistêmica** — observação ≠ inferência ≠ hipótese
3. **Modularidade** — adapters isolados, fácil de estender
4. **Biossegurança** — classificação de risco em organismos
5. **Reprodutibilidade** — mesmos inputs → mesmos outputs
6. **Deploy-first** — infra e app pensadas juntas desde o dia 1

## MCP Servers

Servidores MCP para integração com Claude Code:

| Server | Ferramentas |
|--------|-------------|
| `scientific-bio` | PubMed, UniProt, InterPro, AlphaFold, BLAST, STRING |
| `hostinger-api` | Gerenciamento VPS |
| `postgres` | Queries e migrações |
| `docker` | Gerenciamento de containers |

## Timeline de Desenvolvimento

| Data | Marco |
|------|-------|
| 2025-06-21 | Monorepo + API + Auth + DB + Deploy |
| 2025-06-21 | BLAST worker + Admin panel + CI/CD |
| 2025-06-22 | Frontend PT-BR + DNS + CORS fix |
| 2025-06-22 | Biossegurança + Regulatório GxP + ESM3 |
| 2025-06-22 | Cache Redis + Prefect Workflows + Skills MCP |
| 2025-06-22 | Frontend integrado (todas as features) |

## Próximos Passos

- [x] Screening de biossegurança (Select Agents CDC/USDA)
- [x] Geração de documentos regulatórios GxP (Anvisa Sandbox)
- [x] Adapter ESM3 para predição de mutações
- [x] Cache Redis com TTL por adapter
- [x] Prefect workflows (pipeline multi-step)
- [x] Skills institucionais para Claude Code
- [ ] Visualização 3D de proteínas (3Dmol.js)
- [ ] Classificação filogenética
- [ ] Multi-ômica espacial e grafos de conhecimento (pgvector)
- [ ] Mapeamento geográfico de organismos
- [ ] Reações bioquímicas (KEGG)
- [ ] Submissão no Sandbox Regulatório Anvisa

---

## Licença

MIT

## Autor

**Matheus Angolano** — [@patoangolano](https://github.com/patoangolano)
