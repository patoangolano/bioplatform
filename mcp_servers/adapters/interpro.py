"""InterPro REST API adapter.

Uses the InterPro 7 API:
- Search: https://www.ebi.ac.uk/interpro/api/entry/interpro?search={query}

No authentication required. Rate limits are generous for programmatic access.

Limitations:
- The InterPro search endpoint does full-text search across entry names and
  descriptions. It does not support complex boolean queries.
- Results are paginated; this adapter fetches only the first page.
"""

from __future__ import annotations

import httpx

from mcp_servers.cache import cached
from mcp_servers.models import InterProEntrySummary

_BASE = "https://www.ebi.ac.uk/interpro/api"
_TIMEOUT = 15.0


@cached(ttl=86400, prefix="interpro", model=InterProEntrySummary, is_list=True)
async def search_interpro(
    query: str,
    limit: int = 5,
) -> list[InterProEntrySummary]:
    """Search InterPro entries by text query."""
    params = {
        "search": query,
        "page_size": str(min(limit, 20)),
    }

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        resp = await client.get(f"{_BASE}/entry/interpro", params=params)
        resp.raise_for_status()
        data = resp.json()

    results: list[InterProEntrySummary] = []
    for item in data.get("results", []):
        metadata = item.get("metadata", {})
        accession = metadata.get("accession", "")
        name = metadata.get("name", "")
        entry_type = metadata.get("type", "")
        source_db = metadata.get("source_database", "interpro")

        desc_list = metadata.get("description", [])
        description = ""
        if desc_list and isinstance(desc_list, list):
            for block in desc_list:
                if isinstance(block, str):
                    description = block
                    break
                elif isinstance(block, list):
                    for para in block:
                        if isinstance(para, dict) and para.get("text"):
                            description = para["text"][:200]
                            break
                if description:
                    break

        results.append(
            InterProEntrySummary(
                accession=accession,
                name=name,
                entry_type=entry_type,
                source_database=source_db,
                description=description or None,
            )
        )
    return results
