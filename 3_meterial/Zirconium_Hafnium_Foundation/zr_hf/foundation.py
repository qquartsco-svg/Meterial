from typing import List, Optional
from .contracts import *
def assess_nuclear()->NuclearAssessment: return NuclearAssessment('high','high',['Zr for reactor use requires very low Hf due to neutron capture contrast.'])
def assess_ceramic()->CeramicAssessment: return CeramicAssessment('high','high',['Hf-containing ceramics excel at high T but are processing-intensive.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_no_separation_complexity: flags.append('separation_denial'); omega-=0.3; reasons.append('Zr/Hf separation is chemically difficult and cost-driving.')
 if p.claimed_no_processing_risk: flags.append('processing_denial'); omega-=0.25; reasons.append('High-temp ceramic processing has non-trivial risk and cost.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v,round(max(omega,0),3),flags,reasons)
def collect_layers()->List[ConceptLayer]: return [ConceptLayer('Nuclear Purity Split','Zr/Hf separation is central for reactor-grade zirconium.'), ConceptLayer('Ultra-High-Temp Ceramics','Hf compounds support extreme environments at processing cost.')]
def compute_health(nuc=0.65,cer=0.7,proc=0.45,safety=0.8,econ=0.5)->HealthReport:
 axes=[nuc,cer,proc,safety,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(nuc,cer,proc,safety,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 n=assess_nuclear(); c=assess_ceramic(); s=screen_claim(claim) if claim else None; h=compute_health(proc=0.4 if c.processing_difficulty=='high' else 0.7)
 return FoundationReport(n,c,s,h,collect_layers())
