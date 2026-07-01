#!/usr/bin/env bash
# ============================================================================
# 08_vps_audit_readonly.sh — Auditoria READ-ONLY da VPS Hostinger
#
# Verifica: uptime, Docker, containers, volumes, redes, disco, RAM,
#           versões de serviços, logs recentes, backups existentes.
# NENHUMA ALTERAÇÃO é feita no servidor.
#
# Requer: SSH configurado para o host 'bioplatform-vps' ou VPS_HOST env var.
# ============================================================================
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
REPORT_DIR="$ROOT/docs/retomada"
AUDIT_REPORT="$REPORT_DIR/vps_audit_$(date '+%Y%m%d_%H%M%S').txt"

VPS_HOST="${VPS_HOST:-bioplatform-vps}"
VPS_USER="${VPS_USER:-root}"

mkdir -p "$REPORT_DIR"

echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║           VPS AUDIT — Somente Leitura                       ║${NC}"
echo -e "${CYAN}║           Target: $VPS_USER@$VPS_HOST                          ║${NC}"
echo -e "${CYAN}║           $(date '+%Y-%m-%d %H:%M:%S')                          ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"

# ── Verificar conectividade SSH ──────────────────────────────────────────────
echo -e "\n${CYAN}─── Conectividade SSH ───${NC}"
if ssh -o ConnectTimeout=10 -o BatchMode=yes "$VPS_USER@$VPS_HOST" "echo ok" 2>/dev/null; then
    echo -e "${GREEN}✓ SSH conectado a $VPS_HOST${NC}"
else
    echo -e "${RED}✗ Não foi possível conectar via SSH a $VPS_HOST${NC}"
    echo "  Verifique:"
    echo "  - SSH key configurada (~/.ssh/id_rsa ou ~/.ssh/id_ed25519)"
    echo "  - Host acessível: ping $VPS_HOST"
    echo "  - Variável VPS_HOST definida corretamente"
    exit 1
fi

# ── Função auxiliar ──────────────────────────────────────────────────────────
run_remote() {
    ssh -o ConnectTimeout=10 "$VPS_USER@$VPS_HOST" "$@" 2>/dev/null || echo "ERRO: comando falhou"
}

# ── Iniciar relatório ────────────────────────────────────────────────────────
{
    echo "# VPS Audit Report — $(date '+%Y-%m-%d %H:%M:%S')"
    echo "Target: $VPS_USER@$VPS_HOST"
    echo ""
} > "$AUDIT_REPORT"

# ── Sistema ───────────────────────────────────────────────────────────────────
echo -e "\n${CYAN}─── Sistema ───${NC}"
{
    echo "=== Sistema ==="
    echo "Uptime: $(run_remote 'uptime')"
    echo "OS: $(run_remote 'cat /etc/os-release 2>/dev/null | head -3')"
    echo "Kernel: $(run_remote 'uname -r')"
} >> "$AUDIT_REPORT"
echo -e "${GREEN}✓ Info do sistema coletada${NC}"

# ── Disco ─────────────────────────────────────────────────────────────────────
echo -e "\n${CYAN}─── Disco ───${NC}"
DISK="$(run_remote 'df -h /')"
echo "$DISK"
{
    echo "=== Disco ==="
    echo "$DISK"
} >> "$AUDIT_REPORT"

# ── RAM ───────────────────────────────────────────────────────────────────────
echo -e "\n${CYAN}─── Memória ───${NC}"
RAM="$(run_remote 'free -h')"
echo "$RAM"
{
    echo "=== Memória ==="
    echo "$RAM"
} >> "$AUDIT_REPORT"

# ── Docker ────────────────────────────────────────────────────────────────────
echo -e "\n${CYAN}─── Docker ───${NC}"
DOCKER_VER="$(run_remote 'docker --version 2>/dev/null || echo "Docker não instalado"')"
echo "  $DOCKER_VER"
{
    echo "=== Docker ==="
    echo "Versão: $DOCKER_VER"
    echo ""
    echo "Containers:"
    run_remote 'docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Image}}" 2>/dev/null || echo "Nenhum"'
    echo ""
    echo "Volumes:"
    run_remote 'docker volume ls 2>/dev/null || echo "Nenhum"'
    echo ""
    echo "Redes:"
    run_remote 'docker network ls 2>/dev/null || echo "Nenhuma"'
    echo ""
    echo "Imagens:"
    run_remote 'docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" 2>/dev/null || echo "Nenhuma"'
} >> "$AUDIT_REPORT"
echo -e "${GREEN}✓ Docker inspecionado${NC}"

# ── Docker Compose ────────────────────────────────────────────────────────────
echo -e "\n${CYAN}─── Docker Compose ───${NC}"
{
    echo "=== Docker Compose ==="
    echo "Projetos rodando:"
    run_remote 'docker compose ls 2>/dev/null || echo "Nenhum"'
} >> "$AUDIT_REPORT"

# ── Portas ────────────────────────────────────────────────────────────────────
echo -e "\n${CYAN}─── Portas ───${NC}"
{
    echo "=== Portas em escuta ==="
    run_remote 'ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null || echo "Não disponível"'
} >> "$AUDIT_REPORT"
echo -e "${GREEN}✓ Portas verificadas${NC}"

# ── Backups ───────────────────────────────────────────────────────────────────
echo -e "\n${CYAN}─── Backups ───${NC}"
{
    echo "=== Backups ==="
    run_remote 'ls -la /root/backups/ 2>/dev/null || ls -la /backups/ 2>/dev/null || echo "Nenhum diretório de backup encontrado"'
} >> "$AUDIT_REPORT"

# ── Logs recentes ─────────────────────────────────────────────────────────────
echo -e "\n${CYAN}─── Logs Docker recentes (últimas 20 linhas) ───${NC}"
{
    echo "=== Logs recentes ==="
    run_remote 'docker compose -f /root/bioplatform/docker-compose.yml logs --tail=20 2>/dev/null || docker compose logs --tail=20 2>/dev/null || echo "Não disponível"'
} >> "$AUDIT_REPORT"

# ── Resumo ────────────────────────────────────────────────────────────────────
echo -e "\n${CYAN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Auditoria concluída.${NC}"
echo -e "Relatório salvo em: ${CYAN}$AUDIT_REPORT${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"
