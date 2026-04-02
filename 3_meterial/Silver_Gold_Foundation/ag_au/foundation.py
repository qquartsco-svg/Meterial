from typing import List, Optional
from .contracts import *
def assess_conductor()->ConductorAssessment: return ConductorAssessment(1,'high',['Ag has top electrical conductivity; tarnish/contact design still matters.'])
def assess_noble()->NobleMetalAssessment: return NobleMetalAssessment('high','high',['Au resists corrosion but plating and sourcing cost are significant.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_zero_cost_penalty: flags.append('cost_denial'); omega-=0.3; reasons.append('Ag/Au performance comes with cost and supply penalties.')
 if p.claimed_no_migration_issue: flags.append('migration_denial'); omega-=0.2; reasons.append('Ag migration/contact issues can appear under bias/humidity contexts.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]: return [ConceptLayer('Ag Conductivity','Highest conductivity with practical packaging/contact caveats.'), ConceptLayer('Au Reliability','Corrosion resistance and stable contacts at cost/supply trade-offs.')]
def compute_health(perf=0.8,rel=0.75,supply=0.5,safety=0.85,econ=0.45)->HealthReport:
 axes=[perf,rel,supply,safety,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(perf,rel,supply,safety,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 c=assess_conductor(); n=assess_noble(); s=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(c,n,s,h,collect_layers())
