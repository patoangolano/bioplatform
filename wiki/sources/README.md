# wiki/sources/ — Resumos de Fontes

Resumos de fontes imutáveis armazenadas em `raw/`.

## Propósito

Cada página nesta pasta corresponde a uma ou mais fontes em `raw/`. O resumo extrai:
- Ideias principais
- Métodos e ferramentas mencionados
- Datasets e entidades referenciados
- Claims e evidências
- Questões em aberto

## Template

```markdown
***
title: string
slug: string
type: source-summary
status: seed | draft | active | reviewed
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [array]
source_count: integer
source_files: [array of paths relative to raw/]
related_pages: [array]
***

# Título do Resumo

## Fonte
- Arquivo: `raw/...`
- Tipo: artigo | paper | repo | dataset | web-clip

## Resumo
...

## Ideias-Chave
- ...

## Ferramentas e Métodos
- ...

## Entidades Referenciadas
- ...

## Questões em Aberto
- ...
```
