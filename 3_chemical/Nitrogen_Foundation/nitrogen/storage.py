"""L4 — Liquid N₂ storage."""

from __future__ import annotations

from typing import List

from .constants import N2_BOILING_POINT_K, N2_LATENT_HEAT_KJ_PER_KG, N2_LIQUID_DENSITY_KG_PER_M3_AT_BP
from .contracts import ConceptLayer, StorageAssessment, StorageMethod


def boiloff_percent_per_day(tank_volume_m3: float, fill_level: float, heat_leak_w: float) -> float:
    latent_j = N2_LATENT_HEAT_KJ_PER_KG * 1000.0
    stored_kg = tank_volume_m3 * fill_level * N2_LIQUID_DENSITY_KG_PER_M3_AT_BP
    if stored_kg <= 0:
        return 0.0
    rate_kg_s = heat_leak_w / latent_j
    return rate_kg_s * 86400.0 / stored_kg * 100.0


def assess_ln2_storage(
    tank_volume_m3: float = 20.0,
    heat_leak_w: float = 40.0,
) -> StorageAssessment:
    boil = boiloff_percent_per_day(tank_volume_m3, 0.9, heat_leak_w)
    return StorageAssessment(
        method=StorageMethod.LIQUID_N2,
        boiloff_percent_per_day=boil,
        pressure_mpa=0.15,
        temperature_k=N2_BOILING_POINT_K,
        notes=[f"LN₂ boil-off ~{boil:.3f} %/day (illustrative heat leak)."],
    )


def storage_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="Liquid Nitrogen",
            description="77 K cryogen; inerting, cooling, biological sample storage.",
        ),
    ]
