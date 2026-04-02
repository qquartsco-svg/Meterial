"""L3 — Hydrogen storage methods.

Core question: *How do we keep H₂ available for use?*

Methods:
  - Compressed gas (350 / 700 bar)
  - Liquid hydrogen (20 K)
  - Metal hydrides
  - Chemical carriers (ammonia, LOHC)
"""

from __future__ import annotations

import math
from typing import List

from .constants import (
    H2_BOILING_POINT_K,
    H2_DENSITY_KG_PER_M3_STP,
    H2_LATENT_HEAT_KJ_PER_KG,
    H2_LHV_MJ_PER_KG,
    H2_LIQUID_DENSITY_KG_PER_M3,
    H2_MOLAR_MASS_G_PER_MOL,
    R_GAS_J_PER_MOL_K,
    STANDARD_PRESSURE_PA,
    STANDARD_TEMPERATURE_K,
)
from .contracts import ConceptLayer, StorageAssessment, StorageMethod


# ── Compressed gas ─────────────────────────────────────────────────────

def compressed_gas_density_kg_per_m3(
    pressure_mpa: float,
    temperature_k: float = STANDARD_TEMPERATURE_K,
    compressibility_z: float = 1.0,
) -> float:
    """ρ = P·M / (Z·R·T) for compressed H₂."""
    if temperature_k <= 0 or compressibility_z <= 0:
        raise ValueError("temperature_k and Z must be > 0")
    p_pa = pressure_mpa * 1e6
    m_kg = H2_MOLAR_MASS_G_PER_MOL / 1000.0
    return p_pa * m_kg / (compressibility_z * R_GAS_J_PER_MOL_K * temperature_k)


def compression_energy_kwh_per_kg(
    p_final_mpa: float,
    p_initial_mpa: float = 0.101325,
    temperature_k: float = STANDARD_TEMPERATURE_K,
    n_stages: int = 3,
    isentropic_efficiency: float = 0.75,
    gamma: float = 1.41,
) -> float:
    """Multi-stage isothermal-like compression energy.

    Ideal isothermal work per mol: W = n·R·T·ln(P₂/P₁).
    Divided by isentropic efficiency.
    """
    if p_final_mpa <= p_initial_mpa:
        return 0.0
    ratio = p_final_mpa / p_initial_mpa
    stage_ratio = ratio ** (1.0 / n_stages)
    w_per_mol_j = n_stages * R_GAS_J_PER_MOL_K * temperature_k * math.log(stage_ratio)
    w_per_mol_j /= isentropic_efficiency
    w_per_kg_j = w_per_mol_j / (H2_MOLAR_MASS_G_PER_MOL / 1000.0)
    return w_per_kg_j / 3.6e6


# ── Liquid hydrogen ────────────────────────────────────────────────────

def liquefaction_energy_kwh_per_kg(
    efficiency_fraction: float = 0.30,
) -> float:
    """Energy required to liquefy H₂.

    Ideal (Carnot-limited): ~3.9 kWh/kg.
    Real plants: 10–13 kWh/kg (efficiency ~30 %).
    """
    ideal_kwh = 3.9
    if efficiency_fraction <= 0:
        efficiency_fraction = 0.01
    return ideal_kwh / efficiency_fraction


def boiloff_rate_kg_per_day(
    tank_volume_m3: float,
    heat_leak_w: float,
    fill_level: float = 0.95,
) -> float:
    """Boil-off mass rate from a cryogenic tank.

    ṁ_boiloff = Q_leak / L_vap
    """
    latent_j_per_kg = H2_LATENT_HEAT_KJ_PER_KG * 1000.0
    boiloff_kg_per_s = heat_leak_w / latent_j_per_kg
    return boiloff_kg_per_s * 86400.0


def boiloff_percent_per_day(
    tank_volume_m3: float,
    heat_leak_w: float,
    fill_level: float = 0.95,
) -> float:
    """Boil-off as percentage of stored H₂ per day."""
    stored_kg = tank_volume_m3 * fill_level * H2_LIQUID_DENSITY_KG_PER_M3
    if stored_kg <= 0:
        return 0.0
    return boiloff_rate_kg_per_day(tank_volume_m3, heat_leak_w, fill_level) / stored_kg * 100.0


# ── Metal hydride ──────────────────────────────────────────────────────

def metal_hydride_equilibrium_pressure_mpa(
    temperature_k: float,
    dh_kj_per_mol: float = 30.0,
    ds_j_per_mol_k: float = 110.0,
    p_ref_mpa: float = 0.1,
    t_ref_k: float = 298.15,
) -> float:
    """Van't Hoff equation for metal hydride plateau pressure.

    ln(P/P_ref) = (ΔH/R)(1/T_ref − 1/T) + ΔS/R × (T − T_ref) / T
    Simplified: ln(P/P_ref) = (ΔH/R)(1/T_ref − 1/T)
    """
    dh_j = dh_kj_per_mol * 1000.0
    exponent = (dh_j / R_GAS_J_PER_MOL_K) * (1.0 / t_ref_k - 1.0 / temperature_k)
    return p_ref_mpa * math.exp(exponent)


# ── Assessment helpers ─────────────────────────────────────────────────

def assess_compressed_storage(
    pressure_mpa: float = 70.0,
    tank_mass_kg: float = 100.0,
    h2_mass_kg: float = 5.0,
) -> StorageAssessment:
    """Evaluate compressed gas storage."""
    grav_density = h2_mass_kg / (tank_mass_kg + h2_mass_kg) * 100.0
    vol_density = compressed_gas_density_kg_per_m3(pressure_mpa, compressibility_z=1.2)
    comp_energy = compression_energy_kwh_per_kg(pressure_mpa)
    energy_penalty = comp_energy / (H2_LHV_MJ_PER_KG / 3.6)

    notes = []
    if pressure_mpa > 100:
        notes.append("Pressure > 100 MPa — extreme engineering challenge.")

    return StorageAssessment(
        method=StorageMethod.COMPRESSED_700BAR if pressure_mpa >= 60 else StorageMethod.COMPRESSED_350BAR,
        gravimetric_density_wt_percent=grav_density,
        volumetric_density_kg_h2_per_m3=vol_density,
        energy_penalty_fraction=min(energy_penalty, 1.0),
        boiloff_rate_percent_per_day=0.0,
        pressure_mpa=pressure_mpa,
        temperature_k=STANDARD_TEMPERATURE_K,
        round_trip_efficiency=max(1.0 - energy_penalty, 0.05),
        notes=notes,
    )


def assess_liquid_storage(
    tank_volume_m3: float = 50.0,
    heat_leak_w: float = 50.0,
) -> StorageAssessment:
    """Evaluate liquid hydrogen storage."""
    liq_energy = liquefaction_energy_kwh_per_kg()
    energy_penalty = liq_energy / (H2_LHV_MJ_PER_KG / 3.6)
    boiloff = boiloff_percent_per_day(tank_volume_m3, heat_leak_w)

    return StorageAssessment(
        method=StorageMethod.LIQUID,
        gravimetric_density_wt_percent=14.0,
        volumetric_density_kg_h2_per_m3=H2_LIQUID_DENSITY_KG_PER_M3,
        energy_penalty_fraction=min(energy_penalty, 1.0),
        boiloff_rate_percent_per_day=boiloff,
        pressure_mpa=0.1,
        temperature_k=H2_BOILING_POINT_K,
        round_trip_efficiency=max(1.0 - energy_penalty - boiloff / 100.0, 0.05),
        notes=[
            f"Liquefaction energy: {liq_energy:.1f} kWh/kg",
            f"Boil-off: {boiloff:.2f} %/day",
        ],
    )


# ── Concept layers ─────────────────────────────────────────────────────

def storage_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="Compressed Gas",
            description=(
                "Store H₂ at 350–700 bar in Type III/IV tanks.  "
                "~5 wt % gravimetric density.  Compression takes 5–15 % of H₂ energy."
            ),
            key_equations=[
                "ρ = PM / (ZRT)",
                "W_comp = nRT·ln(P₂/P₁) / η_is  (multi-stage isothermal)",
            ],
        ),
        ConceptLayer(
            name="Liquid Hydrogen",
            description=(
                "Cool to 20 K.  70.8 kg/m³.  Best volumetric density but "
                "liquefaction costs ~30 % of LHV and boil-off is inevitable."
            ),
            key_equations=[
                "ṁ_boiloff = Q_leak / L_vap",
                "W_liq ≈ 3.9 / η_Carnot  kWh/kg (ideal ~3.9, real ~12 kWh/kg)",
            ],
        ),
        ConceptLayer(
            name="Metal Hydrides",
            description=(
                "H₂ absorbed into metal lattice (LaNi₅, MgH₂, …).  "
                "Safe, compact, but heavy and slow kinetics."
            ),
            key_equations=[
                "ln(P/P_ref) = (ΔH/R)(1/T_ref − 1/T)  — Van't Hoff",
            ],
        ),
    ]
