"""Modelos de dados para o serviço de biossegurança e screening."""

from enum import Enum

from pydantic import BaseModel


class RiskLevel(str, Enum):
    """Nível de risco biossegurança."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskFlag(BaseModel):
    """Flag individual de risco identificada no screening."""

    code: str
    description: str
    severity: RiskLevel
    matched_pattern: str | None = None
    position: tuple[int, int] | None = None  # (start, end) na sequência


class BiosecurityResult(BaseModel):
    """Resultado consolidado do screening de biossegurança."""

    risk_level: RiskLevel
    flags: list[RiskFlag]
    recommendation: str
    organism_match: str | None = None
    screening_version: str = "0.1.0"
