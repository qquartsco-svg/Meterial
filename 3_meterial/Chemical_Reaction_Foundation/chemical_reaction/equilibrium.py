"""L4 — Equilibrium: where does the reaction stop?

Core equation: K_eq = exp(−ΔG° / RT)
"""

from __future__ import annotations

import math
from typing import List

from .constants import R_GAS_KJ_PER_MOL_K, STANDARD_TEMPERATURE_K
from .contracts import ConceptLayer


# ── Pedagogical axes ─────────────────────────────────────────────────────

def equilibrium_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="equilibrium_constant",
            summary="K_eq = exp(−ΔG°/RT) — position of equilibrium from thermodynamics.",
            detail=(
                "K >> 1 → products favored. K << 1 → reactants favored. "
                "K depends on temperature (van 't Hoff), NOT on concentration or catalyst."
            ),
        ),
        ConceptLayer(
            name="reaction_quotient",
            summary="Q = same expression as K but with current (non-equilibrium) concentrations.",
            detail=(
                "Q < K → reaction proceeds forward (toward products). "
                "Q > K → reaction proceeds backward (toward reactants). "
                "Q = K → system is at equilibrium."
            ),
        ),
        ConceptLayer(
            name="le_chatelier",
            summary="A system at equilibrium responds to stress by partially counteracting it.",
            detail=(
                "Add reactant → shifts toward products. Remove product → same. "
                "Increase T for exothermic rxn → shifts toward reactants. "
                "Catalyst: NO effect on equilibrium position."
            ),
        ),
    ]


# ── Computational helpers ────────────────────────────────────────────────

def equilibrium_constant(
    delta_g_standard_kj_per_mol: float,
    temperature_k: float = STANDARD_TEMPERATURE_K,
) -> float:
    """K_eq = exp(−ΔG°/RT).

    Parameters
    ----------
    delta_g_standard_kj_per_mol : standard Gibbs free energy change [kJ/mol]
    temperature_k : temperature [K]
    """
    if temperature_k <= 0:
        raise ValueError("temperature must be positive")
    exponent = -delta_g_standard_kj_per_mol / (R_GAS_KJ_PER_MOL_K * temperature_k)
    return math.exp(exponent)


def reaction_quotient(concentrations_products: list[tuple[float, float]],
                      concentrations_reactants: list[tuple[float, float]]) -> float:
    """Compute Q = Π([P]^p) / Π([R]^r).

    Each item is (concentration, stoichiometric_coefficient).
    """
    numerator = 1.0
    for conc, coeff in concentrations_products:
        if conc <= 0:
            return 0.0
        numerator *= conc ** coeff
    denominator = 1.0
    for conc, coeff in concentrations_reactants:
        if conc <= 0:
            return float("inf")
        denominator *= conc ** coeff
    if denominator == 0:
        return float("inf")
    return numerator / denominator


def le_chatelier_shift(q: float, k: float) -> str:
    """Determine direction of shift given Q and K.

    Returns ``'forward'``, ``'backward'``, or ``'at_equilibrium'``.
    """
    if abs(q - k) / max(abs(k), 1e-30) < 1e-6:
        return "at_equilibrium"
    return "forward" if q < k else "backward"


def van_t_hoff_k_at_new_temp(
    k_ref: float,
    delta_h_kj_per_mol: float,
    t_ref_k: float,
    t_new_k: float,
) -> float:
    """Estimate K at a new temperature using the van 't Hoff equation.

    ln(K2/K1) = −(ΔH°/R) · (1/T2 − 1/T1)
    """
    if t_ref_k <= 0 or t_new_k <= 0:
        raise ValueError("temperatures must be positive")
    from .constants import R_GAS_J_PER_MOL_K
    exponent = -(delta_h_kj_per_mol * 1000.0 / R_GAS_J_PER_MOL_K) * (1.0 / t_new_k - 1.0 / t_ref_k)
    return k_ref * math.exp(exponent)


def gibbs_from_k(k_eq: float, temperature_k: float = STANDARD_TEMPERATURE_K) -> float:
    """ΔG° = −RT ln K (inverse of K = exp(−ΔG°/RT))."""
    if k_eq <= 0:
        raise ValueError("K must be positive")
    return -R_GAS_KJ_PER_MOL_K * temperature_k * math.log(k_eq)
