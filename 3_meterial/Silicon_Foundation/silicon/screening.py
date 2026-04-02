from __future__ import annotations

from typing import List

from .contracts import ConceptLayer, SiliconClaimPayload, SiliconScreeningReport, Verdict


def screen_silicon_claim(payload: SiliconClaimPayload) -> SiliconScreeningReport:
    flags: List[str] = []
    reasoning: List[str] = []
    omega = 0.70

    if payload.claimed_zero_defects:
        flags.append("defect_free_myth")
        reasoning.append("Defect-free large-scale silicon fabrication is not realistic.")
        omega -= 0.30
    if payload.claimed_unlimited_efficiency:
        flags.append("efficiency_limit_ignored")
        reasoning.append("PV/device efficiency has physics and process limits.")
        omega -= 0.30

    tags = [t.lower() for t in payload.tags]
    if "no_thermal_budget" in tags:
        flags.append("thermal_handwave")
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
    return SiliconScreeningReport(verdict=v, omega=omega, flags=flags, reasoning=reasoning)


def screening_concept_layers() -> List[ConceptLayer]:
    return [ConceptLayer(name="ATHENA Silicon", description="Flags: defect-free myth, efficiency-limit ignored, thermal handwave.")]
