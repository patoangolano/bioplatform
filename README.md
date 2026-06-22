# 🧬 QuackAI BioLab

**Plataforma de orquestração translacional bioinformática**

> Análise de sequências biológicas com proveniência completa, busca BLAST assíncrona, integração com bancos públicos (UniProt, PubMed, InterPro, AlphaFold, STRING) e deploy automatizado.

🔗 **Live:** [bio.quackai.com.br](https://bio.quackai.com.br)  
📖 **Docs:** [bio.quackai.com.br/docs](https://bio.quackai.com.br/docs)

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
| Auth | JWT (python-jose), bcrypt |
| Worker | asyncio + NCBI BLAST REST |
| Proxy | Caddy 2 (auto-HTTPS) |
| Deploy | Docker Compose, GitHub Actions |
| VPS | Ubuntu 24.04, KVM 4CPU/16GB |

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
│   │   ├── main.py       # App + middleware
│   │   ├── models.py     # SQLAlchemy models
│   │   ├── schemas.py    # Pydantic schemas
│   │   ├── auth.py       # JWT + dependencies
│   │   ├── database.py   # Async engine
│   │   ├── config.py     # Settings
│   │   └── routers/      # auth, sequences, blast, admin
│   └── worker/           # BLAST async processor
├── mcp_servers/          # MCP servers para Claude Code
│   ├── bio_science_mcp.py
│   └── adapters/         # pubmed, uniprot, interpro, blast...
├── infra/
│   ├── docker-compose.yml
│   ├── Caddyfile
│   └── db/migrations/    # SQL migrations
├── .github/workflows/    # CI/CD
└── services/             # Módulos de domínio (futuro)
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
| 2025-06-22 | CORS fix + Frontend PT-BR + DNS |

## Próximos Passos

- [x] Screening de biossegurança (Select Agents CDC/USDA)
- [x] Geração de documentos regulatórios GxP (Anvisa Sandbox)
- [x] Adapter ESM3 para predição de mutações
- [ ] Visualização 3D de proteínas (3Dmol.js)
- [ ] Classificação filogenética
- [ ] Multi-ômica espacial e grafos de conhecimento
- [ ] Integração Prefect (DAGs Python nativos)
- [ ] Redis vetorial (embeddings + cache de contexto MCP)
- [ ] Skills institucionais para Claude Code
- [ ] Mapeamento geográfico de organismos
- [ ] Reações bioquímicas (KEGG)
- [ ] Submissão no Sandbox Regulatório Anvisa

---

## Licença

MIT

## Autor

**Matheus Angolano** — [@patoangolano](https://github.com/patoangolano)
