from __future__ import annotations
from typing import List, Optional

from .constants import FE_CORROSION_RATE_MM_PER_YEAR_TYPICAL, FE_DENSITY_G_PER_CM3, FE_MELTING_POINT_K, FE_MOLAR_MASS_G_PER_MOL
from .contracts import (
    ConceptLayer, CorrosionAssessment, FeProperties, HealthVerdict,
    IronClaimPayload, IronFoundationReport, IronHealthReport, IronScreeningReport,
    ProcessAssessment, ProcessMethod, Verdict,
)


def iron_property_card() -> FeProperties:
    return FeProperties(FE_MOLAR_MASS_G_PER_MOL, FE_DENSITY_G_PER_CM3, FE_MELTING_POINT_K)


def assess_process(method: ProcessMethod = ProcessMethod.BLAST_FURNACE) -> ProcessAssessment:
    if method == ProcessMethod.DRI_EAF:
        return ProcessAssessment(method, 800.0, 14.0, ["H2-DRI reduces CO2 vs blast furnace."])
    if method == ProcessMethod.ELECTROLYTIC_IRON:
        return ProcessAssessment(method, 300.0, 18.0, ["Low carbon possible with clean electricity; still energy-heavy."])
    return ProcessAssessment(method, 1800.0, 20.0, ["Conventional route baseline."])


def assess_corrosion(exposure_factor: float = 1.0) -> CorrosionAssessment:
    rate = FE_CORROSION_RATE_MM_PER_YEAR_TYPICAL * exposure_factor
    return CorrosionAssessment(rate, rate > 0.05, ["Coatings/cathodic protection often required."])


def screen_iron_claim(payload: IronClaimPayload) -> IronScreeningReport:
    flags: List[str] = []
    reasoning: List[str] = []
    omega = 0.7
    if payload.claimed_zero_corrosion:
        flags.append("corrosion_denial")
        omega -= 0.3
        reasoning.append("Iron corrosion is fundamental in ambient oxidizing environments.")
    if payload.claimed_zero_co2_steel:
        flags.append("steel_co2_handwave")
        omega -= 0.3
        reasoning.append("Steelmaking decarbonization requires route/energy transition, not instant zero.")
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
    return IronScreeningReport(v, round(max(omega,0.0),3), flags, reasoning)


def collect_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer("Iron Core", "Structural metal backbone with corrosion as dominant lifecycle cost."),
        ConceptLayer("Steel Decarbonization", "Blast furnace -> DRI/EAF transition is key."),
    ]


def compute_health(process_omega=0.6, corrosion_omega=0.5, recycling_omega=0.7, safety_omega=0.8, econ_omega=0.6) -> IronHealthReport:
    axes = [process_omega, corrosion_omega, recycling_omega, safety_omega, econ_omega]
    c = round(sum(axes)/len(axes),3)
    if c >= 0.7 and min(axes)>=0.4:
        v=HealthVerdict.HEALTHY
    elif c>=0.5:
        v=HealthVerdict.STABLE
    elif c>=0.3:
        v=HealthVerdict.FRAGILE
    else:
        v=HealthVerdict.CRITICAL
    return IronHealthReport(process_omega, corrosion_omega, recycling_omega, safety_omega, econ_omega, c, v)


def run_iron_foundation(claim: Optional[IronClaimPayload]=None) -> IronFoundationReport:
    p = assess_process()
    c = assess_corrosion()
    s = screen_iron_claim(claim) if claim else None
    h = compute_health(process_omega=max(1-p.co2_intensity_kg_per_ton_steel/2500,0.0), corrosion_omega=max(1-c.corrosion_rate_mm_per_year/0.5,0.0))
    return IronFoundationReport(p,c,s,h,collect_concept_layers())
