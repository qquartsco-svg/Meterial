"""L3 — Nitrogen fixation (Haber–Bosch cartoon)."""

from __future__ import annotations

import math
from typing import List

from .constants import HABER_DH_KJ_PER_MOL_RXN, R_GAS_J_PER_MOL_K
from .contracts import ConceptLayer, FixationAssessment


def haber_equilibrium_nh3_mole_fraction(
    temperature_k: float,
    pressure_bar: float,
    *,
    c_offset: float = -12.0,
) -> float:
    """Cartoon mole fraction of NH₃ at stoichiometric N₂:H₂ = 1:3, idealised.

    ln K ∝ −ΔH/(RT) + C; higher P shifts toward NH₃ (fewer gas moles).
    This is not a rigorous equilibrium solver — screening / pedagogy only.
    """
    if temperature_k <= 0 or pressure_bar <= 0:
        return 0.0
    dh_j = HABER_DH_KJ_PER_MOL_RXN * 1000.0
    ln_k0 = -dh_j / (R_GAS_J_PER_MOL_K * temperature_k) + c_offset
    k_eff = math.exp(ln_k0) * (pressure_bar ** 1.0)
    x = min(k_eff / (1.0 + k_eff), 0.65)
    return max(x, 0.0)


def assess_fixation(
    temperature_k: float = 700.0,
    pressure_bar: float = 200.0,
) -> FixationAssessment:
    x = haber_equilibrium_nh3_mole_fraction(temperature_k, pressure_bar)
    notes = [
        "Industrial Haber uses catalyst + recycle; this is equilibrium cartoon only.",
    ]
    return FixationAssessment(
        temperature_k=temperature_k,
        pressure_bar=pressure_bar,
        nh3_equilibrium_mole_fraction=x,
        notes=notes,
    )


def fixation_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="Haber–Bosch",
            description="N₂ + 3H₂ ⇌ 2NH₃; ties to H₂ production cost and energy.",
            key_equations=["Higher P favors NH₃; lower T favors exothermic product (kinetics trade off)."],
        ),
    ]
