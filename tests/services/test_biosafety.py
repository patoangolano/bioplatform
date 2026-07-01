"""Tests for biosafety screening service."""

import pytest

from services.biosafety.models import RiskLevel
from services.biosafety.screener import screen_sequence


@pytest.mark.asyncio
async def test_screen_safe_sequence(sample_protein_sequence):
    """A generic signal peptide should be classified as LOW risk."""
    result = await screen_sequence(sample_protein_sequence, "protein")
    assert result.risk_level == RiskLevel.LOW
    assert len(result.flags) == 0


@pytest.mark.asyncio
async def test_screen_empty_sequence():
    """Empty sequence should return LOW with no flags."""
    result = await screen_sequence("", "protein")
    assert result.risk_level == RiskLevel.LOW


@pytest.mark.asyncio
async def test_screen_short_sequence():
    """Very short sequence should be handled gracefully."""
    result = await screen_sequence("MK", "protein")
    assert result.risk_level == RiskLevel.LOW


@pytest.mark.asyncio
async def test_screen_ricin_organism():
    """Sequence from 'ricinus communis' (ricin source) should be flagged."""
    result = await screen_sequence("MKTLLLTLVVVTIVCLDLGYT", "protein", organism="ricinus communis")
    # Ricin is in SELECT_AGENTS list
    assert result.risk_level in (RiskLevel.CRITICAL, RiskLevel.HIGH)
    assert len(result.flags) > 0


@pytest.mark.asyncio
async def test_screen_bacillus_anthracis():
    """Bacillus anthracis organism should be flagged CRITICAL."""
    result = await screen_sequence("MKTLLLTLVVVTIVCLDLGYT", "protein", organism="bacillus anthracis")
    assert result.risk_level == RiskLevel.CRITICAL


@pytest.mark.asyncio
async def test_screen_result_structure():
    """Result should have all required fields."""
    result = await screen_sequence("MKTLLLTLVVVTIVCLDLGYT", "protein")
    assert hasattr(result, "risk_level")
    assert hasattr(result, "flags")
    assert hasattr(result, "recommendation")
    assert hasattr(result, "screening_version")
    assert isinstance(result.risk_level, RiskLevel)
    assert isinstance(result.flags, list)


@pytest.mark.asyncio
async def test_screen_unknown_organism():
    """Unknown organism should not trigger false positives."""
    result = await screen_sequence("MKTLLLTLVVVTIVCLDLGYT", "protein", organism="unknownus bacterius")
    assert result.risk_level == RiskLevel.LOW
