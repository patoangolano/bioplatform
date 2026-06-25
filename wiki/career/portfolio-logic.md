---
title: "Logica de Portfolio — GitHub como Evidencia Primaria"
slug: "portfolio-logic"
type: career
status: active
created: 2026-06-23
updated: 2026-06-23
tags:
  - portfolio
  - github
  - bioplatform
  - mcp
  - docker
  - infraestrutura-como-codigo
  - ci-cd
  - computacao-cientifica
source_count: 0
source_files: []
related_pages:
  - "[[github-and-portfolio-outputs]]"
  - "[[docker-and-reproducibility]]"
  - "[[claude-code-and-mcp]]"
  - "[[positioning]]"
  - "[[project-to-career-translation]]"
  - "[[tooling-stack]]"
  - "[[career-hub]]"
---

# Logica de Portfolio — GitHub como Evidencia Primaria

O portfolio profissional nao e uma colecao de scripts avulsos. E a propria **[[bioplatform]]** operando como prova viva de competencia — um monorepo publico onde cada componente da plataforma e versionado, testado, documentado e implantado com rastreabilidade completa. O GitHub, nesse modelo, funciona como curriculo verificavel: um recrutador tecnico pode inspecionar o historico de commits convencionais em portugues (`feat:`, `fix:`, `docs:`), os Dockerfiles que compoem a orquestracao de containers, os workflows de CI/CD que executam lint e deploy automatico, e a cobertura de testes que protege regressoes. Nada e montado para impressionar — e montado para funcionar em producao, e isso e o que comunica senioridade.

## Projetos Ativos e Evidencias Estruturadas

A [[bioplatform]] concentra os projetos ativos do portfolio. O backend **FastAPI** expoe uma API REST documentada automaticamente via OpenAPI, com autenticacao JWT e modelos assincronos em SQLAlchemy 2.0. O worker **arq** processa jobs BLAST em background sobre Redis, enquanto o **Prefect 3.x** orquestra workflows multi-step com registro de proveniencia obrigatoria — ferramenta, versao, hash de parametros e timestamp em cada resultado. Os adaptadores bioinformaticos em `mcp_servers/adapters/` encapsulam chamadas a UniProt, PubMed, InterPro, AlphaFold, STRING e NCBI BLAST com cache Redis estratificado por TTL (2h para PubMed, 24h para UniProt, 7d para AlphaFold). O servidor **PostgreSQL-MCP-Server**, construido sobre o protocolo JSON-RPC 2.0 com FastMCP, demonstra design de APIs para consumo por agentes de IA: schemas estaticos, ferramentas com descricoes precisas, e descoberta automatica de chaves estrangeiras implicitas via analise de padroes de nomenclatura.

## Infraestrutura como Codigo e reproducibilidade

O deploy em producao no VPS Hostinger (Ubuntu 24.04, KVM 4 CPU / 16 GB) e inteiramente definido como codigo: `docker-compose.yml` com seis servicos (API, worker, PostgreSQL 16, Redis 7, Caddy), healthchecks com `pg_isready` e `redis-cli ping`, redes isoladas em bridge e volumes nomeados. O proxy **Caddy** gerencia HTTPS automatico via Let's Encrypt. O script `infra/scripts/deploy.sh`, acionado por GitHub Actions a cada push na `main`, executa pull, migracoes de banco, build e `docker compose up -d` com health check final — zero intervencao manual. Esse nivel de automacao comunica que o profissional entende o ciclo completo de DevOps, nao apenas escreve codigo que funciona na maquina local.

## Analises Publicadas e Computacao Cientifica

Cada analise gerada pela plataforma e um entregavel publico e auditavel, classificado como pagina do tipo `output` no wiki. Relatorios de anotacao funcional, buscas BLAST contra NR/NT, predicoes estruturais via AlphaFold e ESM3, e documentos regulatorios GxP (ICH/Anvisa) sao produzidos com registro completo de proveniencia e versionados no repositorio. O servico de **biosseguranca** realiza screening de sequencias contra as listas de Select Agents do CDC e USDA, enquanto o modulo **regulatory_assist** gera protocolos, SAPs e TCLEs com templates parametricos. Esses artefatos demonstram nao apenas competencia em bioinformatica, mas compreensao do contexto regulatorio em que analises genomicas operam.

## Direcao Estrategica

O portfolio cresce em duas frentes: consolidacao da plataforma existente (mais cobertura de testes, mais adaptadores, documentacao de API) e expansao para pipelines comunitarios **nf-core** (`nf-core/rnaseq`, `nf-core/eager`), onde contribuicoes publicas — modulos reutilizaveis, correcoes de bugs, reports de execucao — constroem reputacao na comunidade internacional de bioinformatica. A logica e simples: o GitHub nao armazena codigo morto; ele registra a trajetoria de uma plataforma que opera em producao, evolui com disciplina de commits e produz ciencia reprodutivel. Esse e o sinal que um portfolio deve emitir.
