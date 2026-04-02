from __future__ import annotations

from typing import Dict, List

from .contracts import ConceptLayer

SIBLING_BRIDGES: Dict[str, str] = {
    "Battery_Dynamics_Engine": "Direct: Li-ion dynamics, SOC/SOH, thermal envelopes.",
    "Hydrogen_Foundation": "Grid coupling: Li for short-duration, H2 for long-duration storage.",
    "Chemical_Reaction_Foundation": "Electrochemical side reactions and degradation semantics.",
    "FusionCore_Stack": "Li-6 breeding context for tritium (conceptual bridge).",
    "VectorSpace_102": "Li axes: extraction, battery performance, safety, recycling, economics.",
}


def extension_hooks_concept_layers() -> List[ConceptLayer]:
    return [ConceptLayer(name="Bridges", description="Battery/H2/Chemical/Fusion/VectorSpace links.")]
