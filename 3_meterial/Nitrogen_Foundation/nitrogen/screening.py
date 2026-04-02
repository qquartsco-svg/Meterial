"""L6 — ATHENA screening for nitrogen / fertilizer claims."""

from __future__ import annotations

from typing import List

from .contracts import ConceptLayer, NitrogenClaimPayload, NitrogenScreeningReport, Verdict


def screen_nitrogen_claim(payload: NitrogenClaimPayload) -> NitrogenScreeningReport:
    flags: List[str] = []
    reasoning: List[str] = []
    omega = 0.70

    if payload.claimed_free_fertilizer:
        flags.append("energy_ignored")
        reasoning.append("Ammonia/fertilizer requires H₂ and large energy input (Haber–Bosch).")
        omega -= 0.35

    if payload.claimed_air_is_pure_n2:
        flags.append("air_composition_error")
        reasoning.append("Air is ~78 % N₂, not pure N₂; O₂ and Ar matter for safety and processes.")
        omega -= 0.20

    tags = [t.lower() for t in payload.tags]
    if "no_haber_energy" in tags:
        flags.append("haber_handwave")
        omega -= 0.25

    omega = max(round(omega, 3), 0.0)
    if omega >= 0.65 and not flags:
        verdict = Verdict.POSITIVE
    elif omega >= 0.45:
        verdict = Verdict.NEUTRAL
    elif omega >= 0.25:
        verdict = Verdict.CAUTIOUS
    else:
        verdict = Verdict.NEGATIVE

    if not reasoning:
        reasoning.append("No specific issues detected.")
    return NitrogenScreeningReport(verdict=verdict, omega=omega, flags=flags, reasoning=reasoning)


def screening_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="ATHENA Nitrogen Screening",
            description="Flags: free fertilizer, air composition error, Haber energy handwave.",
        ),
    ]
