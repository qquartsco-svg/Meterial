from typing import List, Optional
from .contracts import *
def assess_pathways()->PathwayAssessment:
 return PathwayAssessment('plating, NiCd legacy, pigments','thermometers/amalgams, industrial releases',['Both elements bioaccumulate; Hg vapor is acutely and chronically hazardous.'])
def assess_regulatory()->RegulatoryAssessment:
 return RegulatoryAssessment('restricted in many product streams','treatment and tracking required',['Substitution and end-of-life rules increasingly push Cd/Hg out of mass-market goods.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.68
 if p.claimed_no_exposure_risk:
  flags.append('exposure_denial'); omega-=0.3; reasons.append('Cd ingestion/inhalation and Hg routes remain occupational and environmental concerns.')
 if p.claimed_safe_mercury_vapor:
  flags.append('hg_vapor_denial'); omega-=0.35; reasons.append('Mercury vapor is not benign without containment and exposure controls.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Bioaccumulation','Cd and Hg move through food chains and workplace air.'),ConceptLayer('Regulatory displacement','Product bans and recycling rules reshape viable applications.')]
def compute_health(safe=0.45,comp=0.6,waste=0.5,sub=0.55,econ=0.5)->HealthReport:
 axes=[safe,comp,waste,sub,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(safe,comp,waste,sub,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 p=assess_pathways(); r=assess_regulatory(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(p,r,sc,h,collect_layers())
