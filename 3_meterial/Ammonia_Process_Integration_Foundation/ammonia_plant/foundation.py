from typing import List, Optional
from .contracts import *
def assess_reactor()->ReactorAssessment:
 return ReactorAssessment('high-pressure synthesis loop','poisoning by sulfur/chlorine traces',['Read after Nitrogen_Foundation for N2/Haber overview; here NH3 plant integration dominates.'])
def assess_hydrogen()->HydrogenCouplingAssessment:
 return HydrogenCouplingAssessment('SMR bundle vs green H2 import','recycle gas management',['Hydrogen_Foundation supplies H2 production grammar; this layer couples it to ammonia mass balance.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.68
 if p.claimed_zero_energy_ammonia:
  flags.append('haber_energy_denial'); omega-=0.34; reasons.append('Haber-Bosch remains one of the most energy-intensive commodity chemical loops.')
 if p.claimed_h2_source_irrelevant:
  flags.append('h2_coupling_denial'); omega-=0.26; reasons.append('Hydrogen sourcing and purity set catalyst life and carbon intensity narratives.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('NH3 as hub','Ammonia bridges fertilizers, explosives precursors, and marine fuel narratives.'),ConceptLayer('Recycle reality','Unconverted syngas components return with compression costs.')]
def compute_health(en=0.52,h2=0.58,cat=0.6,safe=0.62,econ=0.54)->HealthReport:
 axes=[en,h2,cat,safe,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(en,h2,cat,safe,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 r=assess_reactor(); h=assess_hydrogen(); sc=screen_claim(claim) if claim else None; hc=compute_health()
 return FoundationReport(r,h,sc,hc,collect_layers())
