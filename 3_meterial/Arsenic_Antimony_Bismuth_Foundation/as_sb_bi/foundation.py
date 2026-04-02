from typing import List, Optional
from .contracts import *
def assess_applications()->ApplicationAssessment:
 return ApplicationAssessment('III-V semiconductors','halogenated synergists historically','fusible alloys, some pharma contexts',['Use cases differ widely; toxicity profiles are not interchangeable across As/Sb/Bi.'])
def assess_toxicity()->ToxicityAssessment:
 return ToxicityAssessment('As highest concern class; Sb elevated; Bi milder but not inert','As mobility in groundwater is a classic constraint',['Lumping pnictogens as uniformly safe is a common reasoning failure.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_group_equally_safe:
  flags.append('toxicity_conflation'); omega-=0.3; reasons.append('As, Sb, and Bi do not share equivalent toxicology or environmental fate.')
 if p.claimed_no_environmental_mobility:
  flags.append('mobility_denial'); omega-=0.25; reasons.append('Arsenic especially can exhibit significant environmental mobility depending on speciation.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Pnictogen spread','Same column does not imply identical hazard classes.'),ConceptLayer('Engineering uses','High-tech and legacy applications impose different release pathways.')]
def compute_health(tech=0.62,safe=0.5,env=0.48,sup=0.6,econ=0.58)->HealthReport:
 axes=[tech,safe,env,sup,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(tech,safe,env,sup,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 a=assess_applications(); t=assess_toxicity(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(a,t,sc,h,collect_layers())
