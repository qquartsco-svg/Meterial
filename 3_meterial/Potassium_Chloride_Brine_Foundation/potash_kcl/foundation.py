from typing import List, Optional
from .contracts import *
def assess_mining()->MiningAssessment:
 return MiningAssessment('solar evaporation vs solution mining vs hard rock','NaCl and Mg salts dilute and complicate tails',['Read after Potassium_Foundation; brine physics parallels Sodium_Chlorine_Foundation halide grammar.'])
def assess_quality()->QualityAssessment:
 return QualityAssessment('some sedimentary beds carry Cd concerns','K2O equivalent labeling conventions',['Product stewardship narratives must track deposit geology, not generic KCl purity fantasy.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.66
 if p.claimed_trivial_ocean_kcl_without_energy:
  flags.append('potash_abundance_myth'); omega-=0.3; reasons.append('Concentrating KCl from seawater or brines is energy and capex intensive versus bulk NaCl narratives.')
 if p.claimed_zero_trace_heavy_metals:
  flags.append('impurity_denial'); omega-=0.26; reasons.append('Some potash ores require attention to trace elements and product specs.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Muriate of potash','MOP remains dominant K fertilizer salt.'),ConceptLayer('Brine kinship','Chloride loops tie K and Na process families.')]
def compute_health(sup=0.58,proc=0.55,qual=0.52,env=0.5,econ=0.56)->HealthReport:
 axes=[sup,proc,qual,env,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(sup,proc,qual,env,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 m=assess_mining(); q=assess_quality(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(m,q,sc,h,collect_layers())
