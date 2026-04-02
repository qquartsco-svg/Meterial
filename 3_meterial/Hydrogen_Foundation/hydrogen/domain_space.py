"""Domain mapping — Space / Aerospace applications.

Bridges Hydrogen_Foundation to TerraCore_Stack, Satellite_Design_Stack,
and LaunchVehicle_Stack.

Key space-hydrogen topics:
  - LOX/LH₂ rocket propellant
  - ISS / habitat life-support electrolysis
  - In-situ resource utilisation (ISRU) on Mars / Moon
"""

from __future__ import annotations

from typing import List

from .contracts import ConceptLayer


def lox_lh2_specific_impulse_s(
    mixture_ratio: float = 6.0,
    chamber_pressure_mpa: float = 10.0,
) -> float:
    """Rough specific impulse for LOX/LH₂ engine.

    Typical range: 420–465 s (vacuum).
    This is a coarse parametric fit, not a thermochemistry code.
    """
    isp_base = 450.0
    mr_penalty = abs(mixture_ratio - 6.0) * 3.0
    pc_bonus = min((chamber_pressure_mpa - 5.0) * 0.5, 10.0) if chamber_pressure_mpa > 5.0 else 0.0
    return max(isp_base - mr_penalty + pc_bonus, 380.0)


def isru_water_electrolysis_power_kw(
    h2_demand_kg_per_day: float,
    cell_voltage_v: float = 1.8,
    faradaic_efficiency: float = 0.90,
) -> float:
    """Power needed to produce H₂ demand from water electrolysis on Mars/Moon.

    P = (demand_mol/s) × n × F × V_cell / η_F
    """
    from .constants import FARADAY_C_PER_MOL, H2_MOLAR_MASS_G_PER_MOL

    mol_per_s = (h2_demand_kg_per_day * 1000.0 / H2_MOLAR_MASS_G_PER_MOL) / 86400.0
    return mol_per_s * 2 * FARADAY_C_PER_MOL * cell_voltage_v / (faradaic_efficiency * 1000.0)


def space_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="LOX/LH₂ Propellant",
            description=(
                "Highest Isp (~450 s vac) among chemical propellants.  "
                "Used in RS-25 (Shuttle), Vulcain (Ariane), LE-7 (H-IIA).  "
                "Handling complexity: cryogenic, low density, boil-off in long missions."
            ),
            key_equations=["Isp ≈ 450 s (LOX/LH₂, vacuum)"],
        ),
        ConceptLayer(
            name="Life-Support Electrolysis",
            description=(
                "ISS Oxygen Generation System splits water → O₂ + H₂.  "
                "H₂ vented or fed to Sabatier reactor (CO₂ + 4H₂ → CH₄ + 2H₂O).  "
                "Bridges to TerraCore_Stack.hydrosphere."
            ),
        ),
        ConceptLayer(
            name="ISRU (Mars / Moon)",
            description=(
                "Mars: CO₂ atmosphere + water ice → O₂ + H₂ (MOXIE-class).  "
                "Moon: regolith ilmenite reduction (FeTiO₃ + H₂ → Fe + TiO₂ + H₂O).  "
                "Power requirement dominates feasibility."
            ),
        ),
    ]
