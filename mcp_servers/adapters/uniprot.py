"""UniProt REST API adapter.

Uses the UniProt REST API (2022+ version).
- Search: https://rest.uniprot.org/uniprotkb/search
- Entry:  https://rest.uniprot.org/uniprotkb/{accession}

No authentication required.
"""

from __future__ import annotations

import httpx

from mcp_servers.models import UniProtEntryDetail, UniProtEntrySummary

_BASE = "https://rest.uniprot.org/uniprotkb"
_TIMEOUT = 15.0


async def search_uniprot(
    query: str,
    limit: int = 5,
) -> list[UniProtEntrySummary]:
    """Text search against UniProt. Returns compact summaries."""
    params = {
        "query": query,
        "format": "json",
        "size": str(min(limit, 25)),
    }

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        resp = await client.get(f"{_BASE}/search", params=params)
        resp.raise_for_status()
        data = resp.json()

    results: list[UniProtEntrySummary] = []
    for entry in data.get("results", []):
        accession = entry.get("primaryAccession", "")
        protein = entry.get("proteinDescription", {})
        rec_name = protein.get("recommendedName", {})
        full_name = rec_name.get("fullName", {}).get("value", "")
        if not full_name:
            sub_names = protein.get("submissionNames", [])
            if sub_names:
                full_name = sub_names[0].get("fullName", {}).get("value", "")

        genes = entry.get("genes", [])
        gene_name = ""
        if genes:
            gene_name = genes[0].get("geneName", {}).get("value", "")

        organism = entry.get("organism", {}).get("scientificName", "")
        reviewed = entry.get("entryType", "") == "UniProtKB reviewed (Swiss-Prot)"

        results.append(
            UniProtEntrySummary(
                accession=accession,
                protein_name=full_name,
                gene_name=gene_name,
                organism=organism,
                reviewed=reviewed,
            )
        )
    return results


async def get_uniprot_entry(accession: str) -> UniProtEntryDetail:
    """Retrieve detailed entry by accession."""
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        resp = await client.get(f"{_BASE}/{accession}.json")
        resp.raise_for_status()
        entry = resp.json()

    protein = entry.get("proteinDescription", {})
    rec_name = protein.get("recommendedName", {})
    full_name = rec_name.get("fullName", {}).get("value", "")
    if not full_name:
        sub_names = protein.get("submissionNames", [])
        if sub_names:
            full_name = sub_names[0].get("fullName", {}).get("value", "")

    genes = entry.get("genes", [])
    gene_name = genes[0].get("geneName", {}).get("value", "") if genes else ""

    organism = entry.get("organism", {}).get("scientificName", "")
    reviewed = entry.get("entryType", "") == "UniProtKB reviewed (Swiss-Prot)"

    seq = entry.get("sequence", {})
    seq_length = seq.get("length", 0)

    function_desc = ""
    for comment in entry.get("comments", []):
        if comment.get("commentType") == "FUNCTION":
            texts = comment.get("texts", [])
            if texts:
                function_desc = texts[0].get("value", "")
                break

    keywords = [kw.get("name", "") for kw in entry.get("keywords", [])]

    go_terms: list[str] = []
    for xref in entry.get("uniProtKBCrossReferences", []):
        if xref.get("database") == "GO":
            props = xref.get("properties", [])
            for p in props:
                if p.get("key") == "GoTerm":
                    go_terms.append(p.get("value", ""))

    return UniProtEntryDetail(
        accession=accession,
        protein_name=full_name,
        gene_name=gene_name,
        organism=organism,
        sequence_length=seq_length,
        function_description=function_desc,
        reviewed=reviewed,
        keywords=keywords[:15],
        go_terms=go_terms[:15],
    )
