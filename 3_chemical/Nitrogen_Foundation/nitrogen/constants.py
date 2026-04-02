"""Constants for molecular nitrogen (N₂) and ammonia pathway."""

from __future__ import annotations

R_GAS_J_PER_MOL_K: float = 8.314_462
N2_MOLAR_MASS_G_PER_MOL: float = 28.0134
NH3_MOLAR_MASS_G_PER_MOL: float = 17.0305

N2_BOILING_POINT_K: float = 77.36
N2_TRIPLE_POINT_K: float = 63.15
N2_LIQUID_DENSITY_KG_PER_M3_AT_BP: float = 807.0
N2_LATENT_HEAT_KJ_PER_KG: float = 199.0

AIR_N2_MOL_FRACTION: float = 0.78084
AIR_O2_MOL_FRACTION: float = 0.2095

STANDARD_TEMPERATURE_K: float = 298.15
STANDARD_PRESSURE_PA: float = 101_325.0

# Haber process (cartoon): N₂ + 3H₂ ⇌ 2NH₃, exothermic
HABER_DH_KJ_PER_MOL_RXN: float = -92.0  # per 2 mol NH₃ formed (order of magnitude)
