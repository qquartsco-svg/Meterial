"""Sibling bridges."""

from __future__ import annotations

from typing import Dict, List

from .contracts import ConceptLayer

SIBLING_BRIDGES: Dict[str, str] = {
    "Hydrogen_Foundation": "Electrolysis co-produces O₂ with H₂.",
    "Nitrogen_Foundation": "ASU co-produces O₂ and N₂.",
    "Chemical_Reaction_Foundation": "Combustion stoichiometry, ΔG of oxidation.",
    "Element_Capture_Foundation": "O₂ as life-support and propellant species.",
    "TerraCore_Stack": "Electrolysis / atmosphere processing narratives.",
    "VectorSpace_102": "O₂ axes: production, LOX storage, fire risk, economics.",
}

FUTURE_TAGS: List[str] = ["moxie_mass_balance", "sabatier_o2_closure", "medical_o2_supply_chain"]


def extension_hooks_concept_layers() -> List[ConceptLayer]:
    return [ConceptLayer(name="Bridges", description="H₂, N₂, chemical, capture, TerraCore, hub.")]
