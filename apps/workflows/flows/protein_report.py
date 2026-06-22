"""Flow Prefect: Relatório abrangente de proteína.

Pipeline multi-step:
  BLAST → Anotação (UniProt+InterPro+AlphaFold+STRING) → Literatura → Relatório

Usa os mesmos adapters MCP (agora com cache Redis) para evitar
chamadas duplicadas a APIs externas.
"""

from __future__ import annotations

import sys
from pathlib import Path

from prefect import flow

_root = Path(__file__).resolve().parents[3]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from apps.workflows.tasks.blast_task import blast_task
from apps.workflows.tasks.annotation_task import annotation_task
from apps.workflows.tasks.literature_task import literature_task
from apps.workflows.tasks.report_task import report_task


@flow(name="protein-comprehensive-report", retries=1, retry_delay_seconds=60)
async def protein_report_flow(
    sequence: str,
    sequence_type: str = "protein",
    organism: str | None = None,
    database: str = "swissprot",
) -> dict:
    """Pipeline completo de análise proteica.

    Args:
        sequence: Sequência de aminoácidos.
        sequence_type: Tipo da sequência (protein/DNA/RNA).
        organism: Organismo de origem (opcional).
        database: Database BLAST (default: swissprot).

    Returns:
        Relatório consolidado com homologia, anotação, literatura e proveniência.
    """
    program = "blastp" if sequence_type == "protein" else "blastn"

    # Step 1: BLAST homology search
    blast_results = await blast_task(
        sequence=sequence,
        program=program,
        database=database,
    )

    # Step 2: Functional annotation (parallel with literature)
    annotations = await annotation_task(
        blast_hits=blast_results,
        organism=organism,
    )

    # Step 3: Literature search
    literature = await literature_task(
        blast_hits=blast_results,
        organism=organism,
    )

    # Step 4: Compile comprehensive report
    report = await report_task(
        blast_hits=blast_results,
        annotations=annotations,
        literature=literature,
    )

    return report
