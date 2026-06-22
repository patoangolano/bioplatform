"""Tarefa Prefect para busca BLAST."""

from __future__ import annotations

import sys
from pathlib import Path

from prefect import task

# Resolve project root for adapter imports
_root = Path(__file__).resolve().parents[3]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from mcp_servers.adapters.blast import run_blast


@task(name="blast-search", retries=2, retry_delay_seconds=30, timeout_seconds=300)
async def blast_task(
    sequence: str,
    program: str = "blastp",
    database: str = "swissprot",
) -> dict:
    """Submete sequência ao NCBI BLAST e aguarda resultados.

    Returns:
        Dict com hits do BLAST incluindo accessions, scores e e-values.
    """
    result = await run_blast(
        sequence=sequence,
        program=program,
        database=database,
    )
    return result
