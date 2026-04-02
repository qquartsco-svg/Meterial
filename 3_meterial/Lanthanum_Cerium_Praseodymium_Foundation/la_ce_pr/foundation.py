from typing import List, Optional
from .contracts import *
def assess_applications()->ApplicationAssessment:
 return ApplicationAssessment('petroleum FCC rare-earth additives','NiMH / polishing overlap','NdFeB dopant adjacency',['La-Ce-Pr sit upstream of many magnet and catalyst narratives.'])
def assess_separation()->SeparationAssessment:
 return SeparationAssessment('multi-stage SX typical','locked to bastnaesite/monazite/clay routes',['Purity is bought with acid, water, and reagent loops—not a single pot step.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.68
 if p.claimed_one_step_purity:
  flags.append('purity_fantasy'); omega-=0.3; reasons.append('Commercial RE separation is a cascade, not a one-step purity gate.')
 if p.claimed_zero_separation_energy:
  flags.append('energy_denial'); omega-=0.28; reasons.append('Roasting, leaching, and solvent extraction carry intrinsic energy and reagent costs.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Light lanthanide cluster','La/Ce/Pr co-move in mining and separation trains.'),ConceptLayer('Downstream coupling','Catalyst and battery routes recycle different fractions.')]
def compute_health(sep=0.55,recy=0.5,env=0.52,sup=0.58,econ=0.54)->HealthReport:
 axes=[sep,recy,env,sup,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(sep,recy,env,sup,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 a=assess_applications(); s=assess_separation(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(a,s,sc,h,collect_layers())
