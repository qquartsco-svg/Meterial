from typing import List, Optional
from .contracts import *
def assess_electronics()->ElectronicsAssessment:
 return ElectronicsAssessment('transparent conductor stacks','Cu(In,Ga)Se2 indium demand',['Read after Gallium_Germanium_Foundation for III-V and CIGS adjacency.'])
def assess_toxicity()->ToxicityAssessment:
 return ToxicityAssessment('Tl+ acute poisoning class historically','indium lung exposure in poorly controlled refining',['Indium is not thallium; conflating Group 13 neighbors is a reasoning failure.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_in_tl_same_safety_class:
  flags.append('group13_conflation'); omega-=0.32; reasons.append('Thallium salts are among the most acutely toxic common metals; indium risk profiles differ.')
 if p.claimed_infinite_indium_byproduct:
  flags.append('in_supply_myth'); omega-=0.26; reasons.append('Indium remains by-product limited; touch/PV demand can stress effective supply.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Group 13 tail','In follows Ga in display and thin-film stacks; Tl is a different hazard class.'),ConceptLayer('By-product coupling','Zn/Pb smelting tails set indium ceilings.')]
def compute_health(tech=0.65,safe=0.55,sup=0.52,recy=0.48,econ=0.56)->HealthReport:
 axes=[tech,safe,sup,recy,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(tech,safe,sup,recy,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 e=assess_electronics(); t=assess_toxicity(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(e,t,sc,h,collect_layers())
