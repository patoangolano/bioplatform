# Plano de Retomada — bioplatform

**Data:** 2025-07-17
**Contexto:** Máquina formatada, repositório clonado, ambiente limpo.

## Fases

### Fase 1 — Reconhecimento ✅
- Exploração completa do workspace (~50 arquivos)
- Diagnóstico de ambiente (Python 3.13, Node 26, Docker 29, GitHub CLI)
- Identificação de ausências: `.env`, `node_modules`, testes, builds

### Fase 2 — Automação Local 🔄
- [x] `Makefile` — 20+ targets (doctor, setup-local, up, health, test, deploy-safe)
- [x] `AGENTS.md` — instruções para agentes de IA
- [ ] `scripts/setup/` — 10 scripts de setup encadeados
- [ ] `.claude/skills/` — 5 skills customizados
- [ ] `.claude/agents/` — 6 agentes especializados
- [ ] `.mcp.json` — configuração de MCP servers
- [ ] `.env.example` — template de variáveis de ambiente

### Fase 3 — Correções Técnicas ⬜
- [ ] Criar `.env` a partir do template
- [ ] Instalar dependências Python (api, worker, workflows, mcp_servers)
- [ ] Instalar dependências Node (apps/web)
- [ ] Corrigir imports quebrados (mcp_servers vs services)
- [ ] Verificar compatibilidade Python 3.13 com todas libs

### Fase 4 — Auditoria VPS ⬜
- [ ] `make vps-audit` — estado do VPS Hostinger
- [ ] Verificar Docker, containers, volumes, redes
- [ ] Backup de dados remanescentes
- [ ] Decisão: reconstruir ou reparar

### Fase 5 — Execução Local ⬜
- [ ] `make up` — subir stack completa localmente
- [ ] `make health` — verificar todos serviços
- [ ] `make test` — lint + typecheck + testes
- [ ] Validar endpoints da API
- [ ] Build do frontend

### Fase 6 — Deploy Produção ⬜
- [ ] `make deploy-safe` — deploy com confirmação
- [ ] Verificar HTTPS via Caddy
- [ ] Verificar persistência PostgreSQL
- [ ] Verificar logs e monitoramento

### Fase 7 — Entrega Final ⬜
- [ ] `make recovery-report` — relatório completo
- [ ] Documentar lições aprendidas
- [ ] Atualizar `wiki/log.md`

## Riscos Identificados

| Risco | Severidade | Mitigação |
|-------|-----------|-----------|
| Python 3.13 incompatível com libs | Média | Testar instalação cedo, usar Docker como fallback |
| VPS sem dados aproveitáveis | Baixa | Reconstrução limpa é o plano B |
| Frontend nunca buildado | Média | Validar com `npm run build` |
| Sem testes automatizados | Alta | Criar smoke tests na Fase 3 |
| make não disponível no Windows | Média | Usar Git Bash ou WSL; documentar comandos equivalentes |

## Próximos Passos Imediatos

1. Criar `scripts/setup/00_doctor.sh` até `10_deploy_safe.sh`
2. Criar `.env.example`
3. Criar `.mcp.json`
4. Criar skills e agents do Claude Code
5. Executar `make doctor` para validar diagnóstico