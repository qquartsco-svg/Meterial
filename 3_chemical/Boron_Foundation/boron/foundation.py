from typing import List, Optional
from .contracts import *
def assess_glass()->GlassAssessment: return GlassAssessment(0.13,'high',['Borosilicate improves thermal shock tolerance.'])
def assess_composite()->CompositeAssessment: return CompositeAssessment(0.45,'medium',['Boron fiber boosts stiffness but brittleness/process cost rise.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_no_brittleness_tradeoff: flags.append('brittleness_denial'); omega-=0.25; reasons.append('High-stiffness boron systems can trade ductility/toughness.')
 if p.claimed_infinite_doping_gain: flags.append('doping_hype'); omega-=0.25; reasons.append('Semiconductor doping gains are bounded by device physics/process windows.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v, round(max(omega,0),3), flags, reasons)
def collect_layers()->List[ConceptLayer]: return [ConceptLayer('Borosilicate Thermal Control','Boron lowers CTE and improves thermal shock behavior.'), ConceptLayer('Boron Fiber Trade-off','High stiffness with process/cost and brittleness constraints.')]
def compute_health(th=0.75,mech=0.6,proc=0.55,safety=0.75,econ=0.55)->HealthReport:
 axes=[th,mech,proc,safety,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(th,mech,proc,safety,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 g=assess_glass(); c=assess_composite(); s=screen_claim(claim) if claim else None
 h=compute_health(mech=0.55 if c.brittleness_risk=='medium' else 0.75)
 return FoundationReport(g,c,s,h,collect_layers())
