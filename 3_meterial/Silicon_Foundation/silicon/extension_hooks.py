from __future__ import annotations

from typing import Dict, List

from .contracts import ConceptLayer

SIBLING_BRIDGES: Dict[str, str] = {
    "1_calculator": "Silicon hardware substrate for compute stack realization.",
    "Battery_Dynamics_Engine": "PV->battery coupling in energy systems.",
    "Hydrogen_Foundation": "PV electrolysis pathways coupling electricity to H2 production.",
    "Carbon_Composite_Stack": "Package/thermal material interface in devices.",
    "VectorSpace_102": "Si axes: refining, yield, thermal margin, economics.",
}


def extension_hooks_concept_layers() -> List[ConceptLayer]:
    return [ConceptLayer(name="Bridges", description="Calculator/Battery/H2/Carbon/VectorSpace links.")]
