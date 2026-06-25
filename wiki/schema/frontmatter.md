---
title: "Template de Frontmatter YAML"
slug: "frontmatter"
type: schema
status: active
created: 2025-01-15
updated: 2026-06-23
tags:
  - schema
  - frontmatter
  - metadados
source_count: 0
source_files: []
related_pages:
  - "[[page-types]]"
  - "[[naming]]"
  - "[[linking-rules]]"
---

# Template de Frontmatter YAML

Toda pagina da wiki exige o bloco YAML abaixo entre `---`. Campos com valores controlados estao documentados com os vocabularios de referencia.

## Template Obrigatorio

```yaml
---
title: string          # titulo em portugues, descritivo e conciso
slug: string           # derivado automaticamente do nome do arquivo
type: page-type        # um dos tipos definidos em page-types.md
status: seed | draft | active | reviewed | archived
created: YYYY-MM-DD   # data de criacao da pagina
updated: YYYY-MM-DD   # data da ultima atualizacao significativa
tags: [array]          # lista de strings em kebab-case, maximo 10
source_count: integer  # numero de fontes externas referenciadas
source_files: [array]  # caminhos relativos ao repositorio das fontes
related_pages: [array] # links internos no formato [[pagina]]
---
```

## Vocabulario Controlado: `status`

| Valor      | Significado                                                     |
|------------|-----------------------------------------------------------------|
| `seed`     | Ideia inicial registrada; conteudo minimo, ainda nao estruturado|
| `draft`    | Estrutura basica presente; passivel de expansao e revisao       |
| `active`   | Conteudo completo e atualizado; pagina em uso corrente          |
| `reviewed` | Revisao tecnica concluida; validada por segunda leitura         |
| `archived` | Conteudo historico; mantido por referencia, nao mais ativo      |

## Vocabulario Controlado: `tags`

Tags seguem kebab-case em portugues. Prefixos reservados:

- `tipo:` para classificar a natureza da pagina (ex: `tipo:protocolo`)
- `dominio:` para area de conhecimento (ex: `dominio:genomica`)
- `ferramenta:` para ferramentas associadas (ex: `ferramenta:bcftools`)

Exemplos validos: `genomica`, `alinhamento`, `bwa-mem`, `controle-qualidade`, `tipo:tutorial`, `dominio:bioinformatica`, `ferramenta:samtools`.

## Validacao Automatica

O script `lint-workflow.md` verifica:
- Presenca obrigatoria de `title`, `type`, `status`, `created`, `tags`
- `type` pertence ao vocabulario de `page-types.md`
- `status` pertence ao vocabulario acima
- `created` e `updated` no formato ISO 8601 (YYYY-MM-DD)
- `tags` sem duplicatas e em kebab-case
- `related_pages` com links validos para paginas existentes
