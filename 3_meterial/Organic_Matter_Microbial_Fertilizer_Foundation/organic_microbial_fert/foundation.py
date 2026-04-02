from typing import List, Optional
from .contracts import *
def assess_recycle()->RecycleAssessment:
 return RecycleAssessment('Manure, digestate, compost, and biosolids carry C:N and salt loads','Mineralization lags can miss crop demand peaks',['Read after NPK_Blend_Eutrophication_Foundation: organic systems still export nutrients to water.'])
def assess_biology()->BiologyAssessment:
 return BiologyAssessment('Process validation beats adjectives (pathogen indicators, stabilization)','Microbial inoculants are context-specific, not generic yield multipliers',['Regulatory categories differ by jurisdiction; do not conflate with synthetic N safety calculus.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.62
 if p.claimed_organic_always_safe:
  flags.append('organic_safety_denial'); omega-=0.28; reasons.append('Organic amendments can carry pathogens, salts, and metals; management and testing matter.')
 if p.claimed_instant_N_release:
  flags.append('instant_mineralization_myth'); omega-=0.27; reasons.append('N release from organic pools is microbially gated; instant availability claims need rate data.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Soil food web','C quality modulates who gets fed first.'),ConceptLayer('Odor and neighbors','Logistics and social license are part of the system.')]
def compute_health(sup=0.55,proc=0.52,qual=0.5,env=0.49,econ=0.53)->HealthReport:
 axes=[sup,proc,qual,env,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(sup,proc,qual,env,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 r=assess_recycle(); b=assess_biology(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(r,b,sc,h,collect_layers())
