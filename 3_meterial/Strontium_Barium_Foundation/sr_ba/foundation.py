from typing import List, Optional
from .contracts import *
def assess_applications()->ApplicationAssessment:
 return ApplicationAssessment('hard ferrite chemistry','barite-weighted fluids',['Industrial Ba is often BaSO4 chemistry class, not interchangeable with soluble Ba salts.'])
def assess_speciation()->SpeciationAssessment:
 return SpeciationAssessment('BaSO4 sparingly toxic pathway vs Ba2+ acute','radioisotope context separate from stable Sr industrial use',['Confusing medical imaging barite with all Ba compounds is a common error.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_all_barium_safe_like_contrast_agent:
  flags.append('ba_speciation_conflation'); omega-=0.3; reasons.append('Soluble barium salts are not equivalent to BaSO4 imaging chemistry.')
 if p.claimed_strontium_always_benign:
  flags.append('sr_benign_myth'); omega-=0.22; reasons.append('Stable Sr industrial routes still carry dust and process hazards; radio-Sr is a separate governance class.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Mg/Ca axis extension','Read after Magnesium_Calcium_Foundation: heavier alkaline earth process fluids.'),ConceptLayer('Speciation first','Toxicology follows compound class, not element label alone.')]
def compute_health(tech=0.62,safe=0.55,env=0.52,sup=0.58,econ=0.56)->HealthReport:
 axes=[tech,safe,env,sup,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(tech,safe,env,sup,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 a=assess_applications(); s=assess_speciation(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(a,s,sc,h,collect_layers())
