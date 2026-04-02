from __future__ import annotations
from typing import List, Optional

from .contracts import (
    AlTiClaimPayload, AlTiHealthReport, AlTiScreeningReport,
    AluminumTitaniumFoundationReport, ConceptLayer, HealthVerdict, MaterialAssessment,
    ProcessAssessment, Verdict,
)


def assess_materials() -> MaterialAssessment:
    return MaterialAssessment(
        al_strength_mpa=350.0,
        ti_strength_mpa=900.0,
        corrosion_risk='medium',
        notes=['Al-Ti joints need galvanic isolation in wet/chloride environments.'],
    )


def assess_process() -> ProcessAssessment:
    return ProcessAssessment(
        al_energy_kwh_per_kg=14.0,
        ti_energy_kwh_per_kg=30.0,
        co2_risk='medium',
        notes=['Primary Al/Ti routes are energy-intensive; recycling strongly improves footprint.'],
    )


def screen_al_ti_claim(payload: AlTiClaimPayload) -> AlTiScreeningReport:
    flags=[]; reasons=[]; omega=0.7
    if payload.claimed_no_galvanic_corrosion:
        flags.append('galvanic_denial'); omega-=0.3; reasons.append('Al/Ti assemblies can suffer galvanic effects depending on couple/environment.')
    if payload.claimed_zero_process_energy:
        flags.append('energy_denial'); omega-=0.3; reasons.append('Primary Al/Ti extraction/refining is energy-intensive.')
    if omega>=0.65 and not flags: v=Verdict.POSITIVE
    elif omega>=0.45: v=Verdict.NEUTRAL
    elif omega>=0.25: v=Verdict.CAUTIOUS
    else: v=Verdict.NEGATIVE
    if not reasons: reasons.append('No specific issues detected.')
    return AlTiScreeningReport(v, round(max(omega,0),3), flags, reasons)


def collect_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer('Al-Ti Structure Trade-off', 'Al is lighter/cheaper; Ti is stronger/corrosion-resistant but expensive/energy-heavy.'),
        ConceptLayer('Galvanic Interface', 'Mixed-metal design requires isolation and coatings in conductive environments.'),
    ]


def compute_health(mat=0.7, proc=0.5, corr=0.6, safety=0.8, econ=0.55) -> AlTiHealthReport:
    axes=[mat,proc,corr,safety,econ]; c=round(sum(axes)/len(axes),3)
    if c>=0.7 and min(axes)>=0.4: v=HealthVerdict.HEALTHY
    elif c>=0.5: v=HealthVerdict.STABLE
    elif c>=0.3: v=HealthVerdict.FRAGILE
    else: v=HealthVerdict.CRITICAL
    return AlTiHealthReport(mat,proc,corr,safety,econ,c,v)


def run_al_ti_foundation(claim: Optional[AlTiClaimPayload]=None) -> AluminumTitaniumFoundationReport:
    m=assess_materials(); p=assess_process(); s=screen_al_ti_claim(claim) if claim else None
    h=compute_health(proc=max(1-p.ti_energy_kwh_per_kg/60.0,0.0), corr=0.55 if m.corrosion_risk=='medium' else 0.75)
    return AluminumTitaniumFoundationReport(m,p,s,h,collect_concept_layers())
