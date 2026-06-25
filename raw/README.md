# raw/ — Camada de Fontes Imutáveis

Este diretório armazena fontes originais de conhecimento. **Nunca modifique, renomeie ou exclua arquivos aqui.**

## Regras

- Arquivos em `raw/` são tratados como fonte de verdade imutável
- Extrações, resumos e derivações devem ser criados em `wiki/sources/`
- Nunca "limpar", normalizar ou reescrever fontes no lugar
- Mover arquivos para fora de `raw/` apenas sob instrução explícita

## Subdiretórios

| Diretório | Propósito |
|-----------|-----------|
| `articles/` | Artigos salvos, blog posts técnicos |
| `papers/` | Artigos científicos (PDF, texto) |
| `repos/` | Repositórios clonados como referência |
| `datasets/` | Datasets ou metadados de datasets |
| `images/` | Imagens, diagramas, capturas de tela |
| `web-clips/` | Capturas do Obsidian Web Clipper |
| `assets/` | Assets locais referenciados pelo Obsidian |

## Fluxo de ingestão

1. Fonte adicionada a `raw/`
2. Resumo criado em `wiki/sources/`
3. Ideias extraídas atualizam `wiki/concepts/`, `wiki/entities/`, etc.
4. Atualizar `wiki/index.md` e `wiki/log.md`
