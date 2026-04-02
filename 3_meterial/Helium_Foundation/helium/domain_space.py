"""Domain — space / balloons / cryogen coupling."""

from __future__ import annotations

from typing import List

from .constants import HE_MOLAR_MASS_G_PER_MOL, R_GAS_J_PER_MOL_K, STANDARD_TEMPERATURE_K
from .contracts import ConceptLayer


def balloon_lift_n_per_m3(
    air_density_kg_per_m3: float = 1.225,
    he_density_kg_per_m3: float | None = None,
) -> float:
    """Net buoyancy per m³ of displaced air (ideal, dry air)."""
    if he_density_kg_per_m3 is None:
        p = 101_325.0
        m = HE_MOLAR_MASS_G_PER_MOL / 1000.0
        he_density_kg_per_m3 = p * m / (R_GAS_J_PER_MOL_K * STANDARD_TEMPERATURE_K)
    return (air_density_kg_per_m3 - he_density_kg_per_m3) * 9.81


def space_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="High-Altitude Balloons",
            description="He lift vs H₂ — safer but lower lift per m³; venting and boil-off matter.",
        ),
    ]
