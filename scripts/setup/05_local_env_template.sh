#!/usr/bin/env bash
# ============================================================================
# 05_local_env_template.sh — Cria .env a partir de .env.example
#
# Se .env não existe, copia de .env.example (se existir) ou gera um template.
# NUNCA sobrescreve .env existente.
# ============================================================================
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

echo -e "${CYAN}=== 05: Configurando .env ===${NC}"

if [ -f .env ]; then
    echo -e "${GREEN}✓ .env já existe — preservado${NC}"
    # Verificar se tem variáveis críticas
    for var in POSTGRES_PASSWORD DATABASE_URL API_SECRET_KEY; do
        if grep -q "^${var}=" .env 2>/dev/null && ! grep -q "^${var}=change_me\|^${var}=$" .env 2>/dev/null; then
            echo -e "  ${GREEN}✓ $var${NC}"
        else
            echo -e "  ${YELLOW}⚠ $var ausente ou com placeholder — edite .env${NC}"
        fi
    done
    exit 0
fi

# ── Tentar copiar de .env.example ─────────────────────────────────────────────
if [ -f .env.example ]; then
    echo -e "  Copiando .env.example → .env"
    cp .env.example .env
    echo -e "${GREEN}✓ .env criado a partir de .env.example${NC}"
    echo -e "${YELLOW}⚠ Edite .env com valores reais antes de subir os serviços!${NC}"
    exit 0
fi

# ── Gerar template mínimo ─────────────────────────────────────────────────────
echo -e "${YELLOW}⚠ .env.example não encontrado — gerando template mínimo${NC}"

# Gerar senha aleatória
GEN_PASS="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))' 2>/dev/null || \
            openssl rand -base64 32 2>/dev/null || \
            echo 'change_me_please_replace_with_secure_password')"

GEN_SECRET="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))' 2>/dev/null || \
              openssl rand -base64 32 2>/dev/null || \
              echo 'change_me_secret_key_replace')"

cat > .env << EOF
# ============================================================================
# bioplatform — Environment Variables
# Gerado automaticamente por 05_local_env_template.sh
# ALTERE OS VALORES antes de subir para produção!
# ============================================================================

# ── PostgreSQL ──────────────────────────────────────────────────────────────
POSTGRES_USER=bio
POSTGRES_PASSWORD=${GEN_PASS}
POSTGRES_DB=bioplatform
DATABASE_URL=postgresql+asyncpg://bio:${GEN_PASS}@postgres:5432/bioplatform

# ── Redis ───────────────────────────────────────────────────────────────────
REDIS_URL=redis://redis:6379/0

# ── API ─────────────────────────────────────────────────────────────────────
API_SECRET_KEY=${GEN_SECRET}
ALLOWED_ORIGINS=*
DOMAIN=localhost

# ── ESM3 (EvolutionaryScale) ────────────────────────────────────────────────
ESM_API_URL=https://api.evolutionaryscale.ai
ESM_API_KEY=

# ── Biosafety ───────────────────────────────────────────────────────────────
BIOSAFETY_STRICT_MODE=false

# ── Email (opcional) ────────────────────────────────────────────────────────
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
EOF

echo -e "${GREEN}✓ .env template gerado${NC}"
echo -e "${YELLOW}⚠ ALTERE OS VALORES em .env antes de subir os serviços!${NC}"
echo -e "  Especialmente: POSTGRES_PASSWORD, API_SECRET_KEY"
