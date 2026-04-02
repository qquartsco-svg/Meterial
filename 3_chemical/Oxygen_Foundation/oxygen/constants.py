"""Molecular oxygen (O₂) constants."""

from __future__ import annotations

R_GAS_J_PER_MOL_K: float = 8.314_462
O2_MOLAR_MASS_G_PER_MOL: float = 31.9988

O2_BOILING_POINT_K: float = 90.188
O2_LIQUID_DENSITY_KG_PER_M3_AT_BP: float = 1141.0
O2_LATENT_HEAT_KJ_PER_KG: float = 213.0

AIR_O2_MOL_FRACTION: float = 0.2095

STANDARD_TEMPERATURE_K: float = 298.15

# Water electrolysis: 2 H2O -> 2 H2 + O2  => 1 mol O2 per 2 mol H2O ... stoichiometry helper
MOL_O2_PER_MOL_H2_FROM_WATER: float = 0.5
