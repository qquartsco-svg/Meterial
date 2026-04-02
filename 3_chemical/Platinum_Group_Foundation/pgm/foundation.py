from typing import List, Optional
from .contracts import *
def assess_catalyst()->CatalystAssessment: return CatalystAssessment('Pt/Pd/Rh','high','medium',['High catalytic activity with poisoning/sintering management requirements.'])
def assess_supply()->SupplyAssessment: return SupplyAssessment('high','high',['PGM supply is concentrated; recycling is strategic, not optional.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_no_poisoning: flags.append('poisoning_denial'); omega-=0.25; reasons.append('Catalyst poisoning/deactivation remains operational reality.')
 if p.claimed_no_supply_risk: flags.append('supply_denial'); omega-=0.3; reasons.append('PGM supply concentration and price volatility are significant.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]: return [ConceptLayer('Catalyst Power','PGMs enable key reactions at practical rates.'), ConceptLayer('Critical Supply','Concentrated mining + recycling dependence shape system risk.')]
def compute_health(act=0.8,dur=0.6,supply=0.4,safety=0.8,econ=0.45)->HealthReport:
 axes=[act,dur,supply,safety,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(act,dur,supply,safety,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 c=assess_catalyst(); s=assess_supply(); sc=screen_claim(claim) if claim else None; h=compute_health(supply=0.35 if s.concentration_risk=='high' else 0.7)
 return FoundationReport(c,s,sc,h,collect_layers())
