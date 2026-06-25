---
title: "Regras de Linkagem entre Paginas"
slug: "linking-rules"
type: schema
status: active
created: 2025-01-15
updated: 2026-06-23
tags:
  - schema
  - links
  - navegacao
source_count: 0
source_files: []
related_pages:
  - "[[frontmatter]]"
  - "[[page-types]]"
  - "[[naming]]"
---

# Regras de Linkagem entre Paginas

A forca da wiki esta na densidade e qualidade dos links internos. Links devem ser intencionais, verificaveis e bidirecionais sempre que possivel.

## Formato de Link

1. **Wikilinks do Obsidian como padrao unico.** Todo link interno usa o formato `[[pagina]]` ou `[[pagina|texto exibido]]`. Nao usar links Markdown `[texto](caminho.md)` para paginas internas -- isso quebra a retrocompatibilidade com o grafo do Obsidian.

2. **Caminhos relativos a raiz `wiki/`.** O alvo do wikilink e o caminho relativo a partir de `wiki/`, sem a extensao `.md`. Exemplo: `[[schema/naming]]` para linkar `wiki/schema/naming.md`.

3. **Ancoras para secoes.** Usar `[[pagina#secao]]` para linkar uma secao especifica. O titulo da secao no alvo deve estar em lowercase-kebab-case. Exemplo: `[[schema/naming#exemplos-corretos]]`.

## Regras de Linkagem

1. **Preferir hubs ao introduzir topicos.** Quando uma pagina menciona um dominio pela primeira vez, linkar para a pagina hub do dominio, nao para uma pagina-folha. Exemplo: mencionar "genomica" deve linkar `[[genomica-hub]]`, nao `[[alinhamento-bwa-mem]]`.

2. **Backlinks obrigatorios.** Toda pagina A que referencia pagina B deve garantir que B referencia A de volta. Isso pode ser direto (B lista A em `related_pages`) ou indireto (B e um hub que agrega A). A verificacao e feita pelo `lint-workflow.md`.

3. **Links de saida: minimo 1, maximo 10 por pagina.** Toda pagina deve linkar pelo menos uma outra pagina da wiki. Paginas com zero links de saida sao orfas. Paginas com mais de 10 links de saida devem considerar se um hub intermediario e necessario.

4. **Nao linkar a mesma pagina mais de 2 vezes no corpo.** A primeira mencao de um topico recebe o wikilink. Mencoes subsequentes na mesma pagina nao precisam ser linkadas novamente, exceto se houver uma razao contextual forte (maximo 2 mencoes linkadas por pagina alvo).

5. **Links externos usam Markdown padrao.** URLs para fora da wiki usam `[texto](https://...)`. Links externos nao devem ser usados no lugar de uma pagina interna que deveria existir -- se um topico externo e referenciado com frequencia, crie uma pagina `source-summary` para ele.

6. **`related_pages` no frontmatter.** O campo `related_pages` lista links semanticamente relacionados mas nao necessariamente citados no corpo do texto. E um complemento aos links inline, nao uma substituicao.

## Verificacao de Integridade

O script de lint valida:
- Nenhum wikilink aponta para pagina inexistente (link quebrado)
- Toda pagina referenciada em `related_pages` existe
- Nao ha links circulares sem saida (A -> B -> A e nada mais)
- Paginas orfas (zero backlinks) sao reportadas
