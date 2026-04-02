from typing import List, Optional
from .contracts import *
def assess_alloy()->AlloyAssessment:
 return AlloyAssessment('3rd row strengthener in Ni superalloys','Re slows diffusion; cost and sourcing cap penetration',['Read after Molybdenum_Foundation and Tungsten_Foundation for refractory context.'])
def assess_catalyst()->CatalystAssessment:
 return CatalystAssessment('Pt-Re reforming historically','coke/sinter management',['Catalyst life is not infinite; regeneration has energy and loss terms.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.68
 if p.claimed_abundant_rhenium:
  flags.append('re_abundance_myth'); omega-=0.32; reasons.append('Re is rare and tied to Cu/Mo processing tails; not a bulk commodity.')
 if p.claimed_drop_in_replace_moly:
  flags.append('mo_re_conflation'); omega-=0.24; reasons.append('Mo and Re differ in cost, availability, and alloy/catalyst roles.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Group 6 tail','Re extends refractory/catalyst narratives after Mo/W.'),ConceptLayer('By-product ceiling','Supply traces roasting and anode slime paths, not iron ore scale.')]
def compute_health(alloy=0.72,cat=0.6,sup=0.42,recy=0.48,econ=0.5)->HealthReport:
 axes=[alloy,cat,sup,recy,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(alloy,cat,sup,recy,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 a=assess_alloy(); c=assess_catalyst(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(a,c,sc,h,collect_layers())
