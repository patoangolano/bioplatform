#!/usr/bin/env bash
# ============================================================================
# 01_install_base_wsl.sh — Instala pacotes base no WSL/Ubuntu
#
# Só executa em WSL/Linux. No macOS usa Homebrew.
# Windows nativo (Git Bash) pula com aviso.
# ============================================================================
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}=== 01: Pacotes base do sistema ===${NC}"

OS="$(uname -s 2>/dev/null || echo 'Unknown')"

case "$OS" in
    Linux)
        echo -e "${GREEN}Linux detectado — instalando via apt${NC}"
        sudo apt-get update -qq
        sudo apt-get install -y -qq \
            curl \
            wget \
            git \
            build-essential \
            libssl-dev \
            zlib1g-dev \
            libbz2-dev \
            libreadline-dev \
            libsqlite3-dev \
            libncursesw5-dev \
            xz-utils \
            tk-dev \
            libxml2-dev \
            libxmlsec1-dev \
            libffi-dev \
            liblzma-dev \
            jq \
            tree \
            htop \
            net-tools
        echo -e "${GREEN}✓ Pacotes base instalados.${NC}"
        ;;
    Darwin)
        echo -e "${GREEN}macOS detectado — instalando via Homebrew${NC}"
        if ! command -v brew &>/dev/null; then
            echo -e "${YELLOW}Homebrew não encontrado. Instalando...${NC}"
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install curl git jq tree htop
        echo -e "${GREEN}✓ Pacotes base instalados.${NC}"
        ;;
    MINGW*|MSYS*|CYGWIN*)
        echo -e "${YELLOW}⚠ Windows Git Bash detectado — pulando instalação de pacotes.${NC}"
        echo "  Use WSL2 para ambiente Linux completo ou instale manualmente."
        ;;
    *)
        echo -e "${YELLOW}⚠ SO não reconhecido ($OS) — pulando.${NC}"
        ;;
esac
