from __future__ import annotations

from typing import List

from .constants import PHOSPHATE_ORE_GRADE_P2O5_FRACTION_TYPICAL
from .contracts import ConceptLayer, ExtractionAssessment, ExtractionMethod


def assess_phosphate_rock() -> ExtractionAssessment:
    return ExtractionAssessment(
        method=ExtractionMethod.PHOSPHATE_ROCK_MINING,
        ore_grade_p2o5_fraction=PHOSPHATE_ORE_GRADE_P2O5_FRACTION_TYPICAL,
        co2_intensity_kg_per_kg_p2o5=1.2,
        contaminants_risk="medium",
        notes=["Cadmium/uranium impurities can become major policy constraints."],
    )


def extraction_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="Finite Phosphate Ore",
            description="Phosphate rock is geopolitically concentrated and finite on agricultural timescales.",
        ),
    ]
