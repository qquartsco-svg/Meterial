from typing import List, Optional
from .contracts import *
def assess_fuel_cycle()->FuelCycleAssessment: return FuelCycleAssessment('U/Th mixed strategy','medium','high',['Back-end fuel cycle and waste policy are core constraints.'])
def assess_reactor()->ReactorAssessment: return ReactorAssessment('Gen-III+/MSR concepts','medium','high',['Safety and licensing complexity remain first-order design constraints.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_no_waste_issue: flags.append('waste_denial'); omega-=0.3; reasons.append('Nuclear waste handling remains non-zero governance burden.')
 if p.claimed_no_safety_governance_need: flags.append('governance_denial'); omega-=0.25; reasons.append('Nuclear systems require rigorous safety and governance layers.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]: return [ConceptLayer('Fuel Cycle Reality','Front-end and back-end constraints define viability.'), ConceptLayer('Safety Governance','Engineering and governance are inseparable in nuclear deployment.')]
def compute_health(fc=0.6,safety=0.55,waste=0.45,gov=0.5,econ=0.55)->HealthReport:
 axes=[fc,safety,waste,gov,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(fc,safety,waste,gov,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 f=assess_fuel_cycle(); r=assess_reactor(); s=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(f,r,s,h,collect_layers())
