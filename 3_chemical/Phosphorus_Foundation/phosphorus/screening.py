from __future__ import annotations

from typing import List

from .contracts import ConceptLayer, PhosphorusClaimPayload, PhosphorusScreeningReport, Verdict


def screen_phosphorus_claim(payload: PhosphorusClaimPayload) -> PhosphorusScreeningReport:
    flags: List[str] = []
    reasoning: List[str] = []
    omega = 0.70

    if payload.claimed_infinite_phosphate:
        flags.append("reserve_myth")
        reasoning.append("Phosphate ore reserves are finite and regionally concentrated.")
        omega -= 0.30
    if payload.claimed_atp_without_recycling:
        flags.append("atp_cycle_denial")
        reasoning.append("ATP must be regenerated; one-pass ATP energetics is biologically invalid.")
        omega -= 0.30

    tags = [t.lower() for t in payload.tags]
    if "no_pollution_control" in tags:
        flags.append("pollution_handwave")
        omega -= 0.20

    omega = max(round(omega, 3), 0.0)
    if omega >= 0.65 and not flags:
        v = Verdict.POSITIVE
    elif omega >= 0.45:
        v = Verdict.NEUTRAL
    elif omega >= 0.25:
        v = Verdict.CAUTIOUS
    else:
        v = Verdict.NEGATIVE

    if not reasoning:
        reasoning.append("No specific issues detected.")
    return PhosphorusScreeningReport(verdict=v, omega=omega, flags=flags, reasoning=reasoning)


def screening_concept_layers() -> List[ConceptLayer]:
    return [ConceptLayer(name="ATHENA Phosphorus", description="Flags: reserve myth, ATP cycle denial, pollution handwave.")]
