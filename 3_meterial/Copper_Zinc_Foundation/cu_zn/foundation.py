from __future__ import annotations
from typing import List, Optional
from .constants import CU_RESISTIVITY_OHM_M, ZN_RESISTIVITY_OHM_M
from .contracts import *

def assess_conductivity(cu_fraction: float=0.7)->ConductivityAssessment:
    rho=CU_RESISTIVITY_OHM_M*cu_fraction+ZN_RESISTIVITY_OHM_M*(1-cu_fraction)
    conductivity=1.0/rho/1e6
    risk='medium' if cu_fraction<0.8 else 'low'
    return ConductivityAssessment(conductivity, risk, ['Brass reduces conductivity vs pure copper.'])

def assess_alloy(cu_fraction: float=0.7, zn_fraction: float=0.3)->AlloyAssessment:
    return AlloyAssessment(AlloyType.BRASS, cu_fraction, zn_fraction, 'high', ['Machinability improves with Zn addition.'])

def screen_cu_zn_claim(payload: CuZnClaimPayload)->CuZnScreeningReport:
    flags=[]; reasons=[]; omega=0.7
    if payload.claimed_no_corrosion: flags.append('corrosion_denial'); omega-=0.3; reasons.append('Cu/Zn alloys can corrode/dezincify depending on environment.')
    if payload.claimed_perfect_conductivity: flags.append('conductivity_myth'); omega-=0.25; reasons.append('Alloying reduces conductivity from pure Cu ceiling.')
    v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
    if not reasons: reasons.append('No specific issues detected.')
    return CuZnScreeningReport(v, round(max(omega,0),3), flags, reasons)

def collect_concept_layers()->List[ConceptLayer]:
    return [ConceptLayer('Conductive Metals','Cu is conductivity anchor; Zn trades conductivity for machinability/cost.'), ConceptLayer('Brass Trade-off','Cu-Zn balances processability vs electrical/chemical constraints.')]

def compute_health(cond=0.7,corr=0.6,mat=0.7,safety=0.8,econ=0.65)->CuZnHealthReport:
    axes=[cond,corr,mat,safety,econ]; c=round(sum(axes)/len(axes),3)
    v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
    return CuZnHealthReport(cond,corr,mat,safety,econ,c,v)

def run_cu_zn_foundation(claim: Optional[CuZnClaimPayload]=None)->CopperZincFoundationReport:
    a=assess_alloy(); c=assess_conductivity(a.cu_fraction); s=screen_cu_zn_claim(claim) if claim else None
    h=compute_health(cond=min(c.conductivity_ms_m/58.0,1.0), corr=0.55 if c.corrosion_risk=='medium' else 0.75)
    return CopperZincFoundationReport(c,a,s,h,collect_concept_layers())
