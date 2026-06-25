---
title: "Fluxo de Consulta a Wiki"
slug: "query-workflow"
type: schema
status: active
created: 2025-01-15
updated: 2026-06-23
tags:
  - schema
  - workflow
  - consulta
  - pesquisa
source_count: 0
source_files: []
related_pages:
  - "[[page-types]]"
  - "[[linking-rules]]"
  - "[[output-filing]]"
  - "[[home]]"
---

# Fluxo de Consulta a Wiki

Quando um usuario ou agente faz uma pergunta cuja resposta pode residir na wiki, o seguinte fluxo garante que a resposta seja completa, verificada e rastreavel.

## Etapas

### 1. Ler Pagina Indice
Comecar por `home.md`, que lista os hubs principais. Identificar quais dominios estao relacionados a pergunta. Se a pergunta envolve "alinhamento de reads", os hubs candidatos sao `genomica-hub.md` e `ferramentas-hub.md`.

### 2. Identificar Hubs Relevantes
Abrir cada hub candidato. Hubs contem listas de paginas-folha com descricao de uma linha. Selecionar as paginas-folha com maior probabilidade de conter a resposta. Priorizar paginas com status `active` ou `reviewed`.

### 3. Leitura Profunda
Ler integralmente cada pagina-folha selecionada. Nao fazer skim -- a resposta pode estar em uma secao tardia ou em um detalhe de implementacao. Seguir os wikilinks para paginas relacionadas se o conteudo for insuficiente.

### 4. Sintetizar Resposta
Combinar informacoes de multiplas paginas em uma resposta coerente. Citar explicitamente cada pagina-fonte no formato `[[pagina]]`. Se houver contradicao entre paginas, reporta-la -- nao escolher um lado silenciosamente.

### 5. Decidir se a Resposta Torna-se Pagina Duravel
Criterios para promover a resposta a pagina permanente:
- A pergunta foi feita mais de uma vez.
- A sintese conectou 3 ou mais paginas existentes de forma nao obvia.
- A resposta contem conhecimento procedural (passos, comandos, parametros).
- O topico nao esta adequadamente coberto por nenhuma pagina existente.

Se aprovado, criar pagina do tipo `question` ou `concept` em `wiki/`.

### 6. Atualizar Links
Se uma nova pagina foi criada:
- Adiciona-la ao(s) hub(s) relevante(s).
- Garantir backlinks de todas as paginas-fonte referenciadas.
- Atualizar `related_pages` nas paginas conectadas.

### 7. Registrar Log
Adicionar entrada ao `changelog.md`:
```
2026-06-23 | consulta | "Como otimizar o BWA-MEM para reads longos?" | 3 paginas consultadas | 1 nova pagina
```

## Regra de Ouro

Se a wiki nao tem a resposta, a consulta torna-se uma oportunidade de ingestao: registrar a pergunta como pagina `question`, pesquisar fontes externas, executar o `[[ingest-workflow]]`, e entao responder com base na nova fonte ingerida. Nao responder com conhecimento nao verificado.
