---
title: Stack de Ferramentas
tags: [infrastructure, devops, tooling]
created: 2026-06-23
---

# Stack de Ferramentas

O [[bioplatform]] roda sobre **Python 3.11+** com **FastAPI** como framework HTTP, expondo endpoints para ingestao, consulta e analise de dados bioinformaticos. O banco relacional e um **PostgreSQL 16** dedicado, com **Redis 7** atuando como cache de queries e broker de mensagens para tarefas assincronas.

A orquestracao de pipelines ETL e disparada pelo **Prefect 3.x**, que gerencia fluxos de importacao de arquivos FASTA, anotacoes funcionais e varreduras de variantes. Toda a infra roda em containers **Docker Compose** no mesmo VPS, com **Caddy** como proxy reverso e terminador TLS automatico via Let's Encrypt.

O servidor e um VPS **Hostinger KVM4** (4 vCPU, 16 GB RAM, 200 GB NVMe), hospedando tambem os **15 servidores MCP** de bioinformatica -- entre eles NCBI Datasets, UniProt, BLAST, BWA, SAMtools, bcftools, bedtools, FastQC e SeqKit -- expostos ao [[claude-code]] como ferramentas de consulta em linguagem natural.

No ambiente local de desenvolvimento, utiliza-se **WSL2 Ubuntu** com ferramentas do **bioconda** (samtools, bcftools, seqkit, bedtools) instaladas diretamente no PATH. O **Claude Code** funciona como interface primaria tanto para desenvolvimento quanto para analises exploratorias, consumindo os servidores MCP e acionando pipelines via linguagem natural. Consulte [[vps-infrastructure]] para detalhes de provisionamento e [[mcp-server-ecosystem]] para o catalogo completo de servidores MCP.
