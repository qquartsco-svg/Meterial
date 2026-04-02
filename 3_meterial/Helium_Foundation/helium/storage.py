"""L3 — Helium storage (cryogenic + high pressure)."""

from __future__ import annotations

import math
from typing import List

from .constants import (
    HE_BOILING_POINT_K,
    HE_LATENT_HEAT_KJ_PER_KG,
    HE_LIQUID_DENSITY_KG_PER_M3_AT_BP,
    R_GAS_J_PER_MOL_K,
    STANDARD_TEMPERATURE_K,
    HE_MOLAR_MASS_G_PER_MOL,
)
from .contracts import ConceptLayer, StorageAssessment, StorageMethod


def boiloff_rate_kg_per_day(heat_leak_w: float) -> float:
    latent_j = HE_LATENT_HEAT_KJ_PER_KG * 1000.0
    return (heat_leak_w / latent_j) * 86400.0


def boiloff_percent_per_day(tank_volume_m3: float, fill_level: float, heat_leak_w: float) -> float:
    stored_kg = tank_volume_m3 * fill_level * HE_LIQUID_DENSITY_KG_PER_M3_AT_BP
    if stored_kg <= 0:
        return 0.0
    return boiloff_rate_kg_per_day(heat_leak_w) / stored_kg * 100.0


def compression_energy_kwh_per_kg(
    p_final_mpa: float,
    p_initial_mpa: float = 0.101325,
    temperature_k: float = STANDARD_TEMPERATURE_K,
    gamma: float = 1.67,
    isentropic_efficiency: float = 0.75,
) -> float:
    if p_final_mpa <= p_initial_mpa:
        return 0.0
    ratio = p_final_mpa / p_initial_mpa
    w_per_mol = R_GAS_J_PER_MOL_K * temperature_k * math.log(ratio) / isentropic_efficiency
    w_per_kg = w_per_mol / (HE_MOLAR_MASS_G_PER_MOL / 1000.0)
    return w_per_kg / 3.6e6


def assess_liquid_storage(
    tank_volume_m3: float = 100.0,
    heat_leak_w: float = 5.0,
    fill_level: float = 0.9,
) -> StorageAssessment:
    boil = boiloff_percent_per_day(tank_volume_m3, fill_level, heat_leak_w)
    return StorageAssessment(
        method=StorageMethod.LIQUID_DEWAR,
        boiloff_percent_per_day=boil,
        pressure_mpa=0.05,
        temperature_k=HE_BOILING_POINT_K,
        round_trip_efficiency=max(1.0 - boil / 100.0, 0.1),
        notes=[f"Boil-off ~{boil:.3f} %/day for assumed heat leak {heat_leak_w} W"],
    )


def storage_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="Liquid Helium",
            description="4 K dewars for MRI, research, and deep cryogen feed.",
            key_equations=["ṁ_boiloff = Q_leak / L_vap"],
        ),
        ConceptLayer(
            name="High-Pressure Gas",
            description="Cylinder bundles for leak detection and welding cover gas.",
        ),
    ]
