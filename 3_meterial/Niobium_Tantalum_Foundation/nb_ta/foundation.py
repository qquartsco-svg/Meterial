from typing import List, Optional
from .contracts import *
def assess_alloy()->AlloyAssessment: return AlloyAssessment(0.03,0.01,'high',['Nb/Ta additions support high-temp and corrosion performance niches.'])
def assess_capacitor()->CapacitorAssessment: return CapacitorAssessment('high','medium',['Tantalum capacitors are compact but failure modes must be managed.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_no_supply_risk: flags.append('supply_denial'); omega-=0.3; reasons.append('Nb/Ta sources are concentrated and refining chains are sensitive.')
 if p.claimed_no_failure_modes: flags.append('failure_mode_denial'); omega-=0.25; reasons.append('Capacitor and high-temp components retain non-zero failure modes.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]: return [ConceptLayer('High-Temp Alloys','Nb/Ta can improve high-temp performance envelopes.'), ConceptLayer('Capacitor Density','Ta capacitors trade compactness with reliability and supply constraints.')]
def compute_health(alloy=0.7,cap=0.65,supply=0.45,safety=0.75,econ=0.55)->HealthReport:
 axes=[alloy,cap,supply,safety,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(alloy,cap,supply,safety,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 a=assess_alloy(); c=assess_capacitor(); s=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(a,c,s,h,collect_layers())
