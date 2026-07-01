# AGENTS.md — Instruções para Agentes de IA

Este arquivo define como agentes de IA (Claude Code, Copilot, etc.) devem operar neste repositório.

## Identidade do Projeto

**bioplatform** é uma plataforma de orquestração translacional bioinformática com foco em:
- Análise de sequências proteicas (BLAST, AlphaFold, ESM, InterPro, STRING)
- Revisão de literatura (PubMed)
- Anotação funcional com proveniência
- Biossegurança e classificação de risco
- Assistência regulatória (patentes, compliance)

## Regras Operacionais

### 1. Nunca modificar `raw/`
A pasta `raw/` contém fontes imutáveis. Qualquer análise deve partir delas, mas nunca alterá-las.

### 2. Seguir thresholds dos skills
Ao executar análises bioinformáticas, consultar:
- `skills/thresholds/blast_filtering.yaml` — e-value, coverage, identity
- `skills/thresholds/interaction_confidence.yaml` — STRING scores
- `skills/thresholds/structure_quality.yaml` — pLDDT, pTM

### 3. Registrar proveniência
Todo resultado deve incluir: ferramenta, versão, parâmetros, timestamp.

### 4. Separar observação de inferência
- Observação: dado bruto da ferramenta
- Inferência: interpretação baseada em thresholds
- Hipótese: especulação para validação experimental

### 5. Idioma
- Prosa do repositório: **português**
- Código, comandos, nomes técnicos, chaves YAML: **inglês**

### 6. Commits
- Conventional commits em português: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
- Um commit por mudança lógica

### 7. Secrets
- Nunca commitar `.env`, tokens, senhas ou chaves de API
- Usar `.env.example` como template

## Comandos Principais

```bash
make doctor          # diagnóstico do ambiente
make setup-local     # instalação completa
make up              # sobe stack Docker
make health          # verifica serviços
make test            # lint + typecheck + testes
make recovery-report # relatório de estado
```

## Estrutura de Decisão

Ao receber uma tarefa neste repositório:

1. **Diagnóstico**: `make doctor` primeiro
2. **Contexto**: ler `wiki/index.md` para navegação
3. **Protocolos**: consultar `skills/` se for análise bioinformática
4. **Execução**: seguir princípios do `CLAUDE.md`
5. **Registro**: documentar em `wiki/` se produzir conhecimento durável

## MCP Servers

Este projeto expõe MCP servers para ferramentas bioinformáticas. Ver `.mcp.json` para configuração.