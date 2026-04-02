from __future__ import annotations

from typing import List, Optional

from .battery import assess_battery_chemistry, battery_concept_layers
from .contracts import (
    BatteryChemistry,
    ConceptLayer,
    HealthVerdict,
    LithiumClaimPayload,
    LithiumFoundationReport,
    LithiumHealthReport,
)
from .extraction import assess_brine_extraction, extraction_concept_layers
from .extension_hooks import extension_hooks_concept_layers
from .properties import properties_concept_layers
from .screening import screen_lithium_claim, screening_concept_layers


def collect_concept_layers() -> List[ConceptLayer]:
    layers: List[ConceptLayer] = []
    layers.extend(properties_concept_layers())
    layers.extend(extraction_concept_layers())
    layers.extend(battery_concept_layers())
    layers.extend(screening_concept_layers())
    layers.extend(extension_hooks_concept_layers())
    return layers


def compute_health(
    extraction_omega: float = 0.6,
    battery_omega: float = 0.7,
    safety_ok: bool = True,
    recycling_omega: float = 0.4,
    economics_omega: float = 0.6,
) -> LithiumHealthReport:
    omega_safe = 0.85 if safety_ok else 0.30
    axes = [extraction_omega, battery_omega, omega_safe, recycling_omega, economics_omega]
    composite = round(sum(axes) / len(axes), 3)
    warnings: List[str] = []
    if all(a > 0.90 for a in axes):
        warnings.append("All axes > 0.90 — check if degradation/recycling friction is modeled.")
    if min(axes) < 0.30:
        warnings.append(f"Weakest axis = {min(axes):.2f}")

    if composite >= 0.70 and min(axes) >= 0.40:
        v = HealthVerdict.HEALTHY
    elif composite >= 0.50:
        v = HealthVerdict.STABLE
    elif composite >= 0.30:
        v = HealthVerdict.FRAGILE
    else:
        v = HealthVerdict.CRITICAL

    return LithiumHealthReport(
        omega_extraction=round(extraction_omega, 3),
        omega_battery_performance=round(battery_omega, 3),
        omega_safety=round(omega_safe, 3),
        omega_recycling=round(recycling_omega, 3),
        omega_economics=round(economics_omega, 3),
        composite_omega=composite,
        verdict=v,
        warnings=warnings,
    )


def run_lithium_foundation(
    claim: Optional[LithiumClaimPayload] = None,
    chemistry: BatteryChemistry = BatteryChemistry.LFP,
) -> LithiumFoundationReport:
    ext = assess_brine_extraction()
    batt = assess_battery_chemistry(chemistry)
    scr = screen_lithium_claim(claim) if claim else None

    health = compute_health(
        extraction_omega=0.65,
        battery_omega=min(batt.specific_energy_wh_per_kg / 250.0, 1.0),
        safety_ok=(batt.thermal_runaway_risk != "high"),
        recycling_omega=0.45,
        economics_omega=0.60,
    )

    return LithiumFoundationReport(
        extraction=ext,
        battery=batt,
        screening=scr,
        health=health,
        concept_layers=collect_concept_layers(),
    )
