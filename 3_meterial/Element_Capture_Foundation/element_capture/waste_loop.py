from __future__ import annotations

from dataclasses import dataclass

from .contracts import CaptureAssessment, Species


@dataclass(frozen=True)
class WasteLoopReport:
    recovered_species: str
    byproduct_species: str | None
    recovered_kg_day: float
    byproduct_kg_day: float
    recyclable_water_kg_day: float
    loop_closure_score_0_1: float
    recommendation: str


def assess_waste_loop(assessment: CaptureAssessment) -> WasteLoopReport:
    recovered = assessment.net_capture_rate_kg_s * 86400.0
    byproduct_species: str | None = None
    byproduct_kg_day = 0.0
    recyclable_water_kg_day = 0.0
    score = min(1.0, recovered / 10.0)

    if assessment.environment.species is Species.H2:
        byproduct_species = "o2"
        byproduct_kg_day = recovered * 8.0
        score = min(1.0, 0.5 + recovered / 20.0)
    elif assessment.environment.species is Species.CO2:
        byproduct_species = "concentrated_co2_stream"
        byproduct_kg_day = recovered
        recyclable_water_kg_day = recovered * 0.05
    elif assessment.environment.species in (Species.HE, Species.HE3):
        byproduct_species = "light_gas_tailings"
        byproduct_kg_day = recovered * 0.1
    recommendation = (
        "waste loop useful for habitat closure"
        if score >= 0.5
        else "waste loop exists but closure benefit remains limited"
    )
    return WasteLoopReport(
        recovered_species=assessment.environment.species.value,
        byproduct_species=byproduct_species,
        recovered_kg_day=recovered,
        byproduct_kg_day=byproduct_kg_day,
        recyclable_water_kg_day=recyclable_water_kg_day,
        loop_closure_score_0_1=score,
        recommendation=recommendation,
    )
