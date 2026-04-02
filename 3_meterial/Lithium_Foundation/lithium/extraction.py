from __future__ import annotations

from typing import List

from .contracts import ConceptLayer, ExtractionAssessment, ExtractionMethod


def assess_brine_extraction() -> ExtractionAssessment:
    return ExtractionAssessment(
        method=ExtractionMethod.BRINE_EVAPORATION,
        li2co3_equivalent_kg_per_ton_feed=2.5,
        water_intensity_l_per_kg_lce=2000.0,
        co2_intensity_kg_per_kg_lce=5.0,
        notes=["Brine route: lower ore processing energy, high water-land footprint sensitivity."],
    )


def assess_hard_rock_extraction() -> ExtractionAssessment:
    return ExtractionAssessment(
        method=ExtractionMethod.HARD_ROCK_SPODUMENE,
        li2co3_equivalent_kg_per_ton_feed=12.0,
        water_intensity_l_per_kg_lce=500.0,
        co2_intensity_kg_per_kg_lce=12.0,
        notes=["Hard-rock route: higher energy / calcination burden."],
    )


def extraction_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(name="Brine vs Hard Rock", description="Trade-off between water intensity and energy/CO2 intensity."),
    ]
