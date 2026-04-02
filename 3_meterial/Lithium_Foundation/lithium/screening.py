from __future__ import annotations

from typing import List

from .contracts import ConceptLayer, LithiumClaimPayload, LithiumScreeningReport, Verdict


def screen_lithium_claim(payload: LithiumClaimPayload) -> LithiumScreeningReport:
    flags: List[str] = []
    reasoning: List[str] = []
    omega = 0.70

    if payload.claimed_unlimited_supply:
        flags.append("supply_myth")
        reasoning.append("Lithium reserves and refining capacity are finite and geographically concentrated.")
        omega -= 0.30
    if payload.claimed_zero_degradation:
        flags.append("degradation_denial")
        reasoning.append("Li-ion cells degrade via SEI growth, plating, and mechanical aging.")
        omega -= 0.30
    if payload.claimed_zero_recycling_need:
        flags.append("recycling_handwave")
        reasoning.append("Scale-up without recycling drives supply and waste risk.")
        omega -= 0.20

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
    return LithiumScreeningReport(verdict=verdict, omega=omega, flags=flags, reasoning=reasoning)


def screening_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(name="ATHENA Lithium Screening", description="Flags: supply myth, degradation denial, recycling handwave."),
    ]
