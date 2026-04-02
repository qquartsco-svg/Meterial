from __future__ import annotations
from typing import List, Optional
from .contracts import *

def assess_cathode(ch: Chemistry=Chemistry.NMC622)->CathodeAssessment:
    if ch==Chemistry.NMC811: return CathodeAssessment(ch,260,1200,'high','medium',['High energy but stricter thermal envelope.'])
    if ch==Chemistry.NMC111: return CathodeAssessment(ch,180,2200,'low','high',['Lower energy, more cobalt dependence.'])
    if ch==Chemistry.LNO: return CathodeAssessment(ch,280,800,'high','low',['High Ni extreme; stability management critical.'])
    return CathodeAssessment(ch,220,1700,'medium','medium',['Balanced profile baseline.'])

def assess_supply()->SupplyAssessment:
    return SupplyAssessment('low','high','medium','high',['Cobalt geopolitical risk and recycling dependence are non-trivial.'])

def screen_mcn_claim(payload: MCNClaimPayload)->MCNScreeningReport:
    flags=[]; reasons=[]; omega=0.7
    if payload.claimed_no_supply_risk: flags.append('supply_denial'); omega-=0.3; reasons.append('Co/Ni/Mn supply and refining chain risks are real.')
    if payload.claimed_high_ni_no_safety_tradeoff: flags.append('ni_safety_denial'); omega-=0.25; reasons.append('Higher Ni generally tightens thermal/safety constraints.')
    v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
    if not reasons: reasons.append('No specific issues detected.')
    return MCNScreeningReport(v, round(max(omega,0),3), flags, reasons)

def collect_concept_layers()->List[ConceptLayer]:
    return [ConceptLayer('NMC Triangle','Energy density, safety, and cycle life are coupled to Ni/Co/Mn ratio.'), ConceptLayer('Supply Reality','Cathode performance claims must include material supply and recycling constraints.')]

def compute_health(energy=0.7,life=0.65,safety=0.6,supply=0.5,econ=0.6)->MCNHealthReport:
    axes=[energy,life,safety,supply,econ]; c=round(sum(axes)/len(axes),3)
    v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
    return MCNHealthReport(energy,life,safety,supply,econ,c,v)

def run_mcn_foundation(claim: Optional[MCNClaimPayload]=None, chemistry: Chemistry=Chemistry.NMC622)->MCNFoundationReport:
    c=assess_cathode(chemistry); s=assess_supply(); sc=screen_mcn_claim(claim) if claim else None
    safety_omega=0.45 if c.thermal_risk=='high' else (0.6 if c.thermal_risk=='medium' else 0.8)
    h=compute_health(energy=min(c.specific_energy_wh_kg/300,1.0), life=min(c.cycle_life_80pct/2500,1.0), safety=safety_omega, supply=0.45 if s.co_risk=='high' else 0.7, econ=0.6)
    return MCNFoundationReport(c,s,sc,h,collect_concept_layers())
