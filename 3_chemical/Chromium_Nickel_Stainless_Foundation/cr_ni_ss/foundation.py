from typing import List, Optional
from .contracts import *
def assess_alloy(g: Grade=Grade.SS304)->AlloyAssessment:
 if g==Grade.SS316: return AlloyAssessment(g,0.17,0.11,'low',['Mo-bearing grades reduce chloride pitting risk.'])
 if g==Grade.SS430: return AlloyAssessment(g,0.16,0.0,'high',['Ferritic no-Ni route has chloride limits.'])
 return AlloyAssessment(g,0.18,0.08,'medium',['304 baseline.'])
def assess_process()->ProcessAssessment: return ProcessAssessment(0.6,1400.0,['High recycling fraction strongly reduces footprint.'])
def screen_claim(p: ClaimPayload)->ScreeningReport:
 flags=[]; reasons=[]; omega=0.7
 if p.claimed_no_pitting: flags.append('pitting_denial'); omega-=0.3; reasons.append('Stainless is stain-less, not rust-proof in all chloride regimes.')
 if p.claimed_zero_nickel_supply_risk: flags.append('ni_supply_denial'); omega-=0.25; reasons.append('Ni supply and price volatility remain non-trivial.')
 v=Verdict.POSITIVE if omega>=0.65 and not flags else (Verdict.NEUTRAL if omega>=0.45 else (Verdict.CAUTIOUS if omega>=0.25 else Verdict.NEGATIVE))
 if not reasons: reasons.append('No specific issues detected.')
 return ScreeningReport(v, round(max(omega,0),3), flags, reasons)
def collect_layers()->List[ConceptLayer]: return [ConceptLayer('Passive Film','Cr-rich oxide film is corrosion shield backbone.'), ConceptLayer('Ni Role','Ni stabilizes austenite but introduces supply/cost exposure.')]
def compute_health(corr=0.6,supply=0.5,proc=0.65,safety=0.8,econ=0.6)->HealthReport:
 axes=[corr,supply,proc,safety,econ]; c=round(sum(axes)/len(axes),3)
 v=HealthVerdict.HEALTHY if c>=0.7 and min(axes)>=0.4 else (HealthVerdict.STABLE if c>=0.5 else (HealthVerdict.FRAGILE if c>=0.3 else HealthVerdict.CRITICAL))
 return HealthReport(corr,supply,proc,safety,econ,c,v)
def run_foundation(claim: Optional[ClaimPayload]=None, grade: Grade=Grade.SS304)->FoundationReport:
 a=assess_alloy(grade); p=assess_process(); s=screen_claim(claim) if claim else None
 h=compute_health(corr=0.45 if a.pitting_risk=='high' else (0.75 if a.pitting_risk=='low' else 0.6), supply=0.45 if a.ni_fraction>0.08 else 0.7, proc=min(p.recycling_fraction/0.8,1.0))
 return FoundationReport(a,p,s,h,collect_layers())
