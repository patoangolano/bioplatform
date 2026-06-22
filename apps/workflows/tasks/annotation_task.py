"""Tarefa Prefect para anotação funcional via UniProt + InterPro."""

from __future__ import annotations

import sys
from pathlib import Path

from prefect import task

_root = Path(__file__).resolve().parents[3]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from mcp_servers.adapters.uniprot import get_uniprot_entry
from mcp_servers.adapters.interpro import search_interpro
from mcp_servers.adapters.alphafold import get_structure_prediction
from mcp_servers.adapters.string_db import get_interaction_partners


@task(name="annotate-protein", retries=1, retry_delay_seconds=10, timeout_seconds=120)
async def annotation_task(blast_hits: dict, organism: str | None = None) -> dict:
    """Busca anotação funcional para os top hits do BLAST.

    Consulta UniProt, InterPro, AlphaFold e STRING para cada hit.

    Returns:
        Dict com anotações consolidadas por accession.
    """
    annotations = {}
    hits = blast_hits.get("hits", [])[:5]  # Top 5

    for hit in hits:
        accession = hit.get("accession", "")
        if not accession:
            continue

        entry = await get_uniprot_entry(accession)
        domains = await search_interpro(entry.protein_name if entry else accession, limit=3)
        structure = await get_structure_prediction(accession)
        interactions = await get_interaction_partners(
            entry.gene_name if entry and entry.gene_name else accession,
            limit=5,
        )

        annotations[accession] = {
            "uniprot": entry.model_dump() if entry else None,
            "domains": [d.model_dump() for d in domains],
            "structure": structure.model_dump() if structure else None,
            "interactions": [i.model_dump() for i in interactions],
        }

    return annotations
