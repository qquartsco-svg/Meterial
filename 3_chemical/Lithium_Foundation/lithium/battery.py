from __future__ import annotations

from typing import List

from .constants import LI_ION_CELL_NOMINAL_V
from .contracts import BatteryAssessment, BatteryChemistry, ConceptLayer


def assess_battery_chemistry(chem: BatteryChemistry = BatteryChemistry.LFP) -> BatteryAssessment:
    if chem == BatteryChemistry.LFP:
        return BatteryAssessment(
            chemistry=chem,
            nominal_voltage_v=3.2,
            specific_energy_wh_per_kg=160.0,
            cycle_life_80pct=3500,
            thermal_runaway_risk="low",
            notes=["Safer thermal profile, lower specific energy than NMC/NCA."],
        )
    if chem == BatteryChemistry.NMC:
        return BatteryAssessment(
            chemistry=chem,
            nominal_voltage_v=3.7,
            specific_energy_wh_per_kg=230.0,
            cycle_life_80pct=1800,
            thermal_runaway_risk="medium",
            notes=["Higher energy density, tighter thermal management needed."],
        )
    return BatteryAssessment(
        chemistry=chem,
        nominal_voltage_v=LI_ION_CELL_NOMINAL_V,
        specific_energy_wh_per_kg=200.0,
        cycle_life_80pct=1500,
        thermal_runaway_risk="medium",
        notes=["Default fallback."],
    )


def battery_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(name="Li-ion Trade-offs", description="Specific energy, cycle life, and safety form a constrained design triangle."),
    ]
