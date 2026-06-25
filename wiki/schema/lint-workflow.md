---
title: "Checklist de Lint da Wiki"
slug: "lint-workflow"
type: schema
status: active
created: 2025-01-15
updated: 2026-06-23
tags:
  - schema
  - workflow
  - lint
  - qualidade
source_count: 0
source_files: []
related_pages:
  - "[[frontmatter]]"
  - "[[naming]]"
  - "[[linking-rules]]"
  - "[[page-types]]"
---

# Checklist de Lint da Wiki

O processo de lint deve ser executado apos cada sessao de edicao que afete 3 ou mais paginas, ou semanalmente como rotina de manutencao. Cada item da checklist e acionavel e produz um diagnostico especifico.

## 1. Contradicoes
- Varrer pares de paginas que tratam do mesmo topico (mesma tag de dominio).
- Para cada par, comparar claims factuais: parametros, comandos, limiares, versoes.
- Se duas paginas afirmam valores diferentes para o mesmo fato, marcar ambas com tag `contradicao` e abrir pagina `question` para resolucao.

## 2. Claims Obsoletas
- Identificar paginas cujo `updated` e anterior a 6 meses.
- Para cada uma, verificar se as claims ainda sao validas consultando a versao atual das ferramentas referenciadas.
- Claims sobre versoes especificas de software (ex: "GATK 4.2") sao particularmente suscetiveis a obsolescencia.
- Atualizar ou marcar com tag `desatualizado`.

## 3. Paginas Orfas
- Uma pagina e orfa se nenhuma outra pagina da wiki referencia ela (zero backlinks).
- Excecoes: `home.md` e paginas do tipo `output`.
- Para cada orfa: decidir se deve ser linkada a partir de um hub, fundida com pagina similar, ou arquivada.

## 4. Backlinks Ausentes
- Para cada wikilink `[[A]]` encontrado no corpo de uma pagina, verificar se A referencia a pagina de origem em `related_pages` ou no corpo.
- Backlinks assimetricos sao permitidos se A for um hub (hubs nao listam todas as paginas filhas em `related_pages`, pois ja as listam no corpo).

## 5. Links Quebrados
- Todo wikilink `[[X]]` deve corresponder a um arquivo `X.md` existente.
- Todo `[[X#secao]]` deve corresponder a uma secao existente no arquivo `X.md`.
- Links quebrados devem ser corrigidos (se a pagina existe com nome diferente) ou a pagina ausente deve ser criada como `seed`.

## 6. Paginas Duplicadas
- Identificar paginas com titulos muito similares (distancia de Levenshtein < 5) ou mesma tag de dominio + mesmo topico.
- Fundir duplicatas: manter a mais completa, redirecionar a outra com link `[[pagina-canonic]]`.

## 7. Paginas Superdimensionadas
- Paginas com mais de 200 linhas devem ser divididas em sub-paginas.
- Cada sub-pagina herda as tags da pagina original e adiciona uma tag especifica.
- A pagina original torna-se um mini-hub linkando as sub-paginas.

## 8. Lacunas de Dominio
- Comparar as tags de dominio presentes na wiki com uma lista de dominios esperados (definida em `home.md`).
- Dominios sem nenhuma pagina `active` sao reportados como lacunas.
- Para cada lacuna, abrir pagina `question` descrevendo o que falta.

## Frequencia e Responsabilidade

| Gatilho                        | Frequencia        |
|--------------------------------|-------------------|
| Sessao de edicao (3+ paginas)  | Ao final da sessao|
| Sessao de ingestao             | Apos etapa 7      |
| Rotina de manutencao           | Semanal           |
| Pre-release de versao da wiki  | Obrigatorio       |

O resultado do lint e registrado em `wiki/lint-log.md` com data, itens executados, e contagem de problemas encontrados por categoria.
