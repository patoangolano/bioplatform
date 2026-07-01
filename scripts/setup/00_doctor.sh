#!/usr/bin/env bash
# ============================================================================
# 00_doctor.sh — Diagnóstico completo do ambiente de desenvolvimento
#
# Verifica: SO, shell, Docker, Python, Node.js, Git, ferramentas auxiliares,
#           variáveis de ambiente, portas, espaço em disco, conectividade.
# ============================================================================
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

PASS=0
FAIL=0
WARN=0

pass() { echo -e "  ${GREEN}✓${NC} $1"; PASS=$((PASS + 1)); }
fail() { echo -e "  ${RED}✗${NC} $1"; FAIL=$((FAIL + 1)); }
warn() { echo -e "  ${YELLOW}⚠${NC} $1"; WARN=$((WARN + 1)); }
section() { echo -e "\n${CYAN}─── $1 ───${NC}"; }

# ── Cabeçalho ────────────────────────────────────────────────────────────────
echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║           bioplatform — DOCTOR (Diagnóstico)                ║${NC}"
echo -e "${CYAN}║           $(date '+%Y-%m-%d %H:%M:%S')                          ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"

# ── Sistema Operacional ──────────────────────────────────────────────────────
section "Sistema Operacional"
OS="$(uname -s 2>/dev/null || echo 'Unknown')"
ARCH="$(uname -m 2>/dev/null || echo 'Unknown')"
echo -e "  OS: $OS | Arch: $ARCH"

case "$OS" in
    Linux)   pass "Linux detectado" ;;
    Darwin)  pass "macOS detectado" ;;
    MINGW*|MSYS*|CYGWIN*) warn "Windows com Git Bash — alguns scripts podem precisar de WSL" ;;
    *)       warn "SO não reconhecido: $OS" ;;
esac

# ── Shell ─────────────────────────────────────────────────────────────────────
section "Shell"
if [ -n "${BASH_VERSION:-}" ]; then
    pass "Bash ${BASH_VERSION}"
else
    fail "Bash não detectado — scripts requerem Bash"
fi

# ── Docker ────────────────────────────────────────────────────────────────────
section "Docker"
if command -v docker &>/dev/null; then
    pass "Docker: $(docker --version 2>/dev/null || echo 'versão desconhecida')"
    if docker info &>/dev/null 2>&1; then
        pass "Docker daemon rodando"
    else
        warn "Docker daemon não acessível — inicie o Docker Desktop ou serviço"
    fi
else
    fail "Docker não encontrado — instale Docker Desktop ou Docker Engine"
fi

if command -v docker &>/dev/null && docker compose version &>/dev/null 2>&1; then
    pass "Docker Compose: $(docker compose version 2>/dev/null)"
elif command -v docker-compose &>/dev/null; then
    warn "docker-compose (v1) encontrado — prefira 'docker compose' (v2)"
else
    fail "Docker Compose não encontrado"
fi

# ── Python ────────────────────────────────────────────────────────────────────
section "Python"
PYTHON=""
for py in python3 python; do
    if command -v "$py" &>/dev/null; then
        PYTHON="$py"
        break
    fi
done

if [ -n "$PYTHON" ]; then
    PY_VER="$($PYTHON --version 2>&1)"
    pass "$PY_VER"
    PY_MAJOR="$($PYTHON -c 'import sys; print(sys.version_info.major)')"
    PY_MINOR="$($PYTHON -c 'import sys; print(sys.version_info.minor)')"
    if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 11 ]; then
        pass "Python >= 3.11 ✓"
    else
        warn "Python $PY_MAJOR.$PY_MINOR — recomendado 3.11+"
    fi
    # pip
    if $PYTHON -m pip --version &>/dev/null 2>&1; then
        pass "pip: $($PYTHON -m pip --version 2>&1 | head -1)"
    else
        fail "pip não disponível"
    fi
    # venv
    if $PYTHON -m venv --help &>/dev/null 2>&1; then
        pass "venv disponível"
    else
        warn "venv não disponível"
    fi
else
    fail "Python não encontrado — instale Python 3.11+"
fi

# ── Node.js ───────────────────────────────────────────────────────────────────
section "Node.js"
if command -v node &>/dev/null; then
    pass "Node.js: $(node --version 2>/dev/null)"
else
    fail "Node.js não encontrado — instale Node.js 20+"
fi

if command -v npm &>/dev/null; then
    pass "npm: $(npm --version 2>/dev/null)"
else
    warn "npm não encontrado"
fi

if command -v pnpm &>/dev/null; then
    pass "pnpm: $(pnpm --version 2>/dev/null)"
else
    warn "pnpm não instalado — 'npm install -g pnpm' para instalar"
fi

# ── Git ───────────────────────────────────────────────────────────────────────
section "Git"
if command -v git &>/dev/null; then
    pass "Git: $(git --version 2>/dev/null)"
    if git rev-parse --git-dir &>/dev/null 2>&1; then
        BRANCH="$(git branch --show-current 2>/dev/null || echo 'desconhecido')"
        pass "Repositório git: branch '$BRANCH'"
    else
        warn "Não está em um repositório git"
    fi
else
    fail "Git não encontrado"
fi

# ── GitHub CLI ────────────────────────────────────────────────────────────────
section "GitHub CLI"
if command -v gh &>/dev/null; then
    pass "gh: $(gh --version 2>/dev/null | head -1)"
    if gh auth status &>/dev/null 2>&1; then
        pass "gh autenticado"
    else
        warn "gh não autenticado — execute 'gh auth login'"
    fi
else
    warn "GitHub CLI não instalada — opcional para deploy"
fi

# ── Ferramentas auxiliares ────────────────────────────────────────────────────
section "Ferramentas auxiliares"
for tool in curl wget jq make; do
    if command -v "$tool" &>/dev/null; then
        pass "$tool disponível"
    else
        warn "$tool não encontrado"
    fi
done

# ── Espaço em disco ───────────────────────────────────────────────────────────
section "Espaço em disco"
if command -v df &>/dev/null; then
    DISK_USAGE="$(df -h . 2>/dev/null | tail -1 | awk '{print $5 " usado de " $2 " (" $4 " livre)"}')"
    echo -e "  Disco: $DISK_USAGE"
    USED_PCT="$(df . 2>/dev/null | tail -1 | awk '{print $5}' | tr -d '%')"
    if [ "${USED_PCT:-0}" -gt 90 ]; then
        warn "Disco com mais de 90% de uso"
    else
        pass "Espaço em disco OK"
    fi
fi

# ── Portas ────────────────────────────────────────────────────────────────────
section "Portas (conflitos)"
check_port() {
    local port="$1"
    local name="$2"
    if command -v ss &>/dev/null; then
        if ss -tlnp 2>/dev/null | grep -q ":$port "; then
            warn "Porta $port ($name) em uso — pode conflitar com Docker"
        else
            pass "Porta $port ($name) livre"
        fi
    elif command -v netstat &>/dev/null; then
        if netstat -tlnp 2>/dev/null | grep -q ":$port "; then
            warn "Porta $port ($name) em uso"
        else
            pass "Porta $port ($name) livre"
        fi
    else
        warn "Não foi possível verificar porta $port ($name) — ss/netstat indisponível"
    fi
}
check_port 8000 "API"
check_port 5432 "PostgreSQL"
check_port 6379 "Redis"
check_port 80   "HTTP"
check_port 443  "HTTPS"

# ── Variáveis de ambiente ─────────────────────────────────────────────────────
section ".env"
if [ -f .env ]; then
    pass ".env encontrado"
    # Verificar variáveis críticas
    for var in POSTGRES_PASSWORD DATABASE_URL API_SECRET_KEY; do
        if grep -q "^${var}=" .env 2>/dev/null && ! grep -q "^${var}=change_me\|^${var}=$" .env 2>/dev/null; then
            pass "  $var configurado"
        else
            warn "  $var ausente ou com placeholder"
        fi
    done
else
    warn ".env não encontrado — copie .env.example para .env"
fi

# ── Arquivos do projeto ──────────────────────────────────────────────────────
section "Estrutura do projeto"
for dir in apps/api apps/web apps/worker mcp_servers services workflows infra scripts skills wiki raw; do
    if [ -d "$dir" ]; then
        pass "  $dir/"
    else
        warn "  $dir/ ausente"
    fi
done

for file in docker-compose.yml Makefile CLAUDE.md AGENTS.md ruff.toml; do
    if [ -f "$file" ]; then
        pass "  $file"
    else
        warn "  $file ausente"
    fi
done

# ── Docker Compose ────────────────────────────────────────────────────────────
section "docker-compose.yml validação"
if [ -f docker-compose.yml ]; then
    if docker compose config --quiet 2>/dev/null; then
        pass "docker-compose.yml válido"
    else
        warn "docker-compose.yml pode ter problemas (verifique .env)"
    fi
else
    fail "docker-compose.yml não encontrado"
fi

# ── Resumo ────────────────────────────────────────────────────────────────────
echo -e "\n${CYAN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Pass: $PASS${NC}  ${RED}✗ Fail: $FAIL${NC}  ${YELLOW}⚠ Warn: $WARN${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"

if [ "$FAIL" -gt 0 ]; then
    echo -e "\n${RED}Problemas críticos encontrados. Corrija antes de prosseguir.${NC}"
    exit 1
elif [ "$WARN" -gt 0 ]; then
    echo -e "\n${YELLOW}Alguns avisos — pode prosseguir, mas revise os warnings.${NC}"
    exit 0
else
    echo -e "\n${GREEN}Ambiente pronto para desenvolvimento!${NC}"
    exit 0
fi
