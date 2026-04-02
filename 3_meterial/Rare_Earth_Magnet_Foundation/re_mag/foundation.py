from typing import List, Optional
from .contracts import *
def assess_magnet()->MagnetAssessment: return MagnetAssessment(1.3,900.0,'medium',['High flux density with thermal demagnetization management needed.'])
def assess_supply()->SupplyAssessment: return SupplyAssessment('high','high','high',['Nd/Dy concentration and processing bottlenecks are strategic risks.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_no_demag_risk: flags.append('demag_denial'); omega-=0.25; reasons.append('Rare-earth magnets can demagnetize with heat/field stress.')
 if p.claimed_no_supply_risk: flags.append('supply_denial'); omega-=0.3; reasons.append('Rare-earth supply concentration and refining constraints are real.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]: return [ConceptLayer('Magnet Performance','NdFeB enables compact high-torque machines.'), ConceptLayer('Thermal/Supply Limits','Dy additions improve high-temp stability but increase supply pressure.')]
def compute_health(mp=0.8,th=0.6,supply=0.35,safety=0.8,econ=0.45)->HealthReport:
 axes=[mp,th,supply,safety,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(mp,th,supply,safety,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 m=assess_magnet(); s=assess_supply(); sc=screen_claim(claim) if claim else None; h=compute_health(supply=0.3 if s.nd_risk=='high' else 0.7, th=0.55 if m.thermal_risk=='medium' else 0.75)
 return FoundationReport(m,s,sc,h,collect_layers())
