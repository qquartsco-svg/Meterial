"""L2 — Thermodynamics: is this reaction energetically favorable?

Core equation: ΔG = ΔH − TΔS
"""

from __future__ import annotations

from typing import List

from .constants import R_GAS_KJ_PER_MOL_K, STANDARD_TEMPERATURE_K
from .contracts import ConceptLayer, Reaction, ThermodynamicState


# ── Pedagogical axes ─────────────────────────────────────────────────────

def thermodynamic_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="gibbs_free_energy",
            summary="ΔG = ΔH − TΔS  — the master criterion for spontaneity.",
            detail=(
                "ΔG < 0 → spontaneous (exergonic). ΔG > 0 → non-spontaneous (endergonic, "
                "external energy required). ΔG = 0 → equilibrium. "
                "Note: ΔG < 0 does NOT guarantee fast reaction — kinetics is separate."
            ),
        ),
        ConceptLayer(
            name="enthalpy",
            summary="ΔH — heat exchanged at constant pressure.",
            detail=(
                "ΔH < 0 → exothermic (releases heat). ΔH > 0 → endothermic (absorbs heat). "
                "Can be estimated from bond energies: ΔH ≈ Σ(broken) − Σ(formed)."
            ),
        ),
        ConceptLayer(
            name="entropy",
            summary="ΔS — change in disorder / number of accessible microstates.",
            detail=(
                "Reactions that increase gas moles tend to have ΔS > 0. "
                "Dissolution, mixing, and phase transitions to higher states also increase S."
            ),
        ),
        ConceptLayer(
            name="caveat_thermo_vs_kinetics",
            summary="Thermodynamic feasibility ≠ observable reaction.",
            detail=(
                "Diamond → graphite is thermodynamically favorable at STP, "
                "but the activation barrier is so high it never happens at room temperature. "
                "Always pair L2 (thermo) with L3 (kinetics)."
            ),
        ),
    ]


# ── Computational helpers ────────────────────────────────────────────────

def gibbs_free_energy(
    delta_h_kj_per_mol: float,
    delta_s_j_per_mol_k: float,
    temperature_k: float,
) -> float:
    """Calculate ΔG = ΔH − TΔS.

    Parameters
    ----------
    delta_h_kj_per_mol : enthalpy change [kJ/mol]
    delta_s_j_per_mol_k : entropy change [J/(mol·K)]
    temperature_k : absolute temperature [K]

    Returns
    -------
    ΔG in kJ/mol
    """
    return delta_h_kj_per_mol - temperature_k * (delta_s_j_per_mol_k / 1000.0)


def is_spontaneous(delta_g_kj_per_mol: float) -> bool:
    """Return True if ΔG < 0 (thermodynamically favorable)."""
    return delta_g_kj_per_mol < 0.0


def assess_thermodynamic_state(
    delta_h_kj_per_mol: float,
    delta_s_j_per_mol_k: float,
    temperature_k: float = STANDARD_TEMPERATURE_K,
    pressure_pa: float = 101325.0,
) -> ThermodynamicState:
    """Build a full thermodynamic state assessment."""
    dg = gibbs_free_energy(delta_h_kj_per_mol, delta_s_j_per_mol_k, temperature_k)
    return ThermodynamicState(
        temperature_k=temperature_k,
        pressure_pa=pressure_pa,
        delta_g_kj_per_mol=dg,
        delta_h_kj_per_mol=delta_h_kj_per_mol,
        delta_s_j_per_mol_k=delta_s_j_per_mol_k,
        spontaneous=is_spontaneous(dg),
    )


def entropy_sign_heuristic(reaction: Reaction) -> str:
    """Heuristic: compare gas moles on each side.

    More gas moles on product side → likely ΔS > 0.
    """
    from .contracts import Phase

    def _gas_moles(terms):
        return sum(t.coefficient for t in terms if t.species.phase == Phase.GAS)

    r_gas = _gas_moles(reaction.reactants)
    p_gas = _gas_moles(reaction.products)
    if p_gas > r_gas:
        return "likely_positive"
    elif p_gas < r_gas:
        return "likely_negative"
    return "uncertain"


def temperature_crossover(
    delta_h_kj_per_mol: float,
    delta_s_j_per_mol_k: float,
) -> float | None:
    """Temperature at which ΔG = 0  →  T* = ΔH / ΔS.

    Returns None if ΔS ≈ 0 or signs are such that no crossover exists
    in the physically meaningful (T > 0) region.
    """
    if abs(delta_s_j_per_mol_k) < 1e-12:
        return None
    t_star = (delta_h_kj_per_mol * 1000.0) / delta_s_j_per_mol_k
    return t_star if t_star > 0 else None
