---
title: "GitHub como Portfolio e Entregaveis"
slug: "github-and-portfolio-outputs"
type: infrastructure
status: draft
created: 2026-06-23
updated: 2026-06-23
tags:
  - github
  - portfolio
  - conventional-commits
  - reproducibilidade
  - nf-core
  - entregaveis
source_count: 0
source_files: []
related_pages:
  - "[[docker-and-reproducibility]]"
  - "[[nextflow-and-nf-core]]"
  - "[[positioning]]"
  - "[[project-to-career-translation]]"
  - "[[cli-workflow]]"
  - "[[tooling-stack]]"
  - "[[reproducibility-in-bioinformatics]]"
---

# GitHub como Portfolio e Entregaveis

Nao basta ter codigo no GitHub -- e preciso que o historico do repositorio _conte uma historia coerente_. Para isso, adotamos [[conventional-commits|commits convencionais em portugues]] (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`, `perf:`, `ci:`), com mensagens no imperativo e um commit por mudanca logica. Um historico limpo, sem commits do tipo "WIP" ou "ajustes", sinaliza maturidade profissional e facilita `git bisect`, revisao de PR e auditoria de proveniencia.

O repositorio **[[bioplatform]]** e o artefato primario de portfolio: backend FastAPI com testes, workers assincronos com arq, Docker Compose multi-servico com Caddy e PostgreSQL, CI/CD via GitHub Actions, e 15 servidores MCP bioinformaticos documentados em [[mcp-servers]]. Cada componente e versionado no mesmo monorepo e acompanhado de README especifico, compose.yaml funcional e cobertura de testes via pytest -- exatamente o que um contratante tecnico inspeciona em uma avaliacao de competencia.

Para o futuro, as contribuicoes em **pipelines nf-core** ([[nextflow-and-nf-core]]) serao o segundo pilar do portfolio: submeter modulos reutilizaveis, corrigir issues em pipelines comunitarias como `nf-core/rnaseq` e `nf-core/eager`, e publicar analises completas no GitHub com provenance documentada -- do FASTQ bruto ao relatorio final. Essas entregas concretizam o perfil descrito em [[positioning]] e se conectam diretamente a estrategia de traducao de projeto para carreira em [[project-to-career-translation]].

Todo entregavel publico da plataforma -- relatorios de analise, figuras, dashboards, workflows reprodutiveis -- e tratado como **output auditavel**, versionado e vinculado a paginas do tipo `output` neste wiki. Nada e publicado sem registro de ferramenta, versao, parametro e data de execucao. Esse rigor transforma o GitHub de um deposito de codigo em um curriculo vivo e verificavel.
