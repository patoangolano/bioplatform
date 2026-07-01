#!/usr/bin/env bash
# ============================================================================
# 03_setup_node_tools.sh — Configura ambiente Node.js
#
# Instala pnpm (se ausente), dependências do frontend, verifica TypeScript.
# ============================================================================
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
WEB_DIR="$ROOT/apps/web"

echo -e "${CYAN}=== 03: Configurando ambiente Node.js ===${NC}"

# ── Verificar Node.js ─────────────────────────────────────────────────────────
if ! command -v node &>/dev/null; then
    echo -e "${RED}✗ Node.js não encontrado. Instale Node.js 20+ primeiro.${NC}"
    exit 1
fi
echo -e "  Node.js: $(node --version)"

# ── Verificar/instalar pnpm ──────────────────────────────────────────────────
if ! command -v pnpm &>/dev/null; then
    echo -e "  Instalando pnpm..."
    npm install -g pnpm && echo -e "  ${GREEN}✓ pnpm instalado${NC}" || {
        echo -e "${YELLOW}⚠ Falha ao instalar pnpm globalmente — usando npm como fallback${NC}"
    }
else
    echo -e "  pnpm: $(pnpm --version)"
fi

# ── Instalar dependências do frontend ─────────────────────────────────────────
if [ -f "$WEB_DIR/package.json" ]; then
    echo -e "  Instalando dependências do frontend..."
    cd "$WEB_DIR"
    
    if command -v pnpm &>/dev/null; then
        pnpm install --frozen-lockfile 2>/dev/null || pnpm install || {
            echo -e "${YELLOW}⚠ pnpm install falhou — tentando npm${NC}"
            npm install
        }
    else
        npm install
    fi
    
    echo -e "${GREEN}✓ Dependências do frontend instaladas${NC}"
else
    echo -e "${YELLOW}⚠ apps/web/package.json não encontrado${NC}"
fi

# ── Verificar TypeScript ──────────────────────────────────────────────────────
if [ -f "$WEB_DIR/tsconfig.json" ]; then
    echo -e "  Verificando TypeScript..."
    cd "$WEB_DIR"
    if npx tsc --noEmit 2>/dev/null; then
        echo -e "  ${GREEN}✓ TypeScript compila sem erros${NC}"
    else
        echo -e "  ${YELLOW}⚠ TypeScript tem erros (pode ser normal em desenvolvimento)${NC}"
    fi
fi

echo -e "\n${GREEN}✓ Setup Node.js concluído.${NC}"
