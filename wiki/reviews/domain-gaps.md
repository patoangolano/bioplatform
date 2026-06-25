---
title: "Lacunas de Domínio"
date: 2026-06-23
status: "documentado"
tags:
  - arquitetura
  - escopo
  - planejamento
related:
  - "[[plataforma-visao]]"
  - "[[especializacao-rnaseq]]"
  - "[[paleogenomica-track]]"
  - "[[roadmap-fases]]"
---

# Lacunas de Domínio

A plataforma atualmente opera com escopo deliberadamente restrito. As lacunas de domínio
abaixo representam áreas da bioinformática **intencionalmente não cobertas** nesta fase,
em linha com a especialização progressiva que parte de [[rna-seq]] e avança rumo a
[[paleogenomica-track]].

## Lacunas Identificadas

1. **Genética de populações.** Não há suporte para estatísticas F (Fst, Fis, Fit),
   análise de estrutura populacional (STRUCTURE, ADMIXTURE), equilíbrio de Hardy-Weinberg,
   ou testes de seleção (Tajima's D, dN/dS). Totalmente fora do escopo atual.

2. **Single-cell RNA-Seq.** O pipeline de [[rna-seq]] cobre apenas experimentos *bulk*.
   Não há detecção de doublets, *barcode* demultiplexing, integração de amostras (CCA,
   Harmony), análise de trajetória (Monocle, RNA velocity) ou *clustering* baseado em
   grafos (Leiden, Louvain) — padrões essenciais em [[scrna-seq]] que exigiriam
   contêineres com dependências pesadas (Scanpy, Seurat, scVI).

3. **Predição de estrutura proteica.** AlphaFold, ESMFold, RosettaFold e ferramentas de
   *docking* molecular estão ausentes. Não há integração com bancos como [[PDB]] ou
   UniProt para predição *ab initio*. Essa lacuna é estrutural: predição de estrutura
   demanda GPU e não se alinha com o foco em dados de sequenciamento.

4. **Metabolômica.** Ausência total de suporte a espectrometria de massas (m/z,
   LC-MS/MS, GC-MS), anotação de picos, vias metabólicas (KEGG, MetaCyc) ou
   integração multiômica com transcriptômica. A [[metabolomica]] exigiria formatos
   como mzML, mzXML e motores de busca como SIRIUS ou GNPS.

5. **Metagenômica.** Não há pipeline para montagem *de novo* de genomas microbianos
   (MEGAHIT, metaSPAdes), *binning* taxonômico (Kraken2, MetaPhlAn), anotação
   funcional de genes marcadores ou análise de diversidade alfa/beta. [[metagenomica]]
   exigiria infraestrutura de banco de dados de referência (GTDB, RefSeq) que a
   plataforma atual não comporta.

## Justificativa

Estas lacunas são **aceitáveis e intencionais** para a fase corrente. O desenho da
plataforma segue uma especialização em [[rna-seq]] como fundação, com progressão para
[[paleogenomica-track]] — onde o dano *post-mortem* característico do DNA antigo
(fragmentação, desaminação de citosina) exige adaptações específicas do pipeline de
alinhamento e chamada de variantes. Cada lacuna acima poderá ser reavaliada em
[[roadmap-fases]] futuras, mas a prioridade permanece na profundidade vertical do
nicho RNA-Seq em vez da cobertura horizontal de múltiplas ômicas.
