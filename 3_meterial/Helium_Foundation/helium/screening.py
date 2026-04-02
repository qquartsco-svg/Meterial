"""L5 — ATHENA screening for helium claims."""

from __future__ import annotations

from typing import List

from .contracts import ConceptLayer, HeliumClaimPayload, HeliumScreeningReport, Verdict


def screen_helium_claim(payload: HeliumClaimPayload) -> HeliumScreeningReport:
    flags: List[str] = []
    reasoning: List[str] = []
    omega = 0.70

    if payload.claimed_abundance_unlimited:
        flags.append("abundance_myth")
        reasoning.append("He is finite and tied to natural gas geology; not unlimited.")
        omega -= 0.35

    if payload.claimed_cost_usd_per_m3 is not None and payload.claimed_cost_usd_per_m3 < 0.01:
        flags.append("impossible_cost")
        reasoning.append("Claimed He cost is below plausible extraction economics.")
        omega -= 0.25

    tags = [t.lower() for t in payload.tags]
    if "synthetic_helium_cheap" in tags:
        flags.append("synthesis_hype")
        reasoning.append("Bulk He is not economically synthesized from other elements.")
        omega -= 0.30

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
    return HeliumScreeningReport(verdict=verdict, omega=omega, flags=flags, reasoning=reasoning)


def screening_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="ATHENA Helium Screening",
            description="Flags: abundance myth, impossible cost, synthesis hype.",
        ),
    ]
