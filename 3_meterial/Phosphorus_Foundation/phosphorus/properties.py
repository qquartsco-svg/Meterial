from __future__ import annotations

from typing import List

from .constants import P_DENSITY_G_PER_CM3_WHITE, P_MELTING_POINT_K_WHITE, P_MOLAR_MASS_G_PER_MOL
from .contracts import ConceptLayer, PProperties


def phosphorus_property_card() -> PProperties:
    return PProperties(
        molar_mass_g_per_mol=P_MOLAR_MASS_G_PER_MOL,
        density_g_per_cm3_white=P_DENSITY_G_PER_CM3_WHITE,
        melting_point_k_white=P_MELTING_POINT_K_WHITE,
    )


def properties_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="Phosphorus Core",
            description="P is essential in ATP, DNA/RNA backbone, phospholipid membranes, and fertilizer chemistry.",
        ),
    ]
