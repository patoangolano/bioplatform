"""Pydantic schemas for API request/response validation."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


# ─── Sequence ─────────────────────────────────


class SequenceCreate(BaseModel):
    """Request body para submissão de sequência."""

    description: str | None = Field(None, max_length=500)
    sequence_type: Literal["DNA", "RNA", "protein"]
    raw_sequence: str = Field(..., min_length=1)
    organism: str | None = None
    analyze: bool = Field(
        default=True,
        description="Se True, executa análise inline (UniProt/PubMed) na submissão.",
    )


class SequenceResponse(BaseModel):
    """Resposta com dados da sequência armazenada."""

    id: UUID
    description: str | None
    sequence_type: str
    raw_sequence: str
    organism: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Analysis ─────────────────────────────────


class AnalysisResult(BaseModel):
    """Resultado de análise inline."""

    uniprot_matches: list[dict] = Field(default_factory=list)
    literature: list[dict] = Field(default_factory=list)
    interpro_domains: list[dict] = Field(default_factory=list)
    alphafold_structures: list[dict] = Field(default_factory=list)
    string_interactions: list[dict] = Field(default_factory=list)
    provenance: list[dict] = Field(default_factory=list)


class SequenceWithAnalysis(BaseModel):
    """Resposta combinada: sequência + análise inline."""

    sequence: SequenceResponse
    analysis: AnalysisResult | None = None
