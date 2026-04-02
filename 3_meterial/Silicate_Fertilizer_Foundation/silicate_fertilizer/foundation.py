from typing import List, Optional
from .contracts import *
def assess_substances()->SubstancesAssessment:
 return SubstancesAssessment('K/Ca/Mg silicates, slags, and rock meals vs orthophosphate solutions','Weathering-limited release vs immediate ortho-P uptake windows',['Read after Silicon_Foundation: wafer-grade Si is not the same narrative as soil Si supplementation.'])
def assess_release()->ReleaseAssessment:
 return ReleaseAssessment('pH, particle size, and microbial weathering set effective rates','Strong-acid blends or ultrafines shift dust and worker exposure profiles',['Schedule with soil tests; not a blind swap for MAP/DAP timing.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.63
 if p.claimed_silicate_fungible_with_map:
  flags.append('soluble_p_conflation'); omega-=0.3; reasons.append('Silicate carriers are not interchangeable with soluble phosphate schedules without agronomic redesign.')
 if p.claimed_instant_plant_si:
  flags.append('silicate_release_myth'); omega-=0.25; reasons.append('Plant-available Si pathways are kinetic; instant uptake claims need mechanistic backing.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Soil mineralogy','Secondary phases buffer what labels imply.'),ConceptLayer('Industrial symbiosis','Slag and ash products carry trace metal disclosure duties.')]
def compute_health(sup=0.56,proc=0.55,qual=0.53,env=0.51,econ=0.54)->HealthReport:
 axes=[sup,proc,qual,env,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(sup,proc,qual,env,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 s=assess_substances(); r=assess_release(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(s,r,sc,h,collect_layers())
