---
title: "Nextflow e nf-core"
date: 2026-06-23
tags:
  - bioinformatica
  - workflow
  - nextflow
  - nf-core
  - reproducibilidade
  - containers
aliases:
  - "nextflow"
  - "nf-core"
  - "pipelines reprodutiveis"
---

## Nextflow e nf-core: Orquestracao reprodutivel em bioinformatica

Em bioinformatica, pipelines analiticas frequentemente encadeiam dezenas de ferramentas -- alinhadores como [[bwa]], chamadores de variantes como [[gatk]], quantificadores como [[salmon]] -- sobre centenas de amostras. Executar essas etapas manualmente e insustentavel e irreprodutivel. E aqui que entram os _workflow managers_.

O **Nextflow** (DSL2) resolve isso com um modelo baseado em _dataflow_: cada etapa e um `process` que recebe dados de `channel` e emite resultados para o proximo processo, sem que o usuario gerencie arquivos intermediarios. O motor suporta **resumability** -- se uma tarefa falha, o pipeline retoma do ponto exato da falha usando o _work directory_ cacheado, economizando horas de recomputacao. A execucao e **containerizada por padrao** (Docker, Singularity, Podman, Charliecloud), garantindo que cada ferramenta rode no ambiente exato definido pelo desenvolvedor, independente da infraestrutura (HPC, nuvem, desktop). O suporte a **conda** e **spack** oferece alternativas quando containers nao sao viaveis.

O projeto **nf-core** ([[nf-core]]) vai alem: fornece um ecossistema de pipelines comunitarios curados, todos seguindo uma estrutura padronizada de diretorios, _module system_ reutilizavel e **testes de integracao continua (CI)** com GitHub Actions. Cada pipeline publicada passa por _linting_ rigoroso e testes automaticos com dados de referencia antes de ser liberada. Pipelines como `nf-core/rnaseq`, `nf-core/sarek` (variantes somaticas/germinativas), `nf-core/taxprofiler` (perfil taxonomico metagenomico) e `nf-core/mag` (genomas montados a partir de metagenomas) sao mantidas por especialistas da comunidade e revisadas por pares.

A combinacao Nextflow + nf-core resolve o problema central da **reproducibilidade bioinformatica**: um pipeline definido como codigo, versionado no GitHub, executado dentro de containers imutaveis e retomavel em qualquer infraestrutura. O resultado e analise _portable, escalavel e auditavel_ -- requisito fundamental para publicacoes cientificas e para aplicacoes clinicas que dependem de [[regulacao-e-qualidade]].

## Escala e Avaliacao para Producao

Segundo o relatorio [[devops-computational-biology|DevOps Deep Research]] (claim verificada 3-0; *Genome Biology* 2025, DOI 10.1186/s13059-025-03673-9), o nf-core ja oferece **mais de 1.400 modulos reutilizaveis** e cerca de **80 subworkflows** em DSL2. Essa modularidade permite **adocao incremental**: um grupo pode incorporar modulos comunitarios sem reescrever pipelines inteiras.

Uma armadilha de avaliacao destacada pelo relatorio: **nunca julgar um framework de workflow comparando exemplos de prova-de-conceito (PoC)** -- eles parecem enganosamente semelhantes. O que separa componentes prontos para producao (nf-core, snakemake-wrappers, BioWDL) de exemplos didaticos e o que _nao_ aparece no PoC: containerizacao com versao fixa, calculo de memoria-por-CPU, tratamento estruturado de erros, metadados YAML e testes automaticos com validacao por snapshot. Vale notar tambem o que foi **refutado** na verificacao adversarial: afirmacoes de que "Nextflow superou Snakemake em adocao" (metricas de citacao nao medem adocao) e de que "Airflow serve para pipelines bioinformaticos" (Airflow e para ETL, nao DAGs cientificos).
