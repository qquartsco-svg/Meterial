from typing import List, Optional
from .contracts import *
def assess_tooling()->ToolingAssessment: return ToolingAssessment(18.0,'medium',['WC systems are hard but brittle under shock loads.'])
def assess_high_temp(operating_temp_c: float=1200)->HighTempAssessment:
 risk='high' if operating_temp_c>1000 else 'medium'
 return HighTempAssessment(operating_temp_c,risk,['Oxidation protection/coatings are often required at elevated temperatures.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_no_brittleness: flags.append('brittleness_denial'); omega-=0.25; reasons.append('Extreme hardness generally trades off toughness.')
 if p.claimed_no_oxidation: flags.append('oxidation_denial'); omega-=0.25; reasons.append('High-temp oxidation remains a material-system constraint.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v, round(max(omega,0),3), flags, reasons)
def collect_layers()->List[ConceptLayer]: return [ConceptLayer('Extreme Temperature','W-based systems operate where many alloys soften.'), ConceptLayer('Hardness vs Toughness','Wear resistance is high but impact brittleness must be managed.')]
def compute_health(tool=0.7,ht=0.6,safety=0.7,supply=0.55,econ=0.55)->HealthReport:
 axes=[tool,ht,safety,supply,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(tool,ht,safety,supply,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 t=assess_tooling(); h=assess_high_temp(); s=screen_claim(claim) if claim else None
 hp=compute_health(ht=0.45 if h.oxidation_risk=='high' else 0.65)
 return FoundationReport(t,h,s,hp,collect_layers())
