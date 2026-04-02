from typing import List, Optional
from .contracts import *
def assess_device()->DeviceAssessment: return DeviceAssessment('GaN/Ge','high','medium',['High switching performance with packaging thermal constraints.'])
def assess_supply()->SupplyAssessment: return SupplyAssessment('medium','medium','high',['By-product supply paths increase concentration and recovery constraints.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_unlimited_supply: flags.append('supply_denial'); omega-=0.3; reasons.append('Ga/Ge supply is not unlimited; refining/recovery bottlenecks exist.')
 if p.claimed_no_thermal_constraints: flags.append('thermal_denial'); omega-=0.25; reasons.append('High-power devices remain thermally constrained at module level.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]: return [ConceptLayer('Bandgap Tradeoff','GaN high bandgap enables power density gains; Ge supports high-speed/photonics niches.'), ConceptLayer('Supply Coupling','By-product dependence raises strategic supply sensitivity.')]
def compute_health(dev=0.75,th=0.6,supply=0.5,recy=0.55,econ=0.55)->HealthReport:
 axes=[dev,th,supply,recy,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(dev,th,supply,recy,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 d=assess_device(); s=assess_supply(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(d,s,sc,h,collect_layers())
