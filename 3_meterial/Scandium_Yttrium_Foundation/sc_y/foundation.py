from typing import List, Optional
from .contracts import *
def assess_alloy_ceramic()->AlloyCeramicAssessment:
 return AlloyCeramicAssessment('Al-Sc grain refinement','Y-stabilized ZrO2 ionic conductor',['Sc and Y link high-performance metals and functional ceramics.'])
def assess_supply()->SupplyAssessment:
 return SupplyAssessment('often RE processing tails','moderate concentration in supply narratives',['Neither Sc nor Y is typically mined as a pure primary like iron ore.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_trivial_supply:
  flags.append('supply_myth'); omega-=0.28; reasons.append('Sc/Y economics remain tied to separation and by-product recovery.')
 if p.claimed_no_separation_tail_cost:
  flags.append('separation_denial'); omega-=0.25; reasons.append('Solvent extraction and purification tails dominate light/heavy RE pathways.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Functional coupling','Microalloying and stabilizer roles differ but share RE infrastructure.'),ConceptLayer('By-product economics','Pricing traces what the main RE stream optimizes for.')]
def compute_health(tech=0.68,sup=0.52,proc=0.6,recy=0.48,econ=0.55)->HealthReport:
 axes=[tech,sup,proc,recy,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(tech,sup,proc,recy,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 a=assess_alloy_ceramic(); s=assess_supply(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(a,s,sc,h,collect_layers())
