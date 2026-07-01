"""Tests for Pydantic schemas."""

import pytest
from pydantic import ValidationError

from apps.api.schemas import SequenceCreate


def test_sequence_create_valid_protein():
    """Valid protein sequence should pass validation."""
    seq = SequenceCreate(
        sequence_type="protein",
        raw_sequence="MKTLLLTLVVVTIVCLDLGYT",
        description="Test protein",
        organism="Homo sapiens",
    )
    assert seq.sequence_type == "protein"
    assert seq.raw_sequence == "MKTLLLTLVVVTIVCLDLGYT"
    assert seq.analyze is True  # default


def test_sequence_create_valid_dna():
    """Valid DNA sequence should pass validation."""
    seq = SequenceCreate(
        sequence_type="DNA",
        raw_sequence="ATGAAATTTGGG",
    )
    assert seq.sequence_type == "DNA"


def test_sequence_create_empty_sequence():
    """Empty sequence should raise validation error."""
    with pytest.raises(ValidationError):
        SequenceCreate(
            sequence_type="protein",
            raw_sequence="",
        )


def test_sequence_create_invalid_type():
    """Invalid sequence type should raise validation error."""
    with pytest.raises(ValidationError):
        SequenceCreate(
            sequence_type="carbohydrate",  # type: ignore
            raw_sequence="MKTLLL",
        )


def test_sequence_create_without_analysis():
    """analyze=False should be accepted."""
    seq = SequenceCreate(
        sequence_type="protein",
        raw_sequence="MKTLLL",
        analyze=False,
    )
    assert seq.analyze is False


def test_sequence_create_description_too_long():
    """Description > 500 chars should raise validation error."""
    with pytest.raises(ValidationError):
        SequenceCreate(
            sequence_type="protein",
            raw_sequence="MKTLLL",
            description="X" * 501,
        )
