---
title: Posicionamento Profissional
type: career
domain:
  - bioinformática
  - infraestrutura-computacional
level: estratégico
status: draft
tags:
  - posicionamento
  - bioinformática
  - nextflow
  - mcp
  - dna-antigo
created: 2026-06-23
---

# Posicionamento Profissional

Atuo como praticante de bioinformática com forte competência em infraestrutura computacional — uma combinação que vai além do analista que domina pipelines prontas e do engenheiro de dados que desconhece a biologia subjacente. O diferencial está na intersecção: sou capaz de dialogar com o laboratório úmido sobre qualidade de extração, concentração de inibidor e controles de contaminação, e no mesmo turno depurar um erro de `Nextflow` em um executor cloud ou projetar uma arquitetura de [[tooling-ecosystem|ferramentas]] baseada em [[mcp-architecture|MCP]].

## Diferenciais Técnicos

**Reprodutibilidade como princípio, não checklist.** Todo pipeline que desenvolvo parte de ambiente containerizado, versionamento explícito de genomas de referência e rastreabilidade completa de parâmetros — não por exigência de periódico, mas porque já perdi semanas tentando replicar análise alheia sem esses cuidados. Mantenho um [[reproducible-pipelines|framework interno de reprodutibilidade]] que se apoia em `nf-core`, containers Singularity/Docker e documentação embarcada nos workflows.

**Ecossistema de ferramentas via MCP.** Construo [[mcp-servers|servidores MCP]] que expõem APIs de bioinformática como ferramentas orquestráveis — bancos de dados genômicos, preditores de estrutura proteica e utilitários de anotação funcional. Esse ecossistema permite compor análises complexas sem sair do ambiente de consulta, reduzindo atrito e risco de erro manual. Ver [[mcp-ecosystem|visão geral do ecossistema]].

**Engenharia de workflow com Nextflow.** Domino canais, operadores, diretivas de executor (`aws`, `slurm`, `local`) e profiling de processos. Já escrevi workflows para alinhamento competitivo de leituras de [[ancient-dna|DNA antigo]] contra múltiplas referências, chamada de variantes com filtros de dano post-mortem e estimativa de contaminação com `ANGSD` e `AuthentiCT`. Ver [[nextflow-patterns|padrões de Nextflow]].

**Trilha de especialização em DNA antigo.** Entendo os desafios específicos do campo: fragmentação, desaminação em terminais 5' e 3', dano hidrolítico dependente de contexto sequencial, e a necessidade de pipelines que modelem explicitamente esses vieses. Trabalho com genomas de referência arcaicos, mapDamage, PMDtools e métodos Bayesianos de autenticação. Ver [[ancient-dna-pipelines|pipelines para aDNA]].

## Direção Estratégica

O plano é consolidar-me como a pessoa que conecta [[wet-lab|biologia molecular]] com computação de alto desempenho de forma pragmaticamente reprodutível — alguém que uma equipe de genômica chama tanto para discutir profundidade de cobertura esperada em amostras de 50 mil anos quanto para projetar a infraestrutura de execução que processará esses dados de forma rastreável e eficiente.
