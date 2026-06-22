"""Screening de biossegurança para sequências biológicas.

Verifica sequências submetidas contra padrões conhecidos de agentes perigosos,
toxinas regulamentadas e motifs patogênicos. Implementa classificação de risco
em quatro níveis (LOW, MEDIUM, HIGH, CRITICAL) conforme diretrizes CDC/USDA.
"""

import re

from .models import BiosecurityResult, RiskFlag, RiskLevel

# ─── Lista de organismos Select Agent (CDC/USDA) ─────────────────────────────
# Referência: Federal Select Agent Program — https://www.selectagents.gov/
# TODO: Manter sincronizado com lista oficial atualizada periodicamente
SELECT_AGENTS: list[str] = [
    "bacillus anthracis",
    "yersinia pestis",
    "francisella tularensis",
    "burkholderia mallei",
    "burkholderia pseudomallei",
    "brucella abortus",
    "brucella melitensis",
    "brucella suis",
    "clostridium botulinum",
    "coxiella burnetii",
    "ebola virus",
    "marburg virus",
    "variola major",
    "variola minor",
    "reconstructed 1918 influenza",
    "sars-cov",
    "monkeypox virus",
    "rickettsia prowazekii",
    "clostridium perfringens epsilon toxin",
    "staphylococcal enterotoxins",
    "abrin",
    "ricin",
    "botulinum neurotoxin",
    "t-2 toxin",
    "saxitoxin",
    "tetrodotoxin",
]

# ─── Motifs de risco conhecidos (simplificados) ──────────────────────────────
# Padrões representativos de regiões funcionais perigosas.
# TODO: Substituir por verificação contra NCBI BLAST / base curada de motifs
# TODO: Adicionar motifs de toxinas proteicas (shiga, diftérica, etc.)
HAZARDOUS_MOTIFS: list[dict] = [
    {
        "pattern": r"ATGGA[TC]GA[TC]CC[ATCG]{6,12}TGG",
        "name": "anthrax_pa_like",
        "description": "Motif similar ao antígeno protetor de B. anthracis",
        "severity": RiskLevel.CRITICAL,
    },
    {
        "pattern": r"ATGA[AG]A[CT][ATCG]{3}GA[TC]TT[TC]AA[AG]",
        "name": "botulinum_light_chain_like",
        "description": "Região catalítica similar à cadeia leve da toxina botulínica",
        "severity": RiskLevel.CRITICAL,
    },
    {
        "pattern": r"ATG[ATCG]{3}GGA[ATCG]{6}T[GT]T[ATCG]{3}AGC",
        "name": "ricin_a_chain_like",
        "description": "Motif similar à cadeia A da ricina (N-glicosilase)",
        "severity": RiskLevel.HIGH,
    },
    {
        "pattern": r"ATGAA[ATCG]{6,9}CACCAC[ATCG]{3}GAT",
        "name": "shiga_toxin_like",
        "description": "Região similar à toxina Shiga (rRNA N-glicosilase)",
        "severity": RiskLevel.HIGH,
    },
    {
        "pattern": r"ATG[ATCG]{3}GCT[ATCG]{3}TGC[ATCG]{3}TGC",
        "name": "cysteine_rich_toxin_scaffold",
        "description": "Scaffold rico em cisteína comum em toxinas de organismos venenosos",
        "severity": RiskLevel.MEDIUM,
    },
    {
        "pattern": r"AATAAA[ATCG]{10,30}AAAAA{5,}",
        "name": "polyadenylation_pathogenic",
        "description": "Sinal de poliadenilação com cauda poli-A (contexto viral)",
        "severity": RiskLevel.LOW,
    },
]

# ─── Padrões de oligonucleotídeos patogênicos ────────────────────────────────
# Regiões contíguas que indicam potencial de patogenicidade em ssDNA/ssRNA
PATHOGENIC_OLIGO_PATTERNS: list[dict] = [
    {
        "pattern": r"[ATCG]{20,}AAAAAAA[ATCG]{5,}",
        "name": "poly_a_tract_oligo",
        "description": "Trato poli-A longo em oligonucleotídeo — potencial de integração viral",
        "severity": RiskLevel.MEDIUM,
    },
    {
        "pattern": r"(CCCCC|GGGGG)[ATCG]{10,}(CCCCC|GGGGG)",
        "name": "g_quadruplex_flanked",
        "description": "Regiões G-quadruplex flanqueadas — associado a regulação patogênica",
        "severity": RiskLevel.MEDIUM,
    },
]


def _normalize_sequence(raw_sequence: str) -> str:
    """Remove espaços, quebras de linha e converte para maiúsculas."""
    return re.sub(r"\s+", "", raw_sequence).upper()


def _check_select_agent_organism(organism: str | None) -> RiskFlag | None:
    """Verifica se o organismo informado é um select agent."""
    if not organism:
        return None
    organism_lower = organism.lower().strip()
    for agent in SELECT_AGENTS:
        if agent in organism_lower or organism_lower in agent:
            return RiskFlag(
                code="SELECT_AGENT_ORGANISM",
                description=f"Organismo classificado como Select Agent: {agent}",
                severity=RiskLevel.CRITICAL,
                matched_pattern=agent,
            )
    return None


def _scan_hazardous_motifs(sequence: str) -> list[RiskFlag]:
    """Escaneia sequência contra motifs de risco conhecidos."""
    flags: list[RiskFlag] = []
    for motif in HAZARDOUS_MOTIFS:
        for match in re.finditer(motif["pattern"], sequence):
            flags.append(
                RiskFlag(
                    code=f"HAZARDOUS_MOTIF_{motif['name'].upper()}",
                    description=motif["description"],
                    severity=motif["severity"],
                    matched_pattern=match.group()[:50],  # Trunca para não expor sequência completa
                    position=(match.start(), match.end()),
                )
            )
    return flags


def _scan_pathogenic_oligos(sequence: str, sequence_type: str) -> list[RiskFlag]:
    """Verifica oligonucleotídeos single-stranded contra padrões patogênicos."""
    if sequence_type not in ("ssDNA", "ssRNA", "oligonucleotide"):
        return []
    flags: list[RiskFlag] = []
    for pattern_def in PATHOGENIC_OLIGO_PATTERNS:
        for match in re.finditer(pattern_def["pattern"], sequence):
            flags.append(
                RiskFlag(
                    code=f"PATHOGENIC_OLIGO_{pattern_def['name'].upper()}",
                    description=pattern_def["description"],
                    severity=pattern_def["severity"],
                    matched_pattern=match.group()[:50],
                    position=(match.start(), match.end()),
                )
            )
    return flags


def _determine_risk_level(flags: list[RiskFlag]) -> RiskLevel:
    """Determina o nível de risco global baseado nas flags individuais."""
    if not flags:
        return RiskLevel.LOW
    severities = [f.severity for f in flags]
    if RiskLevel.CRITICAL in severities:
        return RiskLevel.CRITICAL
    if RiskLevel.HIGH in severities:
        return RiskLevel.HIGH
    if RiskLevel.MEDIUM in severities:
        return RiskLevel.MEDIUM
    return RiskLevel.LOW


def _generate_recommendation(risk_level: RiskLevel, flags: list[RiskFlag]) -> str:
    """Gera recomendação textual baseada no nível de risco."""
    if risk_level == RiskLevel.CRITICAL:
        return (
            "BLOQUEADO — Sequência contém padrões associados a agentes de alta periculosidade "
            "ou organismos Select Agent. Submissão rejeitada. Contate o comitê de biossegurança "
            "institucional (IBC) para revisão manual."
        )
    if risk_level == RiskLevel.HIGH:
        return (
            "ALERTA — Sequência apresenta similaridade com regiões de toxinas regulamentadas. "
            "Salva com flag de proveniência para revisão. Recomenda-se verificação BLAST contra "
            "base NCBI antes de prosseguir com síntese ou expressão."
        )
    if risk_level == RiskLevel.MEDIUM:
        return (
            "ATENÇÃO — Padrões de risco moderado identificados. Prosseguir com cautela. "
            "Recomenda-se documentação adicional de finalidade e contexto experimental."
        )
    return "OK — Nenhum padrão de risco significativo identificado."


async def screen_sequence(
    raw_sequence: str,
    sequence_type: str,
    organism: str | None = None,
) -> BiosecurityResult:
    """Executa screening de biossegurança em uma sequência biológica.

    Args:
        raw_sequence: Sequência bruta (DNA, RNA ou proteína).
        sequence_type: Tipo da sequência (DNA, RNA, protein, ssDNA, ssRNA, oligonucleotide).
        organism: Organismo de origem (opcional).

    Returns:
        BiosecurityResult com nível de risco, flags e recomendação.
    """
    # TODO: Integrar com NCBI BLAST para verificação de similaridade em tempo real
    # TODO: Adicionar cache de resultados para sequências já verificadas
    # TODO: Implementar rate limiting para evitar abuso do endpoint

    sequence = _normalize_sequence(raw_sequence)
    flags: list[RiskFlag] = []

    # 1. Verifica organismo contra lista de Select Agents
    organism_flag = _check_select_agent_organism(organism)
    if organism_flag:
        flags.append(organism_flag)

    # 2. Escaneia motifs perigosos na sequência
    motif_flags = _scan_hazardous_motifs(sequence)
    flags.extend(motif_flags)

    # 3. Verifica padrões patogênicos em oligonucleotídeos
    oligo_flags = _scan_pathogenic_oligos(sequence, sequence_type)
    flags.extend(oligo_flags)

    # 4. Determina nível de risco consolidado
    risk_level = _determine_risk_level(flags)

    # 5. Gera recomendação
    recommendation = _generate_recommendation(risk_level, flags)

    return BiosecurityResult(
        risk_level=risk_level,
        flags=flags,
        recommendation=recommendation,
        organism_match=organism_flag.matched_pattern if organism_flag else None,
    )
