"""Unified entry for Oxygen_Foundation."""

from __future__ import annotations

from typing import List, Optional

from .contracts import (
    ConceptLayer,
    HealthVerdict,
    OxygenClaimPayload,
    OxygenFoundationReport,
    OxygenHealthReport,
)
from .extension_hooks import extension_hooks_concept_layers
from .production import assess_cryogenic_o2, production_concept_layers
from .properties import properties_concept_layers
from .safety import fire_severity_index, safety_concept_layers
from .screening import screen_oxygen_claim, screening_concept_layers
from .storage import assess_lox_storage, storage_concept_layers
from .domain_space import space_concept_layers


def collect_concept_layers() -> List[ConceptLayer]:
    layers: List[ConceptLayer] = []
    layers.extend(properties_concept_layers())
    layers.extend(production_concept_layers())
    layers.extend(storage_concept_layers())
    layers.extend(safety_concept_layers())
    layers.extend(screening_concept_layers())
    layers.extend(extension_hooks_concept_layers())
    layers.extend(space_concept_layers())
    return layers


def compute_health(
    production_eff: float = 0.85,
    storage_boiloff_pct: float = 0.5,
    o2_vol_percent_ambient: float = 21.0,
    safety_ok: bool = True,
    cost_index: float = 6.0,
    omega_safety_override: float | None = None,
) -> OxygenHealthReport:
    omega_prod = min(production_eff, 1.0)
    omega_stor = max(1.0 - storage_boiloff_pct / 5.0, 0.0)
    omega_ox = 1.0 - fire_severity_index(o2_vol_percent_ambient)
    omega_safe = omega_safety_override if omega_safety_override is not None else (0.85 if safety_ok else 0.30)
    omega_econ = max(1.0 - cost_index / 20.0, 0.0)
    axes = [omega_prod, omega_stor, omega_ox, omega_safe, omega_econ]
    composite = round(sum(axes) / len(axes), 3)
    warnings: List[str] = []
    if all(a > 0.90 for a in axes):
        warnings.append("All axes > 0.90 — verify LOX boil-off and oxidiser fire realism.")
    if min(axes) < 0.30:
        warnings.append(f"Weakest axis = {min(axes):.2f}.")
    if composite >= 0.70 and min(axes) >= 0.40:
        v = HealthVerdict.HEALTHY
    elif composite >= 0.50:
        v = HealthVerdict.STABLE
    elif composite >= 0.30:
        v = HealthVerdict.FRAGILE
    else:
        v = HealthVerdict.CRITICAL
    return OxygenHealthReport(
        omega_production=round(omega_prod, 3),
        omega_storage=round(omega_stor, 3),
        omega_oxidation_risk=round(omega_ox, 3),
        omega_safety=round(omega_safe, 3),
        omega_economics=round(omega_econ, 3),
        composite_omega=composite,
        verdict=v,
        warnings=warnings,
    )


def run_oxygen_foundation(claim: Optional[OxygenClaimPayload] = None) -> OxygenFoundationReport:
    prod = assess_cryogenic_o2()
    stor = assess_lox_storage()
    scr = screen_oxygen_claim(claim) if claim else None
    health = compute_health(storage_boiloff_pct=stor.boiloff_percent_per_day)
    return OxygenFoundationReport(
        production=prod,
        storage=stor,
        screening=scr,
        health=health,
        concept_layers=collect_concept_layers(),
    )
