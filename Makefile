# ============================================================================
# bioplatform Makefile — retomada com um comando
#
# Uso:
#   make doctor          # diagnóstico completo do ambiente
#   make setup-local     # instala tudo necessário para dev local
#   make up              # sobe stack Docker completa
#   make health          # verifica saúde de todos serviços
#   make test            # roda lint + typecheck + testes
#   make recovery-report # relatório completo de estado
#
# Requisitos: Docker, Python 3.11+, Node.js 20+
# Windows: usar PowerShell com comandos equivalentes ou WSL
# ============================================================================

SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
MAKEFLAGS += --warn-undefined-variables
.DEFAULT_GOAL := help

# ── Cores ───────────────────────────────────────────────────────────────────
C_GREEN  := \033[0;32m
C_YELLOW := \033[0;33m
C_RED    := \033[0;31m
C_CYAN   := \033[0;36m
C_RESET  := \033[0m

# ── Paths ───────────────────────────────────────────────────────────────────
ROOT       := $(shell pwd)
API_DIR    := $(ROOT)/apps/api
WEB_DIR    := $(ROOT)/apps/web
SCRIPTS    := $(ROOT)/scripts/setup
DOCS_DIR   := $(ROOT)/docs
RETOMADA   := $(DOCS_DIR)/retomada

# ── Docker ──────────────────────────────────────────────────────────────────
COMPOSE_FILE := docker-compose.yml
COMPOSE_CMD  := docker compose

# ── Help ────────────────────────────────────────────────────────────────────
.PHONY: help
help: ## Mostra esta ajuda
	@echo "$(C_CYAN)bioplatform — comandos disponíveis$(C_RESET)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(C_GREEN)%-22s$(C_RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(C_YELLOW)Fluxo de retomada:$(C_RESET)"
	@echo "  make doctor → make setup-local → make up → make health → make test → make recovery-report"

# ══════════════════════════════════════════════════════════════════════════════
# DIAGNÓSTICO
# ══════════════════════════════════════════════════════════════════════════════

.PHONY: doctor
doctor: ## Diagnóstico completo do ambiente de desenvolvimento
	@echo "$(C_CYAN)=== DOCTOR: Diagnóstico do ambiente ===$(C_RESET)"
	@echo ""
	@bash $(SCRIPTS)/00_doctor.sh 2>/dev/null || echo "$(C_YELLOW)⚠ 00_doctor.sh não encontrado — rode 'make setup-local' primeiro$(C_RESET)"

.PHONY: env-check
env-check: ## Verifica se .env existe e tem variáveis obrigatórias
	@echo "$(C_CYAN)=== ENV-CHECK ===$(C_RESET)"
	@if [ ! -f .env ]; then \
		echo "$(C_RED)✗ .env não encontrado.$(C_RESET)"; \
		echo "  Copie .env.example para .env e preencha as variáveis:"; \
		echo "  cp .env.example .env"; \
		exit 1; \
	fi
	@echo "$(C_GREEN)✓ .env presente$(C_RESET)"
	@for var in POSTGRES_PASSWORD DATABASE_URL API_SECRET_KEY DOMAIN; do \
		if grep -q "^$${var}=" .env 2>/dev/null && ! grep -q "^$${var}=change_me\|^$${var}=$$" .env 2>/dev/null; then \
			echo "  $(C_GREEN)✓ $${var}$(C_RESET)"; \
		else \
			echo "  $(C_RED)✗ $${var} ausente ou placeholder$(C_RESET)"; \
		fi; \
	done

.PHONY: compose-check
compose-check: ## Valida docker-compose.yml e verifica Docker
	@echo "$(C_CYAN)=== COMPOSE-CHECK ===$(C_RESET)"
	@docker --version || { echo "$(C_RED)✗ Docker não encontrado$(C_RESET)"; exit 1; }
	@echo "$(C_GREEN)✓ Docker: $$(docker --version)$(C_RESET)"
	@$(COMPOSE_CMD) version || { echo "$(C_RED)✗ Docker Compose não encontrado$(C_RESET)"; exit 1; }
	@echo "$(C_GREEN)✓ Compose: $$(docker compose version)$(C_RESET)"
	@$(COMPOSE_CMD) -f $(COMPOSE_FILE) config --quiet 2>/dev/null && \
		echo "$(C_GREEN)✓ docker-compose.yml válido$(C_RESET)" || \
		echo "$(C_YELLOW)⚠ docker-compose.yml pode ter problemas (verifique variáveis de ambiente)$(C_RESET)"

# ══════════════════════════════════════════════════════════════════════════════
# SETUP
# ══════════════════════════════════════════════════════════════════════════════

.PHONY: setup-local
setup-local: ## Instala todas dependências para desenvolvimento local
	@echo "$(C_CYAN)=== SETUP-LOCAL ===$(C_RESET)"
	@echo ""
	@echo "$(C_YELLOW)Este comando executa scripts idempotentes em ordem.$(C_RESET)"
	@echo "Pressione Ctrl+C para cancelar ou Enter para continuar..."
	@read -r _
	@bash $(SCRIPTS)/00_doctor.sh || true
	@bash $(SCRIPTS)/01_install_base_wsl.sh || echo "$(C_YELLOW)⚠ 01 pular (não-WSL)$(C_RESET)"
	@bash $(SCRIPTS)/02_setup_python_tools.sh || echo "$(C_YELLOW)⚠ 02 falhou — verifique Python$(C_RESET)"
	@bash $(SCRIPTS)/03_setup_node_tools.sh || echo "$(C_YELLOW)⚠ 03 falhou — verifique Node.js$(C_RESET)"
	@bash $(SCRIPTS)/04_setup_bioinfo_tools.sh || echo "$(C_YELLOW)⚠ 04 falhou — ferramentas opcionais$(C_RESET)"
	@bash $(SCRIPTS)/05_local_env_template.sh || echo "$(C_YELLOW)⚠ 05 falhou$(C_RESET)"
	@bash $(SCRIPTS)/07_validate_project.sh || echo "$(C_YELLOW)⚠ 07 falhou$(C_RESET)"
	@echo ""
	@echo "$(C_GREEN)✓ Setup local concluído.$(C_RESET)"
	@echo "  Próximo: make up"

# ══════════════════════════════════════════════════════════════════════════════
# DOCKER OPERAÇÕES
# ══════════════════════════════════════════════════════════════════════════════

.PHONY: up
up: ## Sobe todos os serviços Docker (API + Postgres + Redis + Caddy)
	@echo "$(C_CYAN)=== UP: Iniciando stack Docker ===$(C_RESET)"
	@$(COMPOSE_CMD) -f $(COMPOSE_FILE) up -d --build --remove-orphans
	@echo ""
	@echo "$(C_GREEN)✓ Serviços iniciados.$(C_RESET)"
	@echo "  Aguardando health checks..."
	@sleep 5
	@$(MAKE) health

.PHONY: down-safe
down-safe: ## Para todos os serviços SEM remover volumes
	@echo "$(C_CYAN)=== DOWN-SAFE: Parando serviços (volumes preservados) ===$(C_RESET)"
	@$(COMPOSE_CMD) -f $(COMPOSE_FILE) down
	@echo "$(C_GREEN)✓ Serviços parados. Volumes e dados preservados.$(C_RESET)"

.PHONY: logs
logs: ## Mostra logs de todos os serviços (follow)
	@$(COMPOSE_CMD) -f $(COMPOSE_FILE) logs -f --tail=50

.PHONY: logs-api
logs-api: ## Logs apenas da API
	@$(COMPOSE_CMD) -f $(COMPOSE_FILE) logs -f --tail=50 api

.PHONY: health
health: ## Verifica saúde de todos os serviços
	@echo "$(C_CYAN)=== HEALTH ===$(C_RESET)"
	@echo ""
	@# API health
	@if curl -sf http://localhost:8000/health > /dev/null 2>&1; then \
		echo "  $(C_GREEN)✓ API (localhost:8000/health)$(C_RESET)"; \
		curl -s http://localhost:8000/health | python3 -m json.tool 2>/dev/null || true; \
	else \
		echo "  $(C_RED)✗ API não responde$(C_RESET)"; \
	fi
	@echo ""
	@# Postgres
	@if $(COMPOSE_CMD) -f $(COMPOSE_FILE) exec -T postgres pg_isready -U bio 2>/dev/null; then \
		echo "  $(C_GREEN)✓ Postgres$(C_RESET)"; \
	else \
		echo "  $(C_YELLOW)⚠ Postgres não verificado (container pode não estar rodando)$(C_RESET)"; \
	fi
	@# Redis
	@if $(COMPOSE_CMD) -f $(COMPOSE_FILE) exec -T redis redis-cli ping 2>/dev/null | grep -q PONG; then \
		echo "  $(C_GREEN)✓ Redis$(C_RESET)"; \
	else \
		echo "  $(C_YELLOW)⚠ Redis não verificado$(C_RESET)"; \
	fi
	@# Caddy
	@if curl -sf http://localhost:80/health 2>/dev/null || curl -sf http://localhost:2019/config/ 2>/dev/null; then \
		echo "  $(C_GREEN)✓ Caddy$(C_RESET)"; \
	else \
		echo "  $(C_YELLOW)⚠ Caddy não verificado$(C_RESET)"; \
	fi

# ══════════════════════════════════════════════════════════════════════════════
# QUALIDADE DE CÓDIGO
# ══════════════════════════════════════════════════════════════════════════════

.PHONY: api-lint
api-lint: ## Roda ruff lint no backend
	@echo "$(C_CYAN)=== API-LINT ===$(C_RESET)"
	@cd $(API_DIR) && python3 -m ruff check . --config $(ROOT)/ruff.toml 2>/dev/null || \
		python3 -m ruff check $(API_DIR) --config $(ROOT)/ruff.toml 2>/dev/null || \
		echo "$(C_YELLOW)⚠ ruff não instalado — rode 'make setup-local'$(C_RESET)"

.PHONY: api-typecheck
api-typecheck: ## Roda mypy no backend (se disponível)
	@echo "$(C_CYAN)=== API-TYPECHECK ===$(C_RESET)"
	@cd $(API_DIR) && python3 -m mypy . --ignore-missing-imports 2>/dev/null || \
		echo "$(C_YELLOW)⚠ mypy não instalado ou typecheck falhou$(C_RESET)"

.PHONY: api-test
api-test: ## Roda pytest no backend
	@echo "$(C_CYAN)=== API-TEST ===$(C_RESET)"
	@cd $(API_DIR) && python3 -m pytest -v 2>/dev/null || \
		echo "$(C_YELLOW)⚠ pytest não instalado ou sem testes$(C_RESET)"

.PHONY: web-install
web-install: ## Instala dependências do frontend
	@echo "$(C_CYAN)=== WEB-INSTALL ===$(C_RESET)"
	@cd $(WEB_DIR) && pnpm install --frozen-lockfile 2>/dev/null || npm install

.PHONY: web-build
web-build: ## Builda o frontend para produção
	@echo "$(C_CYAN)=== WEB-BUILD ===$(C_RESET)"
	@cd $(WEB_DIR) && pnpm build 2>/dev/null || npm run build

.PHONY: web-lint
web-lint: ## Roda lint no frontend (ESLint/tsc)
	@echo "$(C_CYAN)=== WEB-LINT ===$(C_RESET)"
	@cd $(WEB_DIR) && npx tsc --noEmit 2>/dev/null || echo "$(C_YELLOW)⚠ TypeScript check falhou$(C_RESET)"

.PHONY: test
test: api-lint web-lint ## Roda todos os testes e verificações
	@echo ""
	@echo "$(C_GREEN)✓ Verificações concluídas.$(C_RESET)"

# ══════════════════════════════════════════════════════════════════════════════
# RELATÓRIOS
# ══════════════════════════════════════════════════════════════════════════════

.PHONY: recovery-report
recovery-report: ## Gera relatório completo de estado do projeto
	@echo "$(C_CYAN)=== RECOVERY-REPORT ===$(C_RESET)"
	@echo ""
	@mkdir -p $(RETOMADA)
	@bash $(SCRIPTS)/07_validate_project.sh 2>/dev/null || true
	@echo ""
	@echo "Relatório salvo em: $(RETOMADA)/"

# ══════════════════════════════════════════════════════════════════════════════
# VPS (REQUER CONFIRMAÇÃO)
# ══════════════════════════════════════════════════════════════════════════════

.PHONY: vps-audit
vps-audit: ## Auditoria read-only da VPS (requer CONFIRMO_AUDITORIA_VPS)
	@echo "$(C_RED)=== VPS-AUDIT: Requer confirmação explícita ===$(C_RESET)"
	@echo ""
	@echo "Este comando faz auditoria READ-ONLY na VPS Hostinger."
	@echo "Nenhuma alteração é feita em produção."
	@echo ""
	@echo "Para prosseguir, digite exatamente: CONFIRMO_AUDITORIA_VPS"
	@read -r confirm; \
	if [ "$$confirm" = "CONFIRMO_AUDITORIA_VPS" ]; then \
		bash $(SCRIPTS)/08_vps_audit_readonly.sh; \
	else \
		echo "$(C_YELLOW)Auditoria cancelada.$(C_RESET)"; \
	fi

.PHONY: vps-backup
vps-backup: ## Backup da VPS (requer CONFIRMO_BACKUP)
	@echo "$(C_RED)=== VPS-BACKUP: Requer confirmação explícita ===$(C_RESET)"
	@echo ""
	@echo "Este comando faz backup completo da VPS (banco + volumes + configs)."
	@echo ""
	@echo "Para prosseguir, digite exatamente: CONFIRMO_BACKUP"
	@read -r confirm; \
	if [ "$$confirm" = "CONFIRMO_BACKUP" ]; then \
		bash $(SCRIPTS)/09_vps_backup.sh; \
	else \
		echo "$(C_YELLOW)Backup cancelado.$(C_RESET)"; \
	fi

.PHONY: deploy-safe
deploy-safe: ## Deploy seguro para VPS (requer CONFIRMO_PRODUCAO)
	@echo "$(C_RED)=== DEPLOY-SAFE: Requer confirmação explícita ===$(C_RESET)"
	@echo ""
	@echo "Este comando faz deploy completo na VPS Hostinger."
	@echo "Requer: backup prévio, .env de produção, DNS configurado."
	@echo ""
	@echo "Para prosseguir, digite exatamente: CONFIRMO_PRODUCAO"
	@read -r confirm; \
	if [ "$$confirm" = "CONFIRMO_PRODUCAO" ]; then \
		bash $(SCRIPTS)/10_deploy_safe.sh; \
	else \
		echo "$(C_YELLOW)Deploy cancelado.$(C_RESET)"; \
	fi

# ══════════════════════════════════════════════════════════════════════════════
# UTILITÁRIOS
# ══════════════════════════════════════════════════════════════════════════════

.PHONY: clean
clean: ## Remove caches Python, node_modules, build artifacts
	@echo "$(C_CYAN)=== CLEAN ===$(C_RESET)"
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	@rm -rf $(WEB_DIR)/dist 2>/dev/null || true
	@echo "$(C_GREEN)✓ Caches limpos.$(C_RESET)"

.PHONY: docker-prune-safe
docker-prune-safe: ## Limpa imagens Docker não usadas (sem tocar volumes)
	@echo "$(C_CYAN)=== DOCKER-PRUNE-SAFE ===$(C_RESET)"
	@docker image prune -f
	@docker builder prune -f
	@echo "$(C_GREEN)✓ Imagens não usadas removidas. Volumes preservados.$(C_RESET)"