---
title: Projeto de Bioinformatica
type: project
created: 2026-06-23
tags: [projeto, bioinformatica, plataforma, ciencia]
links: [[project-anchor]] [[project-architecture]] [[project-status]]
---

# Projeto de Bioinformatica

A bioplatform e uma plataforma de bioinformatica reprodutivel construida como veiculo de aprendizado e portfolio profissional. Ela integra infraestrutura, ferramentas, pipelines e dominio cientifico em um sistema coerente e operacional.

## Perguntas Cientificas

A plataforma existe para responder perguntas biologicas concretas. As questoes centrais incluem:

1. **Expressao genica diferencial** -- Quais genes tem expressao alterada entre condicoes experimentais? Como isso se relaciona com vias metabolicas e funcoes celulares?

2. **Genomica populacional** -- Como variantes geneticas se distribuem em populacoes? Quais assinaturas de selecao ou deriva sao detectaveis?

3. **Paleogenomica** -- O que genomas antigos revelam sobre historia populacional, migracoes e adaptacao? Como validar a autenticidade de dados de aDNA?

4. **Identificacao taxonomica por proteinas** -- Quais especies estao representadas em conjuntos faunisticos arqueologicos? Como ZooMS complementa a identificacao morfologica?

## Metodos e Ferramentas

### RNA-Seq

Pipeline completo para analise transcriptomica:
- **Qualidade:** FastQC, MultiQC
- **Pre-processamento:** Trimmomatic, cutadapt
- **Alinhamento:** STAR, HISAT2
- **Quantificacao:** featureCounts, StringTie
- **Expressao diferencial:** DESeq2, edgeR
- **Analise funcional:** clusterProfiler, GSEA, enriquecimento GO/KEGG

### BLAST e Alinhamento de Sequencias

- BLASTn, BLASTp, tBLASTn contra bancos NCBI (nt, nr) e personalizados
- Criacao de bancos locais com makeblastdb
- Integracao via API e worker assincrono no backend

### Paleogenomica

- **Dano pos-mortem:** mapDamage, PMDtools
- **Pipeline aDNA:** nf-core/eager
- **Autenticacao:** padroes de fragmentacao, desaminacao terminal, comprimento de fragmento

### Paleoproteomica / ZooMS

- Identificacao por peptideos de colageno tipo I
- Marcadores diagnosticos por taxon
- Simulacao computacional de espectros MALDI-TOF

## Datasets de Referencia

- **SRA / GEO** -- Repositorios publicos de dados NGS para pratica e validacao
- **1000 Genomes Project** -- Variacao genomica populacional humana
- **Genomas antigos publicados** -- Allen Ancient DNA Resource, publicacoes com dados abertos
- **Bancos de colageno** -- Sequencias de referencia para ZooMS

## Conexao com Infraestrutura

A plataforma esta implantada em VPS Hostinger KVM4 ([[project-architecture]]). Os pipelines rodam em containers Docker, orquestrados por Nextflow, com resultados expostos via API FastAPI e consumo via servidores MCP. Consulte o [[infrastructure-hub]] para detalhes tecnicos.

---

Este documento e o resumo executivo do projeto. Para detalhes de implementacao, veja [[project-architecture]]. Para status atual, veja [[project-status]]. Para o proposito e motivacao, veja [[project-anchor]].
