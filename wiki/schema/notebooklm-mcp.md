---
title: "Uso do NotebookLM MCP na Wiki"
slug: "notebooklm-mcp"
type: schema
status: active
created: 2025-01-15
updated: 2026-06-23
tags:
  - schema
  - ferramenta:notebooklm
  - mcp
  - ingestao
source_count: 0
source_files: []
related_pages:
  - "[[ingest-workflow]]"
  - "[[query-workflow]]"
  - "[[workspace-architecture]]"
---

# Uso do NotebookLM MCP na Wiki

O NotebookLM MCP e uma ferramenta de pesquisa auxiliar baseada em Gemini 2.5 com RAG sobre fontes carregadas pelo usuario. Na wiki, ele e usado como acelerador de leitura e sintese, nunca como substituto das fontes cruas.

## Funcoes Suportadas

O servidor MCP `notebooklm` expoe as seguintes operacoes relevantes:

| Funcao               | Uso na Wiki                                                    |
|----------------------|----------------------------------------------------------------|
| `add_notebook`       | Registrar cadernos tematicos (ex: "Artigos de Genomica 2025") |
| `add_source`         | Ingerir artigos PDF e URLs de documentacao no caderno          |
| `ask_question`       | Interrogar o caderno com perguntas em portugues                |
| `generate_audio`     | Gerar Audio Overview para consumo rapido (nao substitui leitura)|
| `get_audio_status`   | Verificar progresso da geracao de audio                        |
| `download_audio`     | Salvar audio localmente para referencia                         |

## Fluxo de Uso para Digestao de Documentos Longos

### 1. Criar Caderno Tematico
Agrupar 3-10 fontes sobre o mesmo topico em um caderno do NotebookLM. Exemplo: "Pipeline de Chamada de Variantes" com artigos sobre GATK, DeepVariant, bcftools.

### 2. Carregar Fontes
Usar `add_source` com `type: "text"` para colar diretamente o texto extraido de PDFs ou com `type: "url"` para documentacao online. Aguardar indexacao (5-30 segundos).

### 3. Interrogar com Perguntas Dirigidas
Fazer perguntas especificas em portugues, por exemplo:
- "Qual a taxa de falsos positivos do GATK HaplotypeCaller em comparacao com DeepVariant?"
- "Quais parametros de filtragem sao recomendados para dados de exoma?"
- "Liste as limitacoes reportadas por cada estudo."

### 4. Refinar Perguntas
Usar o `session_id` retornado para manter contexto e refinar perguntas com base nas respostas anteriores. A sessao RAG do NotebookLM melhora a precisao em perguntas de seguimento.

### 5. Reconciliar com a Wiki
As respostas do NotebookLM sao insumos, nao verdades finais. Para cada insight obtido:
- Verificar contra a fonte original (o NotebookLM pode alucinar ou omitir contexto).
- Redigir em portugues tecnico para a pagina wiki relevante.
- Citar a fonte original, nao o NotebookLM.

## Regras Rigidas

1. **Nunca substituir arquivos crus.** O NotebookLM processa texto extraido; o arquivo original (PDF, URL, video) permanece a fonte canonica e deve ser armazenado no repositorio.

2. **Nunca citar o NotebookLM como fonte.** A citacao e sempre ao artigo, documentacao ou video original. O NotebookLM e uma ferramenta de leitura, nao uma fonte primaria.

3. **Audio Overview nao e revisao.** O audio gerado e util para consumo rapido, mas nao substitui a leitura tecnica cuidadosa. Nao criar paginas na wiki baseadas apenas no audio.

4. **Sessoes sao efemeras.** O `session_id` do NotebookLM expira. Insights extraidos devem ser imediatamente registrados na wiki. Nao depender de sessoes anteriores para recuperar contexto.

5. **Limite de 50 fontes por caderno (gratuito).** Planejar a divisao tematica dos cadernos considerando esse limite. Para projetos grandes, usar um caderno por subdominio.

## Integracao com o Fluxo de Ingestao

O NotebookLM acelera a etapa 2 (Inspecionar) e etapa 3 (Criar source-summary) do `[[ingest-workflow]]`. O fluxo modificado:

```
[Fonte Bruta] --> [NotebookLM: carregar e interrogar] --> [Source-Summary] --> ...
```

A etapa de Extracao (etapa 4) ainda exige leitura humana ou por LLM diretamente da fonte -- o NotebookLM pode perder detalhes tecnicos especificos que sao relevantes para a wiki.
