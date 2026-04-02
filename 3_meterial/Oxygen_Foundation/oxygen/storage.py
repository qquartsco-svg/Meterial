"""L3 — LOX storage."""

from __future__ import annotations

from typing import List

from .constants import O2_BOILING_POINT_K, O2_LATENT_HEAT_KJ_PER_KG, O2_LIQUID_DENSITY_KG_PER_M3_AT_BP
from .contracts import ConceptLayer, StorageAssessment, StorageMethod


def boiloff_percent_per_day(tank_volume_m3: float, fill_level: float, heat_leak_w: float) -> float:
    latent_j = O2_LATENT_HEAT_KJ_PER_KG * 1000.0
    stored_kg = tank_volume_m3 * fill_level * O2_LIQUID_DENSITY_KG_PER_M3_AT_BP
    if stored_kg <= 0:
        return 0.0
    rate_kg_s = heat_leak_w / latent_j
    return rate_kg_s * 86400.0 / stored_kg * 100.0


def assess_lox_storage(
    tank_volume_m3: float = 30.0,
    heat_leak_w: float = 80.0,
) -> StorageAssessment:
    boil = boiloff_percent_per_day(tank_volume_m3, 0.9, heat_leak_w)
    return StorageAssessment(
        method=StorageMethod.LOX,
        boiloff_percent_per_day=boil,
        pressure_mpa=0.15,
        temperature_k=O2_BOILING_POINT_K,
        notes=[f"LOX boil-off ~{boil:.3f} %/day (illustrative)."],
    )


def storage_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="LOX",
            description="Rocket propellant oxidiser; cryogenic handling parallels LN₂ with higher fire risk when vaporised.",
        ),
    ]
