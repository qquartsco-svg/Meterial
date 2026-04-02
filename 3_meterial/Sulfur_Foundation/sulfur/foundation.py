from __future__ import annotations
from typing import List, Optional
from .contracts import *

def assess_process()->SulfurProcessAssessment:
    return SulfurProcessAssessment(500.0,0.95,['SO2 scrubbing/oxidation controls dominate permitting risk.'])

def assess_li_s_battery()->SulfurBatteryAssessment:
    return SulfurBatteryAssessment('Li-S',400.0,500,'high',['High theoretical energy; shuttle effect and cycle life remain challenges.'])

def screen_sulfur_claim(payload: SulfurClaimPayload)->SulfurScreeningReport:
    flags=[]; reasons=[]; omega=0.7
    if payload.claimed_zero_so2_pollution: flags.append('so2_denial'); omega-=0.3; reasons.append('Sulfur routes need strict SOx controls.')
    if payload.claimed_lis_no_shuttle_effect: flags.append('lis_shuttle_denial'); omega-=0.25; reasons.append('Li-S shuttle effect is a known degradation mechanism.')
    v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
    if not reasons: reasons.append('No specific issues detected.')
    return SulfurScreeningReport(v,round(max(omega,0),3),flags,reasons)

def collect_concept_layers()->List[ConceptLayer]:
    return [ConceptLayer('Sulfur Industry','Sulfuric acid is a backbone chemical with environmental controls as first-class constraints.'), ConceptLayer('Li-S Battery','High energy promise with unresolved shuttle/lifetime constraints.')]

def compute_health(proc=0.7,env=0.6,batt=0.5,safety=0.7,econ=0.65)->SulfurHealthReport:
    axes=[proc,env,batt,safety,econ]; c=round(sum(axes)/len(axes),3)
    v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
    return SulfurHealthReport(proc,env,batt,safety,econ,c,v)

def run_sulfur_foundation(claim: Optional[SulfurClaimPayload]=None)->SulfurFoundationReport:
    p=assess_process(); b=assess_li_s_battery(); s=screen_sulfur_claim(claim) if claim else None
    h=compute_health(env=p.so2_control_efficiency, batt=min(b.cycle_life/1200,1.0))
    return SulfurFoundationReport(p,b,s,h,collect_concept_layers())
