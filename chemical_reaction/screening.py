"""L6 — ATHENA screening for chemical claims.

Four-tier verdict: POSITIVE / NEUTRAL / CAUTIOUS / NEGATIVE.
"""

from __future__ import annotations

from typing import List

from .contracts import (
    ChemicalClaimPayload,
    ChemicalScreeningReport,
    ConceptLayer,
    Verdict,
)


# ── Pedagogical axes ─────────────────────────────────────────────────────

def screening_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="mass_conservation_screen",
            summary="Atoms are neither created nor destroyed in a chemical reaction.",
        ),
        ConceptLayer(
            name="energy_conservation_screen",
            summary="Energy is conserved. Over-unity claims violate the first law.",
        ),
        ConceptLayer(
            name="thermodynamic_feasibility_screen",
            summary="ΔG direction determines if a claim is physically possible.",
        ),
        ConceptLayer(
            name="equilibrium_limit_screen",
            summary="No reaction proceeds to 100% completion — equilibrium always applies.",
        ),
        ConceptLayer(
            name="activation_barrier_screen",
            summary="Even favorable reactions need energy to start unless catalysed.",
        ),
    ]


# ── Screening logic ──────────────────────────────────────────────────────

_HARD_NEGATIVE_FLAGS = (
    "violates_mass_conservation",
    "violates_energy_conservation",
    "claims_over_unity",
)

_CAUTIOUS_FLAGS = (
    "violates_thermodynamic_feasibility",
    "claims_perpetual_reaction",
)

_SOFT_FLAGS = (
    "ignores_activation_barrier",
    "ignores_equilibrium_limit",
)

_PENALTY: dict[str, float] = {
    "violates_mass_conservation": 0.30,
    "violates_energy_conservation": 0.30,
    "claims_over_unity": 0.30,
    "violates_thermodynamic_feasibility": 0.20,
    "claims_perpetual_reaction": 0.20,
    "ignores_activation_barrier": 0.10,
    "ignores_equilibrium_limit": 0.10,
}


def screen_chemical_claim(payload: ChemicalClaimPayload) -> ChemicalScreeningReport:
    """Evaluate a chemical claim and return an ATHENA verdict."""
    triggered: list[str] = []
    notes: list[str] = []

    for flag_name in (
        "violates_mass_conservation",
        "violates_energy_conservation",
        "violates_thermodynamic_feasibility",
        "claims_over_unity",
        "claims_perpetual_reaction",
        "ignores_activation_barrier",
        "ignores_equilibrium_limit",
    ):
        if getattr(payload, flag_name, False):
            triggered.append(flag_name)

    total_penalty = sum(_PENALTY.get(f, 0.0) for f in triggered)
    base_omega = 0.70
    omega = max(0.0, base_omega - total_penalty)

    has_hard = any(f in _HARD_NEGATIVE_FLAGS for f in triggered)
    has_cautious = any(f in _CAUTIOUS_FLAGS for f in triggered)

    if has_hard:
        verdict = Verdict.NEGATIVE
        notes.append("Hard violation detected: conservation law or over-unity.")
    elif has_cautious:
        verdict = Verdict.CAUTIOUS
        notes.append("Thermodynamic or equilibrium concern flagged.")
    elif triggered:
        verdict = Verdict.NEUTRAL
        notes.append("Soft concern: activation barrier or equilibrium limit overlooked.")
    else:
        verdict = Verdict.POSITIVE
        notes.append("No flags triggered. Claim appears consistent with known chemistry.")

    if omega > 0.90 and not triggered:
        notes.append("Warning: high omega with no flags — verify input is not trivially true.")

    return ChemicalScreeningReport(
        claim_text=payload.claim_text,
        verdict=verdict,
        omega=round(omega, 4),
        flags_triggered=tuple(triggered),
        notes=tuple(notes),
    )
