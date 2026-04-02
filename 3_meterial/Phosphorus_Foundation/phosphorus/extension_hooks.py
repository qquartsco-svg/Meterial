from __future__ import annotations

from typing import Dict, List

from .contracts import ConceptLayer

SIBLING_BRIDGES: Dict[str, str] = {
    "Token_Dynamics_Foundation": "ATP as bio-energy token with strict regeneration loop.",
    "Nitrogen_Foundation": "N-P-K fertilizer coupling in agriculture.",
    "Chemical_Reaction_Foundation": "Acid/base, precipitation, and nutrient chemistry screening.",
    "TerraCore_Stack": "Habitat nutrient cycles and waste-loop phosphorus recovery.",
    "VectorSpace_102": "P axes: extraction, bio-cycle, pollution, recycling, economics.",
}


def extension_hooks_concept_layers() -> List[ConceptLayer]:
    return [ConceptLayer(name="Bridges", description="Token/Nitrogen/Chemical/TerraCore/VectorSpace links.")]
