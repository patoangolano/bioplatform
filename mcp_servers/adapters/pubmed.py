"""PubMed / NCBI E-utilities adapter.

Uses the NCBI E-utilities REST API (no API key required for low-volume use,
but rate-limited to ~3 req/s without one). Set the NCBI_API_KEY environment
variable to increase throughput to 10 req/s.

References:
- https://www.ncbi.nlm.nih.gov/books/NBK25497/
- https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
"""

from __future__ import annotations

import os
from defusedxml import ElementTree

import httpx

from mcp_servers.models import PubMedAbstract, PubMedArticleSummary

_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
_TIMEOUT = 15.0  # seconds


def _api_key_params() -> dict[str, str]:
    key = os.environ.get("NCBI_API_KEY")
    return {"api_key": key} if key else {}


async def search_pubmed(
    query: str,
    max_results: int = 5,
) -> list[PubMedArticleSummary]:
    """Search PubMed and return compact article summaries."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": str(min(max_results, 50)),
        "retmode": "json",
        **_api_key_params(),
    }

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        resp = await client.get(f"{_BASE}/esearch.fcgi", params=params)
        resp.raise_for_status()
        data = resp.json()
        id_list: list[str] = data.get("esearchresult", {}).get("idlist", [])

        if not id_list:
            return []

        summary_params = {
            "db": "pubmed",
            "id": ",".join(id_list),
            "retmode": "json",
            **_api_key_params(),
        }
        resp = await client.get(f"{_BASE}/esummary.fcgi", params=summary_params)
        resp.raise_for_status()
        summary_data = resp.json().get("result", {})

    articles: list[PubMedArticleSummary] = []
    for pmid in id_list:
        entry = summary_data.get(pmid)
        if not entry:
            continue
        authors = [a.get("name", "") for a in entry.get("authors", [])]
        articles.append(
            PubMedArticleSummary(
                pmid=pmid,
                title=entry.get("title", ""),
                authors=authors[:5],
                journal=entry.get("fulljournalname", ""),
                pub_date=entry.get("pubdate", ""),
            )
        )
    return articles


async def get_pubmed_abstract(pmid: str) -> PubMedAbstract:
    """Retrieve full abstract for a given PMID via efetch (XML)."""
    params = {
        "db": "pubmed",
        "id": pmid,
        "rettype": "abstract",
        "retmode": "xml",
        **_api_key_params(),
    }

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        resp = await client.get(f"{_BASE}/efetch.fcgi", params=params)
        resp.raise_for_status()

    root = ElementTree.fromstring(resp.text)
    article_el = root.find(".//PubmedArticle")
    if article_el is None:
        return PubMedAbstract(
            pmid=pmid, title="", abstract="No article found for this PMID."
        )

    title_el = article_el.find(".//ArticleTitle")
    title = title_el.text if title_el is not None and title_el.text else ""

    abstract_parts: list[str] = []
    for abs_text in article_el.findall(".//AbstractText"):
        label = abs_text.get("Label", "")
        text = abs_text.text or ""
        abstract_parts.append(f"{label}: {text}" if label else text)
    abstract = "\n".join(abstract_parts) if abstract_parts else "Abstract not available."

    authors: list[str] = []
    for author_el in article_el.findall(".//Author"):
        last = author_el.findtext("LastName", "")
        first = author_el.findtext("ForeName", "")
        if last:
            authors.append(f"{last} {first}".strip())

    journal = article_el.findtext(".//Journal/Title", "")

    pub_date_el = article_el.find(".//PubDate")
    pub_date = ""
    if pub_date_el is not None:
        year = pub_date_el.findtext("Year", "")
        month = pub_date_el.findtext("Month", "")
        pub_date = f"{year} {month}".strip()

    return PubMedAbstract(
        pmid=pmid,
        title=title,
        abstract=abstract,
        authors=authors[:10],
        journal=journal,
        pub_date=pub_date,
    )
