"""Router de assistência regulatória para geração de documentos GxP.

Endpoints para geração automatizada de esqueletos documentais
conforme ICH E6(R2) e requisitos Anvisa (RDC 9/2015).
"""

import logging
import sys
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status

# Ajusta path para imports — encontra a raiz do projeto (onde services/ está)
_this_file = Path(__file__).resolve()
for _ancestor in _this_file.parents:
    if (_ancestor / "services").is_dir():
        if str(_ancestor) not in sys.path:
            sys.path.insert(0, str(_ancestor))
        break

from auth import get_current_user
from models import User

from services.regulatory_assist.generator import (
    generate_icf_skeleton,
    generate_protocol_skeleton,
    generate_sap_skeleton,
)
from services.regulatory_assist.models import (
    DocumentType,
    RegulatoryDocument,
    RegulatoryRequest,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/regulatory", tags=["regulatory"])


_TEMPLATES = [
    {
        "document_type": DocumentType.PROTOCOL.value,
        "name": "Protocolo Clínico",
        "description": "Esqueleto de protocolo conforme ICH E6(R2) e RDC 9/2015",
        "sections_count": 10,
    },
    {
        "document_type": DocumentType.SAP.value,
        "name": "Plano de Análise Estatística (SAP)",
        "description": "Esqueleto de SAP conforme ICH E9",
        "sections_count": 6,
    },
    {
        "document_type": DocumentType.ICF.value,
        "name": "Termo de Consentimento Livre e Esclarecido (TCLE)",
        "description": "Esqueleto de TCLE conforme Res. CNS 466/2012 e RDC 9/2015",
        "sections_count": 8,
    },
    {
        "document_type": DocumentType.IB.value,
        "name": "Brochura do Investigador (IB)",
        "description": "Em desenvolvimento — disponível em versão futura",
        "sections_count": 0,
    },
]


@router.get("/templates")
async def list_templates(
    current_user: User = Depends(get_current_user),
):
    """Lista templates de documentos regulatórios disponíveis."""
    return {"templates": _TEMPLATES}


@router.post("/generate", response_model=RegulatoryDocument, status_code=status.HTTP_201_CREATED)
async def generate_document(
    request: RegulatoryRequest,
    current_user: User = Depends(get_current_user),
):
    """Gera esqueleto de documento regulatório a partir dos parâmetros informados."""
    generators = {
        DocumentType.PROTOCOL: generate_protocol_skeleton,
        DocumentType.SAP: generate_sap_skeleton,
        DocumentType.ICF: generate_icf_skeleton,
    }

    generator_fn = generators.get(request.document_type)
    if generator_fn is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de documento '{request.document_type.value}' ainda não suportado para geração.",
        )

    logger.info(
        "Gerando documento %s para estudo '%s' (usuário: %s)",
        request.document_type.value,
        request.study_title,
        current_user.email,
    )

    document = generator_fn(request)
    return document
