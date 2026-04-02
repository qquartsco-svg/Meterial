from __future__ import annotations
from typing import List, Optional

from .constants import (
    SERUM_CA_NORMAL_MG_DL_MAX, SERUM_CA_NORMAL_MG_DL_MIN,
    SERUM_MG_NORMAL_MG_DL_MAX, SERUM_MG_NORMAL_MG_DL_MIN,
)
from .contracts import (
    AlloyAssessment, ConceptLayer, ElectrolyteAssessment, HealthVerdict,
    MgCaClaimPayload, MgCaHealthReport, MgCaScreeningReport,
    MagnesiumCalciumFoundationReport, Verdict,
)


def assess_electrolyte(serum_ca_mg_dl: float = 9.4, serum_mg_mg_dl: float = 1.9) -> ElectrolyteAssessment:
    risk = 'low'
    notes = []
    if not (SERUM_CA_NORMAL_MG_DL_MIN <= serum_ca_mg_dl <= SERUM_CA_NORMAL_MG_DL_MAX):
        risk = 'high'; notes.append('Calcium out of reference range.')
    if not (SERUM_MG_NORMAL_MG_DL_MIN <= serum_mg_mg_dl <= SERUM_MG_NORMAL_MG_DL_MAX):
        risk = 'high'; notes.append('Magnesium out of reference range.')
    if risk == 'low' and (abs(serum_ca_mg_dl-9.5)>0.8 or abs(serum_mg_mg_dl-1.95)>0.2):
        risk='medium'
    return ElectrolyteAssessment(serum_ca_mg_dl, serum_mg_mg_dl, risk, notes)


def assess_alloy(mg_fraction: float = 0.9, ca_fraction: float = 0.1) -> AlloyAssessment:
    risk = 'medium' if mg_fraction > 0.7 else 'low'
    return AlloyAssessment(mg_fraction, ca_fraction, risk, ['Mg-rich alloys need corrosion control.'])


def screen_mg_ca_claim(payload: MgCaClaimPayload) -> MgCaScreeningReport:
    flags=[]; reasons=[]; omega=0.7
    if payload.claimed_no_electrolyte_risk:
        flags.append('electrolyte_denial'); omega-=0.3; reasons.append('Ca/Mg imbalance has clinical risk.')
    if payload.claimed_no_corrosion:
        flags.append('corrosion_denial'); omega-=0.25; reasons.append('Mg-containing alloys are corrosion-sensitive.')
    if omega>=0.65 and not flags: v=Verdict.POSITIVE
    elif omega>=0.45: v=Verdict.NEUTRAL
    elif omega>=0.25: v=Verdict.CAUTIOUS
    else: v=Verdict.NEGATIVE
    if not reasons: reasons.append('No specific issues detected.')
    return MgCaScreeningReport(v, round(max(omega,0),3), flags, reasons)


def collect_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer('Electrolyte Homeostasis', 'Ca/Mg balance governs neuromuscular and cardiac stability.'),
        ConceptLayer('Light Alloy Trade-off', 'Mg/Ca alloying can reduce weight but raises corrosion constraints.'),
    ]


def compute_health(bio=0.7, mat=0.6, safety=0.8, recycling=0.5, econ=0.6) -> MgCaHealthReport:
    axes=[bio,mat,safety,recycling,econ]; c=round(sum(axes)/len(axes),3)
    if c>=0.7 and min(axes)>=0.4: v=HealthVerdict.HEALTHY
    elif c>=0.5: v=HealthVerdict.STABLE
    elif c>=0.3: v=HealthVerdict.FRAGILE
    else: v=HealthVerdict.CRITICAL
    return MgCaHealthReport(bio,mat,safety,recycling,econ,c,v)


def run_mg_ca_foundation(claim: Optional[MgCaClaimPayload]=None) -> MagnesiumCalciumFoundationReport:
    e=assess_electrolyte(); a=assess_alloy(); s=screen_mg_ca_claim(claim) if claim else None
    h=compute_health(bio=0.85 if e.risk_level=='low' else 0.4, mat=0.55 if a.corrosion_risk=='medium' else 0.75)
    return MagnesiumCalciumFoundationReport(e,a,s,h,collect_concept_layers())
