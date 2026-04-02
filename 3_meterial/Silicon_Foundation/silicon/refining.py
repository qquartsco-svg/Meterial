from __future__ import annotations

from typing import List

from .contracts import ConceptLayer, RefiningAssessment, RefiningMethod


def assess_siemens_refining() -> RefiningAssessment:
    return RefiningAssessment(
        method=RefiningMethod.SIEMENS_PROCESS,
        purity_six_nines_fraction=0.999999,
        energy_intensity_kwh_per_kg_si=80.0,
        notes=["High purity for electronics, high electricity burden."],
    )


def refining_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(name="Purity Ladder", description="Metallurgical Si -> polysilicon -> wafer-grade crystal; each step raises cost and energy."),
    ]
