---
title: Paleogenômica e DNA Antigo
tags:
  - paleogenomics
  - ancient-dna
  - bioinformatics
  - molecular-evolution
  - damage-patterns
created: 2026-06-23
aliases:
  - Ancient DNA
  - aDNA
  - Paleogenomic Analysis
---

# Paleogenômica e DNA Antigo

A análise computacional de DNA antigo (aDNA) impõe desafios singulares, uma vez que as moléculas recuperadas de espécimes arqueológicos sofrem degradação post-mortem severa. O principal marcador de autenticidade é o padrão de desaminação da citosina: nas extremidades 5' dos fragmentos, citosinas convertem-se espontaneamente em uracilas, que a polimerase lê como timinas, gerando um excesso característico de substituições C→T que decai ao longo dos primeiros 10 a 15 nucleotídeos. Esse sinal, estatisticamente distinto de polimorfismos biológicos, constitui a pedra angular da lógica de autenticação de sequências antigas.

Além da desaminação, o comprimento médio dos fragmentos endógenos situa-se entre 40 e 80 pares de bases -- muito abaixo do DNA moderno -- e a presença de DNA exógeno (bacteriano, fúngico e humano moderno) frequentemente excede 90% das reads brutas. A autenticação integra, portanto, múltiplas evidências: perfil de dano, distribuição de comprimento dos fragmentos e distância de edição em relação ao genoma de referência. Reads com edit distance anormalmente baixa e ausência de danos típicos são tratadas como potenciais contaminantes modernos.

Do ponto de vista computacional, o alinhamento contra genomas de referência requer ferramentas sensíveis a danos. O [[mapdamage]] (mapDamage) modela a probabilidade de substituição em função da posição na read e do contexto nucleotídico, gerando curvas de dano e estimativas bayesianas de bases genuínas. O [[pmdtools]] (PMDtools) emprega scores de dano post-mortem (PMD scores) para filtrar reads autênticas com base na razão de mismatches C→T nas extremidades. Complementarmente, pipelines como o [[pal-framework]] (PALEOMIX) integram adaptadores, trimming, mapeamento com [[bwa]] e chamada de variantes com [[gatk]] em fluxos reprodutíveis, essenciais para estudos de [[population-genetics]] e [[phylogeography]] com material degradado.
