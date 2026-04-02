from typing import List, Optional
from .contracts import *
def assess_spinel()->SpinelAssessment: return SpinelAssessment('LiMn2O4/Co-Mn spinel','medium','medium',['Spinel can improve power but thermal/oxygen behavior still matters.'])
def assess_supply()->SupplyAssessment: return SupplyAssessment('high','low',['Cobalt remains major supply and ethics risk driver.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_no_thermal_runaway_contrib: flags.append('thermal_denial'); omega-=0.25; reasons.append('Cathode chemistry still contributes to thermal behavior.')
 if p.claimed_no_supply_risk: flags.append('supply_denial'); omega-=0.3; reasons.append('Cobalt chain risk cannot be ignored.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]: return [ConceptLayer('Spinel Stability','Spinel structures balance power density with thermal behavior constraints.'), ConceptLayer('Cobalt Dependency','Supply/ethics exposure remains with cobalt-including routes.')]
def compute_health(stab=0.65,safety=0.6,supply=0.45,recy=0.55,econ=0.6)->HealthReport:
 axes=[stab,safety,supply,recy,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(stab,safety,supply,recy,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 s=assess_spinel(); sp=assess_supply(); sc=screen_claim(claim) if claim else None; h=compute_health(supply=0.35 if sp.co_risk=='high' else 0.7)
 return FoundationReport(s,sp,sc,h,collect_layers())
