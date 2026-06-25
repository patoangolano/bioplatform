---
title: Ecossistema de Servidores MCP
slug: mcp-server-ecosystem
type: entity
status: active
created: 2026-06-24
updated: 2026-06-24
tags: [mcp, servidores, infraestrutura, vps, docker, bioinformatica]
related_pages: [[project-status]] [[project-architecture]] [[claude-code-and-mcp]] [[vps-infrastructure]]
---

# Ecossistema de Servidores MCP

Catálogo completo dos servidores MCP integrados ao Claude Code.

## Servidores na VPS (15)

Deploy via Docker Compose em `/opt/mcp-bio/` na VPS Hostinger. Rede `bioplatform_bionet`, rotas Caddy em `https://bio.quackai.com.br/mcp/{tool}/mcp`.

### Grupo A: bio-mcp-* (Streamable HTTP via `mcp.server` SDK)

| Servidor | Porta | Imagem base | Tool |
|----------|-------|-------------|------|
| mcp-blast | 9001 | quay.io/biocontainers/blast:2.17.0 | BLAST+ |
| mcp-bwa | 9002 | quay.io/biocontainers/bwa:0.7.19 | BWA |
| mcp-samtools | 9003 | quay.io/biocontainers/samtools:1.23.1 | SAMtools |
| mcp-bcftools | 9004 | quay.io/biocontainers/bcftools:1.23.1 | BCFtools |
| mcp-bedtools | 9005 | quay.io/biocontainers/bedtools:2.31.1 | BEDTools |
| mcp-fastqc | 9006 | quay.io/biocontainers/fastqc:0.12.1 | FastQC |
| mcp-seqkit | 9009 | quay.io/biocontainers/seqkit:2.13.0 | SeqKit |

### Grupo B: BioinfoMCP (FastMCP 3.4.2 Streamable HTTP)

| Servidor | Porta | Imagem base | Tool |
|----------|-------|-------------|------|
| mcp-fastqc2 | 9101 | quay.io/biocontainers/fastqc:0.12.1 | FastQC |
| mcp-bwa2 | 9102 | quay.io/biocontainers/bwa:0.7.19 | BWA |
| mcp-samtools2 | 9103 | quay.io/biocontainers/samtools:1.23.1 | SAMtools |
| mcp-minimap2 | 9104 | quay.io/biocontainers/minimap2:2.31 | Minimap2 |
| mcp-cutadapt | 9105 | quay.io/biocontainers/cutadapt:5.2 | Cutadapt |
| mcp-salmon | 9106 | quay.io/biocontainers/salmon:2.1.1 | Salmon |
| mcp-bcftools2 | 9107 | quay.io/biocontainers/bcftools:1.23.1 | BCFtools |
| mcp-gatk-hc | 9108 | quay.io/biocontainers/gatk4:4.6.2.0 | GATK HaplotypeCaller |

## Servidores locais (7)

| Servidor | Tipo | Runtime |
|----------|------|---------|
| postgres | stdio | npx + PostgreSQL Docker |
| pg-mcp-server-stuzero | stdio | npx + DATABASE_URL |
| postgresql-mcp-server-aftabbs | stdio | Python + psycopg2 |
| docker-mcp-py | stdio | uvx docker-mcp |
| docker-mcp-quantgeek | stdio | uv run docker-mcp |
| ncbi-datasets | stdio | Node.js |
| uniprot | stdio | Node.js |

## Servidores de infraestrutura

| Servidor | Status |
|----------|--------|
| github | OK |
| filesystem | OK |
| apify | OK |
| linkedin | OK |
| obsidian-mcp-server | Corrigido (API key) |
| mcp-obsidian | Corrigido (vault path) |
| mcp-fs-obsidian | Corrigido (vault path) |
| obsidian-github-mcp | OK |
| brave-search | Aguardando API key |
| notebooklm | OK |
| playwright | OK |
| puppeteer | OK |
| gget | OK (uvx) |
| biothings-mcp | OK (uvx) |
| opengenes-mcp | OK (uvx) |
| synergy-age-mcp | OK (uvx) |

## Desabilitados

| Servidor | Motivo |
|----------|--------|
| pharmacology-mcp | FastMCP 3.x breaking change |
| mcp-nextflow | FastMCP 3.x breaking change |
| pg-mcp-stuzero (uv) | binário pg-mcp não encontrado |
| docker (npm) | pacote 404 no registry |

## Arquitetura de transporte

```
Claude Code (Windows) ──HTTPS──> Caddy (VPS :443) ──> container mcp-* :9001-9108
                                     │
                                     ├── /mcp/blast/mcp     → mcp-blast:9001
                                     ├── /mcp/bwa/mcp       → mcp-bwa:9002
                                     ├── /mcp/samtools/mcp  → mcp-samtools:9003
                                     ├── ... (15 rotas)
                                     └── /health            → API bioplatform:8000
```

## Comandos úteis

```bash
# Verificar containers na VPS
ssh root@187.77.232.5 "docker ps --filter name=mcp-"

# Verificar saúde de um servidor
curl -X POST https://bio.quackai.com.br/mcp/blast/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'

# Logs de um container
ssh root@187.77.232.5 "docker logs mcp-blast --tail 20"
```
