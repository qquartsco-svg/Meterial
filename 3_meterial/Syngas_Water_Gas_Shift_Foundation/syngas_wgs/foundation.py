from typing import List, Optional
from .contracts import *
def assess_reforming()->ReformingAssessment:
 return ReformingAssessment('CH4+H2O and partial oxidation/autothermal families','steam and oxygen logistics dominate',['Read after Hydrogen_Foundation; syngas is not pure H2 inventory.'])
def assess_shift()->ShiftAssessment:
 return ShiftAssessment('HTS/LTS staging common','methanol vs FT targets differ',['WGS moves CO+H2O toward CO2+H2 with heat management.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_co_benign_like_n2:
  flags.append('co_toxicity_denial'); omega-=0.35; reasons.append('CO is a chemical asphyxiant; never treat like N2 in confined spaces.')
 if p.claimed_shift_zero_energy_cost:
  flags.append('shift_thermo_denial'); omega-=0.26; reasons.append('Shift and reforming steps exchange heat and carry exergy costs.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Ratio engineering','Downstream synthesis sets required H2/CO and inerts tolerance.'),ConceptLayer('Gas safety','CO leaks differ from inert purge gases.')]
def compute_health(integ=0.62,safe=0.55,heat=0.58,cat=0.6,econ=0.54)->HealthReport:
 axes=[integ,safe,heat,cat,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(integ,safe,heat,cat,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 r=assess_reforming(); s=assess_shift(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(r,s,sc,h,collect_layers())
