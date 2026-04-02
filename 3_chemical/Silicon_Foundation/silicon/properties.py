from __future__ import annotations

from typing import List

from .constants import SI_BANDGAP_EV_300K, SI_DENSITY_G_PER_CM3, SI_MELTING_POINT_K, SI_MOLAR_MASS_G_PER_MOL
from .contracts import ConceptLayer, SiProperties


def silicon_property_card() -> SiProperties:
    return SiProperties(
        molar_mass_g_per_mol=SI_MOLAR_MASS_G_PER_MOL,
        density_g_per_cm3=SI_DENSITY_G_PER_CM3,
        melting_point_k=SI_MELTING_POINT_K,
        bandgap_ev_300k=SI_BANDGAP_EV_300K,
    )


def properties_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(name="Silicon Core", description="Semiconductor and PV backbone; defect/yield economics dominate practical performance."),
    ]
