"""Unified entry for Helium_Foundation."""

from __future__ import annotations

from typing import List, Optional

from .contracts import (
    ConceptLayer,
    HealthVerdict,
    HeliumClaimPayload,
    HeliumFoundationReport,
    HeliumHealthReport,
)
from .extension_hooks import extension_hooks_concept_layers
from .properties import properties_concept_layers
from .screening import screen_helium_claim, screening_concept_layers
from .sourcing import assess_natural_gas_sourcing, sourcing_concept_layers
from .storage import assess_liquid_storage, storage_concept_layers
from .safety import safety_concept_layers
from .domain_space import space_concept_layers


def collect_concept_layers() -> List[ConceptLayer]:
    layers: List[ConceptLayer] = []
    layers.extend(properties_concept_layers())
    layers.extend(sourcing_concept_layers())
    layers.extend(storage_concept_layers())
    layers.extend(safety_concept_layers())
    layers.extend(screening_concept_layers())
    layers.extend(extension_hooks_concept_layers())
    layers.extend(space_concept_layers())
    return layers


def compute_health(
    sourcing_frac: float = 0.5,
    storage_rte: float = 0.85,
    utilization: float = 0.7,
    safety_ok: bool = True,
    cost_index: float = 5.0,
    omega_safety_override: float | None = None,
) -> HeliumHealthReport:
    omega_src = min(sourcing_frac, 1.0)
    omega_stor = min(storage_rte / 0.90, 1.0)
    omega_util = min(utilization / 0.80, 1.0)
    omega_safe = omega_safety_override if omega_safety_override is not None else (0.85 if safety_ok else 0.30)
    omega_econ = max(1.0 - cost_index / 15.0, 0.0)
    axes = [omega_src, omega_stor, omega_util, omega_safe, omega_econ]
    composite = round(sum(axes) / len(axes), 3)
    warnings: List[str] = []
    if all(a > 0.90 for a in axes):
        warnings.append("All axes > 0.90 — verify real-world friction (He scarcity, boil-off).")
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
    return HeliumHealthReport(
        omega_sourcing=round(omega_src, 3),
        omega_storage=round(omega_stor, 3),
        omega_utilization=round(omega_util, 3),
        omega_safety=round(omega_safe, 3),
        omega_economics=round(omega_econ, 3),
        composite_omega=composite,
        verdict=v,
        warnings=warnings,
    )


def run_helium_foundation(claim: Optional[HeliumClaimPayload] = None) -> HeliumFoundationReport:
    src = assess_natural_gas_sourcing()
    stor = assess_liquid_storage()
    scr = screen_helium_claim(claim) if claim else None
    health = compute_health(
        sourcing_frac=src.he_recovery_fraction,
        storage_rte=stor.round_trip_efficiency,
        utilization=0.75,
        safety_ok=True,
    )
    return HeliumFoundationReport(
        sourcing=src,
        storage=stor,
        screening=scr,
        health=health,
        concept_layers=collect_concept_layers(),
    )
