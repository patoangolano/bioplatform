***
title: DevOps para Biologia Computacional Sênior — Deep Research
slug: devops-computational-biology
type: output
status: active
created: 2026-06-24
updated: 2026-06-24
tags: [output, deep-research, devops, reproducibilidade, nextflow, kubernetes, carreira]
source_count: 1
source_files: [output/devops-computational-biology-deep-research.md]
related_pages: [[nextflow-and-nf-core]], [[reproducibility-in-bioinformatics]], [[docker-and-reproducibility]], [[learning-priorities]], [[infrastructure-hub]]
***

# DevOps para Biologia Computacional Sênior — Deep Research

Relatório de pesquisa profunda multi-agente sobre as competências de DevOps exigidas para papéis sênior em biologia computacional e bioinformática (2025-2026).

## Proveniência

- **Arquivo:** `output/devops-computational-biology-deep-research.md`
- **Tipo:** relatório de deep research (gerado por workflow adversarial multi-agente)
- **Data:** 2026-06-24
- **Metodologia:** 105 agentes de IA, 23 fontes, 110 claims extraídas, 25 verificadas com revisão adversarial de 3 votos. **11 claims confirmadas, 14 refutadas.** (~20M tokens, 1168 chamadas de ferramenta)
- **Estado:** rascunho em `output/`. Pode ser promovido para `wiki/outputs/reports/2026-06-24-devops-biologia-computacional.md` conforme [[output-filing]].

## Resumo

O relatório mapeia o stack de DevOps que distingue um bioinformata sênior de um júnior, separando rigorosamente o que sobreviveu à verificação adversarial do que foi refutado. A tese central, confirmada por múltiplas fontes (3-0): **containerização congela o software, mas não a semântica biológica** — a reprodutibilidade real exige versionar também identificadores de genes e releases de anotação, não apenas imagens Docker.

## Claims Confirmadas (sobreviveram à verificação)

- **nf-core como padrão comunitário** — 1.400+ módulos reutilizáveis e ~80 subworkflows em Nextflow DSL2, permitindo adoção incremental. (3-0; *Genome Biology* 2025, DOI 10.1186/s13059-025-03673-9). Ver [[nextflow-and-nf-core]].
- **Nunca avaliar frameworks por exemplos PoC** — componentes prontos para produção (nf-core, snakemake-wrappers, BioWDL) adicionam containerização com versão fixa, gestão de recursos, tratamento de erros e testes automáticos ausentes em exemplos didáticos. (2-1; Saeys Lab Polygloty Book).
- **Docker sozinho NÃO basta para reprodutibilidade** — deriva semântica de identificadores de genes é "um modo de falha invisível ao controle de versão e à containerização". A correção é o **grafo de identificadores snapshot-bounded**: declarar a release máxima do Ensembl como parâmetro de configuração explícito. (3-0; IDTrack Preprint, Inecik/Erken/Theis 2026). Ver [[reproducibility-in-bioinformatics]].
- **FAIR não é suficiente** — princípios FAIR não garantem reprodutibilidade; a especificação explícita de ambientes computacionais é o elo perdido. Ambientes "desaparecem após a publicação". (3-0; FOSDEM 2026 RRP).
- **BIOMERO 2.0 como arquitetura de referência** — padrão híbrido: Docker/Compose para dev/CI, Singularity/Apptainer em Slurm para produção/HPC, proveniência FAIR ponta a ponta. (3-0; JoVE 2025).
- **Kubernetes para pipelines de IA bioinformática** — GPU sharing via MIG (partição dura), Time Slicing (compartilhamento leve) e MPS (streams CUDA concorrentes), portável entre EKS/GKE/AKS e bare metal. (2-1; FOSDEM 2026).

## Claims Refutadas (armadilhas a evitar)

- "Nextflow superou Snakemake em adoção" (0-3) — métricas de citação não medem adoção.
- "Apache Airflow serve para pipelines bioinformáticos" (0-3) — Airflow é para ETL, não DAGs científicos.
- "Sistemas de grid são rígidos demais / obsoletos" (0-3) — Slurm é ativamente estendido; de.NBI Cloud tem A100/H100.
- "Cloud vs HPC é uma dicotomia" (refutada) — plataformas web (Galaxy, KBase), workstations GPU e clouds comunitárias federadas são viáveis.
- "Gestores de pacote não fixam dependências transitivas" (refutada) — pip freeze, conda-lock, renv já fazem isso.
- "Docker + Apptainer + Biocontainers basta" (0-3) — falta o versionamento semântico de identificadores.

## Competências Sênior Priorizadas (2025-2026)

Orquestração (Nextflow DSL2 + nf-core) → Containerização dupla (Docker **e** Singularity/Apptainer) → Registries → Kubernetes (scheduling de GPU) → IaC (Terraform) → CI/CD (GitHub Actions) → RDM (openBIS) → **versionamento semântico** (releases de anotação) → especificação de ambiente (repo2docker) → monitoramento (Prometheus + Grafana).

O relatório inclui um caminho de aprendizado de 12 meses em 4 fases (Fundamentos → Infraestrutura → Produção → Maestria) — relevante para [[learning-priorities]] e [[roadmap]].

## Fontes Principais

1. nf-core framework update — *Genome Biology* (2025), DOI 10.1186/s13059-025-03673-9
2. Polygloty Workflow Frameworks Review — Saeys Lab (2025)
3. Accelerating Bioinformatics AI Pipelines with Kubernetes — FOSDEM 2026
4. Reproducible Research Platform (RRP) — FOSDEM 2026
5. IDTrack: Gene Identifier Reproducibility — bioRxiv PPR1224832 (2026)
6. BIOMERO 2.0 — JoVE (2025)
7. Hybrid Cloud for Data-Driven Science — arXiv:2601.04349 (2026)
8. REBEL: Dependency Resolution — bioRxiv DOI 10.64898 (2026)
9. Microbiome Bioinformatics Protocol — Springer Protocols (2026)
10. github.com/eparisis/BioInfo-DevOps

## Questões em Aberto

- O padrão snapshot-bounded do IDTrack já foi validado em produção fora do contexto do preprint?
- Como integrar o versionamento semântico de identificadores ao serviço de [[provenance|proveniência]] da bioplatform?
- Vale adotar openBIS como RDMS, ou o grafo de proveniência atual já cobre o caso de uso?

## Ver Também

- [[nextflow-and-nf-core]] — orquestração DSL2 e ecossistema nf-core
- [[reproducibility-in-bioinformatics]] — reprodutibilidade semântica e snapshot-bounded
- [[docker-and-reproducibility]] — limites da containerização e arquivamento de imagens
- [[learning-priorities]] — prioridades de estudo atualizadas
