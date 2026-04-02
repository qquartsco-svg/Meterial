from typing import List, Optional
from .contracts import *
def assess_decay()->DecayChainAssessment:
 return DecayChainAssessment('Rn daughters from U/Th decay in rocks and building materials','3.8-day Rn-222 dominates many indoor narratives',['Alpha dose to lungs matters; chemical inertness does not imply radiological harmlessness.'])
def assess_indoor()->IndoorAssessment:
 return IndoorAssessment('basement/stack effect and permeation','long-term track detectors vs grab samples',['Read after Rare_Gas_Extended_Foundation for gas-phase transport; source terms tie to Uranium_Thorium_Foundation geology.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.68
 if p.claimed_inert_like_neon_no_dose:
  flags.append('noble_gas_dose_conflation'); omega-=0.32; reasons.append('Radon is chemically noble but radiologically active; dose pathways differ from stable Ne/Ar/Xe.')
 if p.claimed_no_geologic_source_link:
  flags.append('source_chain_denial'); omega-=0.28; reasons.append('Indoor Rn traces U/Th-bearing substrates and permeability paths.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('Noble but radioactive','Phase behavior resembles rare gases; risk is decay not corrosion.'),ConceptLayer('Building geology coupling','Source strength is site-specific, not universal background fiction.')]
def compute_health(safe=0.55,meas=0.6,geo=0.58,gov=0.62,econ=0.52)->HealthReport:
 axes=[safe,meas,geo,gov,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(safe,meas,geo,gov,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 d=assess_decay(); i=assess_indoor(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(d,i,sc,h,collect_layers())
