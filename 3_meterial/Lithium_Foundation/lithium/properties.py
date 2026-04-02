from __future__ import annotations

from typing import List

from .constants import LI_DENSITY_G_PER_CM3, LI_MELTING_POINT_K, LI_MOLAR_MASS_G_PER_MOL
from .contracts import ConceptLayer, LiProperties


def lithium_property_card() -> LiProperties:
    return LiProperties(
        molar_mass_g_per_mol=LI_MOLAR_MASS_G_PER_MOL,
        density_g_per_cm3=LI_DENSITY_G_PER_CM3,
        melting_point_k=LI_MELTING_POINT_K,
    )


def properties_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="Light Alkali Metal",
            description="Low density, high electrochemical potential; key for high specific energy batteries.",
        ),
    ]
