"""Shared fixtures for bioplatform tests."""

import sys
from pathlib import Path

import pytest

# Add project root and apps/api to path so imports work
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "apps" / "api"))


@pytest.fixture
def sample_protein_sequence() -> str:
    """A simple, safe protein sequence for testing."""
    return "MKTLLLTLVVVTIVCLDLGYT"  # Generic signal peptide


@pytest.fixture
def sample_dna_sequence() -> str:
    """A simple DNA sequence for testing."""
    return "ATGAAAACATTATTATTAACATTAGTTGTAGTTACTATAGTTTGTTTAGATTTAGGTTATACA"


@pytest.fixture
def sample_uniprot_response() -> dict:
    """Mock UniProt entry response."""
    return {
        "accession": "P04637",
        "protein_name": "Cellular tumor antigen p53",
        "organism": "Homo sapiens",
        "sequence": "MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPGP",
        "length": 393,
    }


@pytest.fixture
def sample_pubmed_response() -> list[dict]:
    """Mock PubMed search response."""
    return [
        {
            "pmid": "12345678",
            "title": "p53 tumor suppressor: a review",
            "authors": ["Smith J", "Doe A"],
            "journal": "Nature Reviews Cancer",
            "year": "2023",
        }
    ]
