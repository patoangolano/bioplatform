# DevOps for Senior Computational Biology & Bioinformatics
## Deep Research Report — June 2026

**Methodology:** 105 AI agents, 23 sources, 110 claims extracted, 25 claims verified with 3-vote adversarial review. 11 claims confirmed, 14 refuted.

---

## 1. Workflow Orchestration

### nf-core: The Community Standard (3-0 verified)
The nf-core framework provides **over 1,400 reusable pipeline modules** and approximately **80 subworkflows** built on Nextflow DSL2, enabling progressive adoption of community standards by research groups. Modules cover RNA-seq, variant calling, metagenomics, proteomics, and more.

**Source:** Wratten et al., *Genome Biology* (2025), DOI: 10.1186/s13059-025-03673-9

**Key takeaway for senior roles:**
- nf-core is the largest community-driven bioinformatics pipeline library
- DSL2 modularity = adopt incrementally without rewriting entire pipelines
- Enforces: containerization per process, resource labeling, automated CI testing across platforms

### Production-Ready vs Proof-of-Concept (2-1 verified)
Production-ready bioinformatics workflow components (nf-core, snakemake-wrappers, BioWDL) add substantial capabilities absent from PoC examples:
- Version-pinned containerization
- Resource management with memory-per-CPU calculations
- Structured error handling and logging
- YAML metadata documentation
- Extensive parameterization
- Automated testing with snapshot validation

**Source:** Saeys Lab Polygloty Book — Workflow Frameworks Review (2025), saeyslab.github.io/polygloty

**Critical rule: Never evaluate a workflow framework by comparing PoC examples. They look deceptively similar.**

### Framework Evaluation Limitations (3-0 verified)
The 2021 study by Wratten, Wilm, and Goke evaluated workflow managers on only **six criteria**, each scored 1-3. Each category (except scalability) was based on a **single criterion**, making published comparison tables insufficient for production evaluation.

**Source:** Saeys Lab Polygloty Book

### Refuted Claims (Pitfalls to Avoid)
| Claim | Vote | Why Refuted |
|-------|------|-------------|
| "Nextflow surpassed Snakemake in adoption" | 0-3 | Citation metrics unreliable; adoption varies by subfield |
| "Apache Airflow is suitable for bioinformatics pipelines" | 0-3 | Airflow designed for ETL, not scientific workflows |
| "Nextflow and Snakemake score highest among 5 frameworks" | 0-3 | Scoring framework too limited (single criterion per category) |
| "Nextflow, Snakemake, CWL are the 3 WMS with TES API" | 0-3 | Overreaching claim from unreviewed preprint |
| "Grid systems are too rigid for bioinformatics" | 0-3 | de.NBI Cloud has A100/H100 GPUs; Slurm actively extended |

---

## 2. Containerization & Kubernetes

### Kubernetes for Bioinformatics AI Pipelines (2-1 verified)
Bioinformatics pipelines combining **Protein Language Models (PLMs)** and **Antibody Language Models (AbLMs)** can be orchestrated on Kubernetes with GPU sharing:
- **MIG** (Multi-Instance GPU): Hard partitioning
- **Time Slicing**: Soft sharing
- **MPS** (Multi-Process Service): Concurrent CUDA streams

Works across EKS, GKE, AKS and on-prem bare metal.

**Source:** FOSDEM 2026 Talk, code at github.com/alexpilotti

### Docker Alone Is NOT Enough for Reproducibility (3-0 verified)
The most important finding for senior computational biologists: **containerization freezes software but NOT biological semantics.**

Gene identifier semantics drift with upstream annotation releases even when code and containers are frozen. This is described as "a failure mode invisible to version control and containerization."

**Source:** IDTrack Preprint (Inecik, Erken & Theis, 2026), EuropePMC PPR1224832

### Snapshot-Bounded Reproducibility (2-1 verified)
A **snapshot-bounded identifier graph**, where the user declares a maximum Ensembl release boundary, produces reproducible mapping results. The same snapshot boundary + the same YAML configuration = identical conversion results every time.

**Implementation pattern:**
1. Declare Ensembl release boundary as explicit configuration parameter
2. Store YAML configuration alongside container definition
3. Results become auditable and reproducible because semantic mapping is version-locked

### Refuted: "Docker + Apptainer is enough"
The claim that containerization via Docker and Apptainer with Biocontainers is sufficient for reproducibility was **REFUTED (0-3)**. Missing piece: semantic identifier versioning.

---

## 3. Reproducible Research Platforms

### RRP — Reproducible Research Platform (3-0 verified)
The RRP integrates as a unified open-source platform for reproducible research:
- **Data:** openBIS (Research Data Management System)
- **Code:** Git version control
- **Environments:** Docker / repo2docker
- **Execution:** Kubernetes for scalable execution
- **IDEs:** JupyterLab, VS Code, RStudio, MATLAB

**Source:** FOSDEM 2026 — "Reproducible Research Platform"

### FAIR Is Not Enough (3-0 verified)
Widespread adoption of **FAIR data principles has not been sufficient** to guarantee research reproducibility. **Explicit specification of computational environments is the missing link.**

### Environments Vanish After Publication (2-1 verified)
Research computational environments "disappear after publication," making analysis reproduction dependent on expert knowledge even when code is shared. Docker images get deleted, registries go down, dependencies become unresolvable.

**Operational fix:** Container image archiving must be part of publication workflow. Consider Docker Hub to Zenodo archival with DOI.

---

## 4. BIOMERO 2.0 — Reference Architecture (3-0 verified)

BIOMERO 2.0 demonstrates the **production-grade hybrid architecture pattern:**

| Environment | Technology | Purpose |
|-------------|-----------|---------|
| Development/CI | Docker + Docker Compose | Local reproducibility |
| Production/HPC | Singularity/Apptainer on Slurm | Scalable execution |
| Image Registry | DockerHub (cellularimagingcf org) | Distribution |
| Cluster Interaction | Python library + SSH | Automation |
| Provenance | End-to-end FAIR tracking | Audit trail |

**Source:** JoVE Visualized Experiments — BIOMERO 2.0

---

## 5. Essential DevOps Skills for 2025-2026

### Core Competencies (in priority order)

1. **Workflow Orchestration** — Nextflow DSL2 + nf-core (preferred ecosystem); Snakemake as alternative
2. **Containerization** — Docker (dev/cloud) **AND** Singularity/Apptainer (HPC) — must know both
3. **Container Registries** — DockerHub, Biocontainers, institutional registries
4. **Orchestration** — Kubernetes fundamentals (especially GPU workload scheduling: MIG, MPS, Time Slicing)
5. **Infrastructure as Code** — Terraform for cloud resources; reproducible environment specs
6. **CI/CD** — GitHub Actions for automated testing across execution platforms; container build pipelines
7. **Research Data Management** — openBIS or equivalent RDMS
8. **Semantic Versioning** — Beyond code: pin annotation releases, gene identifier versions
9. **Environment Specification** — Dockerfiles + repo2docker + explicit dependency locking
10. **Monitoring** — Prometheus + Grafana for resource tracking; pipeline provenance logging

### Tool Ecosystem

| Category | Primary | Alternative |
|----------|---------|-------------|
| Workflow | Nextflow + nf-core DSL2 | Snakemake + wrappers |
| Containers | Docker + Singularity | Podman, Sarus |
| Orchestration | Kubernetes | Slurm (HPC), Nomad |
| IaC | Terraform | Pulumi, BiBiGrid |
| CI/CD | GitHub Actions | GitLab CI, Jenkins |
| Data Mgmt | openBIS | iRODS, Dataverse |
| Monitoring | Prometheus + Grafana | ELK Stack, Seqera Platform |
| Package Mgmt | Conda/Mamba + Docker | Guix, Nix |

---

## 6. Refuted Claims Summary

The adversarial verification process killed 14 claims. Key lessons:

1. **Airflow is NOT the right choice for bioinformatics** — it is for ETL, not scientific DAGs
2. **Citation counts do not equal adoption** — do not claim one WMS "surpassed" another
3. **"Cloud vs HPC" is a false dichotomy** — web platforms (Galaxy, KBase), GPU workstations, and federated community clouds are viable
4. **Grid systems are NOT obsolete** — actively evolving with modern hardware
5. **Package managers DO pin transitive dependencies** — pip freeze, conda-lock, and renv all support this; the "failure" claim is outdated
6. **Existing gene ID tools DO support version-pinned mapping** — biomaRt, BridgeDb, AnnotationHub all have this capability

---

## 7. Recommended Learning Path

### Phase 1: Foundations (Months 1-2)
- Docker deep dive (multi-stage builds, layer caching, security scanning)
- Nextflow DSL2 basics + run first nf-core pipeline
- Git advanced workflows (branching strategies, semantic versioning)

### Phase 2: Infrastructure (Months 3-4)
- Kubernetes fundamentals (pods, deployments, services, persistent volumes)
- Terraform basics (AWS/GCP resource provisioning)
- CI/CD with GitHub Actions (container builds, automated testing)

### Phase 3: Production (Months 5-6)
- GPU scheduling on Kubernetes (MIG, MPS, Time Slicing)
- Hybrid HPC/cloud deployment patterns
- FAIR computational environment specification
- Research data management integration (openBIS or equivalent)

### Phase 4: Mastery (Months 7-12)
- Custom nf-core module development
- Multi-cloud/hybrid pipeline orchestration
- Semantic identifier reproducibility patterns
- Team workflow standardization and governance

---

## 8. Key Sources

1. **nf-core framework update** — *Genome Biology* (2025), DOI: 10.1186/s13059-025-03673-9
2. **Polygloty Workflow Frameworks Review** — Saeys Lab (2025), saeyslab.github.io/polygloty
3. **Accelerating Bioinformatics AI Pipelines with Kubernetes** — FOSDEM 2026
4. **Reproducible Research Platform (RRP)** — FOSDEM 2026
5. **IDTrack: Gene Identifier Reproducibility** — bioRxiv PPR1224832 (2026)
6. **BIOMERO 2.0: FAIR Infrastructure for Bioimaging** — JoVE (2025)
7. **Hybrid Cloud for Data-Driven Science** — arXiv:2601.04349 (2026)
8. **REBEL: Dependency Resolution** — bioRxiv DOI: 10.64898 (2026)
9. **Microbiome Bioinformatics Protocol** — Springer Protocols (2026), DOI: 10.1007/978-1-0716-5009-7_9
10. **GitHub: BioInfo-DevOps** — github.com/eparisis/BioInfo-DevOps

---

*Report generated June 24, 2026 via multi-agent adversarial deep research workflow.*
*105 agents | ~20M tokens | 1168 tool calls | 11/25 claims survived verification*
