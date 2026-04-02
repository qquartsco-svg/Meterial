"""L2 — Hydrogen production pathways.

Core question: *How is H₂ made, and at what cost?*

Pathways modelled (tree-level):
  - Water electrolysis (PEM / alkaline / SOEC)
  - Steam methane reforming (SMR)
  - Autothermal reforming (ATR)
  - Colour-code classification
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
    THERMONEUTRAL_VOLTAGE_V,
    WATER_ELECTROLYSIS_E0_V,
    WATER_FORMATION_DH_KJ_PER_MOL,
)
from .contracts import (
    ColorCode,
    ConceptLayer,
    ProductionAssessment,
    ProductionMethod,
)


# ── Electrolysis ───────────────────────────────────────────────────────

def electrolysis_cell_voltage(
    current_density_a_per_cm2: float = 1.0,
    *,
    ohmic_resistance_ohm_cm2: float = 0.15,
    activation_overpotential_v: float = 0.3,
    temperature_k: float = STANDARD_TEMPERATURE_K,
) -> float:
    """Approximate operating cell voltage for water electrolysis.

    V_cell = E_rev(T) + η_act + j × R_ohm

    This is a *cartoon model* — enough to rank pathways
    but not a detailed polarisation curve.
    """
    e_rev = WATER_ELECTROLYSIS_E0_V - 8.5e-4 * (temperature_k - 298.15)
    return e_rev + activation_overpotential_v + current_density_a_per_cm2 * ohmic_resistance_ohm_cm2


def electrolysis_h2_rate_mol_per_s(
    current_a: float,
    faradaic_efficiency: float = 1.0,
    n_electrons: int = 2,
) -> float:
    """Faraday's law: mol_H2/s = η_F × I / (n × F)."""
    return faradaic_efficiency * current_a / (n_electrons * FARADAY_C_PER_MOL)


def electrolysis_efficiency(
    cell_voltage_v: float,
    faradaic_efficiency: float = 1.0,
) -> float:
    """Voltage efficiency × faradaic efficiency.

    η = (E°_rev / V_cell) × η_F
    """
    if cell_voltage_v <= 0:
        return 0.0
    return (WATER_ELECTROLYSIS_E0_V / cell_voltage_v) * faradaic_efficiency


def electrolysis_energy_kwh_per_kg_h2(
    cell_voltage_v: float,
    faradaic_efficiency: float = 1.0,
) -> float:
    """Specific energy consumption for water electrolysis.

    E_spec = (n × F × V_cell) / (M_H2 × η_F)   [J/g → kWh/kg]
    """
    n = 2
    j_per_mol = n * FARADAY_C_PER_MOL * cell_voltage_v / faradaic_efficiency
    j_per_kg = j_per_mol / (H2_MOLAR_MASS_G_PER_MOL / 1000.0)
    return j_per_kg / 3.6e6


# ── SMR ────────────────────────────────────────────────────────────────

def smr_equilibrium_constant(temperature_k: float) -> float:
    """Approximate K_eq for CH₄ + H₂O ⇌ CO + 3H₂.

    Uses a simplified van't Hoff form:
        ln K = −ΔH°/(R·T) + C
    ΔH° ≈ +206 kJ/mol  (strongly endothermic).
    """
    dh = 206_000.0  # J/mol
    c = 30.0        # fitted offset for order-of-magnitude
    return math.exp(-dh / (R_GAS_J_PER_MOL_K * temperature_k) + c)


def smr_co2_intensity_kg_per_kg_h2(
    with_ccs: bool = False,
    capture_rate: float = 0.90,
) -> float:
    """Order-of-magnitude CO₂ intensity for SMR.

    Without CCS: ~9–12 kg CO₂ / kg H₂.
    With CCS at 90 % capture: ~1 kg CO₂ / kg H₂.
    """
    baseline = 10.0  # kg CO₂ per kg H₂
    if with_ccs:
        return baseline * (1.0 - capture_rate)
    return baseline


# ── Colour code ────────────────────────────────────────────────────────

def classify_color(
    method: ProductionMethod,
    electricity_renewable: bool = False,
    ccs_attached: bool = False,
) -> ColorCode:
    """Assign a hydrogen colour code based on production context."""
    if method in (
        ProductionMethod.PEM_ELECTROLYSIS,
        ProductionMethod.ALKALINE_ELECTROLYSIS,
        ProductionMethod.SOEC_ELECTROLYSIS,
    ):
        if electricity_renewable:
            return ColorCode.GREEN
        return ColorCode.YELLOW
    if method == ProductionMethod.SMR:
        return ColorCode.BLUE if ccs_attached else ColorCode.GREY
    if method == ProductionMethod.ATR:
        return ColorCode.BLUE if ccs_attached else ColorCode.GREY
    return ColorCode.WHITE


# ── Assessment helper ──────────────────────────────────────────────────

def assess_electrolysis(
    current_a: float = 1000.0,
    cell_voltage_v: float | None = None,
    faradaic_efficiency: float = 0.98,
    method: ProductionMethod = ProductionMethod.PEM_ELECTROLYSIS,
    electricity_renewable: bool = True,
) -> ProductionAssessment:
    """Quick assessment for an electrolysis system."""
    if cell_voltage_v is None:
        cell_voltage_v = electrolysis_cell_voltage()
    eff = electrolysis_efficiency(cell_voltage_v, faradaic_efficiency)
    h2_mol_s = electrolysis_h2_rate_mol_per_s(current_a, faradaic_efficiency)
    h2_kg_s = h2_mol_s * H2_MOLAR_MASS_G_PER_MOL / 1000.0
    power_kw = current_a * cell_voltage_v / 1000.0
    water_l_per_kg_h2 = 9.0  # stoichiometric: 9 L/kg, real ~10–15

    notes = []
    if eff > 0.85:
        notes.append("Efficiency > 85 % — check whether ohmic + activation losses are realistic.")
    color = classify_color(method, electricity_renewable=electricity_renewable)

    return ProductionAssessment(
        method=method,
        color_code=color,
        h2_rate_mol_per_s=h2_mol_s,
        energy_input_kw=power_kw,
        efficiency=eff,
        co2_intensity_kg_per_kg_h2=0.0 if electricity_renewable else 0.5,
        water_consumption_l_per_kg_h2=water_l_per_kg_h2,
        notes=notes,
    )


def assess_smr(
    ch4_feed_mol_per_s: float = 1.0,
    temperature_k: float = 1100.0,
    with_ccs: bool = False,
) -> ProductionAssessment:
    """Quick assessment for steam methane reforming."""
    k_eq = smr_equilibrium_constant(temperature_k)
    conversion = min(k_eq / (1.0 + k_eq), 0.95)
    h2_mol_s = ch4_feed_mol_per_s * 3.0 * conversion
    h2_kg_s = h2_mol_s * H2_MOLAR_MASS_G_PER_MOL / 1000.0
    energy_input_kw = ch4_feed_mol_per_s * 206.0 / conversion if conversion > 0 else 0
    eff_thermal = 0.65 if not with_ccs else 0.56  # CCS parasitic load

    return ProductionAssessment(
        method=ProductionMethod.SMR,
        color_code=classify_color(ProductionMethod.SMR, ccs_attached=with_ccs),
        h2_rate_mol_per_s=h2_mol_s,
        energy_input_kw=energy_input_kw,
        efficiency=eff_thermal,
        co2_intensity_kg_per_kg_h2=smr_co2_intensity_kg_per_kg_h2(with_ccs),
        water_consumption_l_per_kg_h2=4.5,
        notes=[
            f"K_eq(T={temperature_k:.0f} K) ≈ {k_eq:.2e}",
            f"Approximate conversion: {conversion:.1%}",
        ],
    )


# ── Concept layers ─────────────────────────────────────────────────────

def production_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="Water Electrolysis",
            description=(
                "2H₂O → 2H₂ + O₂.  E°_rev = 1.229 V at 298 K.  "
                "Real cell voltages are 1.6–2.0 V due to ohmic and activation losses."
            ),
            key_equations=[
                "V_cell = E_rev + η_act + j·R_ohm",
                "ṁ_H₂ = η_F · I / (n·F)",
                "η = E°_rev / V_cell × η_F",
            ],
        ),
        ConceptLayer(
            name="Steam Methane Reforming (SMR)",
            description=(
                "CH₄ + H₂O ⇌ CO + 3H₂  (ΔH = +206 kJ/mol).  "
                "Dominant industrial route (~95 % of global H₂ production).  "
                "Emits ~10 kg CO₂ per kg H₂ without CCS."
            ),
            key_equations=[
                "K_eq = exp(−ΔH°/RT + C)",
                "CO₂ intensity: ~10 kg/kg_H₂ (grey), ~1 kg/kg_H₂ (blue w/ CCS)",
            ],
        ),
        ConceptLayer(
            name="Colour Code Taxonomy",
            description=(
                "Green = renewable electrolysis, Blue = SMR+CCS, Grey = SMR, "
                "Pink = nuclear electrolysis, Turquoise = methane pyrolysis."
            ),
        ),
    ]
