"""L4 — O₂ fire and enrichment safety."""

from __future__ import annotations

from typing import List

from .contracts import ConceptLayer


def fire_severity_index(o2_vol_percent: float) -> float:
    """0–1 cartoon: 21 % air ≈ 0.2, 100 % O₂ → 1.0."""
    x = (o2_vol_percent - 21.0) / (100.0 - 21.0)
    return max(0.0, min(1.0, x))


def safety_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="Oxidiser Fires",
            description="Materials that do not burn in air can burn in enriched O₂; ignition energy drops.",
        ),
    ]
