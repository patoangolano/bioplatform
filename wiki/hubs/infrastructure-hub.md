---
title: Infrastructure Hub
type: hub
created: 2026-06-23
tags: [hub, infraestrutura, docker, vps, ferramentas, cli]
---

# Infrastructure Hub

Hub de infraestrutura tecnica. Tudo que sustenta a execucao da bioplatform: do VPS ao terminal. Aqui estao documentadas as ferramentas, configuracoes e workflows que fazem a plataforma funcionar em producao.

## Estrutura do Hub

### Stack de Ferramentas

- **VPS** -- Hostinger KVM4, 4 vCPUs, 8 GB RAM, Ubuntu 24.04. Deploy em bio.quackai.com.br.
- **Backend** -- FastAPI (Python 3.12), arq worker para tarefas assincronas
- **Banco de dados** -- PostgreSQL 16 + Redis 7
- **Proxy** -- Caddy com HTTPS automatico
- **Orquestracao** -- Docker Compose para todos os servicos
- **15 servidores MCP** -- Ferramentas bioinformaticas expostas via Model Context Protocol
- **CI/CD** -- GitHub Actions para build, teste e deploy automatizado

### Docker

Gerenciamento de containers como pratica diaria. Dockerfiles para cada servico. Docker Compose para orquestracao local e remota. Volumes para persistencia, networks para isolamento. Estrategia de multi-stage builds para imagens enxutas.

### Claude Code / MCP

Ferramenta primaria de desenvolvimento assistido. Configuracao de hooks, permissions, settings. Ecossistema de servidores MCP bioinformaticos: BLAST, SAMtools, BWA, FastQC, bcftools, bedtools, seqkit. Integracao direta do terminal com analise de dados.

### GitHub / Portfolio

Organizacao do repositorio. Estrategia de branches. Issues como registro de tarefas e decisoes. GitHub Actions para CI/CD. README.md como porta de entrada para visitantes do portfolio.

### CLI Workflow

Ferramentas de terminal essenciais: git, docker, curl, jq, ripgrep, tmux. Scripts de automacao em Bash e Python. Workflow de desenvolvimento: clone, branch, edit, commit, push, deploy. Atalhos e aliases para produtividade.

## Navegacao

- Voltar para [[home]]
- Ir para [[study-hub]]
- Ir para [[bioinformatics-hub]]
- Ir para [[career-hub]]

---

Infraestrutura solida e a base que permite a ciencia acontecer sem atritos. Cada ferramenta aqui documentada esta em uso ativo na plataforma.
