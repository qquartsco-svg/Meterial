from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
class Domain(Enum): BATTERY='battery'; MATERIAL='material'
class Verdict(Enum): POSITIVE='positive'; NEUTRAL='neutral'; CAUTIOUS='cautious'; NEGATIVE='negative'
class HealthVerdict(Enum): HEALTHY='healthy'; STABLE='stable'; FRAGILE='fragile'; CRITICAL='critical'
@dataclass
class ElectrolyteAssessment: salt: str; decomposition_risk: str; hf_generation_risk: str; notes: List[str]=field(default_factory=list)
@dataclass
class PolymerAssessment: material: str; fluorine_content_fraction: float; persistence_risk: str; notes: List[str]=field(default_factory=list)
@dataclass
class ClaimPayload: claim_text: str; claimed_no_hf_risk: bool=False; claimed_no_pfas_issue: bool=False
@dataclass
class ScreeningReport: verdict: Verdict; omega: float; flags: List[str]=field(default_factory=list); reasoning: List[str]=field(default_factory=list)
@dataclass
class HealthReport: omega_performance: float; omega_safety: float; omega_environment: float; omega_recycling: float; omega_economics: float; composite_omega: float=0.0; verdict: HealthVerdict=HealthVerdict.STABLE
@dataclass
class ConceptLayer: name: str; description: str
@dataclass
class FoundationReport: electrolyte: Optional[ElectrolyteAssessment]=None; polymer: Optional[PolymerAssessment]=None; screening: Optional[ScreeningReport]=None; health: Optional[HealthReport]=None; concept_layers: List[ConceptLayer]=field(default_factory=list)
