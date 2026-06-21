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


# ─── AlphaFold ────────────────────────────────────────────────────────────────


class AlphaFoldPrediction(BaseModel):
    """AlphaFold structure prediction metadata."""

    entry_id: str
    uniprot_id: str
    uniprot_description: str = ""
    gene_name: str = ""
    organism: str = ""
    plddt_confidence: float = 0.0
    model_url: str = ""
    pdb_url: str = ""
    pae_image_url: str = ""
    model_page_url: str = ""
    sequence_length: int = 0


# ─── BLAST ────────────────────────────────────────────────────────────────────


class BlastHit(BaseModel):
    """A single BLAST alignment hit."""

    accession: str
    title: str = ""
    scientific_name: str = ""
    evalue: float = 0.0
    bit_score: float = 0.0
    identity_pct: float = 0.0
    align_length: int = 0


# ─── STRING ───────────────────────────────────────────────────────────────────


class StringInteraction(BaseModel):
    """A protein-protein interaction from STRING."""

    protein_a: str
    protein_b: str
    combined_score: float = 0.0
    experimental_score: float = 0.0
    database_score: float = 0.0
    textmining_score: float = 0.0
    coexpression_score: float = 0.0


class StringEnrichment(BaseModel):
    """A functional enrichment term from STRING."""

    category: str = ""
    term: str = ""
    description: str = ""
    p_value: float = 1.0
    fdr: float = 1.0
    number_of_genes: int = 0
    input_genes: list[str] = Field(default_factory=list)
