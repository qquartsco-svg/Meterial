from typing import List, Optional
from .contracts import *
def assess_technetium()->TechnetiumAssessment:
 return TechnetiumAssessment('fission Mo separation and accelerators','Mo-99/Tc-99m generator logistics',['Tc is not a bulk commodity like iron; medical supply chains are specialized.'])
def assess_promethium()->PromethiumAssessment:
 return PromethiumAssessment('nuclear reprocessing tails','all isotopes radioactive',['Pm cannot be inventoried like stable Pr/Nd; half-lives set logistics.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.68
 if p.claimed_natural_bulk_tc_pm:
  flags.append('synthetic_abundance_myth'); omega-=0.32; reasons.append('Tc and Pm are not geologically abundant bulk elements.')
 if p.claimed_pm_stable_inventory_like_pr:
  flags.append('pm_lanthanide_conflation'); omega-=0.3; reasons.append('Promethium has no stable isotope; Pr-style warehouse metaphors fail.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Synthetic d-block tail','Tc sits outside stable-element mining narratives.'),ConceptLayer('Lanthanide gap','Pm breaks stable rare-earth inventory metaphors.')]
def compute_health(sup=0.5,safe=0.58,gov=0.55,med=0.62,econ=0.52)->HealthReport:
 axes=[sup,safe,gov,med,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(sup,safe,gov,med,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 t=assess_technetium(); pr=assess_promethium(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(t,pr,sc,h,collect_layers())
