"""Physical constants for hydrogen science."""

from __future__ import annotations

# --- Universal constants ---
R_GAS_J_PER_MOL_K: float = 8.314_462
FARADAY_C_PER_MOL: float = 96_485.332
AVOGADRO: float = 6.022_140_76e23
BOLTZMANN_J_PER_K: float = 1.380_649e-23

# --- Hydrogen element ---
H_ATOMIC_MASS_AMU: float = 1.007_94
H2_MOLAR_MASS_G_PER_MOL: float = 2.015_88

# --- Thermodynamic data (water splitting / formation) ---
WATER_FORMATION_DG_KJ_PER_MOL: float = -237.1   # ΔG° at 298 K, liquid water
WATER_FORMATION_DH_KJ_PER_MOL: float = -285.8   # ΔH° at 298 K, liquid water (HHV basis)
WATER_ELECTROLYSIS_E0_V: float = 1.229           # reversible cell voltage at 298 K
THERMONEUTRAL_VOLTAGE_V: float = 1.481           # = ΔH / (2F), no external heat needed

# --- Energy density ---
H2_LHV_MJ_PER_KG: float = 120.0     # Lower Heating Value
H2_HHV_MJ_PER_KG: float = 141.8     # Higher Heating Value
H2_LHV_KWH_PER_KG: float = 33.33    # ≈ 120 / 3.6
H2_VOLUMETRIC_ENERGY_MJ_PER_M3_STP: float = 10.8  # at STP gas

# --- Physical properties (at STP unless noted) ---
H2_DENSITY_KG_PER_M3_STP: float = 0.0899
H2_LIQUID_DENSITY_KG_PER_M3: float = 70.8     # at 20 K
H2_BOILING_POINT_K: float = 20.28
H2_CRITICAL_TEMPERATURE_K: float = 33.19
H2_CRITICAL_PRESSURE_MPA: float = 1.296
H2_LATENT_HEAT_KJ_PER_KG: float = 446.0       # heat of vaporisation

# --- Safety ---
H2_LEL_VOL_PERCENT: float = 4.0       # Lower Explosive Limit in air
H2_UEL_VOL_PERCENT: float = 75.0      # Upper Explosive Limit in air
H2_AUTOIGNITION_K: float = 858.15     # ≈ 585 °C
H2_FLAME_SPEED_M_PER_S: float = 3.46  # stoichiometric in air
H2_MIN_IGNITION_ENERGY_MJ: float = 0.017e-3  # ≈ 0.017 mJ

# --- Standard conditions ---
STANDARD_TEMPERATURE_K: float = 298.15
STANDARD_PRESSURE_PA: float = 101_325.0
STANDARD_PRESSURE_MPA: float = 0.101_325

# --- Van der Waals constants for H₂ ---
H2_VDW_A_PA_M6_PER_MOL2: float = 0.02476
H2_VDW_B_M3_PER_MOL: float = 2.661e-5
