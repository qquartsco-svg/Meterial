from __future__ import annotations

from typing import List

from .contracts import BioenergeticsAssessment, ConceptLayer


def assess_atp_cycle(body_mass_kg: float = 70.0) -> BioenergeticsAssessment:
    # textbook-scale order-of-magnitude: tens of kg ATP turned over daily in humans
    turnover = max(40_000.0 * body_mass_kg / 70.0, 1.0)  # mol/day cartoon
    return BioenergeticsAssessment(
        atp_turnover_mol_per_day_human=turnover,
        atp_regeneration_required=True,
        notes=["ATP is recycled continuously; no biological system operates on one-pass ATP stock."],
    )


def bioenergetics_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="ATP Regeneration",
            description="ATP/ADP phosphate cycle couples phosphorus chemistry to cellular energy flux.",
        ),
    ]
