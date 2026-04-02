from __future__ import annotations

from typing import List, Optional

from .bioenergetics import assess_atp_cycle, bioenergetics_concept_layers
from .contracts import (
    ConceptLayer,
    HealthVerdict,
    PhosphorusClaimPayload,
    PhosphorusFoundationReport,
    PhosphorusHealthReport,
)
from .extraction import assess_phosphate_rock, extraction_concept_layers
from .extension_hooks import extension_hooks_concept_layers
from .properties import properties_concept_layers
from .screening import screen_phosphorus_claim, screening_concept_layers


def collect_concept_layers() -> List[ConceptLayer]:
    layers: List[ConceptLayer] = []
    layers.extend(properties_concept_layers())
    layers.extend(extraction_concept_layers())
    layers.extend(bioenergetics_concept_layers())
    layers.extend(screening_concept_layers())
    layers.extend(extension_hooks_concept_layers())
    return layers


def compute_health(
    extraction_omega: float = 0.6,
    bio_cycle_omega: float = 0.8,
    pollution_omega: float = 0.5,
    recycling_omega: float = 0.4,
    economics_omega: float = 0.55,
) -> PhosphorusHealthReport:
    axes = [extraction_omega, bio_cycle_omega, pollution_omega, recycling_omega, economics_omega]
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

    return PhosphorusHealthReport(
        omega_extraction=round(extraction_omega, 3),
        omega_bio_cycle=round(bio_cycle_omega, 3),
        omega_pollution_control=round(pollution_omega, 3),
        omega_recycling=round(recycling_omega, 3),
        omega_economics=round(economics_omega, 3),
        composite_omega=composite,
        verdict=v,
        warnings=warnings,
    )


def run_phosphorus_foundation(claim: Optional[PhosphorusClaimPayload] = None) -> PhosphorusFoundationReport:
    ext = assess_phosphate_rock()
    bio = assess_atp_cycle()
    scr = screen_phosphorus_claim(claim) if claim else None
    health = compute_health()
    return PhosphorusFoundationReport(
        extraction=ext,
        bioenergetics=bio,
        screening=scr,
        health=health,
        concept_layers=collect_concept_layers(),
    )
