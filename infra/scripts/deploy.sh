#!/usr/bin/env bash
###############################################################################
# deploy.sh
#
# Purpose: Deploy the bioplatform application using Docker Compose.
# Supports pulling from git or deploying from a tarball. Copies environment
# config, builds images, starts services, and verifies health.
#
# Usage:
#   deploy.sh [OPTIONS]
#
# Options:
#   --tarball <path>    Deploy from a tarball instead of git pull
#   --build-only        Build images without starting services
#   -h, --help          Show this help message
###############################################################################
set -euo pipefail

# --- Configuration ------------------------------------------------------------
APP_DIR="/opt/bioplatform"
ENV_FILE="${APP_DIR}/.env"
DEPLOY_LOG="${APP_DIR}/deploy.log"
HEALTH_URL="http://localhost:8000/health"
HEALTH_RETRIES=30
HEALTH_INTERVAL=2

# --- Parse arguments ----------------------------------------------------------
TARBALL_PATH=""
BUILD_ONLY=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tarball)
      TARBALL_PATH="$2"
      shift 2
      ;;
    --build-only)
      BUILD_ONLY=true
      shift
      ;;
    -h|--help)
      head -20 "$0" | tail -15
      exit 0
      ;;
    *)
      echo "ERROR: Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

# --- Helper functions ---------------------------------------------------------
log() {
  local timestamp
  timestamp="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  echo "[${timestamp}] $*"
  echo "[${timestamp}] $*" >> "${DEPLOY_LOG}"
}

die() {
  log "FATAL: $*"
  exit 1
}

# --- Pre-flight checks --------------------------------------------------------
if [[ ! -d "${APP_DIR}" ]]; then
  die "Application directory ${APP_DIR} does not exist. Run bootstrap-vps.sh first."
fi

# Ensure deploy log exists
touch "${DEPLOY_LOG}"

log "=== Deploy started ==="

# --- Get the code -------------------------------------------------------------
if [[ -n "${TARBALL_PATH}" ]]; then
  log "Deploying from tarball: ${TARBALL_PATH}"
  [[ -f "${TARBALL_PATH}" ]] || die "Tarball not found: ${TARBALL_PATH}"
  tar -xzf "${TARBALL_PATH}" -C "${APP_DIR}"
else
  log "Pulling latest code from git..."
  cd "${APP_DIR}"
  if [[ -d ".git" ]]; then
    git fetch --all
    git reset --hard origin/main
    git clean -fd
  else
    die "No git repository found in ${APP_DIR} and no --tarball specified."
  fi
fi

cd "${APP_DIR}"

# --- Copy environment file ----------------------------------------------------
if [[ -f "${ENV_FILE}" ]]; then
  log "Copying .env from ${ENV_FILE}"
  cp "${ENV_FILE}" "${APP_DIR}/.env"
else
  log "WARNING: No .env file found at ${ENV_FILE}. Continuing without it."
fi

# --- Disable pre-installed Traefik (Hostinger Ubuntu+Docker template) ---------
if systemctl is-active --quiet traefik 2>/dev/null; then
  log "Disabling pre-installed Traefik (we use Caddy instead)..."
  systemctl stop traefik
  systemctl disable traefik
elif docker ps --format '{{.Names}}' | grep -qi traefik; then
  log "Stopping Traefik container..."
  docker stop $(docker ps --format '{{.Names}}' | grep -i traefik) || true
  docker rm $(docker ps -a --format '{{.Names}}' | grep -i traefik) || true
fi

# --- Run database migrations --------------------------------------------------
log "Running database migrations..."
docker compose up -d postgres
sleep 5  # wait for postgres healthcheck
for migration in "${APP_DIR}"/infra/db/migrations/*.sql; do
  if [[ -f "${migration}" ]]; then
    log "  Applying: $(basename "${migration}")"
    docker compose exec -T postgres psql -U "${POSTGRES_USER:-bio}" -d "${POSTGRES_DB:-biodb}" < "${migration}" 2>&1 || true
  fi
done

# --- Build images -------------------------------------------------------------
log "Building Docker images..."
docker compose build

if [[ "${BUILD_ONLY}" == "true" ]]; then
  log "Build-only mode: skipping service start."
  log "=== Deploy completed (build-only) ==="
  exit 0
fi

# --- Start services -----------------------------------------------------------
log "Starting services..."
docker compose up -d

# --- Health check with retries ------------------------------------------------
log "Waiting for health check at ${HEALTH_URL}..."

healthy=false
for i in $(seq 1 "${HEALTH_RETRIES}"); do
  if curl -sf "${HEALTH_URL}" > /dev/null 2>&1; then
    healthy=true
    break
  fi
  echo "   Attempt ${i}/${HEALTH_RETRIES}: not ready yet, retrying in ${HEALTH_INTERVAL}s..."
  sleep "${HEALTH_INTERVAL}"
done

if [[ "${healthy}" == "true" ]]; then
  log "Health check passed."
else
  log "ERROR: Health check failed after ${HEALTH_RETRIES} attempts."
  log "Dumping container logs for debugging..."
  docker compose logs --tail=50 >> "${DEPLOY_LOG}" 2>&1
  die "Deployment health check failed. Check ${DEPLOY_LOG} for details."
fi

# --- Print status -------------------------------------------------------------
echo ""
echo "============================================================================="
echo "  DEPLOYMENT SUCCESSFUL"
echo "============================================================================="
echo ""
docker compose ps
echo ""
log "=== Deploy completed successfully ==="
