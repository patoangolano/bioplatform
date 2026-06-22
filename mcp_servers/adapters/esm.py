"""ESM3/Evo protein language model adapter (EvolutionaryScale).

Interfaces with the ESM3 API for protein structure prediction,
mutation effect prediction, variant generation, and embeddings.

Configuration:
- ESM_API_URL: Base URL for the ESM3 API (default: https://api.evolutionaryscale.ai)
- ESM_API_KEY: API key for authentication

TODO: Endpoint paths and response schemas are placeholders based on the
expected contract. Update when the actual ESM3 API documentation becomes
available from EvolutionaryScale.
"""

from __future__ import annotations

import hashlib
import os
from datetime import datetime, timezone
from typing import Any

import httpx

# Configuration
_BASE_URL = os.environ.get("ESM_API_URL", "https://api.evolutionaryscale.ai")
_API_KEY = os.environ.get("ESM_API_KEY", "")
_TIMEOUT_PREDICT = 120.0  # Structure/mutation predictions can be slow
_TIMEOUT_DEFAULT = 30.0
_VERSION = "esm3-placeholder-v0.1"


def _input_hash(sequence: str, **extras: Any) -> str:
    """Generate deterministic hash of inputs for provenance tracking."""
    content = sequence + "".join(f"{k}={v}" for k, v in sorted(extras.items()))
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def _provenance(method: str, sequence: str, **extras: Any) -> dict[str, str]:
    """Build provenance metadata block."""
    return {
        "tool": "esm3",
        "version": _VERSION,
        "method": method,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input_hash": _input_hash(sequence, **extras),
    }


class ESMAdapter:
    """Async adapter for the ESM3 protein language model API.

    Usage:
        adapter = ESMAdapter()
        result = await adapter.predict_structure("MKTLLILAVL...")
    """

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
    ) -> None:
        self.base_url = (base_url or _BASE_URL).rstrip("/")
        self.api_key = api_key or _API_KEY

    def _headers(self) -> dict[str, str]:
        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def _request(
        self,
        method: str,
        path: str,
        payload: dict[str, Any],
        timeout: float = _TIMEOUT_DEFAULT,
    ) -> dict[str, Any]:
        """Execute HTTP request against the ESM3 API.

        Raises:
            httpx.HTTPStatusError: On 4xx/5xx responses
            httpx.TimeoutException: If request exceeds timeout
        """
        url = f"{self.base_url}{path}"
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.request(
                method,
                url,
                json=payload,
                headers=self._headers(),
            )
            resp.raise_for_status()
            return resp.json()

    async def predict_structure(self, sequence: str) -> dict[str, Any]:
        """Submit sequence for 3D structure prediction.

        Args:
            sequence: Amino acid sequence (single-letter code)

        Returns:
            Dict with predicted structure data and provenance metadata.

        TODO: Update endpoint path and response parsing when ESM3
        structure prediction API is finalized.
        """
        payload = {"sequence": sequence}

        # TODO: Replace placeholder endpoint with actual ESM3 path
        result = await self._request(
            "POST",
            "/v1/structure/predict",
            payload,
            timeout=_TIMEOUT_PREDICT,
        )

        result["provenance"] = _provenance("predict_structure", sequence)
        return result

    async def predict_mutations(
        self, sequence: str, positions: list[int]
    ) -> dict[str, Any]:
        """Predict mutation effects at specified positions.

        Args:
            sequence: Wild-type amino acid sequence
            positions: 1-indexed residue positions to evaluate

        Returns:
            Dict with per-position mutation scores and provenance metadata.

        TODO: Update endpoint path and response parsing when ESM3
        mutation scoring API is finalized.
        """
        payload = {
            "sequence": sequence,
            "positions": positions,
        }

        # TODO: Replace placeholder endpoint with actual ESM3 path
        result = await self._request(
            "POST",
            "/v1/mutations/predict",
            payload,
            timeout=_TIMEOUT_PREDICT,
        )

        result["provenance"] = _provenance(
            "predict_mutations",
            sequence,
            positions=str(positions),
        )
        return result

    async def generate_variant(
        self, sequence: str, constraints: dict[str, Any]
    ) -> dict[str, Any]:
        """Generate optimized protein variants given constraints.

        Args:
            sequence: Template amino acid sequence
            constraints: Optimization constraints, e.g.:
                - fixed_positions: list[int] — residues to keep unchanged
                - target_property: str — property to optimize
                - num_variants: int — number of variants to generate

        Returns:
            Dict with generated variant sequences and provenance metadata.

        TODO: Update endpoint path and response parsing when ESM3
        variant generation API is finalized.
        """
        payload = {
            "sequence": sequence,
            "constraints": constraints,
        }

        # TODO: Replace placeholder endpoint with actual ESM3 path
        result = await self._request(
            "POST",
            "/v1/variants/generate",
            payload,
            timeout=_TIMEOUT_PREDICT,
        )

        result["provenance"] = _provenance(
            "generate_variant",
            sequence,
            constraints=str(sorted(constraints.keys())),
        )
        return result

    async def get_embeddings(self, sequence: str) -> dict[str, Any]:
        """Get protein embeddings vector for a sequence.

        Args:
            sequence: Amino acid sequence (single-letter code)

        Returns:
            Dict with embedding vector and provenance metadata.

        TODO: Update endpoint path and response parsing when ESM3
        embeddings API is finalized.
        """
        payload = {"sequence": sequence}

        # TODO: Replace placeholder endpoint with actual ESM3 path
        result = await self._request(
            "POST",
            "/v1/embeddings",
            payload,
            timeout=_TIMEOUT_DEFAULT,
        )

        result["provenance"] = _provenance("get_embeddings", sequence)
        return result
