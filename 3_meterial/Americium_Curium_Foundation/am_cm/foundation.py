from typing import List, Optional
from .contracts import *
def assess_americium()->AmericiumAssessment:
 return AmericiumAssessment('microgram-scale sealed sources common','not interchangeable with reactor fuel narratives',['Am-241 in ionization detectors is real but tightly regulated and sealed.'])
def assess_curium()->CuriumAssessment:
 return CuriumAssessment('space RTG history','gram-scale special facilities',['Cm isotopes are heat-heavy; logistics mirror Pu-adjacent governance classes.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.65
 if p.claimed_trivial_handling_no_governance:
  flags.append('governance_denial'); omega-=0.35; reasons.append('Transplutonium alpha emitters require radiological controls and licensing context.')
 if p.claimed_unlimited_domestic_am_supply:
  flags.append('am_supply_myth'); omega-=0.26; reasons.append('Even detector-grade Am is not an unconstrained consumer commodity.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Pu-axis extension','Read after Plutonium_Foundation for actinide governance grammar.'),ConceptLayer('Sealed source vs bulk','Scale and encapsulation change both risk and regulation.')]
def compute_health(safe=0.5,gov=0.48,sup=0.45,sec=0.52,econ=0.48)->HealthReport:
 axes=[safe,gov,sup,sec,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(safe,gov,sup,sec,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 a=assess_americium(); c=assess_curium(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(a,c,sc,h,collect_layers())
