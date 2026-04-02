from typing import List, Optional
from .contracts import *
def assess_criticality()->CriticalityAssessment:
 return CriticalityAssessment('high','moderator/reflector coupling matters',['Subcritical handling still requires engineered geometry and administrative controls.'])
def assess_safeguards()->SafeguardsAssessment:
 return SafeguardsAssessment('MUF/shipper-receiver','elevated for separated Pu',['Separated plutonium raises safeguards and security design minima.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.68
 if p.claimed_no_criticality_engineering:
  flags.append('criticality_denial'); omega-=0.32; reasons.append('Criticality safety remains a first-order constraint for Pu-bearing systems.')
 if p.claimed_no_safeguards_burden:
  flags.append('safeguards_denial'); omega-=0.28; reasons.append('Safeguards and security overhead are intrinsic to separated special nuclear material.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Criticality discipline','Mass, geometry, moderation, and reflection set keff margins.'),ConceptLayer('Governance surface','Accountability, physical protection, and treaty context shape deployment.')]
def compute_health(crit=0.55,safety=0.5,waste=0.45,gov=0.48,econ=0.45)->HealthReport:
 axes=[crit,safety,waste,gov,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(crit,safety,waste,gov,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 c=assess_criticality(); s=assess_safeguards(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(c,s,sc,h,collect_layers())
