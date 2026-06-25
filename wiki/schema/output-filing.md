---
title: "Regras de Arquivamento de Outputs"
slug: "output-filing"
type: schema
status: active
created: 2025-01-15
updated: 2026-06-23
tags:
  - schema
  - output
  - arquivamento
  - entregaveis
source_count: 0
source_files: []
related_pages:
  - "[[page-types]]"
  - "[[query-workflow]]"
  - "[[ingest-workflow]]"
---

# Regras de Arquivamento de Outputs

Outputs sao entregaveis gerados a partir do conhecimento da wiki: relatorios, apresentacoes, figuras, scripts de analise. Eles seguem um ciclo de vida separado das paginas de conhecimento, com pastas e regras proprias.

## Estrutura de Pastas

```
raiz/
  output/                    # rascunhos e trabalhos em andamento
  wiki/outputs/
    reports/                 # relatorios finalizados (PDF, DOCX, MD)
    slides/                  # apresentacoes (PPTX, PDF, MD com reveal.js)
    figures/                 # figuras e diagramas (PNG, SVG, Mermaid)
```

## Regras por Tipo

### `output/` (Rascunhos)
- Uso livre durante o trabalho ativo.
- Nomes de arquivo devem ser descritivos mas nao precisam seguir kebab-case estrito.
- Nenhum arquivo em `output/` e referenciado por paginas da wiki.
- Ao finalizar, o arquivo e movido para a pasta de saida correspondente e uma pagina `output` e criada na wiki.

### `wiki/outputs/reports/` (Relatorios Finalizados)
- Conteudo: analises completas, revisoes de literatura, documentacao de projetos.
- Formatos aceitos: PDF (preferencial), DOCX, MD.
- Cada relatorio ganha uma pagina `output` na wiki com: titulo, resumo, data, caminho do arquivo, paginas-fonte consultadas.
- Nome do arquivo: `YYYY-MM-DD-descricao-breve.pdf`. Exemplo: `2026-06-23-analise-diferencial-rnaseq.pdf`.

### `wiki/outputs/slides/` (Apresentacoes)
- Conteudo: slides para seminarios, aulas, defesas, reunioes.
- Formatos aceitos: PPTX, PDF, MD (para reveal.js ou similar).
- Cada apresentacao ganha pagina `output` na wiki.
- Nome do arquivo: `YYYY-MM-DD-titulo-apresentacao.pptx`.

### `wiki/outputs/figures/` (Figuras)
- Conteudo: diagramas, graficos, ilustracoes tecnicas.
- Formatos aceitos: PNG (rasters), SVG (vetores), Mermaid (diagramas como codigo).
- Figuras devem ser versionadas -- o codigo-fonte que gerou a figura (script Python, R, Mermaid) deve ser armazenado junto ou referenciado na pagina `output`.
- Nome do arquivo: `descricao-breve.png` ou `YYYY-MM-DD-descricao.svg`.

## Promocao de Rascunho para Finalizado

1. Mover arquivo de `output/` para a subpasta de destino correta.
2. Criar pagina `output` na wiki.
3. Preencher frontmatter: `type: output`, status `active`, `source_files` com caminho do arquivo.
4. Linkar a pagina `output` a partir do hub relevante.
5. Adicionar entrada ao `changelog.md`.

## Regra de Imutabilidade

Arquivos em `wiki/outputs/` sao considerados imutaveis apos publicacao. Correcoes geram uma nova versao com nova data no nome do arquivo. A pagina `output` correspondente deve listar o historico de versoes.
