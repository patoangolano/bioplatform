---
title: Bioinformatics Hub
type: hub
created: 2026-06-23
tags: [hub, bioinformatica, ciencia, pipelines, paleogenomica]
---

# Bioinformatics Hub

Nucleo cientifico da bioplatform. Este hub concentra tudo relacionado a biologia computacional: do projeto ancora aos conceitos de RNA-Seq, paleogenomica e reprodutibilidade. Cada pagina conecta teoria, ferramenta e pratica real de laboratorio.

## Estrutura do Hub

### Projeto

- [[project-anchor]] -- Por que este projeto existe. A fusao entre estudo de bioinformatica de longo prazo e execucao tecnica real. Conexao com plano de estudos, infraestrutura e carreira.

- [[project-architecture]] -- Visao arquitetonica: FastAPI, arq worker, PostgreSQL, Redis, Caddy, Docker Compose, 15 servidores MCP bioinformaticos. Links para README e CLAUDE.md do repositorio.

- [[bioinformatics-project]] -- O projeto central: plataforma de bioinformatica reprodutivel. Perguntas cientificas, metodos, ferramentas, datasets. Conexao com infraestrutura implantada no VPS.

- [[project-status]] -- Status atual: Fase 1 concluida (API, DB, auth, BLAST worker, admin, CI/CD). Fase 2 em andamento (Nextflow, RNA-Seq, ecossistema MCP). Deploy em bio.quackai.com.br.

### Conceitos Cientificos

- **RNA-Seq** -- Pipeline completo: FastQC, Trimmomatic, STAR/HISAT2, featureCounts, DESeq2. Controle de qualidade, alinhamento, quantificacao, expressao diferencial.

- **Paleogenomica** -- DNA antigo (aDNA): dano pos-mortem, desaminacao de citosina, fragmentacao. Ferramentas: mapDamage, PMDtools, ANGSD. Genomica populacional em amostras historicas.

- **Paleoproteomica / ZooMS** -- Zooarchaeology by Mass Spectrometry. Identificacao taxonomica por peptideos de colageno. Espectrometria de massa MALDI-TOF. Marcadores de especie em osso fragmentado.

### Engenharia de Workflow

- **Nextflow / nf-core** -- DSL2, canais, processos, containers. Pipelines nf-core: rnaseq, sarek, eager. Execucao em Docker e Kubernetes.

- **Reprodutibilidade** -- Ambientes containerizados, versionamento de workflow, dados de referencia congelados, registros de execucao (provenance). Conda, Docker, Nextflow juntos.

## Navegacao

- Voltar para [[home]]
- Ir para [[study-hub]]
- Ir para [[infrastructure-hub]]
- Ir para [[career-hub]]

---

Este hub e o coracao cientifico do projeto. Cada pagina reflete pratica real, nao apenas teoria de livro-texto.
