"""L5 — ATHENA screening for oxygen claims."""

from __future__ import annotations

from typing import List

from .contracts import ConceptLayer, OxygenClaimPayload, OxygenScreeningReport, Verdict


def screen_oxygen_claim(payload: OxygenClaimPayload) -> OxygenScreeningReport:
    flags: List[str] = []
    reasoning: List[str] = []
    omega = 0.70

    if payload.claimed_pure_o2_safe:
        flags.append("oxidiser_handwave")
        reasoning.append("Pure O₂ increases fire severity; 'safe like air' is misleading.")
        omega -= 0.30

    if payload.claimed_moxie_no_energy:
        flags.append("moxie_energy_ignored")
        reasoning.append("ISRU O₂ from CO₂ requires substantial energy and hardware (e.g. MOXIE-class).")
        omega -= 0.25

    tags = [t.lower() for t in payload.tags]
    if "no_fire_risk" in tags:
        flags.append("fire_risk_denial")
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
    return OxygenScreeningReport(verdict=verdict, omega=omega, flags=flags, reasoning=reasoning)


def screening_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="ATHENA Oxygen Screening",
            description="Flags: oxidiser handwave, MOXIE energy ignored, fire risk denial.",
        ),
    ]
