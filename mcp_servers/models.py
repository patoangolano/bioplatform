"""Normalized response models for bio_science_mcp adapters."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


# ─── PubMed ───────────────────────────────────────────────────────────────────


class PubMedArticleSummary(BaseModel):
    """Compact representation of a PubMed search result."""

    pmid: str
    title: str
    authors: list[str] = Field(default_factory=list)
    journal: str = ""
    pub_date: str = ""


class PubMedAbstract(BaseModel):
    """Full abstract retrieved by PMID."""

    pmid: str
    title: str
    abstract: str
    authors: list[str] = Field(default_factory=list)
    journal: str = ""
    pub_date: str = ""


# ─── UniProt ──────────────────────────────────────────────────────────────────


class UniProtEntrySummary(BaseModel):
    """Compact representation of a UniProt search result."""

    accession: str
    protein_name: str = ""
    gene_name: str = ""
    organism: str = ""
    reviewed: bool = False


class UniProtEntryDetail(BaseModel):
    """Detailed UniProt entry retrieved by accession."""

    accession: str
    protein_name: str = ""
    gene_name: str = ""
    organism: str = ""
    sequence_length: int = 0
    function_description: str = ""
    reviewed: bool = False
    keywords: list[str] = Field(default_factory=list)
    go_terms: list[str] = Field(default_factory=list)


# ─── InterPro ─────────────────────────────────────────────────────────────────


class InterProEntrySummary(BaseModel):
    """Compact representation of an InterPro search result."""

    accession: str
    name: str = ""
    entry_type: str = ""  # e.g. "Family", "Domain", "Homologous_superfamily"
    source_database: str = ""
    description: Optional[str] = None
