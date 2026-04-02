"""L4 — Helium safety (asphyxiation, pressure, cold)."""

from __future__ import annotations

from typing import List

from .contracts import ConceptLayer


def asphyxiation_risk_level(o2_vol_percent: float) -> str:
    if o2_vol_percent < 12.0:
        return "critical"
    if o2_vol_percent < 16.0:
        return "high"
    if o2_vol_percent < 19.5:
        return "marginal"
    return "acceptable"


def safety_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="Asphyxiation",
            description=(
                "He displaces O₂ in confined spaces; risk is silent (no odor). "
                "Ventilation and O₂ monitoring are mandatory."
            ),
        ),
        ConceptLayer(
            name="Cryogenic Burns",
            description="Liquid He contact causes severe cold burns; PPE and training required.",
        ),
    ]
