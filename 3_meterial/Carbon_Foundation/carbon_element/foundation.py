from typing import List, Optional
from .contracts import *
def assess_allotrope()->AllotropeAssessment:
 return AllotropeAssessment('Diamond vs graphite vs graphene vs CF precursors are not interchangeable by name alone.','sp2-rich vs sp3 networks set transport, strength, and oxidation windows.',['Read with Carbon_Composite_Stack for resin-matrix systems; elemental C feedstock still matters.'])
def assess_cycle()->CycleAssessment:
 return CycleAssessment('CO2 is not inventory-grade elemental carbon without reduction work.','Battery-grade synthetic graphite and mined flake have different energy and impurity footprints.',['Tie to Syngas/FT only after explicit reduction/capture accounting.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.64
 if p.claimed_co2_is_elemental_carbon:
  flags.append('co2_element_conflation'); omega-=0.32; reasons.append('CO2 and elemental carbon inventories differ by stoichiometry and process work; do not conflate for mass balance.')
 if p.claimed_infinite_battery_graphite:
  flags.append('graphite_supply_myth'); omega-=0.28; reasons.append('Graphite anode demand competes with purity, energy, and geographic concentration narratives.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Allotrope ladder','Same Z, different networks and defect budgets.'),ConceptLayer('Embodied energy','From coke to fiber, the pathway sets the claim.')]
def compute_health(sup=0.55,proc=0.54,qual=0.53,env=0.5,econ=0.54)->HealthReport:
 axes=[sup,proc,qual,env,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(sup,proc,qual,env,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 a=assess_allotrope(); cy=assess_cycle(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(a,cy,sc,h,collect_layers())
