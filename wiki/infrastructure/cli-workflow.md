---
title: Fluxo de Trabalho CLI
tags:
  - cli
  - wsl2
  - docker
  - git
  - ssh
  - powershell
  - bioinformatica
created: 2026-06-23
---

# Fluxo de Trabalho via Linha de Comando

Toda operacao na [[bioplatform]] e orientada a CLI, sem dependencia de interfaces graficas. O ambiente e composto por camadas distintas, cada uma com seu shell nativo.

## WSL2 Ubuntu -- Ferramentas Bioinformaticas

O [[wsl2-setup]] abriga o ecossistema bioinformatico completo: [[samtools]], [[bcftools]], [[fastqc]], [[seqkit]], [[blast]], [[bwa]] e scripts em Python/R. Executamos pipelines diretamente do terminal Ubuntu, com acesso ao filesystem do Windows via `/mnt/c/`. Dados brutos de sequenciamento sao processados aqui antes de subir para o [[data-lake]].

## PowerShell -- Operacoes Windows

PowerShell gerencia o lado Windows da infraestrutura: provisionamento de diretorios no [[storage-array]], manipulacao de arquivos grandes com `robocopy`, administracao de permissoes NTFS e automacao de backups locais. Scripts `.ps1` orquestram a ponte entre o WSL2 e os volumes NTFS, garantindo que pipelines UNIX enxerguem os dados sem conflito de encoding ou quebra de linha.

## Docker CLI -- Conteinerizacao

Containers no [[docker-host]] sao gerenciados exclusivamente via `docker compose` e `docker` CLI. Cada servico ([[postgres-mcp]], [[nginx-reverse-proxy]], [[pgadmin]]) tem seu `compose.yaml` versionado no repositorio. Imagens sao construidas localmente com `docker build` e push para o [[container-registry]]. Logs sao inspecionados com `docker logs --tail`, e volumes persistem em paths mapeados do [[storage-array]].

## Git -- Versionamento

Todo codigo, configuracao e documentacao vive em repositorios git no [[github-org]]. O fluxo segue trunk-based development: branches curtos, commits atomicos, merge via PR. Hooks de pre-commit validam sintaxe de `compose.yaml` e checagem de segredos com [[gitleaks]]. A wiki (este proprio diretorio) e versionada junto com o codigo, garantindo que documentacao e implementacao evoluam em sincronia.

## SSH -- Deploy e Monitoramento

Acesso ao VPS de producao em [[hetzner-vps]] e exclusivamente via SSH com chaves ED25519. Deploys sao disparados por `ssh <host> 'cd /opt/bioplatform && docker compose pull && docker compose up -d'`. Monitoramento de recursos (CPU, RAM, disco) usa `ssh <host> 'htop -b'` e alertas do [[uptime-kuma]]. Tuneis SSH reversos conectam servicos internos quando necessario, conforme documentado em [[ssh-tunnels]].
