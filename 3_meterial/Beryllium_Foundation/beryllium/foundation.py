from typing import List, Optional
from .contracts import *
def assess_materials()->MaterialAssessment:
 return MaterialAssessment('aerospace/thermal interfaces','favorable specific stiffness',['Be alloys are valued for stiffness-to-mass but remain niche and costly.'])
def assess_safety()->SafetyAssessment:
 return SafetyAssessment('high if dust generated','mandatory for particulate routes',['Chronic Be exposure can cause berylliosis; processes must control dust and fume.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_no_respiratory_risk:
  flags.append('respiratory_denial'); omega-=0.32; reasons.append('Be particulates pose documented chronic lung disease risk when uncontrolled.')
 if p.claimed_trivial_machining:
  flags.append('machining_denial'); omega-=0.22; reasons.append('Be is brittle and hazardous to machine; specialized controls are expected.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Specific stiffness','Be offers high modulus per mass for selected thermal/mechanical roles.'),ConceptLayer('Toxicology guardrails','Inhalable Be requires containment, ventilation, and occupational hygiene.')]
def compute_health(mat=0.65,safe=0.5,sup=0.45,proc=0.55,econ=0.5)->HealthReport:
 axes=[mat,safe,sup,proc,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(mat,safe,sup,proc,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 m=assess_materials(); s=assess_safety(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(m,s,sc,h,collect_layers())
