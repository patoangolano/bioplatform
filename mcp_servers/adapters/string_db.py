"""STRING database REST API adapter.

Uses the STRING API v12.0:
- Network: https://string-db.org/api/json/network
- Interaction partners: https://string-db.org/api/json/interaction_partners
- Functional enrichment: https://string-db.org/api/json/enrichment

No authentication required. Rate limit: 1 request/second.
Caller identity required via 'caller_identity' parameter.

STRING provides protein-protein interaction networks.
"""

from __future__ import annotations

import httpx

from mcp_servers.models import StringInteraction, StringEnrichment

_BASE = "https://string-db.org/api/json"
_TIMEOUT = 20.0
_CALLER_ID = "bioplatform_quackai"


async def get_interaction_partners(
    protein: str,
    species: int = 9606,
    limit: int = 10,
    required_score: int = 400,
) -> list[StringInteraction]:
    """Get protein-protein interaction partners from STRING.
    
    Args:
        protein: Protein name or identifier (e.g. "BRCA1", "TP53")
        species: NCBI taxonomy ID (9606 = Homo sapiens)
        limit: Max number of interaction partners
        required_score: Minimum combined score (0-1000, 400=medium confidence)
    
    Returns:
        List of interaction partners with scores
    """
    params = {
        "identifiers": protein,
        "species": str(species),
        "limit": str(min(limit, 50)),
        "required_score": str(required_score),
        "caller_identity": _CALLER_ID,
    }

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        resp = await client.get(f"{_BASE}/interaction_partners", params=params)
        resp.raise_for_status()
        data = resp.json()

    interactions: list[StringInteraction] = []
    for item in data:
        interactions.append(StringInteraction(
            protein_a=item.get("preferredName_A", ""),
            protein_b=item.get("preferredName_B", ""),
            combined_score=item.get("score", 0.0),
            experimental_score=item.get("escore", 0.0),
            database_score=item.get("dscore", 0.0),
            textmining_score=item.get("tscore", 0.0),
            coexpression_score=item.get("ascore", 0.0),
        ))

    return interactions


async def get_functional_enrichment(
    proteins: list[str],
    species: int = 9606,
) -> list[StringEnrichment]:
    """Get functional enrichment analysis for a set of proteins.
    
    Args:
        proteins: List of protein names/identifiers
        species: NCBI taxonomy ID
    
    Returns:
        List of enriched GO terms / KEGG pathways
    """
    params = {
        "identifiers": "%0d".join(proteins),
        "species": str(species),
        "caller_identity": _CALLER_ID,
    }

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        resp = await client.get(f"{_BASE}/enrichment", params=params)
        resp.raise_for_status()
        data = resp.json()

    enrichments: list[StringEnrichment] = []
    for item in data[:20]:  # Cap at 20 most significant
        enrichments.append(StringEnrichment(
            category=item.get("category", ""),
            term=item.get("term", ""),
            description=item.get("description", ""),
            p_value=item.get("p_value", 1.0),
            fdr=item.get("fdr", 1.0),
            number_of_genes=item.get("number_of_genes", 0),
            input_genes=item.get("inputGenes", "").split(",") if item.get("inputGenes") else [],
        ))

    return enrichments


async def get_network_image_url(
    proteins: list[str],
    species: int = 9606,
) -> str:
    """Get URL for the STRING network visualization image.
    
    Args:
        proteins: List of protein names
        species: NCBI taxonomy ID
    
    Returns:
        URL to the network image (SVG)
    """
    identifiers = "%0d".join(proteins)
    return (
        f"https://string-db.org/api/svg/network"
        f"?identifiers={identifiers}"
        f"&species={species}"
        f"&caller_identity={_CALLER_ID}"
    )
