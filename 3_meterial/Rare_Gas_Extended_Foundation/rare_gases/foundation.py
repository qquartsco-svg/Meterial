from typing import List, Optional
from .contracts import *
def assess_supply()->SupplyChainAssessment:
 return SupplyChainAssessment('cryogenic air separation','historically spiky for Xe',['Ne/Ar are ASU staples; Kr/Xe are low-concentration tails with market sensitivity.'])
def assess_cryo()->CryoAssessment:
 return CryoAssessment('non-trivial','insulation + heat leak set standing losses',['Liquefaction and storage dominate lifecycle cost for bulk rare gases.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_unlimited_supply:
  flags.append('supply_myth'); omega-=0.3; reasons.append('Rare gas markets, especially Xe, have shown concentration and price volatility.')
 if p.claimed_zero_cryo_cost:
  flags.append('cryo_denial'); omega-=0.28; reasons.append('Cryogenic separation and storage are never zero-overhead.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]:
 return [ConceptLayer('ASU tail economics','Light noble gases tie to air separation and downstream purification.'),ConceptLayer('Mission coupling','Xe electric propulsion couples thruster demand to commodity tails.')]
def compute_health(sup=0.62,cryo=0.58,safe=0.72,log=0.6,econ=0.55)->HealthReport:
 axes=[sup,cryo,safe,log,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(sup,cryo,safe,log,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 s=assess_supply(); c=assess_cryo(); sc=screen_claim(claim) if claim else None; h=compute_health()
 return FoundationReport(s,c,sc,h,collect_layers())
