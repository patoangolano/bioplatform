"""Background worker for long-running bioinformatics analyses (BLAST, etc.)."""

import hashlib
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

from arq import func
from arq.connections import RedisSettings
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Add project root to path for mcp_servers imports
_this_file = Path(__file__).resolve()
for _ancestor in _this_file.parents:
    if (_ancestor / "mcp_servers").is_dir():
        if str(_ancestor) not in sys.path:
            sys.path.insert(0, str(_ancestor))
        break

from mcp_servers.adapters.blast import run_blast

logger = logging.getLogger(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+asyncpg://bio:changeme@postgres:5432/biodb")
REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379")


def _hash_content(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()


async def run_blast_analysis(
    ctx: dict,
    job_id: str,
    sequence_id: str,
    raw_sequence: str,
    program: str = "blastp",
    database: str = "swissprot",
    limit: int = 10,
) -> dict:
    """Run BLAST analysis as background job."""
    session_factory = ctx["session_factory"]

    async with session_factory() as db:
        # Update job to running
        await db.execute(
            update(JobTable)
            .where(JobTable.c.id == job_id)
            .values(status="running", started_at=datetime.now(timezone.utc))
        )
        await db.commit()

    try:
        # Run BLAST (can take 30s-5min)
        logger.info(f"Starting BLAST job {job_id}: {program}/{database}, seq len={len(raw_sequence)}")
        hits = await run_blast(raw_sequence, program, database, limit)
        hits_data = [h.model_dump() for h in hits]

        async with session_factory() as db:
            # Store result
            from sqlalchemy import text
            result_id = (await db.execute(text(
                "INSERT INTO results (job_id, result_type, data, confidence) "
                "VALUES (:job_id, 'blast_search', :data, :confidence) RETURNING id"
            ), {
                "job_id": job_id,
                "data": __import__("json").dumps({"hits": hits_data}),
                "confidence": hits[0].identity_pct / 100 if hits else None,
            })).scalar()

            # Provenance
            await db.execute(text(
                "INSERT INTO provenance_records "
                "(result_id, source_tool, tool_version, parameters, input_hash, output_hash, classification) "
                "VALUES (:result_id, 'ncbi_blast', '2.16', :params, :in_hash, :out_hash, 'observation')"
            ), {
                "result_id": str(result_id),
                "params": __import__("json").dumps({"program": program, "database": database, "limit": limit}),
                "in_hash": _hash_content(raw_sequence),
                "out_hash": _hash_content(str(hits_data)),
            })

            # Complete job
            await db.execute(
                update(JobTable)
                .where(JobTable.c.id == job_id)
                .values(status="completed", completed_at=datetime.now(timezone.utc))
            )
            await db.commit()

        logger.info(f"BLAST job {job_id} completed: {len(hits)} hits")
        return {"job_id": job_id, "hits": len(hits)}

    except Exception as e:
        logger.error(f"BLAST job {job_id} failed: {e}")
        async with session_factory() as db:
            await db.execute(
                update(JobTable)
                .where(JobTable.c.id == job_id)
                .values(status="failed", error_message=str(e)[:500])
            )
            await db.commit()
        raise


async def startup(ctx: dict) -> None:
    """Create DB engine on worker startup."""
    engine = create_async_engine(DATABASE_URL, pool_size=5)
    ctx["engine"] = engine
    ctx["session_factory"] = async_sessionmaker(engine, expire_on_commit=False)
    
    # Import table metadata for updates
    from sqlalchemy import MetaData, Table
    metadata = MetaData()
    global JobTable
    JobTable = Table("jobs", metadata, autoload_with=engine)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.reflect)
    JobTable = metadata.tables["jobs"]
    
    logger.info("bioplatform-worker started")


async def shutdown(ctx: dict) -> None:
    """Dispose DB engine on worker shutdown."""
    await ctx["engine"].dispose()
    logger.info("bioplatform-worker stopped")


class WorkerSettings:
    functions = [func(run_blast_analysis)]
    redis_settings = RedisSettings.from_dsn(REDIS_URL)
    on_startup = startup
    on_shutdown = shutdown
    max_jobs = 3
    job_timeout = 600  # 10 minutes max for BLAST
