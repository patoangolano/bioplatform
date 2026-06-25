---
title: "Paleoproteomica e ZooMS: Identificacao Taxonomica por Colageno"
slug: "paleoproteomics-and-zoo-ms"
type: concept
status: active
created: 2026-06-23
updated: 2026-06-23
tags:
  - paleoproteomica
  - zooms
  - maldi-tof
  - colageno
  - espectrometria-de-massa
  - identificacao-taxonomica
  - dominio:paleogenomica
  - tipo:conceito
source_count: 0
source_files: []
related_pages:
  - "[[bioinformatics-hub]]"
  - "[[project-anchor]]"
  - "[[paleogenomica]]"
---
# Paleoproteomica e ZooMS: Identificacao Taxonomica por Colageno

ZooMS (Zooarchaeology by Mass Spectrometry) e um metodo de paleoproteomica que utiliza **fingerprinting de colageno tipo I** para identificar a especie de origem de fragmentos osseos quando a morfologia e insuficiente para diagnostico. O colageno e a proteina estrutural dominante no tecido osseo e sobrevive por dezenas de milhares de anos em condicoes arqueologicas, resistindo a degradacao melhor que o DNA devido a sua estrutura de tripla helice estabilizada por ligacoes cruzadas.

## Principio do Metodo

O colageno e extraido por desmineralizacao com HCl, digerido com tripsina, e os peptideos resultantes sao analisados por **espectrometria de massa MALDI-TOF** (Matrix-Assisted Laser Desorption/Ionization -- Time of Flight). O espectro produz um perfil de massas peptidicas -- um *peptide mass fingerprint* (PMF) -- que funciona como uma assinatura taxonomica. Os picos diagnosticos correspondem a mutacoes puntuais nos genes COL1A1 e COL1A2 que alteram a massa de peptideos triticos especificos entre especies proximas.

## Marcadores Diagnosticos

Os biomarcadores classicos incluem o peptideo COL1A2 502-519 (m/z ~1427 em Bos, ~1457 em Ovis/Capra) e o COL1A1 508-519 (m/z ~1105 em Cervus, ~1161 em Rangifer). A resolucao taxonomica alcanca genero e frequentemente especie, distinguindo por exemplo *Bos taurus* de *Bison* sp., ou *Ovis aries* de *Capra hircus*. Especies com divergencia evolutiva inferior a ~200 mil anos podem exigir sequenciamento tandem (LC-MS/MS) para resolucao adicional.

## Relevancia Computacional

Do ponto de vista da bioinformatica, a analise de dados ZooMS envolve tres etapas fundamentais:

1. **Processamento de espectros**: normalizacao de linha de base, deteccao de picos, calibracao interna com calibradores de massa conhecida (bradicinina, angiotensinogenio).

2. **Matching contra banco de dados**: os picos detectados sao comparados com bibliotecas de referencia de PMFs, como o banco ZooMS Reference Database. O pareamento utiliza tolerancia de massa tipica de 50-100 ppm e considera conjuntos de marcadores diagnosticos, nao picos isolados.

3. **Atribuicao taxonomica**: algoritmos de similaridade (distancia Euclidiana em espaco de massas, Jaccard sobre presenca/ausencia de picos) atribuem a amostra a um taxon. Ferramentas como mMass e scripts em R/Python implementam pipelines automatizadas para batch processing de centenas de espectros.

A [[paleogenomica]] oferece resolucao taxonomica superior via DNA antigo (aDNA), porem com custo e taxa de falha muito maiores em amostras degradadas do Holoceno. ZooMS e ordens de magnitude mais barato e rapido, funcionando como triagem -- amostras identificadas por ZooMS podem ser priorizadas para analise genomica posterior. A integracao de ambos os metodos e pratica corrente em estudos de [[bioinformatics-hub|bioinformatica]] aplicada a arqueologia molecular, onde pipelines como nf-core/eager integram dados proteomicos e genomicos em um unico grafo de proveniencia.
