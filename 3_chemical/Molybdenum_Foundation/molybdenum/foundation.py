from typing import List, Optional
from .contracts import *
def assess_alloy()->AlloyAssessment: return AlloyAssessment(0.04,'high',['Mo improves high-temp creep resistance in steels/superalloys.'])
def assess_catalyst()->CatalystAssessment: return CatalystAssessment('MoS2-derived','medium',['Catalyst poisoning/deactivation remains a practical limit.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_no_poisoning: flags.append('poisoning_denial'); omega-=0.25; reasons.append('Catalyst poisoning/deactivation cannot be ignored in long operation.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v, round(max(omega,0),3), flags, reasons)
def collect_layers()->List[ConceptLayer]: return [ConceptLayer('High-Temp Alloying','Mo additions increase creep strength at elevated temperatures.'), ConceptLayer('Catalyst Durability','Activity gains must be balanced with poisoning/deactivation controls.')]
def compute_health(alloy=0.7,cat=0.6,safety=0.75,supply=0.55,econ=0.6)->HealthReport:
 axes=[alloy,cat,safety,supply,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(alloy,cat,safety,supply,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 a=assess_alloy(); c=assess_catalyst(); s=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(a,c,s,h,collect_layers())
