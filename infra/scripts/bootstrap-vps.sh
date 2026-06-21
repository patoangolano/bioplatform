#!/usr/bin/env bash
###############################################################################
# bootstrap-vps.sh
#
# Purpose: Provision a fresh Ubuntu VPS for the bioplatform stack.
# Installs Docker Engine + Compose plugin, Caddy, creates the bioplatform
# service user, sets up directories, configures UFW firewall, and enables
# unattended security upgrades.
#
# Requirements: Must be run as root on Ubuntu 22.04+ (tested on 22.04/24.04).
###############################################################################
set -euo pipefail

# --- Root check ---------------------------------------------------------------
if [[ "$(id -u)" -ne 0 ]]; then
  echo "ERROR: This script must be run as root." >&2
  exit 1
fi

echo "==> Starting bioplatform VPS bootstrap..."

# --- Update system packages ---------------------------------------------------
echo "==> Updating system packages..."
apt-get update -y
apt-get upgrade -y

# --- Install prerequisites ----------------------------------------------------
echo "==> Installing prerequisites..."
apt-get install -y \
  ca-certificates \
  curl \
  gnupg \
  lsb-release \
  software-properties-common \
  apt-transport-https

# --- Install Docker Engine (official repo) ------------------------------------
echo "==> Installing Docker Engine..."

# Remove old/conflicting packages
for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do
  apt-get remove -y "$pkg" 2>/dev/null || true
done

# Add Docker GPG key
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

# Add Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update -y
apt-get install -y \
  docker-ce \
  docker-ce-cli \
  containerd.io \
  docker-buildx-plugin \
  docker-compose-plugin

# Enable and start Docker
systemctl enable docker
systemctl start docker

echo "   Docker version: $(docker --version)"
echo "   Compose version: $(docker compose version)"

# --- Disable pre-installed Traefik (Hostinger Docker template) ----------------
echo "==> Checking for pre-installed Traefik..."
if systemctl is-active --quiet traefik 2>/dev/null; then
  echo "   Stopping and disabling Traefik systemd service..."
  systemctl stop traefik
  systemctl disable traefik
  echo "   Traefik disabled (bioplatform uses Caddy instead)."
elif docker ps --format '{{.Names}}' 2>/dev/null | grep -qi traefik; then
  echo "   Stopping Traefik Docker container..."
  docker stop $(docker ps --format '{{.Names}}' | grep -i traefik) || true
  docker rm $(docker ps -a --format '{{.Names}}' | grep -i traefik) || true
  echo "   Traefik container removed."
else
  echo "   No Traefik found, skipping."
fi

# --- Install Caddy (official repo) --------------------------------------------
echo "==> Installing Caddy..."

curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | \
  gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg

curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | \
  tee /etc/apt/sources.list.d/caddy-stable.list > /dev/null

apt-get update -y
apt-get install -y caddy

echo "   Caddy version: $(caddy version)"

# --- Create bioplatform user --------------------------------------------------
echo "==> Creating bioplatform user..."

if id "bioplatform" &>/dev/null; then
  echo "   User 'bioplatform' already exists, skipping creation."
else
  useradd --system --create-home --shell /bin/bash bioplatform
  echo "   User 'bioplatform' created."
fi

# Add to docker group so it can manage containers without sudo
usermod -aG docker bioplatform

# --- Create application directories ------------------------------------------
echo "==> Creating application directories..."
mkdir -p /opt/bioplatform/backups
chown -R bioplatform:bioplatform /opt/bioplatform

# --- Configure UFW firewall ---------------------------------------------------
echo "==> Configuring UFW firewall..."

apt-get install -y ufw

# Reset to defaults (deny incoming, allow outgoing)
ufw default deny incoming
ufw default allow outgoing

# Allow required ports
ufw allow 22/tcp comment "SSH"
ufw allow 80/tcp comment "HTTP"
ufw allow 443/tcp comment "HTTPS"

# Enable firewall (non-interactive)
ufw --force enable
echo "   UFW status:"
ufw status verbose

# --- Enable unattended upgrades -----------------------------------------------
echo "==> Enabling unattended security upgrades..."

apt-get install -y unattended-upgrades
dpkg-reconfigure -plow unattended-upgrades

# Ensure security updates are enabled in the config
cat > /etc/apt/apt.conf.d/20auto-upgrades << 'EOF'
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
APT::Periodic::AutocleanInterval "7";
EOF

systemctl enable unattended-upgrades
systemctl start unattended-upgrades

# --- Summary ------------------------------------------------------------------
echo ""
echo "============================================================================="
echo "  BIOPLATFORM VPS BOOTSTRAP COMPLETE"
echo "============================================================================="
echo ""
echo "  Installed:"
echo "    - Docker Engine:    $(docker --version)"
echo "    - Docker Compose:   $(docker compose version)"
echo "    - Caddy:            $(caddy version)"
echo ""
echo "  Configuration:"
echo "    - User:             bioplatform (docker group member)"
echo "    - App directory:    /opt/bioplatform"
echo "    - Backups:          /opt/bioplatform/backups"
echo "    - Firewall:         UFW enabled (SSH/HTTP/HTTPS only)"
echo "    - Auto-upgrades:    Enabled (security patches)"
echo ""
echo "  Next steps:"
echo "    1. Copy your .env file to /opt/bioplatform/.env"
echo "    2. Deploy with: sudo -u bioplatform bash infra/scripts/deploy.sh"
echo "============================================================================="
