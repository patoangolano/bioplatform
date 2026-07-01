#!/usr/bin/env bash
# ============================================================================
# 09_vps_backup.sh — Backup completo da VPS Hostinger
#
# Faz dump do PostgreSQL, backup de volumes Docker, e salva configs.
# Tudo é baixado para docs/retomada/backups/
#
# Requer: SSH configurado, VPS_HOST env var.
# ============================================================================
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
BACKUP_DIR="$ROOT/docs/retomada/backups/$(date '+%Y%m%d_%H%M%S')"
VPS_HOST="${VPS_HOST:-bioplatform-vps}"
VPS_USER="${VPS_USER:-root}"

mkdir -p "$BACKUP_DIR"

echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║           VPS BACKUP                                        ║${NC}"
echo -e "${CYAN}║           Target: $VPS_USER@$VPS_HOST                          ║${NC}"
echo -e "${CYAN}║           Destino: $BACKUP_DIR                               ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"

# ── Verificar SSH ────────────────────────────────────────────────────────────
echo -e "\n${CYAN}─── Verificando conectividade ───${NC}"
if ! ssh -o ConnectTimeout=10 -o BatchMode=yes "$VPS_USER@$VPS_HOST" "echo ok" 2>/dev/null; then
    echo -e "${RED}✗ SSH falhou para $VPS_HOST${NC}"
    exit 1
fi
echo -e "${GREEN}✓ SSH OK${NC}"

# ── 1. Dump do PostgreSQL ────────────────────────────────────────────────────
echo -e "\n${CYAN}─── 1/4: Dump PostgreSQL ───${NC}"
PG_DUMP_FILE="$BACKUP_DIR/postgres_dump_$(date '+%Y%m%d_%H%M%S').sql.gz"

# Tentar dump via container Docker
ssh "$VPS_USER@$VPS_HOST" "
    if docker ps --format '{{.Names}}' | grep -q 'postgres'; then
        POSTGRES_CONTAINER=\$(docker ps --format '{{.Names}}' | grep postgres | head -1)
        POSTGRES_USER=\$(docker exec \$POSTGRES_CONTAINER env | grep POSTGRES_USER | cut -d= -f2 || echo 'bio')
        POSTGRES_DB=\$(docker exec \$POSTGRES_CONTAINER env | grep POSTGRES_DB | cut -d= -f2 || echo 'bioplatform')
        docker exec \$POSTGRES_CONTAINER pg_dump -U \$POSTGRES_USER -d \$POSTGRES_DB | gzip
    else
        echo 'NO_POSTGRES_CONTAINER'
    fi
" > "$PG_DUMP_FILE" 2>/dev/null

if [ -s "$PG_DUMP_FILE" ] && ! grep -q "NO_POSTGRES_CONTAINER" "$PG_DUMP_FILE"; then
    echo -e "${GREEN}✓ Dump PostgreSQL: $(du -h "$PG_DUMP_FILE" | cut -f1)${NC}"
else
    echo -e "${YELLOW}⚠ Dump PostgreSQL não disponível (container não encontrado)${NC}"
    rm -f "$PG_DUMP_FILE"
fi

# ── 2. Configs ───────────────────────────────────────────────────────────────
echo -e "\n${CYAN}─── 2/4: Configurações ───${NC}"
CONFIG_DIR="$BACKUP_DIR/configs"
mkdir -p "$CONFIG_DIR"

# Baixar .env e docker-compose.yml
scp -q "$VPS_USER@$VPS_HOST:/root/bioplatform/.env" "$CONFIG_DIR/.env" 2>/dev/null || \
    echo -e "${YELLOW}⚠ .env não encontrado no servidor${NC}"

scp -q "$VPS_USER@$VPS_HOST:/root/bioplatform/docker-compose.yml" "$CONFIG_DIR/docker-compose.yml" 2>/dev/null || \
    echo -e "${YELLOW}⚠ docker-compose.yml não encontrado${NC}"

# Caddyfile
scp -q "$VPS_USER@$VPS_HOST:/root/bioplatform/infra/caddy/Caddyfile" "$CONFIG_DIR/Caddyfile" 2>/dev/null || \
    echo -e "${YELLOW}⚠ Caddyfile não encontrado${NC}"

echo -e "${GREEN}✓ Configs baixadas${NC}"

# ── 3. Lista de volumes ──────────────────────────────────────────────────────
echo -e "\n${CYAN}─── 3/4: Metadados de volumes ───${NC}"
ssh "$VPS_USER@$VPS_HOST" "docker volume ls --format '{{.Name}} {{.Mountpoint}}'" > "$BACKUP_DIR/volumes_list.txt" 2>/dev/null
echo -e "${GREEN}✓ Lista de volumes salva${NC}"

# ── 4. Docker compose status ─────────────────────────────────────────────────
echo -e "\n${CYAN}─── 4/4: Status dos serviços ───${NC}"
ssh "$VPS_USER@$VPS_HOST" "docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Image}}'" > "$BACKUP_DIR/containers_status.txt" 2>/dev/null
echo -e "${GREEN}✓ Status dos containers salvo${NC}"

# ── Resumo ────────────────────────────────────────────────────────────────────
echo -e "\n${CYAN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Backup concluído.${NC}"
echo -e "  Destino: ${CYAN}$BACKUP_DIR${NC}"
echo ""
echo -e "  Arquivos:"
ls -la "$BACKUP_DIR"/
echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"
