#!/usr/bin/env bash
# ============================================================================
# 04_setup_bioinfo_tools.sh — Instala ferramentas bioinformáticas opcionais
#
# BLAST+, HMMER, Clustal Omega, etc. — via conda/mamba ou apt.
# Estas são ferramentas de linha de comando, não dependências Python.
# ============================================================================
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}=== 04: Ferramentas bioinformáticas (opcionais) ===${NC}"
echo -e "${YELLOW}Estas ferramentas são opcionais para desenvolvimento local.${NC}"
echo -e "${YELLOW}Os adaptadores MCP usam APIs remotas (NCBI, UniProt, etc.) e não requerem estas.${NC}"
echo ""

OS="$(uname -s 2>/dev/null || echo 'Unknown')"

# ── Verificar conda/mamba ─────────────────────────────────────────────────────
if command -v conda &>/dev/null; then
    echo -e "${GREEN}✓ conda disponível${NC}"
    CONDA="conda"
elif command -v mamba &>/dev/null; then
    echo -e "${GREEN}✓ mamba disponível${NC}"
    CONDA="mamba"
else
    echo -e "${YELLOW}⚠ conda/mamba não encontrado — pulando instalação de ferramentas bioinfo${NC}"
    echo "  Para instalar: https://github.com/conda-forge/miniforge"
    exit 0
fi

# ── Instalar via conda ────────────────────────────────────────────────────────
echo -e "  Instalando ferramentas bioinformáticas via $CONDA..."

install_if_missing() {
    local pkg="$1"
    if ! command -v "$pkg" &>/dev/null; then
        echo -e "  Instalando $pkg..."
        $CONDA install -y -c bioconda "$pkg" 2>/dev/null && \
            echo -e "  ${GREEN}✓ $pkg${NC}" || \
            echo -e "  ${YELLOW}⚠ $pkg falhou${NC}"
    else
        echo -e "  ${GREEN}✓ $pkg já instalado${NC}"
    fi
}

# Ferramentas comuns de bioinformática
for tool in blast hmmer clustalo mafft samtools seqtk; do
    install_if_missing "$tool"
done

echo -e "\n${GREEN}✓ Setup bioinfo concluído.${NC}"
