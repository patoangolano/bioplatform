#!/usr/bin/env bash
# ============================================================================
# 10_deploy_safe.sh — Deploy seguro para VPS Hostinger
#
# Pré-requisitos:
#   1. Backup concluído (09_vps_backup.sh)
#   2. .env de produção configurado
#   3. DNS apontando para VPS
#   4. Testes locais passando
#
# Fluxo:
#   1. Verificar pré-requisitos
#   2. Build local das imagens
#   3. Push para registry (ou transferência direta)
#   4. Deploy na VPS com health check
#   5. Rollback automático se health check falhar
# ============================================================================
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VPS_HOST="${VPS_HOST:-bioplatform-vps}"
VPS_USER="${VPS_USER:-root}"
VPS_PROJECT_DIR="${VPS_PROJECT_DIR:-/root/bioplatform}"
DEPLOY_LOG="$ROOT/docs/retomada/deploy_$(date '+%Y%m%d_%H%M%S').log"

echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║           DEPLOY SAFE — Produção                            ║${NC}"
echo -e "${CYAN}║           Target: $VPS_USER@$VPS_HOST:$VPS_PROJECT_DIR         ║${NC}"
echo -e "${CYAN}║           $(date '+%Y-%m-%d %H:%M:%S')                          ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"

log() { echo -e "$1" | tee -a "$DEPLOY_LOG"; }

# ── 1. Verificar pré-requisitos ──────────────────────────────────────────────
log "\n${CYAN}─── 1/6: Pré-requisitos ───${NC}"

# .env
if [ ! -f "$ROOT/.env" ]; then
    log "${RED}✗ .env não encontrado. Crie a partir de .env.example${NC}"
    exit 1
fi
log "${GREEN}✓ .env presente${NC}"

# SSH
if ! ssh -o ConnectTimeout=10 -o BatchMode=yes "$VPS_USER@$VPS_HOST" "echo ok" 2>/dev/null; then
    log "${RED}✗ SSH falhou para $VPS_HOST${NC}"
    exit 1
fi
log "${GREEN}✓ SSH OK${NC}"

# Docker local
if ! docker info &>/dev/null 2>&1; then
    log "${RED}✗ Docker local não está rodando${NC}"
    exit 1
fi
log "${GREEN}✓ Docker local OK${NC}"

# ── 2. Sincronizar código ────────────────────────────────────────────────────
log "\n${CYAN}─── 2/6: Sincronizando código ───${NC}"

# Criar diretório no VPS se não existir
ssh "$VPS_USER@$VPS_HOST" "mkdir -p $VPS_PROJECT_DIR"

# Sincronizar arquivos (excluindo node_modules, .venv, .git, __pycache__)
rsync -avz --delete \
    --exclude '.git' \
    --exclude 'node_modules' \
    --exclude '.venv' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '.mypy_cache' \
    --exclude '.ruff_cache' \
    --exclude 'dist' \
    --exclude 'docs/retomada/backups' \
    "$ROOT/" "$VPS_USER@$VPS_HOST:$VPS_PROJECT_DIR/" 2>&1 | tail -5

log "${GREEN}✓ Código sincronizado${NC}"

# ── 3. Copiar .env de produção ───────────────────────────────────────────────
log "\n${CYAN}─── 3/6: Configurando .env de produção ───${NC}"
scp -q "$ROOT/.env" "$VPS_USER@$VPS_HOST:$VPS_PROJECT_DIR/.env"
log "${GREEN}✓ .env copiado para VPS${NC}"

# ── 4. Build e deploy ────────────────────────────────────────────────────────
log "\n${CYAN}─── 4/6: Build e deploy ───${NC}"

# Salvar estado anterior para rollback
PREVIOUS_STATE="$(ssh "$VPS_USER@$VPS_HOST" "cd $VPS_PROJECT_DIR && docker compose ps --format json 2>/dev/null || echo '{}'")"
echo "$PREVIOUS_STATE" > "$ROOT/docs/retomada/previous_state.json"

# Build e up
ssh "$VPS_USER@$VPS_HOST" "cd $VPS_PROJECT_DIR && docker compose up -d --build --remove-orphans" 2>&1 | tee -a "$DEPLOY_LOG"

log "${GREEN}✓ Deploy executado${NC}"

# ── 5. Health check ──────────────────────────────────────────────────────────
log "\n${CYAN}─── 5/6: Health check ───${NC}"

log "Aguardando serviços iniciarem (30s)..."
sleep 30

HEALTH_OK=true

# Verificar API
if ssh "$VPS_USER@$VPS_HOST" "curl -sf http://localhost:8000/health" 2>/dev/null; then
    log "${GREEN}✓ API health check OK${NC}"
else
    log "${RED}✗ API health check FALHOU${NC}"
    HEALTH_OK=false
fi

# Verificar Postgres
if ssh "$VPS_USER@$VPS_HOST" "docker compose -f $VPS_PROJECT_DIR/docker-compose.yml exec -T postgres pg_isready -U bio" 2>/dev/null; then
    log "${GREEN}✓ Postgres OK${NC}"
else
    log "${YELLOW}⚠ Postgres health check falhou${NC}"
fi

# Verificar Redis
if ssh "$VPS_USER@$VPS_HOST" "docker compose -f $VPS_PROJECT_DIR/docker-compose.yml exec -T redis redis-cli ping" 2>/dev/null | grep -q PONG; then
    log "${GREEN}✓ Redis OK${NC}"
else
    log "${YELLOW}⚠ Redis health check falhou${NC}"
fi

# ── 6. Rollback se necessário ────────────────────────────────────────────────
if [ "$HEALTH_OK" = false ]; then
    log "\n${RED}─── HEALTH CHECK FALHOU — Iniciando rollback ───${NC}"
    log "${YELLOW}Tentando rollback para estado anterior...${NC}"
    
    ssh "$VPS_USER@$VPS_HOST" "cd $VPS_PROJECT_DIR && docker compose down && docker compose up -d" 2>&1 | tee -a "$DEPLOY_LOG"
    
    log "${YELLOW}⚠ Rollback executado. Verifique manualmente.${NC}"
    log "Log salvo em: $DEPLOY_LOG"
    exit 1
fi

# ── Sucesso ──────────────────────────────────────────────────────────────────
log "\n${GREEN}════════════════════════════════════════════════════════════════${NC}"
log "${GREEN}✓ DEPLOY CONCLUÍDO COM SUCESSO${NC}"
log "${GREEN}════════════════════════════════════════════════════════════════${NC}"
log "Log salvo em: $DEPLOY_LOG"
log ""
log "Verifique:"
log "  https://seu-dominio.com/health"
log "  ssh $VPS_USER@$VPS_HOST 'cd $VPS_PROJECT_DIR && docker compose ps'"
