from __future__ import annotations

from typing import List, Optional

from .contracts import (
    ConceptLayer,
    DomainMode,
    HealthVerdict,
    SiliconClaimPayload,
    SiliconFoundationReport,
    SiliconHealthReport,
)
from .device import assess_logic_device, assess_pv_device, device_concept_layers
from .extension_hooks import extension_hooks_concept_layers
from .properties import properties_concept_layers
from .refining import assess_siemens_refining, refining_concept_layers
from .screening import screen_silicon_claim, screening_concept_layers


def collect_concept_layers() -> List[ConceptLayer]:
    layers: List[ConceptLayer] = []
    layers.extend(properties_concept_layers())
    layers.extend(refining_concept_layers())
    layers.extend(device_concept_layers())
    layers.extend(screening_concept_layers())
    layers.extend(extension_hooks_concept_layers())
    return layers


def compute_health(
    refining_omega: float = 0.6,
    device_omega: float = 0.7,
    yield_omega: float = 0.65,
    thermal_omega: float = 0.6,
    economics_omega: float = 0.55,
) -> SiliconHealthReport:
    axes = [refining_omega, device_omega, yield_omega, thermal_omega, economics_omega]
    composite = round(sum(axes) / len(axes), 3)
    warnings: List[str] = []
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

    return SiliconHealthReport(
        omega_refining=round(refining_omega, 3),
        omega_device_performance=round(device_omega, 3),
        omega_yield=round(yield_omega, 3),
        omega_thermal=round(thermal_omega, 3),
        omega_economics=round(economics_omega, 3),
        composite_omega=composite,
        verdict=v,
        warnings=warnings,
    )


def run_silicon_foundation(
    claim: Optional[SiliconClaimPayload] = None,
    domain: DomainMode = DomainMode.PHOTOVOLTAIC,
) -> SiliconFoundationReport:
    ref = assess_siemens_refining()
    dev = assess_pv_device() if domain == DomainMode.PHOTOVOLTAIC else assess_logic_device()
    scr = screen_silicon_claim(claim) if claim else None
    health = compute_health(
        refining_omega=min(ref.purity_six_nines_fraction / 0.999999, 1.0),
        device_omega=dev.efficiency_fraction,
        yield_omega=max(1.0 - dev.defect_density_cm2 / 2e5, 0.0),
        thermal_omega=max(min(dev.thermal_margin_c / 50.0, 1.0), 0.0),
        economics_omega=0.55,
    )
    return SiliconFoundationReport(
        refining=ref,
        device=dev,
        screening=scr,
        health=health,
        concept_layers=collect_concept_layers(),
    )
