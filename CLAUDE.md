# bioplatform

Plataforma de orquestração translacional bioinformática.

## Princípios

1. **Proveniência obrigatória** — todo resultado deve rastrear origem (ferramenta, versão, parâmetros, timestamp)
2. **Separação epistêmica** — distinguir observação, inferência e hipótese
3. **Modularidade** — adapters, services, workflows isolados
4. **Biossegurança** — sandboxing de operações com organismos, classificação de risco
5. **Reprodutibilidade** — workflows devem ser repetíveis com mesmos inputs
6. **Segurança operacional** — secrets nunca em código versionado, mínimo de portas expostas
7. **Deploy-first** — infraestrutura e aplicação pensadas juntas desde o início

## Arquitetura

```
apps/api/          — backend FastAPI
apps/web/          — frontend (futuro)
apps/worker/       — processamento assíncrono
services/          — módulos de domínio:
                     provenance, literature, annotation,
                     taxonomy, biosafety, regulatory_assist
mcp_servers/       — MCP servers para Claude Code
infra/             — scripts de deploy, Docker, proxy
```

## Stack

- Python 3.11+, FastAPI, PostgreSQL, Redis
- Docker Compose, Caddy (reverse proxy)
- Prefect 3.x (orquestração de workflows multi-step)
- Cache Redis com TTL por adapter (UniProt 24h, PubMed 2h, AlphaFold 7d)

## Deploy

- Target: VPS Hostinger KVM8 (Ubuntu)
- Proxy: Caddy com HTTPS automático
- Containers: Docker Compose em produção
- CI/CD: GitHub Actions (ruff lint → SSH deploy)

## Skills (Protocolos Institucionais)

Carregar protocolos de `skills/` para padronizar análises:
- `skills/protocols/` — workflows passo-a-passo (BLAST, caracterização, literatura)
- `skills/thresholds/` — limiares numéricos (e-value, pLDDT, STRING scores)
- `skills/templates/` — formatos de relatório com proveniência

Ao executar análises, seguir os thresholds e classificações definidos nos skills.

## MCP Servers disponíveis

- hostinger-api — gerenciamento VPS
- scientific-bio — ferramentas bioinformáticas
- github — repositórios e CI
- filesystem — operações locais de arquivo
- postgres — queries e migrações
- docker — gerenciamento de containers

## Regras de commits

- Conventional commits em português: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
- Mensagens descritivas no imperativo: "adiciona endpoint de anotação"
- Um commit por mudança lógica

## Regras de secrets

- Usar `.env` para variáveis sensíveis (nunca commitar)
- `.env` deve estar no `.gitignore`
- Em produção, injetar via Docker secrets ou variáveis de ambiente do host
- Nunca logar tokens, senhas ou chaves de API

---

# 🧠 Wiki & Knowledge Workspace

Esta seção estabelece o modelo de 5 camadas do repositório como sistema operacional de conhecimento.

## Modelo de Cinco Camadas

1. **Camada Raw (`raw/`)** — Fontes imutáveis. Nunca modificar, renomear ou excluir.
2. **Camada Wiki (`wiki/`)** — Base de conhecimento mantida pelo LLM em markdown.
3. **Camada Schema (`wiki/schema/` + `CLAUDE.md`)** — Regras operacionais do repositório.
4. **Camada Operacional** — Código, infra, tools, logs, MCP servers, workflows.
5. **Camada Output (`wiki/outputs/` + `output/`)** — Entregáveis duráveis.

## Regras Não-Negociáveis

1. `raw/` é imutável e fonte de verdade
2. `wiki/` é mantido pelo LLM — criação, revisão, links, navegação
3. Navegação (`wiki/index.md`) deve permanecer atualizada
4. Compatibilidade Obsidian é obrigatória (wikilinks, frontmatter YAML, paths relativos)
5. Reprodutibilidade é valor central do repositório
6. Não criar overengineering na primeira execução

## Política de Idioma

- **Prosa do repositório em português** por padrão
- **Exceções em inglês:** nomes de arquivos, chaves YAML, código, comandos shell, sintaxe de configuração, nomes de protocolos, nomes de ferramentas, padrões técnicos, texto de fontes citadas

## Tipos de Página

| Tipo | Propósito |
|------|-----------|
| `source-summary` | Resumo de fonte em `raw/` |
| `concept` | Conceito técnico sintetizado |
| `entity` | Ferramenta, dataset, instituição, organismo |
| `project` | Estado e arquitetura de projeto |
| `study-plan` | Plano de estudo e roadmap |
| `career` | Posicionamento profissional |
| `infrastructure` | Docker, MCP, deploy, CLI |
| `question` | Pergunta preservada com resposta |
| `output` | Relatório, figura, slide |
| `review` | Auditoria de saúde do wiki |
| `hub` | Roteador de navegação |
| `schema` | Regra operacional do repositório |

## Frontmatter Padrão

```yaml
***
title: string
slug: string
type: page-type
status: seed | draft | active | reviewed | archived
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [array]
source_count: integer
source_files: [array]
related_pages: [array]
***
```

## Fluxo de Ingestão

Quando nova fonte aparece em `raw/`:
1. Identificar tipo e caminho da fonte
2. Inspecionar sem modificar
3. Criar/atualizar resumo em `wiki/sources/`
4. Extrair ideias, métodos, ferramentas, datasets, entidades, claims
5. Atualizar páginas afetadas (study-plan, concepts, infrastructure, etc.)
6. Atualizar `wiki/index.md` se novas páginas duráveis foram criadas
7. Adicionar entrada em `wiki/log.md`
8. Registrar incertezas, contradições e oportunidades de follow-up

## Fluxo de Query

Ao responder perguntas significativas:
1. Ler `wiki/index.md` primeiro
2. Identificar hubs e páginas de detalhe relevantes
3. Inspecionar páginas mais relevantes
4. Sintetizar resposta fundamentada no wiki
5. Decidir se resposta deve virar página durável em `wiki/questions/` ou `wiki/outputs/`
6. Atualizar links e índice se novas páginas criadas
7. Adicionar entrada de query em `wiki/log.md` se o repositório foi melhorado

## Fluxo de Lint

Verificações recorrentes:
- Contradições entre páginas
- Claims obsoletas
- Páginas órfãs
- Backlinks ausentes
- Frontmatter fraco ou ausente
- Links relativos quebrados
- Páginas duplicadas ou sobrepostas
- Tópicos repetidos sem página de conceito dedicada
- Páginas muito grandes que devem ser divididas
- Lacunas de domínio a pesquisar

## NotebookLM MCP

- Se servidor MCP NotebookLM estiver disponível, usá-lo como camada auxiliar de leitura e síntese
- Ideal para digestão de documentos longos, clustering, refinamento de perguntas
- **Nunca** tratar output do NotebookLM como substituto de arquivos raw imutáveis
- Reconciliar insights úteis de volta para páginas markdown em português

## Compatibilidade Obsidian

- Wikilinks `[[página]]` para navegação interna
- Frontmatter YAML compatível com Dataview
- Paths relativos para todos os links
- Nomes de arquivo estáveis e descritivos
- Páginas que fazem sentido no graph view

## Manutenção de Índice e Log

- `wiki/index.md` é orientado a conteúdo, agrupado por categoria, com descrições de uma linha
- `wiki/log.md` é cronológico, append-only, entradas no formato `## [YYYY-MM-DD] tipo | título`
- Nunca reescrever entradas antigas do log sem instrução explícita

## Limites de Tools e Infra

- `tools/` contém scripts auxiliares leves (validadores, detectores, exportadores)
- `infra/` contém scaffolding de reprodutibilidade (Dockerfiles, compose, scripts, postgres)
- `logs/` contém rastros operacionais não-wiki
- `output/` contém artefatos gerados antes da promoção para `wiki/outputs/`
