---
title: Prioridades de Aprendizado
type: study-plan
created: 2026-06-23
tags: [estudo, prioridades, foco, estrategia]
links: [[overview]] [[roadmap]] [[study-method]]
---

# Prioridades de Aprendizado

As prioridades estao ranqueadas por urgencia, impacto no projeto e dependencias entre topicos. O criterio e pragmatico: o que desbloqueia mais capacidade de execucao agora?

## 1. Docker e Workflows Containerizados

**Por que e a prioridade maxima:**
- Docker e a espinha dorsal da reproducibilidade na plataforma
- Toda ferramenta bioinformatica roda em container no VPS
- Sem fluencia em Docker, nao ha Nextflow funcional (que orquestra containers)
- Impacto direto em 3 camadas do modelo: infraestrutura, ferramentas e pipelines

**O que praticar:**
- Criar Dockerfiles para ferramentas especificas (STAR, DESeq2, FastQC)
- Multi-stage builds para imagens menores
- Debug de containers (logs, exec interativo, volumes)
- Docker Compose para orquestracao multi-servico
- Publicacao de imagens em registro (Docker Hub, ghcr.io)

**Conexao com o projeto:** Cada servico da bioplatform esta em container. Dominar Docker significa operar a plataforma com confianca.

## 2. RNA-Seq Ponta a Ponta

**Por que e segunda prioridade:**
- RNA-Seq e o pipeline bioinformatico mais canonico e versatil
- Ensina todo o ciclo: qualidade, alinhamento, quantificacao, estatistica
- Habilidades transferiveis para qualquer analise de NGS
- Dados publicos abundantes para pratica e validacao

**O que praticar:**
- Download de FASTQs do SRA via fasterq-dump ou prefetch
- Controle de qualidade: entender cada metrica do FastQC
- Alinhamento com STAR: criar indice, ajustar parametros para reads paired-end
- Quantificacao e matriz de contagem
- DESeq2: design formula, resultados, interpretacao biologica

**Conexao com o projeto:** Pipeline central da plataforma. Sera o primeiro workflow Nextflow completo.

## 3. Nextflow Fundamentos

**Por que e terceira prioridade:**
- Depende de Docker (prioridade 1) e conhecimento de pipeline (prioridade 2)
- Nextflow e o padrao da industria para workflows bioinformaticos
- nf-core oferece pipelines prontos e curados para validacao

**O que praticar:**
- Sintaxe DSL2: channels, processes, workflows
- Executar pipeline simples (fastqc sozinho, depois multi-etapa)
- Entender diretorio de trabalho, cache, resume
- Configurar profiles para execucao local e Docker

**Conexao com o projeto:** Substituira scripts manuais por workflows automatizados e reprodutiveis.

## 4. Praticas de Reprodutibilidade

**Por que e quarta prioridade:**
- A reprodutibilidade e o diferencial de valor do portfolio
- Envolve disciplina de documentacao, versionamento e ambientes selados
- E mais habito que topico tecnico

**O que praticar:**
- Manter ambiente definido como codigo (Dockerfile, docker-compose.yml)
- Versionar dados de referencia com checksums
- Registrar parametros exatos de cada execucao
- Escrever documentacao que permita replicacao independente

**Conexao com o projeto:** A bioplatform existe para ser inteiramente reprodutivel.

## 5. Conhecimento de Dominio (Biologia Molecular, Genetica)

**Por que e quinta prioridade:**
- Essencial para interpretar resultados corretamente
- Mas e uma camada de longo prazo, construida incrementalmente
- Cada analise de dados ensina conceitos biologicos no contexto certo

**O que estudar:**
- Estrutura e funcao do DNA/RNA/proteinas
- Mecanismos de expressao genica e splicing
- Principios de genetica populacional (deriva, selecao, migracao)
- Especificidades de DNA antigo: degradacao, contaminacao, autenticacao

**Conexao com o projeto:** Sem dominio, os pipelines geram numeros sem significado. Com dominio, cada resultado conta uma historia biologica.

---

As prioridades mudam conforme o aprendizado avanca. Revise esta pagina a cada marco do [[roadmap]].
