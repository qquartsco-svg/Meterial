from typing import List, Optional
from .contracts import *
def assess_solder()->SolderAssessment:
 return SolderAssessment('Sn-Pb legacy vs SAC lead-free','medium-high for SAC','flux-dependent',['Lead-free Sn finishes can grow whiskers under stress; Pb-Sn is regulated but mature.'])
def assess_environmental()->EnvironmentalAssessment:
 return EnvironmentalAssessment('dust/fume ingestion','RoHS restricts Pb in many electronics streams',['Pb toxicity and disposal rules remain first-order for Pb-bearing processes.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.72
 if p.claimed_no_whisker_issue:
  flags.append('whisker_denial'); omega-=0.28; reasons.append('Tin whisker risk is not universally eliminable for Sn-rich systems.')
 if p.claimed_pb_harmless_without_controls:
  flags.append('pb_toxicity_denial'); omega-=0.35; reasons.append('Lead exposure pathways require engineering and regulatory controls.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Interconnect reliability','Solder joints couple wetting, IMC growth, and mechanical fatigue.'),ConceptLayer('Pb stewardship','Pb use is increasingly constrained; substitutes bring new failure modes.')]
def compute_health(proc=0.68,rel=0.62,safe=0.55,comp=0.7,econ=0.65)->HealthReport:
 axes=[proc,rel,safe,comp,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(proc,rel,safe,comp,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 s=assess_solder(); e=assess_environmental(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(s,e,sc,h,collect_layers())
