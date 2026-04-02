from typing import List, Optional
from .contracts import *
def assess_sources()->SourceAssessment:
 return SourceAssessment('electrolytic blow-out stacks common','caliche/brine and by-product routes',['Iodine markets can spike on supply shocks; bromine is more seawater-anchored.'])
def assess_safety()->SafetyAssessment:
 return SafetyAssessment('strong oxidizer chemistry class','medical and environmental iodine pathways require dose discipline',['Halogens are not fungible: reactivity and exposure routes differ sharply.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_halogens_interchangeable:
  flags.append('halogen_conflation'); omega-=0.3; reasons.append('I2, Br2, and Cl2 differ in vapor pressure, toxicity, and corrosion coupling.')
 if p.claimed_no_corrosion_or_toxicity_issue:
  flags.append('hazard_denial'); omega-=0.28; reasons.append('Elemental halogens and many halide process streams remain corrosive and regulated.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Supply morphology','Seawater Br vs iodine caliche/by-product define volatility.'),ConceptLayer('Regulatory biology','Iodine couples to human and ecosystem dose contexts.')]
def compute_health(sup=0.58,safe=0.55,proc=0.6,env=0.52,econ=0.56)->HealthReport:
 axes=[sup,safe,proc,env,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(sup,safe,proc,env,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 s=assess_sources(); sf=assess_safety(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(s,sf,sc,h,collect_layers())
