#!/usr/bin/env bash
###############################################################################
# rollback.sh
#
# Purpose: Roll back the bioplatform to a previous Docker image version.
# Lists available tagged images, accepts a version argument, swaps to that
# version, and verifies service health.
#
# Usage:
#   rollback.sh [OPTIONS] [TAG]
#
# Options:
#   --list              List available bioplatform image tags and exit
#   -h, --help          Show this help message
#
# Examples:
#   rollback.sh --list
#   rollback.sh v1.2.3
###############################################################################
set -euo pipefail

# --- Configuration ------------------------------------------------------------
APP_DIR="/opt/bioplatform"
DEPLOY_LOG="${APP_DIR}/deploy.log"
HEALTH_URL="http://localhost:8000/health"
HEALTH_RETRIES=30
HEALTH_INTERVAL=2
IMAGE_FILTER="bioplatform"

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

list_images() {
  echo "Available bioplatform images:"
  echo ""
  docker images --filter "reference=*${IMAGE_FILTER}*" \
    --format "table {{.Repository}}\t{{.Tag}}\t{{.CreatedAt}}\t{{.Size}}"
  echo ""
}

# --- Parse arguments ----------------------------------------------------------
TARGET_TAG=""
LIST_ONLY=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --list)
      LIST_ONLY=true
      shift
      ;;
    -h|--help)
      head -22 "$0" | tail -17
      exit 0
      ;;
    -*)
      echo "ERROR: Unknown option: $1" >&2
      exit 1
      ;;
    *)
      TARGET_TAG="$1"
      shift
      ;;
  esac
done

# --- Ensure deploy log exists -------------------------------------------------
touch "${DEPLOY_LOG}"

# --- List mode ----------------------------------------------------------------
if [[ "${LIST_ONLY}" == "true" ]]; then
  list_images
  exit 0
fi

# --- Validate target tag ------------------------------------------------------
if [[ -z "${TARGET_TAG}" ]]; then
  echo "ERROR: No target tag specified." >&2
  echo ""
  list_images
  echo "Usage: rollback.sh <TAG>"
  exit 1
fi

# Verify the tag exists locally
if ! docker images --filter "reference=*${IMAGE_FILTER}*:${TARGET_TAG}" \
  --format "{{.Tag}}" | grep -q "^${TARGET_TAG}$"; then
  echo "ERROR: Tag '${TARGET_TAG}' not found in local images." >&2
  echo ""
  list_images
  die "Rollback aborted: image tag not found."
fi

log "=== Rollback started: target tag '${TARGET_TAG}' ==="

# --- Stop current services ----------------------------------------------------
log "Stopping current services..."
cd "${APP_DIR}"
docker compose down --timeout 30

# --- Start services with target tag -------------------------------------------
log "Starting services with tag '${TARGET_TAG}'..."
export IMAGE_TAG="${TARGET_TAG}"
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
  log "Health check passed after rollback to '${TARGET_TAG}'."
else
  log "ERROR: Health check failed after rollback to '${TARGET_TAG}'."
  log "Container status:"
  docker compose ps >> "${DEPLOY_LOG}" 2>&1
  die "Rollback health check failed. Manual intervention required."
fi

# --- Print status -------------------------------------------------------------
echo ""
echo "============================================================================="
echo "  ROLLBACK SUCCESSFUL"
echo "============================================================================="
echo "  Rolled back to tag: ${TARGET_TAG}"
echo ""
docker compose ps
echo ""
log "=== Rollback completed successfully: tag '${TARGET_TAG}' ==="
