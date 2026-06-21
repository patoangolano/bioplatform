"""BLAST background job router.

Submits BLAST searches as async jobs and retrieves results.
"""

import logging
from uuid import UUID

from arq import create_pool
from arq.connections import RedisSettings
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth import get_current_user
from config import settings
from database import get_db
from models import Job, Result, User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/blast", tags=["blast"])


class BlastSubmit(BaseModel):
    sequence_id: UUID
    program: str = Field(default="blastp", pattern="^(blastn|blastp|blastx|tblastn|tblastx)$")
    database: str = Field(default="swissprot")
    limit: int = Field(default=10, ge=1, le=50)


class BlastJobResponse(BaseModel):
    job_id: UUID
    status: str
    message: str


class BlastResultResponse(BaseModel):
    job_id: UUID
    status: str
    started_at: str | None = None
    completed_at: str | None = None
    error_message: str | None = None
    results: dict | None = None


@router.post("/submit", response_model=BlastJobResponse, status_code=status.HTTP_202_ACCEPTED)
async def submit_blast(
    payload: BlastSubmit,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Submit a BLAST search job (runs in background)."""
    from models import Sequence

    # Verify sequence exists
    result = await db.execute(select(Sequence).where(Sequence.id == payload.sequence_id))
    seq = result.scalar_one_or_none()
    if not seq:
        raise HTTPException(status_code=404, detail="Sequence not found")

    # Create job record
    job = Job(
        sequence_id=payload.sequence_id,
        job_type="blast_search",
        status="pending",
        parameters={
            "program": payload.program,
            "database": payload.database,
            "limit": payload.limit,
        },
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)

    # Enqueue to worker
    try:
        redis = await create_pool(RedisSettings.from_dsn(settings.REDIS_URL))
        await redis.enqueue_job(
            "run_blast_analysis",
            str(job.id),
            str(payload.sequence_id),
            seq.raw_sequence,
            payload.program,
            payload.database,
            payload.limit,
        )
        await redis.close()
    except Exception as e:
        logger.error(f"Failed to enqueue BLAST job: {e}")
        job.status = "failed"
        job.error_message = f"Queue error: {e}"
        await db.commit()
        raise HTTPException(status_code=503, detail="Worker queue unavailable")

    return BlastJobResponse(
        job_id=job.id,
        status="pending",
        message="BLAST job submitted. Poll GET /blast/jobs/{job_id} for results.",
    )


@router.get("/jobs/{job_id}", response_model=BlastResultResponse)
async def get_blast_job(
    job_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get BLAST job status and results."""
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    response = BlastResultResponse(
        job_id=job.id,
        status=job.status,
        started_at=job.started_at.isoformat() if job.started_at else None,
        completed_at=job.completed_at.isoformat() if job.completed_at else None,
        error_message=job.error_message,
    )

    if job.status == "completed":
        res = await db.execute(select(Result).where(Result.job_id == job.id))
        blast_result = res.scalar_one_or_none()
        if blast_result:
            response.results = blast_result.data

    return response
