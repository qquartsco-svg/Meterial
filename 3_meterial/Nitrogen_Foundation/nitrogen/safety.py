"""L5 — N₂ / LN₂ safety."""

from __future__ import annotations

from typing import List

from .contracts import ConceptLayer


def safety_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="Asphyxiation",
            description="N₂ is odourless; confined-space release displaces O₂.",
        ),
        ConceptLayer(
            name="Cold Burns",
            description="LN₂ contact — thermal injury; vapor expansion hazard.",
        ),
    ]
