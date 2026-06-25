---
title: Status do Projeto
slug: project-status
type: project
status: active
created: 2026-06-23
updated: 2026-06-24
tags: [projeto, status, progresso, fases, mcp, deploy, vps]
source_count: 0
source_files: []
related_pages: [[bioinformatics-project]] [[project-architecture]] [[project-anchor]] [[mcp-server-ecosystem]] [[vps-infrastructure]]
---

# Status do Projeto

Registro do estado atual da bioplatform. Atualizado em 24 de junho de 2026.

## Fase 1: Fundação (CONCLUÍDA — 21-22 jun 2026)

- **API Backend** — FastAPI com autenticação JWT, OpenAPI automática, endpoints RESTful
- **Banco de Dados** — PostgreSQL 16 (container Docker `postgres:16-alpine`), Redis 7 para cache e filas
- **Auth** — JWT + bcrypt, roles, tokens 24h
- **Worker Assíncrono** — arq worker para BLAST e tarefas longas
- **BLAST Worker** — BLASTn/BLASTp contra NCBI e bancos locais
- **Admin Panel** — Gestão de usuários, sequências, jobs, estatísticas
- **CI/CD** — GitHub Actions (ruff lint → SSH deploy)
- **Deploy** — https://bio.quackai.com.br, Hostinger KVM4 (4 vCPU, 16 GB RAM, 200 GB disco), Ubuntu 24.04, Docker Compose, Caddy reverse proxy com HTTPS automático

## Fase 2: Ecossistema MCP e Reprodutibilidade (CONCLUÍDA — 24 jun 2026)

### Servidores MCP na VPS (15 containers Docker)

**Grupo A — bio-mcp-\* (7 servidores):** Imagens multi-stage (biocontainers → python:3.11-slim), transporte Streamable HTTP `POST /mcp`, rede `bioplatform_bionet`.

| Servidor | Porta | Tool | URL |
|----------|-------|------|-----|
| mcp-blast | 9001 | NCBI BLAST+ 2.17.0 | `/mcp/blast/mcp` |
| mcp-bwa | 9002 | BWA 0.7.19 | `/mcp/bwa/mcp` |
| mcp-samtools | 9003 | SAMtools 1.23.1 | `/mcp/samtools/mcp` |
| mcp-bcftools | 9004 | BCFtools 1.23.1 | `/mcp/bcftools/mcp` |
| mcp-bedtools | 9005 | BEDTools 2.31.1 | `/mcp/bedtools/mcp` |
| mcp-fastqc | 9006 | FastQC 0.12.1 | `/mcp/fastqc/mcp` |
| mcp-seqkit | 9009 | SeqKit 2.13.0 | `/mcp/seqkit/mcp` |

**Grupo B — BioinfoMCP (8 servidores):** FastMCP 3.4.2 com `run_http_async(transport="streamable-http")`.

| Servidor | Porta | Tool | URL |
|----------|-------|------|-----|
| mcp-fastqc2 | 9101 | FastQC 0.12.1 | `/mcp/fastqc2/mcp` |
| mcp-bwa2 | 9102 | BWA 0.7.19 | `/mcp/bwa2/mcp` |
| mcp-samtools2 | 9103 | SAMtools 1.23.1 | `/mcp/samtools2/mcp` |
| mcp-minimap2 | 9104 | Minimap2 2.31 | `/mcp/minimap2/mcp` |
| mcp-cutadapt | 9105 | Cutadapt 5.2 | `/mcp/cutadapt/mcp` |
| mcp-salmon | 9106 | Salmon 2.1.1 | `/mcp/salmon/mcp` |
| mcp-bcftools2 | 9107 | BCFtools 1.23.1 | `/mcp/bcftools2/mcp` |
| mcp-gatk-hc | 9108 | GATK4 4.6.2.0 | `/mcp/gatk-hc/mcp` |

URL base: `https://bio.quackai.com.br`. Caddy com 15 rotas `handle_path`.

### Servidores MCP locais corrigidos

| Servidor | Status | Correção |
|----------|--------|----------|
| postgres | OK | PostgreSQL via Docker (`docker run postgres:16-alpine`, restart unless-stopped) |
| pg-mcp-server-stuzero | OK | `DATABASE_URL` configurado no env |
| postgresql-mcp-server-aftabbs | Corrigido | Removido param `capabilities` obsoleto do FastMCP, pandas instalado |
| docker-mcp-py | OK | Já funcionava via `uvx docker-mcp` |
| docker-mcp-quantgeek | Corrigido | Alterado de `npx` para `uv --directory ... run docker-mcp` |
| ncbi-datasets | OK | `node_modules` presentes, servidor inicia |
| uniprot | OK | `node_modules` presentes, servidor inicia |
| obsidian-mcp-server | Corrigido | Adicionado `OBSIDIAN_API_KEY` ao env |
| mcp-obsidian | Corrigido | Adicionado path do vault como argumento |
| mcp-fs-obsidian | Corrigido | Adicionado path do vault como argumento |

### Ferramentas bioinformáticas locais (WSL2)

Instaladas via conda no WSL2 Ubuntu: fastqc, bwa, samtools, minimap2, cutadapt, salmon, bcftools. Wrappers batch em `C:\Users\Manec\bin\wsl-bio\` para acesso via PowerShell.

### Servidores desabilitados (bugs upstream)

| Servidor | Motivo |
|----------|--------|
| pharmacology-mcp | Crash com FastMCP 3.x (`TypeError` no `FastMCP.from_fastapi()`) |
| mcp-nextflow | Crash com FastMCP 3.x (`TypeError: unexpected keyword argument`) |
| pg-mcp-stuzero | Binário `pg-mcp` não encontrado (config removida) |
| docker | Pacote npm `@modelcontextprotocol/server-docker` retorna 404 |

### Aguardando API key

| Servidor | Campo | Valor atual |
|----------|-------|-------------|
| brave-search | `BRAVE_API_KEY` | `YOUR_BRAVE_SEARCH_API_KEY` (placeholder) |

## Fase 3: Pipelines com Nextflow (PLANEJADA)

- Integração do executor Nextflow ao backend
- Pipeline RNA-Seq funcional (FastQC → STAR/Salmon → DESeq2)
- Primeiro pipeline nf-core executado na VPS
- Análise de enriquecimento funcional (GO, KEGG, GSEA)

## Fase 4: Especialização (FUTURO)

- nf-core/eager para DNA antigo
- Paleoproteômica / ZooMS (simulação computacional)
- Genômica populacional (PCA, ADMIXTURE, f-statistics)
- Integração multi-ômica

## Infraestrutura Atual

| Componente | Detalhe |
|------------|---------|
| VPS | Hostinger KVM4, 4 vCPUs, **16 GB RAM**, 200 GB disco |
| SO | Ubuntu 24.04 com Docker e Caddy |
| Containers VPS | 21 (5 bioplatform + 15 MCP + 1 PostgreSQL externo) |
| Deploy | Docker Compose, Caddy reverse proxy, HTTPS automático |
| Domínio | https://bio.quackai.com.br |
| CI/CD | GitHub Actions (ruff lint → SSH deploy) |
| Local | Windows 11, WSL2 Ubuntu, Claude Code |
| MCP ativos | 22 (15 VPS + 7 locais) |
| MCP desabilitados | 4 (bugs upstream) |

---

Status atualizado em 24 de junho de 2026. Consulte [[project-architecture]] para detalhes técnicos, [[mcp-server-ecosystem]] para URLs e portas, e [[bioinformatics-project]] para escopo científico.
