from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
class Verdict(Enum): POSITIVE='positive'; NEUTRAL='neutral'; CAUTIOUS='cautious'; NEGATIVE='negative'
class HealthVerdict(Enum): HEALTHY='healthy'; STABLE='stable'; FRAGILE='fragile'; CRITICAL='critical'
@dataclass
class CatalystAssessment: oxygen_storage_capacity: str; sulfur_tolerance: str; notes: List[str]=field(default_factory=list)
@dataclass
class MaterialsAssessment: polishing_performance: str; slurry_waste_risk: str; notes: List[str]=field(default_factory=list)
@dataclass
class ClaimPayload: claim_text: str; claimed_no_deactivation: bool=False; claimed_no_waste_issue: bool=False
@dataclass
class ScreeningReport: verdict: Verdict; omega: float; flags: List[str]=field(default_factory=list); reasoning: List[str]=field(default_factory=list)
@dataclass
class HealthReport: omega_catalyst: float; omega_materials: float; omega_supply: float; omega_safety: float; omega_economics: float; composite_omega: float=0.0; verdict: HealthVerdict=HealthVerdict.STABLE
@dataclass
class ConceptLayer: name: str; description: str
@dataclass
class FoundationReport: catalyst: Optional[CatalystAssessment]=None; materials: Optional[MaterialsAssessment]=None; screening: Optional[ScreeningReport]=None; health: Optional[HealthReport]=None; concept_layers: List[ConceptLayer]=field(default_factory=list)
