---
title: Roadmap de Estudos
type: study-plan
created: 2026-06-23
tags: [estudo, roadmap, fases, planejamento]
links: [[overview]] [[learning-priorities]] [[study-method]]
---

# Roadmap de Estudos

Roteiro faseado de formacao em bioinformatica. Cada fase tem marcos concretos, ferramentas especificas e entregaveis conectados ao projeto. As fases sao sequenciais mas permitem sobreposicao -- voce pode avancar conceitos de uma fase enquanto pratica ferramentas da anterior.

## Fase 1: Fundamentos (em consolidacao)

**Objetivo:** Dominio do ambiente de desenvolvimento e operacao basica.

**Topicos:**
- Terminal Linux e CLI: navegacao, pipes, redirecionamento, grep, sed, awk
- Git: clone, branch, commit, push, pull, merge, rebase, .gitignore
- Docker: imagens, containers, volumes, networks, Dockerfile, docker-compose.yml
- Python para bioinformatica: scripts, argparse, pandas, BioPython, subprocess
- Estrutura de projetos: diretorios, README, documentacao, logging

**Entregaveis:**
- Repositorio GitHub organizado com CI/CD basico
- Docker Compose funcional no VPS
- Scripts Python para tarefas bioinformaticas rotineiras (parse de FASTA, consulta BLAST)

**Status:** Fase majoritariamente concluida. Manter pratica continua de CLI e Docker.

## Fase 2: Nucleo Bioinformatico (em andamento)

**Objetivo:** Executar e compreender um pipeline completo de RNA-Seq.

**Topicos:**
- Controle de qualidade: FastQC, MultiQC
- Pre-processamento: Trimmomatic, cutadapt
- Alinhamento: STAR, HISAT2 (indices, parametros, SAM/BAM)
- Pos-processamento: samtools (sort, index, flagstat)
- Quantificacao: featureCounts, StringTie
- Expressao diferencial: DESeq2 (design formula, normalizacao, p-valor ajustado)
- Visualizacao: PCA, heatmaps, volcano plots, IGV

**Entregaveis:**
- Pipeline RNA-Seq documentado com resultados validados
- Relatorio de qualidade (MultiQC) interpretado
- Analise de expressao diferencial com conclusoes biologicas

**Status:** Fase ativa. Foco atual do estudo.

## Fase 3: Engenharia de Workflow (curto prazo)

**Objetivo:** Automatizar e containerizar pipelines com Nextflow.

**Topicos:**
- Nextflow DSL2: canais, processos, workflows, operadores
- nf-core: estrutura, parametros, profiles, configuracao
- Containers para cada etapa: Dockerfiles otimizados
- Orquestracao: execucao local, execucao remota no VPS
- Rastreabilidade: Nextflow trace, reports, timeline

**Entregaveis:**
- Pipeline Nextflow funcional para RNA-Seq
- nf-core/rnaseq executado e customizado
- Imagens Docker publicadas no Docker Hub ou GitHub Container Registry

**Status:** Preparacao. Iniciar apos consolidacao da Fase 2.

## Fase 4: Especializacao (longo prazo)

**Objetivo:** Mergulhar em paleogenomica e paleoproteomica.

**Topicos:**
- DNA antigo (aDNA): fragmentacao, desaminacao, contaminacao
- nf-core/eager: pipeline para aDNA
- mapDamage: padroes de dano pos-mortem
- PMDtools: filtro de leituras com dano caracteristico
- Genomica populacional: PCA, ADMIXTURE, f-statistics
- ZooMS: espectrometria de massa MALDI-TOF, identificacao por peptideos de colageno
- Contexto arqueologico e etica em aDNA

**Entregaveis:**
- Analise de conjunto de dados publicos de aDNA
- Pipeline eager funcional com interpretacao de dano
- Protocolo ZooMS documentado (teorico, com simulacao computacional)

**Status:** Horizonte futuro. Depende de dominio solido das Fases 2 e 3.

---

Cada fase alimenta o [[bioinformatics-project]] e gera paginas de wiki. O roadmap e vivo -- ajuste conforme necessario, mas mantenha o registro das decisoes.
