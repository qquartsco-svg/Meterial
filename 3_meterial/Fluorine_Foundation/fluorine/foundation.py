from typing import List, Optional
from .contracts import *
def assess_electrolyte()->ElectrolyteAssessment: return ElectrolyteAssessment('LiPF6','medium','high',['Moisture/heat can elevate HF risk.'])
def assess_polymer()->PolymerAssessment: return PolymerAssessment('PVDF',0.59,'medium',['Durability high, end-of-life handling non-trivial.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_no_hf_risk: flags.append('hf_denial'); omega-=0.3; reasons.append('HF risk exists in damaged/moist/overheated LiPF6 systems.')
 if p.claimed_no_pfas_issue: flags.append('persistence_denial'); omega-=0.25; reasons.append('Fluorinated material persistence and disposal concerns remain.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v, round(max(omega,0),3), flags, reasons)
def collect_layers()->List[ConceptLayer]: return [ConceptLayer('Electrolyte Stability','F-bearing salts improve performance but add decomposition/safety complexity.'), ConceptLayer('Persistence','Fluorinated polymers can be durable yet difficult at end-of-life.')]
def compute_health(perf=0.75,safety=0.5,env=0.45,recycling=0.4,econ=0.6)->HealthReport:
 axes=[perf,safety,env,recycling,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(perf,safety,env,recycling,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None)->FoundationReport:
 e=assess_electrolyte(); p=assess_polymer(); s=screen_claim(claim) if claim else None
 h=compute_health(safety=0.45 if e.hf_generation_risk=='high' else 0.7, env=0.45 if p.persistence_risk in ('high','medium') else 0.75)
 return FoundationReport(e,p,s,h,collect_layers())
