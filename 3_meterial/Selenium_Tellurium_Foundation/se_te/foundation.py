from typing import List, Optional
from .contracts import *
def assess_tech()->TechAssessment:
 return TechAssessment('CdTe thin film stack','Cu(In,Ga)Se2 absorber',['Te routes often couple to `Cadmium_Mercury_Foundation` via CdTe supply narratives.'])
def assess_supply()->SupplyAssessment:
 return SupplyAssessment('often electrolytic Cu refining by-product','Te especially thin',['Tellurium is not an abundant primary commodity like sulfur from acid plants.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_chalcogen_same_hazard_as_sulfur_only:
  flags.append('chalcogen_conflation'); omega-=0.26; reasons.append('Se/Te semiconductor and fume toxicology differ from bulk sulfuric acid plant narratives.')
 if p.claimed_infinite_tellurium:
  flags.append('te_abundance_myth'); omega-=0.3; reasons.append('Tellurium supply is by-product limited and historically volatile.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Sulfur axis extension','Read after Sulfur_Foundation: same group, different supply and thin-film coupling.'),ConceptLayer('By-product ceiling','Te economics trace copper electrorefining, not sulfur mining alone.')]
def compute_health(tech=0.65,sup=0.5,safe=0.58,recy=0.52,econ=0.54)->HealthReport:
 axes=[tech,sup,safe,recy,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(tech,sup,safe,recy,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 t=assess_tech(); s=assess_supply(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(t,s,sc,h,collect_layers())
