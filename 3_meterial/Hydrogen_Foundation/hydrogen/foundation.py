"""Unified entry point for Hydrogen_Foundation.

Collects all concept layers and runs a composite assessment pipeline.
"""

from __future__ import annotations

from typing import List, Optional

from .contracts import (
    ConceptLayer,
    FuelCellType,
    HealthVerdict,
    HydrogenClaimPayload,
    HydrogenFoundationReport,
    HydrogenHealthReport,
    ProductionMethod,
)
from .fuel_cell import assess_fuel_cell, fuel_cell_concept_layers
from .production import assess_electrolysis, production_concept_layers
from .properties import properties_concept_layers
from .safety import assess_safety, safety_concept_layers
from .screening import screen_hydrogen_claim, screening_concept_layers
from .storage import assess_liquid_storage, assess_compressed_storage, storage_concept_layers
from .extension_hooks import extension_hooks_concept_layers
from .domain_space import space_concept_layers
from .domain_grid import grid_concept_layers
from .domain_transport import transport_concept_layers


def collect_concept_layers() -> List[ConceptLayer]:
    """Gather all concept layers across all modules."""
    layers: List[ConceptLayer] = []
    layers.extend(properties_concept_layers())
    layers.extend(production_concept_layers())
    layers.extend(storage_concept_layers())
    layers.extend(fuel_cell_concept_layers())
    layers.extend(safety_concept_layers())
    layers.extend(screening_concept_layers())
    layers.extend(extension_hooks_concept_layers())
    layers.extend(space_concept_layers())
    layers.extend(grid_concept_layers())
    layers.extend(transport_concept_layers())
    return layers


def compute_health(
    production_eff: float = 0.0,
    storage_rte: float = 0.0,
    fc_eff: float = 0.0,
    safety_ok: bool = True,
    cost_usd_per_kg: float = 10.0,
    omega_safety_override: float | None = None,
) -> HydrogenHealthReport:
    """Compute 5-axis health report."""
    omega_prod = min(production_eff / 0.80, 1.0)
    omega_stor = min(storage_rte / 0.90, 1.0)
    omega_conv = min(fc_eff / 0.60, 1.0)
    if omega_safety_override is not None:
        omega_safe = omega_safety_override
    else:
        omega_safe = 0.85 if safety_ok else 0.30
    omega_econ = max(1.0 - cost_usd_per_kg / 20.0, 0.0)

    axes = [omega_prod, omega_stor, omega_conv, omega_safe, omega_econ]
    composite = sum(axes) / len(axes)
    composite = round(composite, 3)

    warnings: List[str] = []
    if all(a > 0.90 for a in axes):
        warnings.append("All axes > 0.90 — verify that real-world friction is included.")
    if min(axes) < 0.30:
        warnings.append(f"Weakest axis = {min(axes):.2f} — this axis dominates system fragility.")

    if composite >= 0.70 and min(axes) >= 0.40:
        verdict = HealthVerdict.HEALTHY
    elif composite >= 0.50:
        verdict = HealthVerdict.STABLE
    elif composite >= 0.30:
        verdict = HealthVerdict.FRAGILE
    else:
        verdict = HealthVerdict.CRITICAL

    return HydrogenHealthReport(
        omega_production=round(omega_prod, 3),
        omega_storage=round(omega_stor, 3),
        omega_conversion=round(omega_conv, 3),
        omega_safety=round(omega_safe, 3),
        omega_economics=round(omega_econ, 3),
        composite_omega=composite,
        verdict=verdict,
        warnings=warnings,
    )


def run_hydrogen_foundation(
    claim: Optional[HydrogenClaimPayload] = None,
    production_method: ProductionMethod = ProductionMethod.PEM_ELECTROLYSIS,
    fuel_cell_type: FuelCellType = FuelCellType.PEMFC,
    storage_type: str = "compressed",
    h2_concentration_vol_percent: float = 0.0,
) -> HydrogenFoundationReport:
    """Run the full Hydrogen Foundation pipeline.

    Returns a composite report with production, storage, fuel cell,
    safety, screening, health, and concept layers.
    """
    prod = assess_electrolysis(method=production_method)
    if storage_type == "liquid":
        stor = assess_liquid_storage()
    else:
        stor = assess_compressed_storage()
    fc = assess_fuel_cell(cell_type=fuel_cell_type)
    safe = assess_safety(h2_concentration_vol_percent=h2_concentration_vol_percent)

    screening_report = None
    if claim is not None:
        screening_report = screen_hydrogen_claim(claim)

    health = compute_health(
        production_eff=prod.efficiency,
        storage_rte=stor.round_trip_efficiency,
        fc_eff=fc.efficiency_electric,
        safety_ok=(safe.risk_level == "acceptable"),
        cost_usd_per_kg=10.0,
    )

    return HydrogenFoundationReport(
        production=prod,
        storage=stor,
        fuel_cell=fc,
        safety=safe,
        screening=screening_report,
        health=health,
        concept_layers=collect_concept_layers(),
    )
