"""L6 — Sibling bridges."""

from __future__ import annotations

from typing import Dict, List

from .contracts import ConceptLayer

SIBLING_BRIDGES: Dict[str, str] = {
    "Hydrogen_Foundation": "He cools H₂ liquefaction trains and superconducting magnets.",
    "FusionCore_Stack": "D-T produces He-4 + n; He ash handling in plasma-facing systems.",
    "Element_Capture_Foundation": "Trace He in natural gas / regolith contexts (conceptual).",
    "Chemical_Reaction_Foundation": "He is inert — chemistry layer treats transport/thermo only.",
    "VectorSpace_102": "He axes: sourcing, storage boil-off, safety, scarcity proxy.",
}

FUTURE_TAGS: List[str] = [
    "he3_spin_polarization",
    "mri_cryostat_model",
    "balloon_lift_isa",
    "regolith_he_extraction",
]


def extension_hooks_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(name="Sibling Bridges", description="Links to H₂, fusion, capture, math hub."),
    ]
