#!/usr/bin/env bash
# ============================================================================
# 07_validate_project.sh — Validação completa do projeto
#
# Verifica: imports Python, lint, typecheck, estrutura de diretórios,
#           docker-compose syntax, formatação de arquivos críticos.
# Gera relatório em docs/retomada/validation_report.txt
# ============================================================================
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
REPORT_DIR="$ROOT/docs/retomada"
REPORT="$REPORT_DIR/validation_report.txt"
PASS=0
FAIL=0
WARN=0

mkdir -p "$REPORT_DIR"

pass() { echo -e "  ${GREEN}✓${NC} $1"; echo "  PASS: $1" >> "$REPORT"; PASS=$((PASS + 1)); }
fail() { echo -e "  ${RED}✗${NC} $1"; echo "  FAIL: $1" >> "$REPORT"; FAIL=$((FAIL + 1)); }
warn() { echo -e "  ${YELLOW}⚠${NC} $1"; echo "  WARN: $1" >> "$REPORT"; WARN=$((WARN + 1)); }
section() { echo -e "\n${CYAN}─── $1 ───${NC}"; echo "" >> "$REPORT"; echo "=== $1 ===" >> "$REPORT"; }

# ── Iniciar relatório ────────────────────────────────────────────────────────
echo "# Validation Report — $(date '+%Y-%m-%d %H:%M:%S')" > "$REPORT"
echo "" >> "$REPORT"

echo -e "${CYAN}=== 07: Validação do projeto ===${NC}"

# ── Estrutura de diretórios ──────────────────────────────────────────────────
section "Estrutura de diretórios"
for dir in apps/api apps/web apps/worker mcp_servers mcp_servers/adapters services workflows infra scripts skills wiki raw; do
    if [ -d "$ROOT/$dir" ]; then
        pass "$dir/"
    else
        warn "$dir/ ausente"
    fi
done

# ── Arquivos críticos ────────────────────────────────────────────────────────
section "Arquivos críticos"
for file in docker-compose.yml Makefile CLAUDE.md AGENTS.md ruff.toml .gitignore README.md; do
    if [ -f "$ROOT/$file" ]; then
        pass "$file"
    else
        warn "$file ausente"
    fi
done

# ── Python: imports ──────────────────────────────────────────────────────────
section "Python — imports"
cd "$ROOT"

# Tentar ativar venv
source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate 2>/dev/null || true

check_import() {
    local module="$1"
    local source="$2"
    if python -c "import $module" 2>/dev/null; then
        pass "import $module ($source)"
    else
        warn "import $module falhou ($source)"
    fi
}

check_import fastapi "apps/api"
check_import sqlalchemy "apps/api"
check_import redis "apps/api"
check_import httpx "apps/api"
check_import pydantic "apps/api"

# ── Python: lint (ruff) ──────────────────────────────────────────────────────
section "Python — lint (ruff)"
if python -m ruff check "$ROOT/apps/api" --config "$ROOT/ruff.toml" 2>/dev/null; then
    pass "ruff: apps/api sem erros"
else
    warn "ruff: apps/api tem avisos (verifique)"
fi

# ── Python: typecheck (mypy) ─────────────────────────────────────────────────
section "Python — typecheck (mypy)"
if python -m mypy "$ROOT/apps/api" --ignore-missing-imports 2>/dev/null; then
    pass "mypy: apps/api OK"
else
    warn "mypy: apps/api tem issues (ou mypy não instalado)"
fi

# ── Docker Compose ───────────────────────────────────────────────────────────
section "Docker Compose"
if docker compose -f "$ROOT/docker-compose.yml" config --quiet 2>/dev/null; then
    pass "docker-compose.yml válido"
else
    warn "docker-compose.yml inválido ou .env ausente"
fi

# ── Dockerfiles ──────────────────────────────────────────────────────────────
section "Dockerfiles"
for df in apps/api/Dockerfile apps/worker/Dockerfile apps/web/Dockerfile workflows/Dockerfile; do
    if [ -f "$ROOT/$df" ]; then
        pass "$df presente"
    else
        warn "$df ausente"
    fi
done

# ── Frontend ──────────────────────────────────────────────────────────────────
section "Frontend"
if [ -f "$ROOT/apps/web/package.json" ]; then
    pass "package.json presente"
    if [ -d "$ROOT/apps/web/node_modules" ]; then
        pass "node_modules instalado"
    else
        warn "node_modules ausente — rode 'make web-install'"
    fi
else
    fail "apps/web/package.json ausente"
fi

# ── Git ───────────────────────────────────────────────────────────────────────
section "Git"
if git rev-parse --git-dir &>/dev/null 2>&1; then
    BRANCH="$(git branch --show-current 2>/dev/null || echo '?')"
    pass "branch: $BRANCH"
    UNTRACKED="$(git status --porcelain 2>/dev/null | wc -l)"
    if [ "$UNTRACKED" -gt 0 ]; then
        warn "$UNTRACKED arquivos não commitados"
    else
        pass "working tree limpo"
    fi
fi

# ── Resumo ────────────────────────────────────────────────────────────────────
echo "" >> "$REPORT"
echo "=== RESUMO ===" >> "$REPORT"
echo "PASS: $PASS  FAIL: $FAIL  WARN: $WARN" >> "$REPORT"

echo -e "\n${CYAN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Pass: $PASS${NC}  ${RED}✗ Fail: $FAIL${NC}  ${YELLOW}⚠ Warn: $WARN${NC}"
echo -e "Relatório salvo em: ${CYAN}$REPORT${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"
