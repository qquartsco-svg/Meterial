from typing import List, Optional
from .contracts import *
def assess_stoich()->StoichiometryAssessment:
 return StoichiometryAssessment('CO + 2 H2 -> CH3OH nominal','argon/methane tails need purge policy',['Read after Syngas_Water_Gas_Shift_Foundation for feed ratio reality.'])
def assess_process()->ProcessAssessment:
 return ProcessAssessment('loop gas boosters','sulfur/chloride sensitivity',['Commercial loops tolerate only bounded single-pass conversion.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.68
 if p.claimed_single_pass_full_conversion:
  flags.append('conversion_fantasy'); omega-=0.32; reasons.append('Methanol synthesis is equilibrium-limited; recycle is standard, not optional magic.')
 if p.claimed_no_catalyst_decay:
  flags.append('catalyst_denial'); omega-=0.24; reasons.append('Catalyst deactivation and poisons remain first-order constraints.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Recycle physics','Unreacted syngas returns with heat integration penalties.'),ConceptLayer('Downstream bridge','Methanol is hub to fuels, olefins, and formaldehyde families in other engines later.')]
def compute_health(eq=0.58,rec=0.6,safe=0.62,cat=0.55,econ=0.56)->HealthReport:
 axes=[eq,rec,safe,cat,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(eq,rec,safe,cat,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 s=assess_stoich(); pr=assess_process(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(s,pr,sc,h,collect_layers())
