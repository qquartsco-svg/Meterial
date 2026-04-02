"""Domain — agriculture / fertilizer link (conceptual)."""

from __future__ import annotations

from typing import List

from .contracts import ConceptLayer


def agriculture_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="Fertilizer Loop",
            description="NH₃ → ammonium salts / urea; energy and H₂ footprint dominate LCA.",
        ),
    ]
