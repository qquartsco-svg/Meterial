"""Domain — propulsion / ISRU (conceptual)."""

from __future__ import annotations

from typing import List

from .contracts import ConceptLayer


def space_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="LOX / GOX Propulsion",
            description="LOX as oxidiser with kerosenes, H₂, CH₄; boil-off and slosh are mission risks.",
        ),
        ConceptLayer(
            name="Planetary ISRU",
            description="CO₂ → O₂ pathways (MOXIE-class) are energy- and mass-limited; not 'free O₂'.",
        ),
    ]
