"""L1 — Hydrogen physical and chemical properties.

What is hydrogen?  The simplest, lightest, most abundant element.
This module provides its static property card plus derived helpers
for density under non-standard conditions.
"""

from __future__ import annotations

import math
from typing import List

from .constants import (
    H2_BOILING_POINT_K,
    H2_DENSITY_KG_PER_M3_STP,
    H2_HHV_MJ_PER_KG,
    H2_LEL_VOL_PERCENT,
    H2_LHV_MJ_PER_KG,
    H2_MOLAR_MASS_G_PER_MOL,
    H2_UEL_VOL_PERCENT,
    H2_AUTOIGNITION_K,
    H2_VDW_A_PA_M6_PER_MOL2,
    H2_VDW_B_M3_PER_MOL,
    R_GAS_J_PER_MOL_K,
    STANDARD_PRESSURE_PA,
    STANDARD_TEMPERATURE_K,
)
from .contracts import ConceptLayer, H2Properties


def hydrogen_property_card() -> H2Properties:
    """Return the reference property card for molecular H₂."""
    return H2Properties(
        molar_mass_g_per_mol=H2_MOLAR_MASS_G_PER_MOL,
        density_kg_per_m3_stp=H2_DENSITY_KG_PER_M3_STP,
        boiling_point_k=H2_BOILING_POINT_K,
        lhv_mj_per_kg=H2_LHV_MJ_PER_KG,
        hhv_mj_per_kg=H2_HHV_MJ_PER_KG,
        lel_vol_percent=H2_LEL_VOL_PERCENT,
        uel_vol_percent=H2_UEL_VOL_PERCENT,
        autoignition_k=H2_AUTOIGNITION_K,
    )


def ideal_gas_density_kg_per_m3(
    temperature_k: float,
    pressure_pa: float,
) -> float:
    """H₂ density via ideal gas law: ρ = PM / (RT).

    Acceptable for low pressures (< ~5 MPa) and moderate temperatures.
    """
    if temperature_k <= 0:
        raise ValueError("temperature_k must be > 0")
    molar_mass_kg = H2_MOLAR_MASS_G_PER_MOL / 1000.0
    return pressure_pa * molar_mass_kg / (R_GAS_J_PER_MOL_K * temperature_k)


def van_der_waals_pressure_pa(
    temperature_k: float,
    molar_volume_m3: float,
) -> float:
    """Pressure from Van der Waals EOS for H₂.

    P = RT / (V_m − b) − a / V_m²
    """
    if molar_volume_m3 <= H2_VDW_B_M3_PER_MOL:
        raise ValueError("molar_volume must exceed Van der Waals b parameter")
    a = H2_VDW_A_PA_M6_PER_MOL2
    b = H2_VDW_B_M3_PER_MOL
    return (
        R_GAS_J_PER_MOL_K * temperature_k / (molar_volume_m3 - b)
        - a / (molar_volume_m3 ** 2)
    )


def compressibility_factor(
    temperature_k: float,
    pressure_pa: float,
) -> float:
    """Approximate Z = PV/(nRT) using a simple Van der Waals iteration.

    Returns Z ≈ 1 for ideal conditions and deviates at high pressure.
    One Newton step from the ideal-gas seed.
    """
    if temperature_k <= 0 or pressure_pa <= 0:
        raise ValueError("temperature and pressure must be > 0")
    a = H2_VDW_A_PA_M6_PER_MOL2
    b = H2_VDW_B_M3_PER_MOL
    rt = R_GAS_J_PER_MOL_K * temperature_k
    vm_ideal = rt / pressure_pa
    vm = vm_ideal
    for _ in range(5):
        p_calc = rt / (vm - b) - a / vm**2
        dp_dvm = -rt / (vm - b)**2 + 2.0 * a / vm**3
        vm -= (p_calc - pressure_pa) / dp_dvm
    return pressure_pa * vm / rt


def energy_content_kwh(mass_kg: float, basis: str = "lhv") -> float:
    """Total energy in *mass_kg* of H₂.

    basis: 'lhv' (default) or 'hhv'.
    """
    if basis == "hhv":
        return mass_kg * H2_HHV_MJ_PER_KG / 3.6
    return mass_kg * H2_LHV_MJ_PER_KG / 3.6


def properties_concept_layers() -> List[ConceptLayer]:
    """Concept layers for L1."""
    return [
        ConceptLayer(
            name="Hydrogen Element",
            description=(
                "Simplest atom (Z=1).  H₂ is the diatomic molecular form.  "
                "Lightest gas, highest gravimetric energy density of any chemical fuel."
            ),
            key_equations=["ρ = PM / (RT)  — ideal gas density"],
        ),
        ConceptLayer(
            name="Real-Gas Behaviour",
            description=(
                "At pressures above ~5 MPa the ideal gas law under-predicts density.  "
                "Van der Waals or more advanced EOS (Peng-Robinson) are needed."
            ),
            key_equations=[
                "P = RT/(V_m − b) − a/V_m²  — Van der Waals",
                "Z = PV/(nRT)  — compressibility factor",
            ],
        ),
    ]
