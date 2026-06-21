"""AlphaFold Protein Structure Database REST API adapter.

Uses the AlphaFold DB API:
- Prediction: https://alphafold.ebi.ac.uk/api/prediction/{qualifier}
- pLDDT: Available in prediction metadata
- 3D structure: CIF/PDB files available via URL

No authentication required. Generous rate limits.

AlphaFold DB provides AI-predicted protein structures for UniProt entries.
"""

from __future__ import annotations

from typing import Optional

import httpx

from mcp_servers.models import AlphaFoldPrediction

_BASE = "https://alphafold.ebi.ac.uk/api"
_TIMEOUT = 15.0


async def get_structure_prediction(
    uniprot_id: str,
) -> Optional[AlphaFoldPrediction]:
    """Get AlphaFold structure prediction for a UniProt accession.
    
    Args:
        uniprot_id: UniProt accession (e.g. "P38398" for BRCA1)
    
    Returns:
        AlphaFoldPrediction with structure metadata and URLs, or None if not found
    """
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        resp = await client.get(f"{_BASE}/prediction/{uniprot_id}")
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        data = resp.json()

    if not data:
        return None

    # API returns a list; take first entry
    entry = data[0] if isinstance(data, list) else data

    return AlphaFoldPrediction(
        entry_id=entry.get("entryId", ""),
        uniprot_id=entry.get("uniprotAccession", uniprot_id),
        uniprot_description=entry.get("uniprotDescription", ""),
        gene_name=entry.get("gene", ""),
        organism=entry.get("organismScientificName", ""),
        plddt_confidence=entry.get("globalMetricValue", 0.0),
        model_url=entry.get("cifUrl", ""),
        pdb_url=entry.get("pdbUrl", ""),
        pae_image_url=entry.get("paeImageUrl", ""),
        model_page_url=f"https://alphafold.ebi.ac.uk/entry/{entry.get('entryId', '')}",
        sequence_length=entry.get("uniprotEnd", 0) - entry.get("uniprotStart", 0) + 1,
    )


async def search_alphafold_by_name(
    query: str,
    limit: int = 5,
) -> list[AlphaFoldPrediction]:
    """Search AlphaFold DB via UniProt text search, then fetch predictions.
    
    This is a convenience function that first searches UniProt for matching
    proteins, then fetches AlphaFold predictions for each result.
    
    Args:
        query: Protein name or description text
        limit: Max results to return
    
    Returns:
        List of AlphaFold predictions for matching proteins
    """
    # First search UniProt to get accessions
    from mcp_servers.adapters.uniprot import search_uniprot

    uniprot_results = await search_uniprot(query, limit=limit)
    
    predictions: list[AlphaFoldPrediction] = []
    for entry in uniprot_results:
        pred = await get_structure_prediction(entry.accession)
        if pred:
            predictions.append(pred)
    
    return predictions
