from typing import List, Optional
from .contracts import *
def assess_stoich()->StoichiometryAssessment:
 return StoichiometryAssessment('ammonium carbamate intermediate','stripper/evaporator heat duty',['Urea couples nitrogen fertilizer demand to CO2 logistics.'])
def assess_co2()->CO2SourceAssessment:
 return CO2SourceAssessment('CO2 from ammonia reforming train common','purification and compression not optional',['Element_Capture_Foundation frames generic CO2 separation; here urea sets purity and pressure context.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.68
 if p.claimed_free_pure_co2_anywhere:
  flags.append('co2_purity_myth'); omega-=0.3; reasons.append('Food-grade or high-purity CO2 has conditioning and transport costs.')
 if p.claimed_no_stripper_steam:
  flags.append('stripper_energy_denial'); omega-=0.26; reasons.append('Melt and stripper sections carry substantial steam and vacuum burdens.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('N-P-K coupling','Urea is central to nitrogen fertilizer logistics.'),ConceptLayer('Carbon loop honesty','CO2 source attribution affects carbon accounting stories.')]
def compute_health(co2=0.55,en=0.52,integ=0.58,env=0.54,econ=0.56)->HealthReport:
 axes=[co2,en,integ,env,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(co2,en,integ,env,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 s=assess_stoich(); c=assess_co2(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(s,c,sc,h,collect_layers())
