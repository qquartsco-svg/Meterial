from typing import List, Optional
from .contracts import *
def assess_stoich()->StoichiometryAssessment:
 return StoichiometryAssessment('Typical bag grades: MAP carries more P2O5 per unit N than DAP; verify N–P2O5 on the label.','Soil pH footprint differs by product and rate; MAP often more acidifying per unit P than DAP in extension summaries—use soil tests.',['Read after Phosphorus_Foundation; NH3 supply couples to Ammonia_Process_Integration_Foundation.'])
def assess_handling()->HandlingAssessment:
 return HandlingAssessment('both salts are moisture sensitive','pile height and cladding matter',['Blending with urea can accelerate quality loss if unmanaged.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.68
 if p.claimed_map_dap_fungible_no_agronomy:
  flags.append('np_ratio_conflation'); omega-=0.3; reasons.append('MAP and DAP differ in N/P mass ratio and soil pH footprints; not blindly interchangeable.')
 if p.claimed_no_caking_or_moisture_risk:
  flags.append('caking_denial'); omega-=0.24; reasons.append('Ammonium phosphates are hygroscopic; moisture management is operational reality.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('N-P bridge','Granular P carriers often carry ammonium nitrogen in the same crystal.'),ConceptLayer('Logistics coupling','Ocean freight and humidity set shelf behavior.')]
def compute_health(agr=0.6,han=0.55,sup=0.58,env=0.52,econ=0.56)->HealthReport:
 axes=[agr,han,sup,env,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(agr,han,sup,env,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 s=assess_stoich(); h=assess_handling(); sc=screen_claim(claim) if claim else None; hc=compute_health()
 return FoundationReport(s,h,sc,hc,collect_layers())
