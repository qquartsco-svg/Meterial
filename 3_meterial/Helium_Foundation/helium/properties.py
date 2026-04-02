"""L1 — Helium physical properties."""

from __future__ import annotations

from typing import List

from .constants import (
    HE_BOILING_POINT_K,
    HE_DENSITY_KG_PER_M3_STP,
    HE_LIQUID_DENSITY_KG_PER_M3_AT_BP,
    HE_MOLAR_MASS_G_PER_MOL,
    R_GAS_J_PER_MOL_K,
    STANDARD_PRESSURE_PA,
    STANDARD_TEMPERATURE_K,
)
from .contracts import ConceptLayer, HeProperties


def helium_property_card() -> HeProperties:
    return HeProperties(
        molar_mass_g_per_mol=HE_MOLAR_MASS_G_PER_MOL,
        density_kg_per_m3_stp=HE_DENSITY_KG_PER_M3_STP,
        boiling_point_k=HE_BOILING_POINT_K,
        liquid_density_kg_per_m3_at_bp=HE_LIQUID_DENSITY_KG_PER_M3_AT_BP,
    )


def ideal_gas_density_kg_per_m3(temperature_k: float, pressure_pa: float) -> float:
    if temperature_k <= 0:
        raise ValueError("temperature_k must be > 0")
    m_kg = HE_MOLAR_MASS_G_PER_MOL / 1000.0
    return pressure_pa * m_kg / (R_GAS_J_PER_MOL_K * temperature_k)


def properties_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="Noble Gas Baseline",
            description=(
                "He-4 is chemically inert. Transport and storage dominate engineering; "
                "reaction chemistry is negligible except at extreme astrophysical conditions."
            ),
            key_equations=["ρ = PM/(RT) — ideal gas density"],
        ),
        ConceptLayer(
            name="Ultra-Low Boiling Point",
            description=(
                "4.22 K boiling point — deepest cryogen in common industrial use after H₂. "
                "Couples tightly to hydrogen liquefaction and superconducting magnets."
            ),
        ),
    ]
