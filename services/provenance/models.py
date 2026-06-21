"""Modelos de dados para o serviço de proveniência."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class ProvenanceRecord(BaseModel):
    """Registro de proveniência para rastreabilidade de resultados de análise."""

    id: UUID
    source_tool: str
    tool_version: str
    parameters: dict
    input_hash: str
    output_hash: str
    timestamp: datetime
    classification: Literal["observation", "inference", "hypothesis"]
