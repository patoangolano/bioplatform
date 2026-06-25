---
title: "Regras de Nomenclatura de Arquivos e Pastas"
slug: "naming"
type: schema
status: active
created: 2025-01-15
updated: 2026-06-23
tags:
  - schema
  - nomenclatura
  - convencoes
source_count: 0
source_files: []
related_pages:
  - "[[frontmatter]]"
  - "[[page-types]]"
  - "[[linking-rules]]"
---

# Regras de Nomenclatura

Toda pagina e pasta da wiki segue um conjunto estrito de convencoes de nomenclatura. O objetivo e garantir previsibilidade, evitando colisoes e ambiguidades na linkagem entre paginas.

## Regras para Arquivos Markdown

1. **lowercase-kebab-case obrigatorio.** Todo nome de arquivo `.md` usa apenas letras minusculas, digitos e hifens. Exemplo: `alinhamento-bwa-mem.md`. Nada de underscores, camelCase, espacos ou caracteres especiais.

2. **Extensao unica `.md`.** Nao usar `.mdx`, `.markdown` ou outras variantes. O ecossistema de ferramentas (Obsidian, MkDocs, scripts de lint) espera exclusivamente `.md`.

3. **Nomes descritivos e estaveis.** O nome do arquivo deve refletir o conteudo de forma precisa e duradoura. Evitar nomes genericos como `notas.md` ou `rascunho.md`. Preferir `chamada-de-variantes-gatk.md` a `variant-calling.md` (portugues sempre).

4. **Paginas hub terminam em `-hub.md`.** Excecao unica: a pagina raiz da wiki chama-se `home.md`. Exemplos: `genomica-hub.md`, `ferramentas-hub.md`, `projetos-hub.md`.

5. **Proibido espacos e underscores.** O sistema de linkagem `[[pagina]]` do Obsidian trata espacos e underscores de forma inconsistente entre plataformas. Hifens sao o unico separador permitido.

6. **Profundidade maxima de 3 niveis.** Nenhum arquivo `.md` deve estar a mais de 3 niveis de profundidade a partir de `wiki/`. Exemplo valido: `wiki/dominios/genomica/alinhamento.md`. Exemplo invalido: `wiki/a/b/c/d/pagina.md`.

## Regras para Pastas

1. Mesmo esquema lowercase-kebab-case dos arquivos.
2. Nomes no plural para pastas que contem colecoes: `entidades/`, `projetos/`, `fontes/`.
3. Nomes no singular para pastas de infraestrutura: `schema/`, `output/`, `template/`.
4. Nenhuma pasta vazia deve existir no repositorio.

## Regras para Titulos (Dentro do Frontmatter)

1. O campo `title` no YAML frontmatter deve estar em portugues.
2. Deve ser descritivo o suficiente para identificar o conteudo sem abrir o arquivo.
3. Maximo de 80 caracteres. Sem dois-pontos no titulo (conflito com sintaxe YAML).
4. O titulo pode conter espacos e maiusculas -- e um campo de apresentacao, nao um slug.

## Exemplos Corretos

| Arquivo                          | Valido? | Motivo                                      |
|----------------------------------|---------|---------------------------------------------|
| `home.md`                        | Sim     | Pagina raiz, excecao documentada            |
| `genomica-hub.md`                | Sim     | Hub segue sufixo `-hub`                     |
| `alinhamento-bwa-mem.md`         | Sim     | lowercase-kebab-case em portugues           |
| `Alinhamento.md`                 | Nao     | Contem maiuscula                            |
| `bwa_mem.md`                     | Nao     | Usa underscore em vez de hifen              |
| `meu artigo sobre pipelines.md`  | Nao     | Contem espacos                              |
