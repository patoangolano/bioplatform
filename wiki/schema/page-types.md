---
title: "Tipos de Paginas da Wiki"
slug: "page-types"
type: schema
status: active
created: 2025-01-15
updated: 2026-06-23
tags:
  - schema
  - page-types
  - vocabulario-controlado
source_count: 0
source_files: []
related_pages:
  - "[[frontmatter]]"
  - "[[naming]]"
  - "[[linking-rules]]"
---

# Tipos de Paginas da Wiki

Cada pagina da wiki pertence a exatamente um tipo. O tipo determina a estrutura esperada, o nivel de detalhe e as regras de linkagem aplicaveis.

## Catalogo de Tipos

| Tipo              | Descricao                                                                 |
|-------------------|---------------------------------------------------------------------------|
| `source-summary`  | Resumo tecnico de uma fonte externa: artigo, documentacao, video, dataset. |
| `concept`         | Definicao aprofundada de um conceito, metodo, algoritmo ou teoria.         |
| `entity`          | Descricao de uma entidade concreta: gene, proteina, farmaco, doenca.       |
| `project`         | Registro de um projeto de pesquisa ou desenvolvimento em andamento.        |
| `study-plan`      | Plano de estudos estruturado com topicos, recursos e cronograma.           |
| `career`          | Informacoes sobre carreira, habilidades, curriculo ou portfolio.           |
| `infrastructure`  | Documentacao de ferramentas, pipelines, scripts e ambiente computacional.  |
| `question`        | Pergunta de pesquisa registrada com contexto, hipoteses e estado.          |
| `output`          | Entregavel finalizado: relatorio, apresentacao, figura ou analise.         |
| `review`          | Revisao critica de literatura, ferramenta ou metodo com parecer tecnico.   |
| `hub`             | Pagina indice que agrega links para um topico ou dominio.                  |
| `schema`          | Documento normativo que define regras, formatos ou vocabularios da wiki.   |

## Regras por Tipo

### `source-summary`
- Deve conter: resumo, metodos principais, resultados-chave, limitacoes, link para fonte original.
- O campo `source_files` do frontmatter deve listar o caminho do arquivo-fonte.

### `concept`
- Deve conter: definicao formal, contexto historico, aplicacoes, referencias cruzadas.
- Usar diagramas Mermaid quando possivel para ilustrar relacoes.

### `entity`
- Deve conter: identificadores externos (NCBI, UniProt, PDB), funcao, localizacao, relevancia.
- Estrutura tabular para dados curados.

### `hub`
- Deve ser uma pagina de indice, nao de conteudo denso.
- Listar paginas filhas com descricao de uma linha cada.
- Nome do arquivo termina em `-hub.md`, exceto `home.md`.

### `schema`
- Define regras; nao contem opinioes ou analises.
- Deve ser conciso e normativo; cada regra deve ser testavel.
