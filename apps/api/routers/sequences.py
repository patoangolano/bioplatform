"""Router de sequências biológicas com análise inline.

Submete sequência ao banco e opcionalmente executa análise em tempo real
usando os adapters de UniProt e PubMed.
"""

import hashlib
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Job, ProvenanceRecord, Result, Sequence
from schemas import AnalysisResult, SequenceCreate, SequenceResponse, SequenceWithAnalysis

# Add project root to path so we can import mcp_servers adapters
# Works both locally (parents[3] = bioplatform/) and in Docker (parents[1] = /app/)
_this_file = Path(__file__).resolve()
for _ancestor in _this_file.parents:
    if (_ancestor / "mcp_servers").is_dir():
        if str(_ancestor) not in sys.path:
            sys.path.insert(0, str(_ancestor))
        break

from mcp_servers.adapters.uniprot import get_uniprot_entry, search_uniprot
from mcp_servers.adapters.pubmed import search_pubmed

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sequences", tags=["sequences"])


def _hash_content(content: str) -> str:
    """SHA-256 hash for provenance tracking."""
    return hashlib.sha256(content.encode()).hexdigest()


async def _run_inline_analysis(
    sequence: Sequence, db: AsyncSession
) -> AnalysisResult:
    """Executa análise inline: busca UniProt + literatura PubMed."""
    uniprot_matches = []
    literature = []
    provenance_records = []

    # Monta query de busca baseada no tipo de sequência
    search_query = sequence.description or sequence.organism or "protein"
    if sequence.organism and sequence.description:
        search_query = f"{sequence.description} AND {sequence.organism}"

    # ─── UniProt search ───────────────────────────
    try:
        uniprot_results = await search_uniprot(search_query, limit=3)
        for entry in uniprot_results:
            detail = await get_uniprot_entry(entry.accession)
            uniprot_matches.append(detail.model_dump())

        # Cria job + result + proveniência
        job = await _create_job(sequence.id, "uniprot_search", db)
        result = Result(
            job_id=job.id,
            result_type="uniprot_search",
            data={"matches": uniprot_matches},
        )
        db.add(result)
        await db.flush()

        prov = ProvenanceRecord(
            result_id=result.id,
            source_tool="uniprot_rest_api",
            tool_version="2024.1",
            parameters={"query": search_query, "limit": 3},
            input_hash=_hash_content(search_query),
            output_hash=_hash_content(str(uniprot_matches)),
            classification="observation",
        )
        db.add(prov)
        provenance_records.append(prov)
    except Exception as e:
        logger.warning(f"UniProt analysis failed: {e}")

    # ─── PubMed search ────────────────────────────
    try:
        pubmed_query = f"{sequence.description or ''} {sequence.organism or ''}".strip()
        if not pubmed_query:
            pubmed_query = "bioinformatics"
        pubmed_results = await search_pubmed(pubmed_query, max_results=5)
        literature = [article.model_dump() for article in pubmed_results]

        job = await _create_job(sequence.id, "pubmed_search", db)
        result = Result(
            job_id=job.id,
            result_type="pubmed_search",
            data={"articles": literature},
        )
        db.add(result)
        await db.flush()

        prov = ProvenanceRecord(
            result_id=result.id,
            source_tool="ncbi_eutils",
            tool_version="2.0",
            parameters={"query": pubmed_query, "max_results": 5},
            input_hash=_hash_content(pubmed_query),
            output_hash=_hash_content(str(literature)),
            classification="observation",
        )
        db.add(prov)
        provenance_records.append(prov)
    except Exception as e:
        logger.warning(f"PubMed analysis failed: {e}")

    await db.commit()

    return AnalysisResult(
        uniprot_matches=uniprot_matches,
        literature=literature,
        provenance=[
            {
                "tool": p.source_tool,
                "classification": p.classification,
                "input_hash": p.input_hash[:12] + "...",
            }
            for p in provenance_records
        ],
    )


async def _create_job(sequence_id: UUID, job_type: str, db: AsyncSession) -> Job:
    """Cria um job de análise associado à sequência."""
    job = Job(
        sequence_id=sequence_id,
        job_type=job_type,
        status="completed",
        completed_at=datetime.now(timezone.utc),
    )
    db.add(job)
    await db.flush()
    return job

@router.post("/", response_model=SequenceWithAnalysis, status_code=201)
async def submit_sequence(
    payload: SequenceCreate,
    db: AsyncSession = Depends(get_db),
):
    """Submete uma sequência biológica e opcionalmente executa análise inline.

    A análise consulta UniProt e PubMed em tempo real, armazena resultados
    e registra proveniência de cada operação.
    """
    # Persiste sequência
    seq = Sequence(
        description=payload.description,
        sequence_type=payload.sequence_type,
        raw_sequence=payload.raw_sequence,
        organism=payload.organism,
    )
    db.add(seq)
    await db.flush()

    # Análise inline se solicitada
    analysis = None
    if payload.analyze:
        analysis = await _run_inline_analysis(seq, db)

    await db.commit()
    await db.refresh(seq)

    return SequenceWithAnalysis(
        sequence=SequenceResponse.model_validate(seq),
        analysis=analysis,
    )


@router.get("/{sequence_id}", response_model=SequenceResponse)
async def get_sequence(
    sequence_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Recupera uma sequência pelo ID."""
    result = await db.execute(select(Sequence).where(Sequence.id == sequence_id))
    seq = result.scalar_one_or_none()
    if not seq:
        raise HTTPException(status_code=404, detail="Sequence not found")
    return SequenceResponse.model_validate(seq)


@router.get("/", response_model=list[SequenceResponse])
async def list_sequences(
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """Lista sequências com paginação simples."""
    result = await db.execute(
        select(Sequence).order_by(Sequence.created_at.desc()).limit(limit).offset(offset)
    )
    sequences = result.scalars().all()
    return [SequenceResponse.model_validate(s) for s in sequences]