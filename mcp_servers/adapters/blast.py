"""NCBI BLAST REST API adapter.

Uses the NCBI BLAST URL API:
- Submit: https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi (PUT)
- Poll:   https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD=Get&RID=xxx
- Results: JSON format

No authentication required but NCBI_API_KEY increases rate limits.
BLAST is asynchronous — submit, poll until done, then retrieve results.

Rate limits: 1 request/second without key, 10/second with key.
"""

from __future__ import annotations

import asyncio
import os
from typing import Optional

import httpx

from mcp_servers.models import BlastHit

_BASE = "https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi"
_TIMEOUT = 30.0
_MAX_POLL_ATTEMPTS = 30
_POLL_INTERVAL = 10  # seconds


def _api_key_params() -> dict[str, str]:
    key = os.environ.get("NCBI_API_KEY")
    return {"api_key": key} if key else {}


async def submit_blast(
    sequence: str,
    program: str = "blastp",
    database: str = "nr",
    limit: int = 5,
) -> Optional[str]:
    """Submit a BLAST search and return the Request ID (RID).
    
    Args:
        sequence: Raw amino acid or nucleotide sequence
        program: blastn, blastp, blastx, tblastn, tblastx
        database: nr, swissprot, pdb, etc.
        limit: Max alignments to return
    
    Returns:
        RID string if submission succeeded, None otherwise
    """
    params = {
        "CMD": "Put",
        "PROGRAM": program,
        "DATABASE": database,
        "QUERY": sequence,
        "FORMAT_TYPE": "JSON2",
        "HITLIST_SIZE": str(min(limit, 20)),
        **_api_key_params(),
    }

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        resp = await client.post(_BASE, data=params)
        resp.raise_for_status()
        text = resp.text

    # Extract RID from response
    for line in text.split("\n"):
        if line.strip().startswith("RID ="):
            return line.split("=")[1].strip()
    return None


async def poll_blast(rid: str) -> bool:
    """Poll BLAST for job completion. Returns True when ready."""
    params = {
        "CMD": "Get",
        "FORMAT_OBJECT": "SearchInfo",
        "RID": rid,
        **_api_key_params(),
    }

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        resp = await client.get(_BASE, params=params)
        resp.raise_for_status()
        text = resp.text

    if "Status=WAITING" in text:
        return False
    if "Status=READY" in text:
        return True
    # FAILED or UNKNOWN
    return True  # Will handle error in get_results


async def get_blast_results(rid: str) -> list[BlastHit]:
    """Retrieve BLAST results for a completed job."""
    params = {
        "CMD": "Get",
        "FORMAT_TYPE": "JSON2",
        "RID": rid,
        **_api_key_params(),
    }

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        resp = await client.get(_BASE, params=params)
        resp.raise_for_status()
        data = resp.json()

    hits: list[BlastHit] = []
    try:
        search = data.get("BlastOutput2", [{}])[0]
        report = search.get("report", {})
        results = report.get("results", {})
        search_hits = results.get("search", {}).get("hits", [])

        for hit in search_hits[:20]:
            description = hit.get("description", [{}])[0]
            hsps = hit.get("hsps", [{}])[0] if hit.get("hsps") else {}

            hits.append(BlastHit(
                accession=description.get("accession", ""),
                title=description.get("title", ""),
                scientific_name=description.get("sciname", ""),
                evalue=hsps.get("evalue", 0.0),
                bit_score=hsps.get("bit_score", 0.0),
                identity_pct=round(
                    (hsps.get("identity", 0) / max(hsps.get("align_len", 1), 1)) * 100, 1
                ) if hsps else 0.0,
                align_length=hsps.get("align_len", 0),
            ))
    except (KeyError, IndexError, TypeError):
        pass

    return hits


async def run_blast(
    sequence: str,
    program: str = "blastp",
    database: str = "swissprot",
    limit: int = 5,
) -> list[BlastHit]:
    """Full BLAST workflow: submit, poll, retrieve.
    
    This is the main entry point. Submits the sequence, polls until
    completion (or timeout), and returns parsed hits.
    
    Note: BLAST can take 30s-5min depending on database size.
    For production, consider submitting and checking later via job system.
    """
    rid = await submit_blast(sequence, program, database, limit)
    if not rid:
        return []

    # Poll until ready
    for _ in range(_MAX_POLL_ATTEMPTS):
        ready = await poll_blast(rid)
        if ready:
            break
        await asyncio.sleep(_POLL_INTERVAL)
    else:
        return []  # Timeout

    return await get_blast_results(rid)
