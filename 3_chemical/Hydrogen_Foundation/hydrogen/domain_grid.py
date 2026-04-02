"""Domain mapping — Grid-scale energy storage.

Bridges Hydrogen_Foundation to PROMETHEUS_LAYER, Battery_Dynamics_Engine,
and Token_Dynamics_Foundation (energy token).

Key topics:
  - Power-to-Gas (P2G): excess renewable → electrolyser → H₂ storage → fuel cell
  - Seasonal storage (vs batteries for short-duration)
  - H₂ blending in natural gas pipelines
"""

from __future__ import annotations

from typing import List

from .contracts import ConceptLayer


def round_trip_efficiency_p2g(
    electrolyser_eff: float = 0.65,
    storage_loss_fraction: float = 0.05,
    fuel_cell_eff: float = 0.50,
) -> float:
    """Round-trip efficiency for Power-to-Gas-to-Power.

    η_rt = η_elec × (1 − loss) × η_fc
    Typical: 0.65 × 0.95 × 0.50 ≈ 31 %.
    """
    return electrolyser_eff * (1.0 - storage_loss_fraction) * fuel_cell_eff


def levelised_cost_of_hydrogen_usd_per_kg(
    electricity_cost_usd_per_kwh: float = 0.03,
    energy_consumption_kwh_per_kg: float = 55.0,
    capex_usd_per_kw: float = 1200.0,
    capacity_factor: float = 0.40,
    stack_lifetime_h: float = 80_000.0,
    o_and_m_fraction: float = 0.03,
) -> float:
    """Simplified LCOH estimate.

    LCOH ≈ electricity_cost × kWh/kg + annualised_capex / annual_production + O&M.
    """
    annual_hours = 8760 * capacity_factor
    annual_production_kg = annual_hours * (1.0 / energy_consumption_kwh_per_kg) * 1000.0
    lifetime_years = stack_lifetime_h / (8760 * capacity_factor)
    if lifetime_years <= 0 or annual_production_kg <= 0:
        return float("inf")
    annualised_capex = capex_usd_per_kw / lifetime_years
    capex_per_kg = annualised_capex * 1000.0 / annual_production_kg
    elec_per_kg = electricity_cost_usd_per_kwh * energy_consumption_kwh_per_kg
    om_per_kg = o_and_m_fraction * capex_per_kg
    return elec_per_kg + capex_per_kg + om_per_kg


def grid_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="Power-to-Gas (P2G)",
            description=(
                "Converts curtailed renewable electricity to H₂.  "
                "Round-trip efficiency ~30 % — worse than batteries for short-duration, "
                "but competitive for seasonal (weeks-to-months) storage."
            ),
            key_equations=[
                "η_rt = η_elec × (1 − loss) × η_fc",
            ],
        ),
        ConceptLayer(
            name="Levelised Cost of Hydrogen (LCOH)",
            description=(
                "Depends on electricity cost (dominant for electrolysis), "
                "electrolyser CAPEX, capacity factor, and stack lifetime.  "
                "Target: <$2/kg for competitiveness with grey H₂."
            ),
            key_equations=[
                "LCOH ≈ e_cost × kWh/kg + CAPEX_annualised / production + O&M",
            ],
        ),
    ]
