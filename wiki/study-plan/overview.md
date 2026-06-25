---
title: Visao Geral do Plano de Estudos
type: study-plan
created: 2026-06-23
tags: [estudo, plano, overview, aprendizado]
links: [[roadmap]] [[learning-priorities]] [[study-method]] [[bioinformatics-project]]
---

# Visao Geral do Plano de Estudos

O plano de estudos da bioplatform e cumulativo e profundamente conectado a execucao pratica do projeto. Nao se estuda para depois aplicar -- estuda-se aplicando, documentando e iterando. Cada topico estudado vira uma pagina de wiki, um script funcional, ou uma melhoria na plataforma.

## Filosofia

Aprendizado orientado a projeto (project-driven learning): o projeto define o que estudar, e o estudo alimenta o projeto. Ciclo virtuoso onde teoria e pratica se reforcam mutuamente. O wiki e o registro vivo desse processo.

## Estagios do Plano

### Foco Atual (Junho 2026)

O momento presente esta concentrado em duas frentes:

1. **Praticas de RNA-Seq** -- Executar o pipeline completo com dados publicos (SRA, GEO). Passar por FastQC, Trimmomatic, alinhamento com STAR, quantificacao com featureCounts, analise de expressao diferencial com DESeq2. Documentar cada etapa no wiki. Comparar resultados com a literatura para validacao.

2. **Fluencia em Docker** -- Criar Dockerfiles para ferramentas bioinformaticas. Entender multi-stage builds, entrypoints, volumes, networks. Fazer deploy de containers no VPS. A meta e operar Docker com naturalidade, como quem usa o terminal.

### Proximos Passos (Curto Prazo)

Assim que o foco atual estiver solido:

- **Fundamentos de Nextflow** -- Sintaxe DSL2, canais, processos, operadores. Escrever pipelines simples antes de usar nf-core. Entender o modelo de execucao e o trace de tarefas.

- **Primeiro pipeline nf-core** -- Rodar nf-core/rnaseq com dados de teste. Entender parametros, profiles, configuracao de execucao (local, Docker). Comparar saida com o pipeline manual feito antes.

- **Containerizacao de pipelines** -- Criar imagens Docker para cada etapa. Garantir que o pipeline rode identico em qualquer maquina.

### Estagio Avancado (Longo Prazo)

Horizontes de especializacao:

- **Paleogenomica** -- DNA antigo, dano pos-mortem, desaminacao. Ferramentas especializadas: mapDamage, PMDtools, ANGSD. nf-core/eager. Desafios de baixa cobertura e contaminacao.

- **Paleoproteomica / ZooMS** -- Identificacao de especies por colageno. Preparo de amostra, MALDI-TOF, analise de espectros. Conexao com contextos arqueologicos.

## Conexao com o Projeto

Cada estagio do plano produz artefatos concretos no repositorio:
- Scripts de analise documentados
- Dockerfiles e docker-compose.yml
- Pipelines Nextflow versionados
- Paginas de wiki com resultados e interpretacoes

O plano nao e um cronograma rigido -- e um mapa que se ajusta conforme o aprendizado avanca e o projeto evolui. Consulte [[roadmap]] para a visao faseada e [[learning-priorities]] para as prioridades atuais ranqueadas.
