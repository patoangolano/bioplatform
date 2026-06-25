---
tags:
  - review
  - wiki
  - meta
  - health-check
date: 2026-06-23
status: draft
---

# Wiki Health

## O Que Esta Avaliacao Cobre

Este documento e uma avaliacao inicial da saude do wiki da bioplatform. Ele inspeciona quatro eixos principais:

1. **Conceitos de Bioinformatica**: paginas como [[sequence-alignment]], [[variant-calling]], [[phylogenetics]] e [[rna-seq-workflow]] estabelecem o vocabulario tecnico compartilhado. A maioria ja possui definicoes e referencias a ferramentas como BWA, SAMtools e GATK, porem ainda carecem de exemplos com dados concretos.

2. **Infraestrutura**: as paginas de [[infra]] documentam a configuracao do ambiente — PostgreSQL local, contas AWS, JupyterHub — e as decisoes de arquitetura (Docker Compose para reproducibilidade, scripts em `bin/` para ingestao). O status esta atualizado, mas nao ha diagrama de rede.

3. **Status do Projeto**: as paginas em [[projects/]] detalham entregas passadas e a sprint atual. A rastreabilidade entre tarefas e codigo-fonte (links para commits e issues) e consistente. Falta um sumario executivo de risco por projeto.

4. **Plano de Estudos**: as paginas de [[study-plan]] mapeiam topicos de genomica, transcriptomica e biologia de sistemas com cronograma semanal. Os links para artigos no PubMed e cursos no Coursera estao funcionais, mas nao ha exercicios praticos vinculados.

## O Que Esta Ausente

- **`raw/` esta vazio**: nao ha sumarios de fontes primarias (artigos, manuais, changelogs de bancos publicos). Sem isso, as paginas de conceito perdem rastreabilidade com a literatura.
- **Entidades faltantes**: ferramentas como [[STAR]], [[DESeq2]], [[GATK]] e bancos como [[Ensembl]], [[UniProt]], [[dbSNP]] nao tem paginas proprias. Cada uma deveria ter ficha tecnica, parametros principais e exemplos de saida.
- **Paginas de pergunta**: nao existem paginas no formato `questions/` que articulem duvidas em aberto — por exemplo, "Qual a melhor estrategia de normalizacao para RNA-Seq de baixa cobertura?" — que orientem o estudo e a implementacao.

## Acoes Recomendadas

- [ ] Ingerir as primeiras 3-5 fontes em [[raw/]] (prioridade: artigos de revisao de 2024-2025 sobre single-cell e long-reads)
- [ ] Criar entity pages para STAR, DESeq2 e GATK com parametros e comandos minimos via [[templates/entity]]
- [ ] Popular [[raw/]] com sumarios estruturados (DOI, ano, metodos-chave, figuras principais)
- [ ] Gerar a primeira pagina de pergunta em [[questions/normalization-low-coverage]]
- [ ] Revisar este health-check em 30 dias
