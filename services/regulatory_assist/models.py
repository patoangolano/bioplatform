"""Modelos de dados para o serviço de assistência regulatória GxP."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    """Tipos de documentos regulatórios suportados."""

    PROTOCOL = "protocol"
    ICF = "icf"  # Termo de Consentimento Livre e Esclarecido
    SAP = "sap"  # Plano de Análise Estatística
    IB = "ib"  # Brochura do Investigador


class Section(BaseModel):
    """Seção de um documento regulatório."""

    number: str = Field(..., description="Número da seção (ex: '1', '1.1')")
    title: str = Field(..., description="Título da seção")
    content: str = Field(..., description="Conteúdo da seção")
    references: list[str] = Field(default_factory=list, description="Referências normativas")


class RegulatoryRequest(BaseModel):
    """Request para geração de documento regulatório."""

    document_type: DocumentType
    study_title: str = Field(..., min_length=5, max_length=500)
    therapeutic_area: str = Field(..., min_length=2, max_length=200)
    phase: str = Field(..., pattern="^(I|II|III|IV|I/II|II/III)$")
    sponsor: str = Field(..., min_length=2, max_length=300)
    principal_investigator: str = Field(..., min_length=2, max_length=300)
    endpoints: list[str] = Field(default_factory=list, description="Desfechos do estudo")
    population_criteria: str = Field(
        ..., min_length=10, description="Critérios de inclusão/exclusão da população"
    )


class RegulatoryDocument(BaseModel):
    """Documento regulatório gerado."""

    document_type: DocumentType
    title: str
    sections: list[Section] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    version: str = "0.1-draft"
