from typing import List, Optional
from .contracts import *
def assess_electrochem()->ElectrochemAssessment:
 return ElectrochemAssessment('DSA and chlor-alkali / PEM contexts','thin noble coatings wear and dissolve over time',['Read after Platinum_Group_Foundation for shared PGM supply grammar.'])
def assess_hazard()->HazardAssessment:
 return HazardAssessment('volatile Os oxide extreme toxicity class','sealed lab/industrial protocols only',['Bulk Os metal is not the same hazard class as OsO4 vapor pathways.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.66
 if p.claimed_osmium_benign_bulk:
  flags.append('os_hazard_conflation'); omega-=0.3; reasons.append('Osmium chemistry includes high-toxicity volatile oxide forms; casual benign claims fail.')
 if p.claimed_pgm_byproduct_unlimited:
  flags.append('pgm_supply_myth'); omega-=0.28; reasons.append('Ru/Ir/Os still trace PGMs with mining and refining bottlenecks.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('PGM extension','Ru/Ir/Os follow Pt/Pd/Rh supply stories with different hazard peaks.'),ConceptLayer('Coating economics','Electrodes are material-thin but cost-heavy.')]
def compute_health(ele=0.68,safe=0.52,sup=0.48,recy=0.5,econ=0.52)->HealthReport:
 axes=[ele,safe,sup,recy,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(ele,safe,sup,recy,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 e=assess_electrochem(); h=assess_hazard(); sc=screen_claim(claim) if claim else None; hc=compute_health()
 return FoundationReport(e,h,sc,hc,collect_layers())
