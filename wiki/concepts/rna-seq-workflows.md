---
title: "Fluxos de Trabalho RNA-Seq"
date: 2026-06-23
tags:
  - transcriptomica
  - bioinformatica
  - pipeline
  - ngs
  - expressao-genica
  - reproducibilidade
related:
  - "[[controle-qualidade-fastqc]]"
  - "[[alinhamento-star-hisat2]]"
  - "[[quantificacao-salmon-kallisto]]"
  - "[[expressao-diferencial-deseq2]]"
  - "[[plataforma-bioplatform]]"
  - "[[mcp-servers-vps]]"
status: em_andamento
---

## Visao Geral

RNA-Seq funciona como dominio-ancora pratico para toda a [[plataforma-bioplatform]]. A partir de leituras FASTQ brutas, a cadeia tipica percorre controle de qualidade, quantificacao de transcritos e expressao diferencial, cada etapa disparando chamadas a servidores MCP hospedados no VPS.

## Controle de Qualidade

O ponto de partida e o [[controle-qualidade-fastqc|FastQC]], executado via `mcp__bio-fastqc__fastqc_single` e sumarizado com `mcp__bio-fastqc__multiqc_report`. Leituras de baixa qualidade, contaminacao por adaptadores ou vies de GC sao sinalizadas antes de qualquer processamento downstream -- corrigir aqui evita propagar ruido para as etapas seguintes.

## Alinhamento e Quantificacao

Dois caminhos coexistem. O classico usa alinhadores splice-aware como [[alinhamento-star-hisat2|STAR ou HISAT2]], acionados via `mcp__bio-bwa__bwa_mem` ou ferramentas dedicadas, gerando BAMs que o `mcp__bio-samtools__samtools_sort` e `mcp__bio-samtools__samtools_index` organizam. A alternativa moderna -- [[quantificacao-salmon-kallisto|Salmon ou kallisto]] -- quantifica diretamente contra o transcriptoma de referencia sem produzir alinhamentos intermediarios, sendo muito mais rapida e igualmente acurada para expressao diferencial.

## Expressao Diferencial

Com matrizes de contagem em maos, o [[expressao-diferencial-deseq2|DESeq2]] (R/Bioconductor) modela a dispersao e aplica testes de Wald generalizados. O VPS executa scripts R como processos persistentes via `mcp__plugin_desktop-commander_desktop-commander__start_process`, e os resultados -- log2 fold changes, p-values ajustados, genes diferencialmente expressos -- sao persistidos no PostgreSQL do projeto (`mcp__postgres__query`) para consulta e visualizacao.

## Visualizacao e Reproducibilidade

Graficos de vulcao, heatmaps e PCA sao gerados programaticamente e versionados junto ao codigo da analise. Toda a cadeia e orquestrada de forma reprodutivel: parametros de cada etapa ficam registrados no banco, e snapshots de ambiente (versoes de pacotes R, indices de referencia usados) garantem que qualquer resultado possa ser recalculado. A integracao com os [[mcp-servers-vps|servidores MCP no VPS]] permite disparar pipelines completos a partir do chat, com logs centralizados e notificacoes ao final de cada etapa.
