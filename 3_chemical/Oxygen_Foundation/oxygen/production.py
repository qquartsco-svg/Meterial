"""L2 — O₂ production pathways."""

from __future__ import annotations

from typing import List

from .constants import MOL_O2_PER_MOL_H2_FROM_WATER
from .contracts import ConceptLayer, ProductionAssessment, ProductionMethod


def assess_cryogenic_o2(
    specific_energy_kwh_per_kg: float = 0.35,
    purity: float = 0.995,
) -> ProductionAssessment:
    return ProductionAssessment(
        method=ProductionMethod.CRYOGENIC_AIR_SEP,
        purity_o2_fraction=purity,
        specific_energy_kwh_per_kg_o2=specific_energy_kwh_per_kg,
        notes=["Co-produced with N₂ in ASU; energy is shared in real plants."],
    )


def o2_from_electrolysis_mol_per_s(h2_mol_per_s: float) -> float:
    """Stoichiometry: 1 mol O₂ per 2 mol H₂ from water splitting."""
    return h2_mol_per_s * MOL_O2_PER_MOL_H2_FROM_WATER


def production_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="Electrolysis Coupling",
            description="Water electrolysis yields O₂ as co-product with H₂ — ties to Hydrogen_Foundation.",
            key_equations=["ṅ_O₂ = 0.5 × ṅ_H₂ (ideal stoichiometry)"],
        ),
    ]
