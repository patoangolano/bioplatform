---
title: "Arquitetura em Camadas do Workspace"
slug: "workspace-architecture"
type: schema
status: active
created: 2025-01-15
updated: 2026-06-23
tags:
  - schema
  - arquitetura
  - workspace
  - infraestrutura
source_count: 0
source_files: []
related_pages:
  - "[[frontmatter]]"
  - "[[page-types]]"
  - "[[naming]]"
  - "[[output-filing]]"
  - "[[notebooklm-mcp]]"
---

# Arquitetura em Camadas do Workspace

O workspace `bioplatform` e organizado em cinco camadas com responsabilidades e regras de acoplamento bem definidas. A separacao em camadas garante que alteracoes em uma camada nao corrompam outra e que cada artefato tenha um local canonico.

## Modelo de Cinco Camadas

```
+------------------------------------------------------------------+
|  CAMADA 5: OUTPUT       (entregaveis, relatorios, slides)        |
|  Diretorio: wiki/outputs/ + output/                              |
+------------------------------------------------------------------+
|  CAMADA 4: OPERATIONAL   (ferramentas, scripts, infra, codigo)   |
|  Diretorio: tools/ + config/ + notebooks/                        |
+------------------------------------------------------------------+
|  CAMADA 3: SCHEMA        (regras, formatos, vocabularios)        |
|  Diretorio: wiki/schema/                                         |
+------------------------------------------------------------------+
|  CAMADA 2: WIKI          (paginas de conhecimento, mantidas)     |
|  Diretorio: wiki/                                                |
+------------------------------------------------------------------+
|  CAMADA 1: RAW           (fontes imutaveis, dados crus)          |
|  Diretorio: data/ + papers/ + references/                        |
+------------------------------------------------------------------+
```

## Camada 1: RAW (Fontes Imutaveis)

- **Diretorios:** `data/` (datasets, FASTQ, BAM, VCF), `papers/` (PDFs de artigos), `references/` (genomas de referencia, anotacoes).
- **Regra fundamental:** Arquivos nesta camada nunca sao modificados apos a ingestao inicial. Alteracoes geram novas copias com versao no nome.
- **Interacao com outras camadas:** A camada WIKI referencia arquivos RAW via `source_files` no frontmatter. A camada OPERATIONAL le dados de RAW para processamento. Nenhuma camada escreve em RAW.

## Camada 2: WIKI (Conhecimento Estruturado)

- **Diretorio:** `wiki/` e todas as subpastas exceto `wiki/schema/`, `wiki/outputs/` e `wiki/templates/`.
- **Conteudo:** Paginas Markdown com frontmatter YAML. Cada pagina e um no no grafo de conhecimento.
- **Manutencao:** Mantida por LLMs (Claude, via MCP do Obsidian) e revisao humana periodica.
- **Interacao com outras camadas:** Le SCHEMA para validar formato. Escreve em OUTPUT ao gerar entregaveis. Le RAW para criar `source-summary`. Usa ferramentas de OPERATIONAL para gerar conteudo.

## Camada 3: SCHEMA (Regras e Formatos)

- **Diretorio:** `wiki/schema/`.
- **Conteudo:** Documentos normativos que definem como a wiki funciona. Cada pagina schema e do tipo `schema`.
- **Proposito:** Garantir consistencia estrutural. Toda pagina da wiki deve estar em conformidade com `frontmatter.md`, `naming.md`, `linking-rules.md` e `page-types.md`.
- **Interacao com outras camadas:** E lida pela camada WIKI para auto-validacao. Altera-la requer revisao de impacto em todas as paginas existentes.

## Camada 4: OPERATIONAL (Ferramentas e Infraestrutura)

- **Diretorios:** `tools/` (scripts CLI, Makefiles, Dockerfiles), `config/` (arquivos de configuracao), `notebooks/` (Jupyter notebooks para analise).
- **Conteudo:** Codigo executavel que processa dados, gera figuras, valida a wiki, automatiza ingestao.
- **Interacao com outras camadas:** Le dados de RAW, gera artefatos para OUTPUT. Scripts de lint validam WIKI contra SCHEMA. Pode ser versionada com git.

## Camada 5: OUTPUT (Entregaveis)

- **Diretorios:** `output/` (rascunhos), `wiki/outputs/reports/`, `wiki/outputs/slides/`, `wiki/outputs/figures/`.
- **Conteudo:** Produtos finais do trabalho: relatorios, apresentacoes, diagramas, dashboards.
- **Interacao com outras camadas:** Gerado a partir do conhecimento na WIKI e dados em RAW usando ferramentas de OPERATIONAL. Regido por `output-filing.md`. Imutavel apos publicacao.

## Fluxo de Dados Entre Camadas

```
RAW --[leitura]--> OPERATIONAL --[processamento]--> OUTPUT
  |                      |
  |                      v
  +----[leitura]----> WIKI --[validacao]--> SCHEMA
                         |
                         +----[geracao]----> OUTPUT
```

Cada seta no diagrama e unidirecional -- nao ha dependencias circulares entre camadas. A camada WIKI depende de SCHEMA e RAW, mas SCHEMA e RAW nao dependem de nada acima delas.

## Regra de Acoplamento

Uma camada N pode depender apenas de camadas com numero menor que N. Exemplos:
- WIKI (camada 2) depende de RAW (camada 1) e SCHEMA (camada 3) -- permitido.
- SCHEMA (camada 3) nao pode depender de OUTPUT (camada 5) -- proibido.
- OPERATIONAL (camada 4) pode ler RAW (1), referenciar SCHEMA (3), e escrever OUTPUT (5).
