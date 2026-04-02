from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
class Verdict(Enum): POSITIVE='positive'; NEUTRAL='neutral'; CAUTIOUS='cautious'; NEGATIVE='negative'
class HealthVerdict(Enum): HEALTHY='healthy'; STABLE='stable'; FRAGILE='fragile'; CRITICAL='critical'
@dataclass
class FuelCycleAssessment: pathway: str; proliferation_risk: str; waste_burden: str; notes: List[str]=field(default_factory=list)
@dataclass
class ReactorAssessment: type_name: str; safety_margin: str; complexity: str; notes: List[str]=field(default_factory=list)
@dataclass
class ClaimPayload: claim_text: str; claimed_no_waste_issue: bool=False; claimed_no_safety_governance_need: bool=False
@dataclass
class ScreeningReport: verdict: Verdict; omega: float; flags: List[str]=field(default_factory=list); reasoning: List[str]=field(default_factory=list)
@dataclass
class HealthReport: omega_fuel_cycle: float; omega_safety: float; omega_waste: float; omega_governance: float; omega_economics: float; composite_omega: float=0.0; verdict: HealthVerdict=HealthVerdict.STABLE
@dataclass
class ConceptLayer: name: str; description: str
@dataclass
class FoundationReport: fuel_cycle: Optional[FuelCycleAssessment]=None; reactor: Optional[ReactorAssessment]=None; screening: Optional[ScreeningReport]=None; health: Optional[HealthReport]=None; concept_layers: List[ConceptLayer]=field(default_factory=list)
