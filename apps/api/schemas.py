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


# ─── Auth ─────────────────────────────────────


class UserCreate(BaseModel):
    """Request body para registro de usuário."""

    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str | None = None


class UserRead(BaseModel):
    """Resposta com dados do usuário (sem senha)."""

    id: UUID
    email: str
    full_name: str | None
    is_active: bool
    is_admin: bool = False
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"


# ─── Admin ───────────────────────────────────


class AdminUserUpdate(BaseModel):
    """Request body para atualização de usuário pelo admin."""

    is_active: bool | None = None
    is_admin: bool | None = None
    full_name: str | None = None


class PlatformStats(BaseModel):
    """Estatísticas gerais da plataforma."""

    total_users: int
    total_sequences: int
    total_jobs: int
    active_jobs: int
    completed_jobs: int
    failed_jobs: int
