"""Tarefa Prefect para compilação de relatório consolidado."""

from __future__ import annotations

from datetime import datetime, timezone

from prefect import task


@task(name="compile-report", timeout_seconds=30)
async def report_task(
    blast_hits: dict,
    annotations: dict,
    literature: list[dict],
) -> dict:
    """Compila relatório consolidado de análise proteica.

    Combina resultados de BLAST, anotação funcional e literatura
    num único documento estruturado com proveniência.

    Returns:
        Relatório consolidado com seções e proveniência.
    """
    report = {
        "title": "Relatório de Análise Proteica Abrangente",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sections": {
            "homology": {
                "title": "Homologia (BLAST)",
                "data": blast_hits,
                "classification": "observation",
            },
            "annotation": {
                "title": "Anotação Funcional",
                "data": annotations,
                "classification": "inference",
            },
            "literature": {
                "title": "Literatura Relacionada",
                "data": literature,
                "classification": "observation",
            },
        },
        "summary": {
            "total_hits": len(blast_hits.get("hits", [])),
            "annotated_proteins": len(annotations),
            "articles_found": len(literature),
        },
        "provenance": {
            "pipeline": "protein-comprehensive-report",
            "version": "0.1.0",
            "tools": ["NCBI BLAST", "UniProt", "InterPro", "AlphaFold", "STRING", "PubMed"],
        },
    }

    return report
