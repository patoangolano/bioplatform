# Guia de Colaboração com IA — bioplatform

## Agentes Disponíveis

### Claude Code (via VS Code)
- **MCP servers**: scientific-bio, hostinger-api, github, filesystem, postgres, docker
- **Skills**: protocolos bioinformáticos, thresholds, templates
- **Arquivo de instruções**: `CLAUDE.md` (raiz), `AGENTS.md` (raiz)

### GitHub Copilot (via VS Code)
- **Chat**: assistência inline, explicação de código, geração de testes
- **Edits**: modificações com review
- **Agentes**: code-auditor, code-explorer, test-generator

## Como Dar Instruções Eficazes

### 1. Contexto é tudo
```
"Analisa a sequência XP_001234 no contexto de paleoproteômica,
seguindo o protocolo protein_characterization.md,
com thresholds de structure_quality.yaml"
```

### 2. Referencie arquivos específicos
```
"Usa o adapter uniprot.py para buscar Q9H4A3,
cacheia em Redis 24h, e formata com o template analysis_report.md"
```

### 3. Peça verificações intermediárias
```
"Antes de continuar, faz make health e confirma que
postgres e redis estão respondendo"
```

### 4. Use os skills como contratos
- `skills/protocols/` — o que fazer
- `skills/thresholds/` — como julgar
- `skills/templates/` — como apresentar

## Padrões de Interação

### Análise Bioinformática
```
1. "Busca [proteína] no UniProt via adapter"
2. "Faz BLAST contra [database] com thresholds de blast_filtering.yaml"
3. "Prediz estrutura com AlphaFold/ESM"
4. "Anota domínios com InterPro"
5. "Busca interações no STRING"
6. "Revisa literatura no PubMed"
7. "Gera relatório com template analysis_report.md"
```

### Operações DevOps
```
1. "make doctor" — diagnóstico
2. "make health" — saúde dos serviços
3. "make deploy-safe" — deploy com confirmação
4. "make recovery-report" — relatório completo
```

### Manutenção do Wiki
```
1. "Processa nova fonte em raw/"
2. "Cria página de conceito para [tópico]"
3. "Faz lint do wiki — links quebrados, órfãos, contradições"
4. "Atualiza index.md após novas páginas"
```

## Regras de Ouro

1. **Nunca modificar `raw/`** — fontes são imutáveis
2. **Sempre registrar proveniência** — ferramenta, versão, parâmetros, timestamp
3. **Separar observação de inferência** — não confundir dado com interpretação
4. **Seguir thresholds dos skills** — não improvisar limiares
5. **Commits convencionais em português** — `feat:`, `fix:`, `docs:`
6. **Secrets nunca em código** — `.env` no `.gitignore`

## Troubleshooting

| Sintoma | Diagnóstico | Ação |
|---------|------------|------|
| "Adapter X não responde" | Redis pode estar down | `make health` |
| "Docker não sobe" | Portas em conflito | `docker ps` e `netstat` |
| "Import quebrado" | Python path | `PYTHONPATH=. python -c "import mcp_servers"` |
| "Frontend branco" | node_modules ausente | `cd apps/web && npm install` |
| "make não funciona" | Windows sem bash | Usar Git Bash ou WSL |