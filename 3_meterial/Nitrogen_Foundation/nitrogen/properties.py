"""L1 — N₂ properties."""

from __future__ import annotations

from typing import List

from .constants import (
    N2_BOILING_POINT_K,
    N2_LIQUID_DENSITY_KG_PER_M3_AT_BP,
    N2_MOLAR_MASS_G_PER_MOL,
    R_GAS_J_PER_MOL_K,
    STANDARD_PRESSURE_PA,
    STANDARD_TEMPERATURE_K,
)
from .contracts import ConceptLayer, N2Properties


def n2_property_card() -> N2Properties:
    return N2Properties(
        molar_mass_g_per_mol=N2_MOLAR_MASS_G_PER_MOL,
        boiling_point_k=N2_BOILING_POINT_K,
        liquid_density_kg_per_m3_at_bp=N2_LIQUID_DENSITY_KG_PER_M3_AT_BP,
    )


def ideal_gas_density_kg_per_m3(temperature_k: float, pressure_pa: float) -> float:
    if temperature_k <= 0:
        raise ValueError("temperature_k must be > 0")
    m_kg = N2_MOLAR_MASS_G_PER_MOL / 1000.0
    return pressure_pa * m_kg / (R_GAS_J_PER_MOL_K * temperature_k)


def properties_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="Diatomic Nitrogen",
            description="N₂ triple bond — kinetically inert at ambient; fixation requires energy.",
        ),
    ]
