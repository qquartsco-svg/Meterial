"""L2 — Air separation to N₂ (and O₂ co-product)."""

from __future__ import annotations

from typing import List

from .constants import AIR_N2_MOL_FRACTION
from .contracts import ConceptLayer, SeparationAssessment, SeparationMethod


def assess_cryogenic_separation(
    specific_energy_kwh_per_kg_n2: float = 0.4,
    purity: float = 0.999,
) -> SeparationAssessment:
    return SeparationAssessment(
        method=SeparationMethod.CRYOGENIC_DISTILLATION,
        purity_n2_fraction=purity,
        specific_energy_kwh_per_kg_n2=specific_energy_kwh_per_kg_n2,
        notes=["Cryogenic ASU is dominant for high-purity N₂/O₂."],
    )


def nitrogen_yield_from_air_mol_per_mol_air() -> float:
    return AIR_N2_MOL_FRACTION


def separation_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="Cryogenic ASU",
            description="Linde cycle — N₂ and O₂ as co-products; energy-intensive.",
        ),
    ]
