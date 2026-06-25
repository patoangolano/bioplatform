---
title: Arquitetura do Projeto
type: project
created: 2026-06-23
tags: [projeto, arquitetura, infraestrutura, backend, containers]
links: [[bioinformatics-project]] [[project-status]] [[project-anchor]] [[infrastructure-hub]]
---

# Arquitetura do Projeto

Visao tecnica da arquitetura da bioplatform. Este documento descreve a estrutura de servicos, o fluxo de dados e as decisoes de design que sustentam a plataforma.

## Diagrama de Componentes

```
                        Internet
                           |
                        Caddy (HTTPS)
                           |
                      FastAPI (API)
                      /      |      \
                  arq worker  |    MCP servers (x15)
                     |        |        |
               PostgreSQL   Redis   Docker containers
                     |
               Docker Compose (VPS KVM4)
```

## Componentes Principais

### FastAPI Backend

Framework Python assincrono que expoe a API REST. Responsavel por:
- Autenticacao e autorizacao (JWT)
- Roteamento de requisicoes para workers e servicos
- Documentacao OpenAPI automatica em `/docs`
- Validacao de entrada com Pydantic
- Execucao em container Docker com Uvicorn

### arq Worker

Sistema de filas assincronas baseado em Redis. Gerencia tarefas de longa duracao:
- Execucoes BLAST contra bancos NCBI e locais
- Alinhamentos com BWA e STAR
- Pipelines Nextflow disparados como tarefas assincronas
- Notificacao de conclusao via callback ou polling

### PostgreSQL 16

Banco de dados relacional principal. Armazena:
- Usuarios, roles e permissoes
- Metadados de execucoes (pipelines, tarefas, resultados)
- Referencias a arquivos e datasets
- Schema gerenciado via migracoes (Alembic)

### Redis 7

Cache e message broker. Usado para:
- Fila de tarefas do arq
- Cache de resultados de consultas frequentes
- Sessoes e tokens de curta duracao
- Lock distribuido para operacoes concorrentes

### Caddy

Reverse proxy com HTTPS automatico via Let's Encrypt. Responsavel por:
- Terminacao TLS
- Roteamento de dominios e subdominios
- Headers de seguranca (CORS, CSP, HSTS)
- Log de acesso e erros

### Ecossistema MCP (15 servidores)

Servidores Model Context Protocol que expoem ferramentas bioinformaticas:
- **Analise de sequencias:** BLAST, BWA, seqkit
- **Variantes e alinhamento:** bcftools, samtools, bedtools
- **Qualidade:** FastQC, MultiQC
- **Bases de dados:** BioThings (genes, variantes, quimica), NCBI Datasets, UniProt
- **Envelhecimento:** OpenGenes, SynergyAge
- **Infraestrutura:** PostgreSQL, GitHub, Docker, Playwright, NotebookLM

Cada servidor roda em container Docker independente, gerenciado pelo ecossistema Claude Code.

## Fluxo de Dados

### Submissao de Analise

1. Cliente autentica via API (JWT)
2. Submete parametros de analise (ex.: FASTQs para RNA-Seq, query para BLAST)
3. API valida entrada e enfileira tarefa no Redis (arq)
4. Worker processa tarefa (executa ferramenta, coleta resultados)
5. Resultados armazenados (banco + filesystem)
6. Cliente consulta status e obtem resultados via API

### Execucao de Pipeline

1. Usuario define parametros via API ou CLI
2. API gera config Nextflow e dispara worker
3. Worker executa `nextflow run` com profile Docker
4. Cada processo Nextflow roda em container proprio
5. Nextflow gerencia diretorio de trabalho, cache, resume
6. Resultados finais copiados para volume compartilhado
7. Relatorios (MultiQC, Nextflow report) disponiveis via API

## Decisoes de Design

- **Containeres para tudo** -- Cada ferramenta em container proprio. Sem instalacao no host. Reproduibilidade garantida.
- **Assincrono por padrao** -- Toda operacao longa e delegada a workers. API responde rapido.
- **Infraestrutura como codigo** -- Toda configuracao versionada: Dockerfiles, docker-compose.yml, scripts de deploy.
- **MCP como interface de ferramentas** -- Ferramentas bioinformaticas expostas via protocolo padrao, consumiveis por qualquer cliente MCP.

## Documentacao Relacionada

- README.md do repositorio (raiz do projeto)
- CLAUDE.md do repositorio (instrucoes para Claude Code)
- Dockerfiles em `docker/`
- docker-compose.yml na raiz

---

Para status de implantacao, veja [[project-status]]. Para o proposito do projeto, veja [[project-anchor]].
