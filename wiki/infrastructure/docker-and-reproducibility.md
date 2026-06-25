---
title: "Docker e Reprodutibilidade Computacional"
slug: "docker-and-reproducibility"
type: infrastructure
status: active
created: 2026-06-23
updated: 2026-06-23
tags:
  - infraestrutura
  - docker
  - reprodutibilidade
  - biocontainers
  - devops
  - dominio:bioinformatica
  - ferramenta:docker
source_count: 1
source_files:
  - "output/devops-computational-biology-deep-research.md"
related_pages:
  - "[[tooling-stack]]"
  - "[[bioplatform]]"
  - "[[project-architecture]]"
  - "[[infrastructure-hub]]"
  - "[[devops-computational-biology]]"
  - "[[reproducibility-in-bioinformatics]]"
---

# Docker e Reprodutibilidade Computacional

A reprodutibilidade em bioinformatica colapsa sem controle de ambiente. Cada pipeline -- do alinhamento com BWA-MEM a chamada de variantes com bcftools -- depende de versoes especificas de bibliotecas, indices de referencia e dependencias de sistemas que raramente sobrevivem a uma reinstalacao. O Docker resolve isso congelando todo o ambiente de execucao em uma imagem imutavel.

## Multi-stage Builds e Biocontainers

O padrao de build da bioplatform usa **multi-stage builds**: um estagio de compilacao (`builder`) instala dependencias pesadas e gera artefatos; um estagio final enxuto (`runtime`) copia apenas os binarios necessarios. Isso reduz imagens de 2-3 GB para 200-400 MB. Para ferramentas bioinformaticas, o registro `quay.io/biocontainers` e a fonte primaria -- imagens mantidas pela comunidade BioConda com versoes pareadas a cada release de software, garantindo reprodutibilidade bit a bit entre execucoes.

## Orquestracao com Docker Compose

O [[project-architecture|projeto]] define todos os servicos -- FastAPI, arq worker, PostgreSQL, Redis, Caddy -- em um unico `docker-compose.yml`. Redes internas isolam o banco de dados do trafego externo; volumes nomeados persistem dados entre reinicializacoes. O proxy reverso Caddy gerencia termino TLS automatico e roteamento para cada servico por nome de host.

## Padrao de Deploy da Bioplatform

O ciclo de deploy segue tres passos: (1) **build local ou no VPS** com `docker compose build`, gerando imagens etiquetadas com o commit SHA; (2) **push para registro** (Docker Hub ou GitHub Container Registry) quando o build ocorre localmente; (3) **compose up no VPS** com `docker compose pull && docker compose up -d`, substituindo containers em execucao sem downtime. Este fluxo esta documentado no script `infra/deploy.sh` e e disparado automaticamente pelo GitHub Actions apos lint e testes passarem.

Para ferramentas bioinformaticas que exigem imagens especializadas -- como pipelines do [[nf-core]] ou ambientes com dependencias conflitantes -- utiliza-se containers efemeros disparados sob demanda, montando volumes de dados e referencia como bind mounts. O resultado de cada execucao e registrado com metadados de proveniencia (imagem digest, comando, timestamp), fechando o ciclo de reprodutibilidade ponta a ponta.

## Onde o Docker Para: Limites da Containerizacao

O relatorio [[devops-computational-biology|DevOps Deep Research]] verificou (3-0) que **Docker sozinho NAO basta para reprodutibilidade**. Duas lacunas que a imagem imutavel nao fecha:

1. **Semantica de identificadores.** A imagem congela binarios, mas anotacoes de genes (Ensembl/Entrez) derivam com releases upstream. A correcao mora na camada de [[reproducibility-in-bioinformatics|reprodutibilidade semantica]]: pinar a release de anotacao em YAML (grafo snapshot-bounded), nao so o digest da imagem.
2. **Persistencia da imagem.** Ambientes "desaparecem apos a publicacao" -- registries caem, imagens sao deletadas. A recomendacao operacional e tratar o **arquivamento da imagem como parte do fluxo de publicacao** (ex: Docker Hub -> Zenodo com DOI), tornando a imagem citavel e duravel.

Como referencia de arquitetura de producao, o relatorio aponta o **BIOMERO 2.0** (padrao hibrido validado 3-0): Docker + Compose em dev/CI, **Singularity/Apptainer em Slurm** para producao/HPC, com proveniencia FAIR ponta a ponta. A licao para a bioplatform: dominar _ambos_ os runtimes (Docker para nuvem, Apptainer para HPC) e mover GPU scheduling (MIG, MPS, Time Slicing) para o radar quando pipelines de modelos de linguagem proteicos entrarem em cena.

Consulte [[tooling-stack]] para o panorama completo da stack e [[infrastructure-hub]] para navegacao entre as paginas de infraestrutura.
