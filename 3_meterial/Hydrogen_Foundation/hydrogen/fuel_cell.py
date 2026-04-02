"""L4 — Fuel cell electrochemistry.

Core question: *How efficiently can H₂ be converted back to electricity?*

Fuel cell types modelled (tree-level):
  - PEMFC (Proton Exchange Membrane)
  - SOFC (Solid Oxide)
  - AFC (Alkaline)
"""

from __future__ import annotations

import math
from typing import List

from .constants import (
    FARADAY_C_PER_MOL,
    H2_LHV_MJ_PER_KG,
    H2_MOLAR_MASS_G_PER_MOL,
    R_GAS_J_PER_MOL_K,
    STANDARD_TEMPERATURE_K,
    WATER_ELECTROLYSIS_E0_V,
    WATER_FORMATION_DG_KJ_PER_MOL,
    WATER_FORMATION_DH_KJ_PER_MOL,
)
from .contracts import ConceptLayer, FuelCellAssessment, FuelCellType


# ── Nernst potential ───────────────────────────────────────────────────

def nernst_ocv(
    temperature_k: float = STANDARD_TEMPERATURE_K,
    p_h2_atm: float = 1.0,
    p_o2_atm: float = 0.21,
    p_h2o_atm: float = 1.0,
) -> float:
    """Open-circuit voltage for H₂/O₂ fuel cell via Nernst equation.

    E = E°(T) + (RT / 2F) · ln(P_H₂ · √P_O₂ / P_H₂O)

    E° adjusted for temperature: E°(T) ≈ 1.229 − 8.5×10⁻⁴(T − 298.15)
    """
    e0 = WATER_ELECTROLYSIS_E0_V - 8.5e-4 * (temperature_k - 298.15)
    if p_h2_atm <= 0 or p_o2_atm <= 0 or p_h2o_atm <= 0:
        return e0
    q = (p_h2_atm * math.sqrt(p_o2_atm)) / p_h2o_atm
    return e0 + (R_GAS_J_PER_MOL_K * temperature_k / (2 * FARADAY_C_PER_MOL)) * math.log(q)


# ── Efficiency ─────────────────────────────────────────────────────────

def thermodynamic_efficiency_limit(temperature_k: float = STANDARD_TEMPERATURE_K) -> float:
    """Maximum electric efficiency η_max = ΔG / ΔH.

    At 298 K: 237.1 / 285.8 ≈ 83 %.
    Adjusts slightly with temperature via ΔG(T) ≈ ΔH − TΔS.
    """
    ds = (WATER_FORMATION_DH_KJ_PER_MOL - WATER_FORMATION_DG_KJ_PER_MOL) / 298.15  # kJ/mol·K
    dg_t = WATER_FORMATION_DH_KJ_PER_MOL - temperature_k * ds
    return abs(dg_t / WATER_FORMATION_DH_KJ_PER_MOL)


def voltage_efficiency(cell_voltage_v: float, temperature_k: float = STANDARD_TEMPERATURE_K) -> float:
    """η_voltage = V_cell / E_thermo_neutral ≈ V_cell / 1.481."""
    e_tn = abs(WATER_FORMATION_DH_KJ_PER_MOL * 1000.0) / (2 * FARADAY_C_PER_MOL)
    if e_tn <= 0:
        return 0.0
    return min(cell_voltage_v / e_tn, 1.0)


def electric_efficiency(cell_voltage_v: float, utilisation: float = 0.95) -> float:
    """Combined voltage + fuel utilisation efficiency.

    η_e = (V_cell / 1.481) × U_fuel
    """
    return voltage_efficiency(cell_voltage_v) * utilisation


# ── Power density ──────────────────────────────────────────────────────

def power_density_w_per_cm2(
    cell_voltage_v: float,
    current_density_a_per_cm2: float,
) -> float:
    """P = V × j."""
    return cell_voltage_v * current_density_a_per_cm2


# ── Assessment helpers ─────────────────────────────────────────────────

_FC_DEFAULTS = {
    FuelCellType.PEMFC: {
        "temperature_k": 353.0,
        "cell_voltage_v": 0.65,
        "current_density": 1.0,
        "degradation_uv_h": 10.0,
    },
    FuelCellType.SOFC: {
        "temperature_k": 1073.0,
        "cell_voltage_v": 0.80,
        "current_density": 0.5,
        "degradation_uv_h": 5.0,
    },
    FuelCellType.AFC: {
        "temperature_k": 343.0,
        "cell_voltage_v": 0.70,
        "current_density": 0.3,
        "degradation_uv_h": 15.0,
    },
}


def assess_fuel_cell(
    cell_type: FuelCellType = FuelCellType.PEMFC,
    cell_voltage_v: float | None = None,
    current_density_a_per_cm2: float | None = None,
) -> FuelCellAssessment:
    """Quick fuel-cell assessment using default or custom parameters."""
    defaults = _FC_DEFAULTS.get(cell_type, _FC_DEFAULTS[FuelCellType.PEMFC])
    v = cell_voltage_v if cell_voltage_v is not None else defaults["cell_voltage_v"]
    j = current_density_a_per_cm2 if current_density_a_per_cm2 is not None else defaults["current_density"]
    temp = defaults["temperature_k"]

    eff_e = electric_efficiency(v)
    eff_total = eff_e * 1.15 if cell_type == FuelCellType.SOFC else eff_e
    eff_total = min(eff_total, 0.95)

    notes = []
    if eff_e > 0.60:
        notes.append("Electric efficiency above 60 % — verify polarisation curve data.")

    return FuelCellAssessment(
        cell_type=cell_type,
        cell_voltage_v=v,
        current_density_a_per_cm2=j,
        efficiency_electric=round(eff_e, 4),
        efficiency_total=round(eff_total, 4),
        degradation_rate_uv_per_h=defaults["degradation_uv_h"],
        power_density_w_per_cm2=round(power_density_w_per_cm2(v, j), 4),
        operating_temperature_k=temp,
        notes=notes,
    )


# ── Concept layers ─────────────────────────────────────────────────────

def fuel_cell_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="Fuel Cell Electrochemistry",
            description=(
                "H₂ + ½O₂ → H₂O.  Reverse of electrolysis.  "
                "Nernst OCV sets the thermodynamic ceiling."
            ),
            key_equations=[
                "E = E°(T) + (RT/2F)·ln(P_H₂·√P_O₂ / P_H₂O)",
                "η_max = ΔG/ΔH ≈ 83 % at 298 K",
            ],
        ),
        ConceptLayer(
            name="PEMFC",
            description=(
                "Operates 60–80 °C.  Fast start-up.  Main type for vehicles (FCEV).  "
                "Pt catalyst, proton-exchange membrane.  Degradation ~10 µV/h."
            ),
        ),
        ConceptLayer(
            name="SOFC",
            description=(
                "Operates 700–1000 °C.  High efficiency (>50 % electric, >80 % CHP).  "
                "Ceramic electrolyte.  Slow start-up.  Best for stationary power."
            ),
        ),
    ]
