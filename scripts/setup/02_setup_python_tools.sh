#!/usr/bin/env bash
# ============================================================================
# 02_setup_python_tools.sh — Configura ambiente Python
#
# Cria venv, instala pip-tools, ruff, mypy, pytest.
# Instala dependências de apps/api, apps/worker, mcp_servers, workflows.
# ============================================================================
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

echo -e "${CYAN}=== 02: Configurando ambiente Python ===${NC}"

# Encontrar Python
PYTHON=""
for py in python3 python; do
    if command -v "$py" &>/dev/null; then
        PYTHON="$py"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo -e "${RED}✗ Python não encontrado. Instale Python 3.11+ primeiro.${NC}"
    exit 1
fi

echo -e "  Python: $($PYTHON --version)"

# ── Criar venv se não existir ─────────────────────────────────────────────────
if [ ! -d "$ROOT/.venv" ]; then
    echo -e "  Criando .venv..."
    $PYTHON -m venv "$ROOT/.venv"
    echo -e "${GREEN}✓ .venv criado${NC}"
else
    echo -e "${GREEN}✓ .venv já existe${NC}"
fi

# Ativar venv
source "$ROOT/.venv/bin/activate" 2>/dev/null || source "$ROOT/.venv/Scripts/activate" 2>/dev/null || {
    echo -e "${YELLOW}⚠ Não foi possível ativar .venv automaticamente${NC}"
}

# ── Upgrade pip ───────────────────────────────────────────────────────────────
echo -e "  Atualizando pip..."
pip install --upgrade pip -q

# ── Instalar ferramentas de desenvolvimento ──────────────────────────────────
echo -e "  Instalando ferramentas de dev..."
pip install -q pip-tools ruff mypy pytest pytest-asyncio httpx

# ── Instalar dependências de cada módulo ──────────────────────────────────────
install_reqs() {
    local dir="$1"
    local name="$2"
    if [ -f "$dir/requirements.txt" ]; then
        echo -e "  Instalando dependências de $name..."
        pip install -q -r "$dir/requirements.txt" && \
            echo -e "  ${GREEN}✓ $name${NC}" || \
            echo -e "  ${YELLOW}⚠ $name — alguns pacotes podem ter falhado${NC}"
    else
        echo -e "  ${YELLOW}⚠ $name: requirements.txt não encontrado${NC}"
    fi
}

install_reqs "$ROOT/apps/api" "apps/api"
install_reqs "$ROOT/apps/worker" "apps/worker"
install_reqs "$ROOT/mcp_servers" "mcp_servers" 2>/dev/null || true
install_reqs "$ROOT/workflows" "workflows" 2>/dev/null || true

# ── Instalar requirements-mcp.txt se existir ──────────────────────────────────
if [ -f "$ROOT/requirements-mcp.txt" ]; then
    echo -e "  Instalando requirements-mcp.txt..."
    pip install -q -r "$ROOT/requirements-mcp.txt" && \
        echo -e "  ${GREEN}✓ requirements-mcp.txt${NC}" || \
        echo -e "  ${YELLOW}⚠ requirements-mcp.txt — alguns pacotes podem ter falhado${NC}"
fi

# ── Verificar imports críticos ────────────────────────────────────────────────
echo -e "\n${CYAN}Verificando imports críticos...${NC}"
cd "$ROOT"

check_import() {
    local module="$1"
    if python -c "import $module" 2>/dev/null; then
        echo -e "  ${GREEN}✓ $module${NC}"
    else
        echo -e "  ${YELLOW}⚠ $module — não importável (pode precisar de dependências de sistema)${NC}"
    fi
}

check_import fastapi
check_import sqlalchemy
check_import redis
check_import httpx
check_import pydantic

echo -e "\n${GREEN}✓ Setup Python concluído.${NC}"
