from typing import List, Optional
from .contracts import *
def assess_reactivity()->ReactivityAssessment:
 return ReactivityAssessment('stronger than Na/K','fresh surfaces ignite in air; violent water reaction',['Rb/Cs are not interchangeable with milder alkali handling playbooks.'])
def assess_applications()->ApplicationAssessment:
 return ApplicationAssessment('frequency standards niche','Cs historically in some thrusters; Xe dominates now',['Supply is specialized; use cases are narrow vs Na/K industrial scale.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.68
 if p.claimed_mild_alkali_like_na:
  flags.append('alkali_conflation'); omega-=0.3; reasons.append('Heavier alkalis escalate pyrophoricity and water reactivity vs Na.')
 if p.claimed_no_pyrophoric_or_water_risk:
  flags.append('reactivity_denial'); omega-=0.32; reasons.append('Air/moisture contact for metals and reactive salts requires engineered controls.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Potassium axis extension','Read after Potassium_Foundation: same group, higher hazard class.'),ConceptLayer('Storage chemistry','Mineral oil/inert gas protocols differ from Na inventory.')]
def compute_health(safe=0.48,sup=0.55,stor=0.5,pur=0.58,econ=0.52)->HealthReport:
 axes=[safe,sup,stor,pur,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(safe,sup,stor,pur,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 r=assess_reactivity(); a=assess_applications(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(r,a,sc,h,collect_layers())
