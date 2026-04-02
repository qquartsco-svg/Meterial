"""L3 — Kinetics: how fast does the reaction proceed?

Core equation: k = A · exp(−Ea / RT)  (Arrhenius)
"""

from __future__ import annotations

import math
from typing import List

from .constants import R_GAS_J_PER_MOL_K, R_GAS_KJ_PER_MOL_K
from .contracts import ConceptLayer, KineticState


# ── Pedagogical axes ─────────────────────────────────────────────────────

def kinetic_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="arrhenius",
            summary="k = A·exp(−Ea/RT) — rate constant depends on temperature and activation energy.",
            detail=(
                "A = pre-exponential (frequency) factor. "
                "Ea = activation energy [kJ/mol]. "
                "Higher T or lower Ea → faster reaction."
            ),
        ),
        ConceptLayer(
            name="rate_law",
            summary="r = k·[A]^a·[B]^b — rate depends on concentrations raised to their orders.",
            detail=(
                "Order is determined experimentally, not from stoichiometry. "
                "Zero-order: r = k (independent of concentration). "
                "First-order: r = k[A]. Second-order: r = k[A]^2 or k[A][B]."
            ),
        ),
        ConceptLayer(
            name="half_life",
            summary="Time for reactant concentration to halve.",
            detail=(
                "First-order: t½ = ln2/k (independent of [A]₀). "
                "Second-order: t½ = 1/(k·[A]₀). "
                "Zero-order: t½ = [A]₀/(2k)."
            ),
        ),
        ConceptLayer(
            name="catalyst",
            summary="A catalyst lowers Ea without being consumed.",
            detail=(
                "Catalysts do NOT change ΔG or equilibrium position. "
                "They only provide an alternative reaction pathway with lower Ea. "
                "This is a key ATHENA screening point: any claim that a catalyst "
                "'shifts equilibrium' is incorrect."
            ),
        ),
    ]


# ── Computational helpers ────────────────────────────────────────────────

def arrhenius_rate_constant(
    pre_exponential_a: float,
    activation_energy_kj_per_mol: float,
    temperature_k: float,
) -> float:
    """Arrhenius rate constant k = A·exp(−Ea/RT).

    Parameters
    ----------
    pre_exponential_a : frequency factor A [same units as k]
    activation_energy_kj_per_mol : Ea [kJ/mol]
    temperature_k : absolute temperature [K]
    """
    if temperature_k <= 0:
        raise ValueError("temperature_k must be positive")
    exponent = -(activation_energy_kj_per_mol * 1000.0) / (R_GAS_J_PER_MOL_K * temperature_k)
    return pre_exponential_a * math.exp(exponent)


def half_life(k: float, order: float, initial_conc: float = 1.0) -> float:
    """Calculate half-life for a given reaction order.

    Supports order 0, 1, and 2. Other orders raise ValueError.
    """
    if k <= 0:
        raise ValueError("rate constant k must be positive")
    if abs(order - 0.0) < 1e-9:
        if initial_conc <= 0:
            raise ValueError("initial_conc required for zero-order")
        return initial_conc / (2.0 * k)
    elif abs(order - 1.0) < 1e-9:
        return math.log(2.0) / k
    elif abs(order - 2.0) < 1e-9:
        if initial_conc <= 0:
            raise ValueError("initial_conc required for second-order")
        return 1.0 / (k * initial_conc)
    raise ValueError(f"half_life not implemented for order={order}")


def rate_law(k: float, concentrations: list[float], orders: list[float]) -> float:
    """Compute reaction rate r = k · Π([Ci]^ni).

    Parameters
    ----------
    k : rate constant
    concentrations : list of reactant concentrations [mol/L]
    orders : list of reaction orders (same length as concentrations)
    """
    if len(concentrations) != len(orders):
        raise ValueError("concentrations and orders must have same length")
    rate = k
    for conc, n in zip(concentrations, orders):
        if conc < 0:
            raise ValueError("concentration cannot be negative")
        rate *= conc ** n
    return rate


def catalyst_ea_reduction(
    ea_uncatalyzed_kj: float,
    ea_catalyzed_kj: float,
) -> float:
    """Return fractional reduction of Ea by a catalyst (0–1)."""
    if ea_uncatalyzed_kj <= 0:
        return 0.0
    reduction = (ea_uncatalyzed_kj - ea_catalyzed_kj) / ea_uncatalyzed_kj
    return max(0.0, min(1.0, reduction))


def temperature_rate_ratio(
    ea_kj_per_mol: float,
    t1_k: float,
    t2_k: float,
) -> float:
    """Ratio k(T2)/k(T1) from Arrhenius — how much faster at T2 vs T1."""
    if t1_k <= 0 or t2_k <= 0:
        raise ValueError("temperatures must be positive")
    exponent = (ea_kj_per_mol * 1000.0 / R_GAS_J_PER_MOL_K) * (1.0 / t1_k - 1.0 / t2_k)
    return math.exp(exponent)


def assess_kinetic_state(
    pre_exponential_a: float,
    activation_energy_kj_per_mol: float,
    temperature_k: float,
    order: float = 1.0,
    initial_conc: float = 1.0,
    catalyst_effect: str = "none",
) -> KineticState:
    """Build a kinetic state assessment."""
    k = arrhenius_rate_constant(pre_exponential_a, activation_energy_kj_per_mol, temperature_k)
    try:
        hl = half_life(k, order, initial_conc)
    except ValueError:
        hl = None
    return KineticState(
        rate_constant_k=k,
        order=order,
        half_life_s=hl,
        catalyst_effect=catalyst_effect,
    )
