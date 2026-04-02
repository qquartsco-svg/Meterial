from typing import List, Optional
from .contracts import *
def assess_asf()->ASFAssessment:
 return ASFAssessment('Schulz-Flory style broadening','C1-C4 always competes with wax',['Perfect single-cut product slates contradict chain-growth statistics.'])
def assess_heat()->HeatIntegrationAssessment:
 return HeatIntegrationAssessment('multi-tube reactors','hydrocracking/isomerization add steps',['Read after Syngas_Water_Gas_Shift_Foundation; FT is downstream of ratio-clean syngas.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.68
 if p.claimed_only_diesel_no_light_ends:
  flags.append('selectivity_fantasy'); omega-=0.3; reasons.append('FT typically yields a distribution; eliminating light ends is not default.')
 if p.claimed_zero_co2_from_ft:
  flags.append('co2_byproduct_denial'); omega-=0.26; reasons.append('Water-gas shift coupling and regeneration burn CO2 burdens remain.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Product slate','Liquids plus gases define carbon efficiency narratives.'),ConceptLayer('Scale-up heat','Exotherm management scales with reactor technology class.')]
def compute_health(sel=0.55,ht=0.58,up=0.6,cat=0.57,econ=0.5)->HealthReport:
 axes=[sel,ht,up,cat,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(sel,ht,up,cat,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 a=assess_asf(); h=assess_heat(); sc=screen_claim(claim) if claim else None; hc=compute_health()
 return FoundationReport(a,h,sc,hc,collect_layers())
