---
title: "Reprodutibilidade em Bioinformatica"
slug: "reproducibility-in-bioinformatics"
type: concept
status: active
created: 2026-06-23
updated: 2026-06-23
tags:
  - reproducibilidade
  - proveniencia
  - docker
  - nextflow
  - boas-praticas
source_count: 1
source_files:
  - "output/devops-computational-biology-deep-research.md"
related_pages:
  - "[[project-anchor]]"
  - "[[project-architecture]]"
  - "[[infrastructure/tooling-stack]]"
  - "[[reproducibility]]"
  - "[[devops-computational-biology]]"
---

# Reprodutibilidade em Bioinformatica

A reprodutibilidade e o quinto dos [[project-anchor|7 principios de design]] da bioplatform e, na pratica, o mais transversal: sem ela, nenhum resultado de pipeline sobrevive a uma auditoria ou a uma segunda execucao seis meses depois. No contexto bioinformatico, reproducibilidade significa que um workflow executado sobre os mesmos dados de entrada -- com as mesmas versoes de ferramentas, parametros e genomas de referencia -- produz saidas identicas, bit a bit, independentemente de quem ou quando o executa.

## Pilares Tecnicos

**Containers imutaveis.** Cada ferramenta do pipeline (FastQC, Trimmomatic, STAR, featureCounts, DESeq2) e empacotada em uma imagem Docker com hash de camada registrado. O [[infrastructure/tooling-stack|Docker Compose]] de producao fixa tags explicitas (`biocontainers/fastqc:v0.12.1`) -- nunca `latest`. Isso elimina a classe mais comum de falha: deriva de versao de dependencia entre ambientes.

**Pipelines versionados.** Workflows [[nextflow]]/nf-core sao declarados em DSL2 e versionados no repositorio com `git`. Cada execucao registra o commit SHA do workflow, o perfil de execucao (docker/singularity), e o digest das imagens utilizadas. O [[nf-core]] impoe parametros de referencia congelados (genoma de referencia, anotacao GTF, indices de alinhamento) cujo hash e validado antes do processamento.

**Ambientes documentados.** O ambiente computacional completo -- sistema operacional, versao do kernel, drivers, variaveis de ambiente -- e capturado no inicio de cada execucao e armazenado junto aos metadados de proveniencia. Nao existe "funcionou na minha maquina" porque a maquina esta descrita.

## Proveniencia como Evidencia

A bioplatform implementa o primeiro principio -- **proveniencia obrigatoria** -- via um servico dedicado que registra, para cada resultado computacional: ferramenta e versao, hash do container, parametros exatos da linha de comando, timestamp de execucao, hash SHA-256 dos arquivos de entrada e saida, e identidade do executor (humano ou agendado). Esse grafo de proveniencia permite reconstruir qualquer resultado a partir dos metadados, funcionando como um _lab notebook_ digital imutavel.

A conexao entre reproducibilidade e proveniencia e bidirecional: a proveniencia documenta o que foi feito; a reproducibilidade prova que o registro e fiel. Juntas, elas transformam a plataforma de uma colecao de scripts em um sistema de conhecimento cientifico auditavel -- alinhado com o principio de [[separacao-epistemica|separacao epistemica]] entre observacao e inferencia.

## O Limite da Containerizacao: Reprodutibilidade Semantica

Containers garantem que o _software_ nao mude -- mas nao garantem que o _significado_ dos dados permaneca estavel. O relatorio [[devops-computational-biology|DevOps Deep Research]] identifica isso como o achado mais importante para bioinformatas seniores: **a containerizacao congela o software, mas nao a semantica biologica.** Identificadores de genes (Ensembl, Entrez) sofrem deriva conforme novas releases de anotacao sao publicadas upstream -- um mapeamento que era correto em uma release pode mudar na seguinte, ainda que o codigo e a imagem Docker estejam congelados. O preprint IDTrack (Inecik, Erken & Theis, 2026) descreve isso como "um modo de falha invisivel ao controle de versao e a containerizacao".

A correcao e o **grafo de identificadores snapshot-bounded**: o usuario declara explicitamente uma _release maxima do Ensembl_ como parametro de configuracao, armazenado em YAML junto a definicao do container. Mesma fronteira de snapshot + mesma configuracao = resultados de conversao identicos, toda vez. Isso estende o versionamento alem do codigo, fechando uma lacuna que Docker + Apptainer + Biocontainers sozinhos nao cobrem.

No mesmo sentido, a adesao a principios **FAIR nao basta** para garantir reprodutibilidade (FOSDEM 2026, Reproducible Research Platform): o elo perdido e a especificacao explicita do ambiente computacional, que tende a "desaparecer apos a publicacao". A licao operacional para a bioplatform e dupla -- (1) pinar releases de anotacao no [[provenance|grafo de proveniencia]], nao apenas digests de imagem; (2) tratar o arquivamento da imagem (ex: Docker Hub -> Zenodo com DOI) como parte do fluxo de publicacao. Ver [[docker-and-reproducibility]] para a camada de infraestrutura.

## Ver Tambem

- [[devops-computational-biology]] -- relatorio de deep research que fundamenta a secao semantica
- [[project-anchor]] -- os 7 principios de design na integra
- [[infrastructure/tooling-stack]] -- stack de containers e orquestracao
- [[nextflow]] -- pipelines reprodutiveis com nf-core
- [[provenance]] -- sistema de rastreamento de proveniencia da plataforma
