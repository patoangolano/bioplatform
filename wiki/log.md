***
title: Log do Repositório
slug: repo-log
type: hub
status: active
created: 2026-06-24
updated: 2026-06-24
tags: [log, cronologia, manutenção]
related_pages: [[home]], [[wiki-health]]
***

# Log do Repositório

Histórico cronológico append-only de mudanças no repositório de conhecimento.

## [2026-06-24] setup | Inicialização do workspace de conhecimento

**Sistema de 5 camadas estabelecido no repositório `bioplatform`.**

Criado:
- Estrutura de diretórios: `raw/` (7 subdirs), `wiki/` (12 subdirs), `output/`, `tools/`, `logs/`
- `CLAUDE.md` expandido com: modelo de 5 camadas, regras não-negociáveis, política de idioma, frontmatter padrão, fluxos de ingestão/query/lint, compatibilidade Obsidian, manutenção de índice/log
- `wiki/schema/` com 10 arquivos: frontmatter, page-types, naming, linking-rules, ingest-workflow, query-workflow, lint-workflow, output-filing, notebooklm-mcp, workspace-architecture
- `wiki/hubs/` com 5 arquivos: home, study-hub, bioinformatics-hub, career-hub, infrastructure-hub
- `wiki/study-plan/` com 4 arquivos: overview, roadmap, learning-priorities, study-method
- `wiki/projects/` com 4 arquivos: bioinformatics-project, project-status, project-architecture, project-anchor
- `wiki/concepts/` com 5 arquivos: nextflow-and-nf-core, rna-seq-workflows, paleogenomics-and-ancient-dna, paleoproteomics-and-zoo-ms, reproducibility-in-bioinformatics
- `wiki/infrastructure/` com 5 arquivos: tooling-stack, docker-and-reproducibility, claude-code-and-mcp, github-and-portfolio-outputs, cli-workflow
- `wiki/career/` com 3 arquivos: positioning, portfolio-logic, project-to-career-translation
- `wiki/reviews/` com 2 arquivos: wiki-health, domain-gaps
- `wiki/index.md` e `wiki/log.md`
- README.md atualizado com seção Wiki & Knowledge Workspace
- READMEs operacionais: `raw/`, `tools/`, `logs/`, `infra/`, `output/`

Total: **43 arquivos** criados ou atualizados.

Contexto do repositório:
- Projeto bioplatform ativo (FastAPI + PostgreSQL + Redis + Docker na VPS Hostinger)
- 15 servidores MCP de bioinformática deployados via Docker na VPS (`bio.quackai.com.br`)
- 7 servidores MCP locais (PostgreSQL, Obsidian, Docker, filesystem, etc.)
- WSL2 Ubuntu com ferramentas bioinformáticas via conda
- Claude Code como interface primária

Próximos passos:
- Popular `raw/` com primeiras fontes (artigos, papers)
- Criar primeiras páginas `wiki/sources/` e `wiki/entities/`
- Executar primeira ingestão completa
- Rodar primeiro lint de saúde do wiki

## [2026-06-24] deploy | 15 servidores MCP bioinformática na VPS

Deploy completo de servidores MCP como containers Docker na VPS Hostinger:

**bio-mcp-* (7 servidores):** blast, bwa, samtools, bcftools, bedtools, fastqc, seqkit
- Imagens multi-stage (biocontainers → python:3.11-slim)
- Transporte Streamable HTTP no endpoint `POST /mcp`
- Portas 9001-9009, rede `bioplatform_bionet`
- Rotas Caddy: `https://bio.quackai.com.br/mcp/{tool}/mcp`

**BioinfoMCP (8 servidores):** fastqc2, bwa2, samtools2, minimap2, cutadapt, salmon, bcftools2, gatk-hc
- FastMCP 3.4.2 com `mcp.run_http_async(transport="streamable-http")`
- Imagens simplificadas (biocontainer + Python 3.11-slim)
- Portas 9101-9108

Infraestrutura de suporte:
- PostgreSQL via Docker (bio:bio123@localhost:5432/biodb)
- WSL2 Ubuntu com ferramentas bioinformáticas via conda (fastqc, bwa, samtools, minimap2, cutadapt, salmon, bcftools)
- 4 servidores desabilitados (bugs upstream): pharmacology-mcp, mcp-nextflow, pg-mcp-stuzero, docker (npm 404)

## [2026-06-24] update | Correção do estado do projeto e entidades MCP

**Páginas criadas:**
- `wiki/entities/mcp-server-ecosystem.md` — Catálogo completo: 15 servidores VPS (portas, imagens, URLs), 7 locais, 4 desabilitados, diagrama de arquitetura
- `wiki/infrastructure/vps-infrastructure.md` — VPS Hostinger KVM4 (16 GB), 21 containers, rede bioplatform_bionet, Caddy routes

**Páginas corrigidas:**
- `wiki/projects/project-status.md` — Reescrito com estado real: tabelas dos 15 MCP, specs corretas (16 GB), correções locais, desabilitados
- `wiki/infrastructure/tooling-stack.md` — Links corrigidos para [[vps-infrastructure]] e [[mcp-server-ecosystem]]
- `wiki/index.md` — Adicionadas 2 novas páginas (infra + entities)

## [2026-06-24] ingestão | DevOps para Biologia Computacional — Deep Research

**Fonte:** `output/devops-computational-biology-deep-research.md` — relatório de deep research multi-agente (105 agentes, 23 fontes, 25 claims verificadas com revisão adversarial de 3 votos; 11 confirmadas, 14 refutadas).

**Página nova (1):**
- `wiki/outputs/devops-computational-biology.md` — primeira página `output` da wiki: proveniência, claims confirmadas vs refutadas, competências sênior priorizadas, fontes, questões em aberto

**Páginas afetadas (4):**
- `wiki/concepts/reproducibility-in-bioinformatics.md` — nova seção "O Limite da Containerização: Reprodutibilidade Semântica" (deriva de identificadores Ensembl, grafo snapshot-bounded, FAIR não basta); source_count 0→1
- `wiki/concepts/nextflow-and-nf-core.md` — nova seção "Escala e Avaliação para Produção" (1.400+ módulos, ~80 subworkflows; regra "nunca avaliar por PoC"; claims refutadas)
- `wiki/infrastructure/docker-and-reproducibility.md` — nova seção "Onde o Docker Para" (Docker não basta, arquivamento Docker Hub→Zenodo, BIOMERO 2.0, runtime duplo Docker/Apptainer); source_count 0→1
- `wiki/index.md` — seção Outputs preenchida com [[devops-computational-biology]]

**Achado central:** containerização congela o software, mas não a semântica biológica — reprodutibilidade real exige versionar releases de anotação, não apenas imagens.

**Follow-ups registrados:** integrar versionamento semântico de identificadores ao serviço de [[provenance|proveniência]]; avaliar openBIS como RDMS; validar o padrão snapshot-bounded do IDTrack fora do preprint.
