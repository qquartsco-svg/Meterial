"""Sibling bridges."""

from __future__ import annotations

from typing import Dict, List

from .contracts import ConceptLayer

SIBLING_BRIDGES: Dict[str, str] = {
    "Hydrogen_Foundation": "Haber–Bosch consumes H₂; NH₃ is H₂ + N₂ coupling.",
    "Chemical_Reaction_Foundation": "ΔG, K_eq, kinetics for fixation and NOx pathways.",
    "Element_Capture_Foundation": "N₂ as capture species; air fractionation context.",
    "TerraCore_Stack": "Habitat inerting, fertilizer loop narratives.",
    "VectorSpace_102": "N₂ axes: separation, fixation, storage, safety.",
}

FUTURE_TAGS: List[str] = ["nox_formation", "biological_nitrogen_fixation", "electrochemical_n2_reduction"]


def extension_hooks_concept_layers() -> List[ConceptLayer]:
    return [ConceptLayer(name="Bridges", description="H₂, chemical, capture, TerraCore, hub.")]
