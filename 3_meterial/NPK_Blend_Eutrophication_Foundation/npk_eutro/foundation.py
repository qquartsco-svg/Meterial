from typing import List, Optional
from .contracts import *
def assess_blend()->BlendAssessment:
 return BlendAssessment('sulfur or polymer coatings on urea','particle density differences segregate in transport',['Reads across Urea_CO2_Loop_Foundation, Ammonium_Phosphate_Foundation, Potassium_Chloride_Brine_Foundation inputs.'])
def assess_runoff()->RunoffAssessment:
 return RunoffAssessment('P attaches to soil particles yet also moves dissolved','nitrate mobile in sandy soils',['Eutrophication is watershed-scale, not bag-scale marketing.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.68
 if p.claimed_fertilizer_never_causes_algae:
  flags.append('eutrophication_denial'); omega-=0.34; reasons.append('Excess N and P loads routinely drive algal blooms when hydrology and management fail.')
 if p.claimed_perfect_blend_homogeneity:
  flags.append('blend_homogeneity_myth'); omega-=0.22; reasons.append('Bulk blends segregate in handling; quality control sampling is required.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('NPK systems view','Granular recipe ties three nutrient engines plus logistics.'),ConceptLayer('Water receiver','Rivers and lakes integrate cumulative loading.')]
def compute_health(agr=0.55,wq=0.48,log=0.58,gov=0.52,econ=0.54)->HealthReport:
 axes=[agr,wq,log,gov,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(agr,wq,log,gov,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 b=assess_blend(); r=assess_runoff(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(b,r,sc,h,collect_layers())
