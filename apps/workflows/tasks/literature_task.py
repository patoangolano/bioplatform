"""Tarefa Prefect para busca de literatura via PubMed."""

from __future__ import annotations

import sys
from pathlib import Path

from prefect import task

_root = Path(__file__).resolve().parents[3]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from mcp_servers.adapters.pubmed import search_pubmed


@task(name="literature-search", retries=1, retry_delay_seconds=10, timeout_seconds=60)
async def literature_task(blast_hits: dict, organism: str | None = None) -> list[dict]:
    """Busca literatura relevante para os hits do BLAST.

    Estratégia: combina nome da proteína + organismo como query PubMed.

    Returns:
        Lista de artigos relevantes encontrados.
    """
    articles = []
    hits = blast_hits.get("hits", [])[:3]

    for hit in hits:
        name = hit.get("description", hit.get("accession", ""))
        query = f"{name} {organism}" if organism else name
        results = await search_pubmed(query, max_results=3)
        articles.extend([a.model_dump() for a in results])

    # Deduplica por PMID
    seen = set()
    unique = []
    for article in articles:
        pmid = article.get("pmid")
        if pmid and pmid not in seen:
            seen.add(pmid)
            unique.append(article)

    return unique[:10]
