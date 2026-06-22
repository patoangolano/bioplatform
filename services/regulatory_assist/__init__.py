"""Serviço de assistência regulatória para documentação científica.

Gera esqueletos de documentos GxP (protocolos, SAP, TCLE) conforme
ICH E6(R2), ICH E9 e requisitos Anvisa (RDC 9/2015).
"""

from .generator import (
    generate_icf_skeleton,
    generate_protocol_skeleton,
    generate_sap_skeleton,
)
from .models import DocumentType, RegulatoryDocument, RegulatoryRequest, Section

__all__ = [
    "DocumentType",
    "RegulatoryDocument",
    "RegulatoryRequest",
    "Section",
    "generate_icf_skeleton",
    "generate_protocol_skeleton",
    "generate_sap_skeleton",
]
