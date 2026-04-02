"""Unified entry for Nitrogen_Foundation."""

from __future__ import annotations

from typing import List, Optional

from .air_separation import assess_cryogenic_separation, separation_concept_layers
from .contracts import (
    ConceptLayer,
    HealthVerdict,
    NitrogenClaimPayload,
    NitrogenFoundationReport,
    NitrogenHealthReport,
)
from .extension_hooks import extension_hooks_concept_layers
from .fixation import assess_fixation, fixation_concept_layers
from .properties import properties_concept_layers
from .screening import screen_nitrogen_claim, screening_concept_layers
from .storage import assess_ln2_storage, storage_concept_layers
from .safety import safety_concept_layers
from .domain_agriculture import agriculture_concept_layers


def collect_concept_layers() -> List[ConceptLayer]:
    layers: List[ConceptLayer] = []
    layers.extend(properties_concept_layers())
    layers.extend(separation_concept_layers())
    layers.extend(fixation_concept_layers())
    layers.extend(storage_concept_layers())
    layers.extend(safety_concept_layers())
    layers.extend(screening_concept_layers())
    layers.extend(extension_hooks_concept_layers())
    layers.extend(agriculture_concept_layers())
    return layers


def compute_health(
    separation_eff: float = 0.85,
    fixation_x_nh3: float = 0.15,
    storage_boiloff_pct: float = 0.5,
    safety_ok: bool = True,
    cost_index: float = 6.0,
    omega_safety_override: float | None = None,
) -> NitrogenHealthReport:
    omega_sep = min(separation_eff, 1.0)
    omega_fix = min(fixation_x_nh3 / 0.25, 1.0)
    omega_stor = max(1.0 - storage_boiloff_pct / 5.0, 0.0)
    omega_safe = omega_safety_override if omega_safety_override is not None else (0.85 if safety_ok else 0.30)
    omega_econ = max(1.0 - cost_index / 20.0, 0.0)
    axes = [omega_sep, omega_fix, omega_stor, omega_safe, omega_econ]
    composite = round(sum(axes) / len(axes), 3)
    warnings: List[str] = []
    if all(a > 0.90 for a in axes):
        warnings.append("All axes > 0.90 — verify Haber energy and boil-off realism.")
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
    return NitrogenHealthReport(
        omega_separation=round(omega_sep, 3),
        omega_fixation=round(omega_fix, 3),
        omega_storage=round(omega_stor, 3),
        omega_safety=round(omega_safe, 3),
        omega_economics=round(omega_econ, 3),
        composite_omega=composite,
        verdict=v,
        warnings=warnings,
    )


def run_nitrogen_foundation(claim: Optional[NitrogenClaimPayload] = None) -> NitrogenFoundationReport:
    sep = assess_cryogenic_separation()
    fix = assess_fixation()
    stor = assess_ln2_storage()
    scr = screen_nitrogen_claim(claim) if claim else None
    health = compute_health(
        storage_boiloff_pct=stor.boiloff_percent_per_day,
        fixation_x_nh3=fix.nh3_equilibrium_mole_fraction,
    )
    return NitrogenFoundationReport(
        separation=sep,
        fixation=fix,
        storage=stor,
        screening=scr,
        health=health,
        concept_layers=collect_concept_layers(),
    )
