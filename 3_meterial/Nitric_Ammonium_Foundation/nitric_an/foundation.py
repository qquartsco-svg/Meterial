from typing import List, Optional
from .contracts import *
def assess_ostwald()->OstwaldAssessment:
 return OstwaldAssessment('Pt/Rh net oxidation','absorption towers and tail gas treatment',['Nitric acid ties back to Ammonia_Process_Integration_Foundation feedstock.'])
def assess_an()->ANSafetyAssessment:
 return ANSafetyAssessment('strong oxidizer with organic contamination risk','storage and pile thermal runaway class',['AN is not urea in hazard class; security and fire narratives differ.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.66
 if p.claimed_an_inert_like_urea:
  flags.append('an_hazard_conflation'); omega-=0.32; reasons.append('Ammonium nitrate is a high-consequence oxidizer under upset conditions.')
 if p.claimed_zero_nox_abatement_cost:
  flags.append('nox_cost_denial'); omega-=0.24; reasons.append('NOx tail gas treatment and absorption loops carry capex and opex.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Downstream N chemistry','Nitric acid unlocks nitrates beyond urea.'),ConceptLayer('Governance surface','High-consequence fertilizers intersect security and transport rules.')]
def compute_health(proc=0.58,safe=0.5,env=0.55,gov=0.52,econ=0.54)->HealthReport:
 axes=[proc,safe,env,gov,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(proc,safe,env,gov,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 o=assess_ostwald(); a=assess_an(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(o,a,sc,h,collect_layers())
