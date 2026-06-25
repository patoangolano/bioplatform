---
title: "Fluxo de Ingestao de Fontes"
slug: "ingest-workflow"
type: schema
status: active
created: 2025-01-15
updated: 2026-06-23
tags:
  - schema
  - workflow
  - ingestao
  - fontes
source_count: 0
source_files: []
related_pages:
  - "[[page-types]]"
  - "[[frontmatter]]"
  - "[[linking-rules]]"
  - "[[lint-workflow]]"
---

# Fluxo de Ingestao de Fontes

O processo de ingestao transforma fontes externas (artigos, documentacoes, videos, datasets) em paginas estruturadas da wiki. Cada etapa produz um artefato verificavel. Nenhuma etapa pode ser pulada.

## Etapas

### 1. Detectar Fonte
Identificar o tipo de fonte: artigo academico (DOI), pagina de documentacao (URL), video (YouTube ID), dataset (accession number), repositorio (GitHub URL), livro (ISBN). O tipo determina o template inicial e os campos obrigatorios.

### 2. Inspecionar
Abrir e examinar a fonte. Para artigos: ler abstract, figuras principais, conclusao. Para documentacao: identificar a versao, escopo e pre-requisitos. Para videos: assistir em velocidade acelerada, anotar timestamps de secoes relevantes.

### 3. Criar `source-summary`
Criar pagina do tipo `source-summary` em `wiki/fontes/`. A pagina deve conter obrigatoriamente:
- **Resumo:** 3-5 paragrafos em portugues cobrindo motivacao, metodo, resultados, conclusao.
- **Metadados da fonte:** DOI, URL, autores, data de publicacao, versao.
- **Pontos-chave:** lista de 3-7 afirmacoes tecnicas extraidas.
- **Limitacoes:** vieses, escopo restrito, dados ausentes.
- **Link cru:** caminho para o arquivo-fonte no repositorio.

### 4. Extrair Ideias, Ferramentas e Entidades
Para cada conceito, ferramenta ou entidade mencionada na fonte:
- Se ja existe pagina na wiki, adicionar mencionar a fonte como referencia e atualizar `source_count`.
- Se nao existe, criar pagina minima (`seed`) com o essencial extraido da fonte.
- Registrar a ligacao em ambos os lados (fonte -> pagina e pagina -> fonte).

### 5. Atualizar Paginas Afetadas
Varrer todas as paginas que referenciam conceitos alterados pela nova fonte. Atualizar claims com a nova evidencia. Adicionar contra-pontos se a fonte contradiz conhecimento existente (marcar com tag `contradicao` para revisao posterior).

### 6. Atualizar Indice
Adicionar a nova `source-summary` ao hub correspondente (ex: `fontes-hub.md`). Se o dominio nao tem hub, criar um.

### 7. Registrar Entrada de Log
Adicionar linha ao arquivo `wiki/changelog.md` com: data, tipo de fonte, titulo, paginas afetadas, numero de novas paginas criadas. Exemplo:

```
2026-06-23 | artigo | "FastQC: quality control for high-throughput sequence data" | 3 paginas afetadas | 1 nova pagina
```

## Diagrama de Estados

```
[Fonte Bruta] --> [Inspecao] --> [Source-Summary] --> [Extracao] --> [Atualizacao] --> [Indice] --> [Log]
                      |                                    |
                      v                                    v
                 [Arquivo Fonte]                    [Novas Paginas Seed]
```
