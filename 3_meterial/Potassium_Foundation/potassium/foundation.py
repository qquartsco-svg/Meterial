from __future__ import annotations
from typing import List, Optional
from .constants import SERUM_K_NORMAL_MMOl_L_MIN, SERUM_K_NORMAL_MMOl_L_MAX
from .contracts import *

def assess_electrolyte(serum_k_mmol_l: float=4.2)->ElectrolyteAssessment:
    if serum_k_mmol_l < SERUM_K_NORMAL_MMOl_L_MIN: risk='high'; notes=['Hypokalemia risk.']
    elif serum_k_mmol_l > SERUM_K_NORMAL_MMOl_L_MAX: risk='high'; notes=['Hyperkalemia risk.']
    else: risk='low'; notes=[]
    return ElectrolyteAssessment(serum_k_mmol_l, risk, notes)

def assess_fertilizer(k2o_equivalent_kg_per_ton: float=120.0)->FertilizerAssessment:
    risk='medium' if k2o_equivalent_kg_per_ton>150 else 'low'
    return FertilizerAssessment(k2o_equivalent_kg_per_ton, risk, ['Runoff/leaching management required in intensive use.'])

def screen_potassium_claim(payload: PotassiumClaimPayload)->PotassiumScreeningReport:
    flags=[]; reasons=[]; omega=0.7
    if payload.claimed_no_hyperkalemia_risk: flags.append('electrolyte_denial'); omega-=0.3; reasons.append('K+ imbalance can cause severe cardiac risk.')
    if payload.claimed_no_leaching: flags.append('agri_leaching_denial'); omega-=0.2; reasons.append('Potash overuse can still lead to nutrient runoff/leaching contexts.')
    v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
    if not reasons: reasons.append('No specific issues detected.')
    return PotassiumScreeningReport(v, round(max(omega,0),3), flags, reasons)

def collect_concept_layers()->List[ConceptLayer]:
    return [ConceptLayer('Electrolyte Potassium','K+ is central to membrane potential and cardiac rhythm.'), ConceptLayer('Potash Agriculture','K fertilizer boosts yield but requires water/soil governance.')]

def compute_health(elec=0.7,agri=0.6,safety=0.8,recycling=0.5,econ=0.6)->PotassiumHealthReport:
    axes=[elec,agri,safety,recycling,econ]; c=round(sum(axes)/len(axes),3)
    v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
    return PotassiumHealthReport(elec,agri,safety,recycling,econ,c,v)

def run_potassium_foundation(claim: Optional[PotassiumClaimPayload]=None)->PotassiumFoundationReport:
    e=assess_electrolyte(); f=assess_fertilizer(); s=screen_potassium_claim(claim) if claim else None
    h=compute_health(elec=0.85 if e.risk_level=='low' else 0.35, agri=0.55 if f.leaching_risk=='medium' else 0.75)
    return PotassiumFoundationReport(e,f,s,h,collect_concept_layers())
