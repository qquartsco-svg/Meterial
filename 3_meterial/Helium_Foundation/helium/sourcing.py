"""L2 — Helium sourcing (not 'production' in chemical sense)."""

from __future__ import annotations

from typing import List

from .constants import HE_NATURAL_GAS_MOL_FRACTION_TYPICAL
from .contracts import ConceptLayer, SourcingAssessment, SourcingMethod


def stripping_recovery_fraction(
    feed_he_mol_fraction: float,
    strip_efficiency: float = 0.85,
) -> float:
    """Order-of-magnitude He recovery from natural gas feed."""
    if feed_he_mol_fraction <= 0:
        return 0.0
    return min(strip_efficiency * feed_he_mol_fraction / HE_NATURAL_GAS_MOL_FRACTION_TYPICAL, 1.0)


def assess_natural_gas_sourcing(
    feed_he_mol_fraction: float = 0.002,
    energy_kwh_per_kg: float = 12.0,
) -> SourcingAssessment:
    notes: List[str] = []
    if feed_he_mol_fraction < HE_NATURAL_GAS_MOL_FRACTION_TYPICAL:
        notes.append("Lean He feed — economics marginal.")
    return SourcingAssessment(
        method=SourcingMethod.NATURAL_GAS_STRIPPING,
        he_recovery_fraction=stripping_recovery_fraction(feed_he_mol_fraction),
        energy_intensity_kwh_per_kg=energy_kwh_per_kg,
        notes=notes,
    )


def sourcing_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="Primary Source",
            description=(
                "Industrial He is overwhelmingly from natural gas fields with elevated He, "
                "plus LNG boil-off recovery. It is not synthesized at scale."
            ),
        ),
        ConceptLayer(
            name="Scarcity",
            description=(
                "He is non-renewable on human timescales; venting from MRI/LNG is a "
                "long-term supply risk. Recycling and closed-loop cryogen matter."
            ),
        ),
    ]
