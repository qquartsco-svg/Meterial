from typing import List, Optional
from .contracts import *
def assess_vrfb()->VRFBAssessment: return VRFBAssessment(1.6,0.78,['VRFB favors long-duration cycles with lower fire risk than Li-ion.'])
def assess_alloy()->AlloyAssessment: return AlloyAssessment(0.02,'medium',['V microalloying can improve strength-toughness balance.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_zero_electrolyte_degradation: flags.append('degradation_denial'); omega-=0.25; reasons.append('Electrolyte crossover/imbalance and maintenance are real.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v, round(max(omega,0),3), flags, reasons)
def collect_layers()->List[ConceptLayer]: return [ConceptLayer('VRFB Redox','Vanadium valence states support reversible long-duration storage.'), ConceptLayer('Microalloying','Small V additions can shift steel performance envelopes.')]
def compute_health(storage=0.75,mat=0.65,safety=0.85,supply=0.5,econ=0.6)->HealthReport:
 axes=[storage,mat,safety,supply,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(storage,mat,safety,supply,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 v=assess_vrfb(); a=assess_alloy(); s=screen_claim(claim) if claim else None; h=compute_health(storage=v.round_trip_efficiency)
 return FoundationReport(v,a,s,h,collect_layers())
