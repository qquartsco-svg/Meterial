from typing import List, Optional
from .contracts import *
def assess_catalyst()->CatalystAssessment: return CatalystAssessment('high','medium',['Ceria-based systems buffer oxygen but still deactivate in contaminants.'])
def assess_materials()->MaterialsAssessment: return MaterialsAssessment('high','medium',['Ce/La polishing slurries need waste handling discipline.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_no_deactivation: flags.append('deactivation_denial'); omega-=0.25; reasons.append('Catalyst deactivation cannot be fully eliminated.')
 if p.claimed_no_waste_issue: flags.append('waste_denial'); omega-=0.2; reasons.append('Slurry and process waste require treatment/control.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v, round(max(omega,0),3), flags, reasons)
def collect_layers()->List[ConceptLayer]: return [ConceptLayer('Oxygen Storage Catalysis','Ce oxides enable redox buffering in catalytic cycles.'), ConceptLayer('Process Waste','Polishing/ceramic pathways bring waste-treatment constraints.')]
def compute_health(cat=0.7,mat=0.65,supply=0.5,safety=0.75,econ=0.6)->HealthReport:
 axes=[cat,mat,supply,safety,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(cat,mat,supply,safety,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 c=assess_catalyst(); m=assess_materials(); s=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(c,m,s,h,collect_layers())
