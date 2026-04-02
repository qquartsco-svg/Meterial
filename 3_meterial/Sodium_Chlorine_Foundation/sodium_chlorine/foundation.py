from __future__ import annotations
from typing import List, Optional

from .constants import CHLOR_ALKALI_CELL_V_TYPICAL, NACL_SOLUBILITY_G_PER_L_25C
from .contracts import (
    ConceptLayer, HealthVerdict, NaClClaimPayload, NaClHealthReport,
    NaClScreeningReport, ProcessAssessment, ProcessMethod,
    SaltSystemAssessment, SodiumChlorineFoundationReport, Verdict,
)


def assess_chlor_alkali() -> ProcessAssessment:
    return ProcessAssessment(
        ProcessMethod.CHLOR_ALKALI,
        naoh_kg_per_ton_brine=220.0,
        cl2_kg_per_ton_brine=200.0,
        h2_kg_per_ton_brine=5.6,
        notes=[f"Cell voltage cartoon ~{CHLOR_ALKALI_CELL_V_TYPICAL} V; power cost dominates."],
    )


def assess_salt_system(salinity_g_per_l: float = 35.0) -> SaltSystemAssessment:
    return SaltSystemAssessment(
        salinity_g_per_l=salinity_g_per_l,
        corrosion_risk="high" if salinity_g_per_l > 20 else "medium",
        scaling_risk="medium",
        notes=["Seawater salinity accelerates corrosion and materials selection constraints."],
    )


def screen_nacl_claim(payload: NaClClaimPayload) -> NaClScreeningReport:
    flags: List[str] = []
    reasoning: List[str] = []
    omega = 0.7
    if payload.claimed_no_corrosion_in_saltwater:
        flags.append("corrosion_denial")
        omega -= 0.3
        reasoning.append("Chloride environments are among the most aggressive for many metals.")
    if payload.claimed_free_cl2_no_power:
        flags.append("energy_denial")
        omega -= 0.3
        reasoning.append("Chlor-alkali electrolysis requires substantial electrical input.")
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
    return NaClScreeningReport(v, round(max(omega,0.0),3), flags, reasoning)


def collect_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer("Salt Chemistry", "NaCl links water systems, corrosion, and chlor-alkali industry."),
        ConceptLayer("Chlor-alkali Coupling", "Brine electrolysis co-produces Cl2, NaOH, H2."),
    ]


def compute_health(process_omega=0.6, materials_omega=0.4, safety_omega=0.6, waste_omega=0.5, econ_omega=0.6) -> NaClHealthReport:
    axes=[process_omega, materials_omega, safety_omega, waste_omega, econ_omega]
    c=round(sum(axes)/len(axes),3)
    if c>=0.7 and min(axes)>=0.4:
        v=HealthVerdict.HEALTHY
    elif c>=0.5:
        v=HealthVerdict.STABLE
    elif c>=0.3:
        v=HealthVerdict.FRAGILE
    else:
        v=HealthVerdict.CRITICAL
    return NaClHealthReport(process_omega, materials_omega, safety_omega, waste_omega, econ_omega, c, v)


def run_sodium_chlorine_foundation(claim: Optional[NaClClaimPayload]=None) -> SodiumChlorineFoundationReport:
    p=assess_chlor_alkali()
    s=assess_salt_system()
    sc=screen_nacl_claim(claim) if claim else None
    h=compute_health(materials_omega=max(1-s.salinity_g_per_l/100.0,0.0))
    return SodiumChlorineFoundationReport(p,s,sc,h,collect_concept_layers())
