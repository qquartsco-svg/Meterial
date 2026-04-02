from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
class Verdict(Enum): POSITIVE='positive'; NEUTRAL='neutral'; CAUTIOUS='cautious'; NEGATIVE='negative'
class HealthVerdict(Enum): HEALTHY='healthy'; STABLE='stable'; FRAGILE='fragile'; CRITICAL='critical'
@dataclass
class ConductorAssessment: ag_conductivity_rank: int; contact_reliability: str; notes: List[str]=field(default_factory=list)
@dataclass
class NobleMetalAssessment: au_corrosion_resistance: str; plating_cost_risk: str; notes: List[str]=field(default_factory=list)
@dataclass
class ClaimPayload: claim_text: str; claimed_zero_cost_penalty: bool=False; claimed_no_migration_issue: bool=False
@dataclass
class ScreeningReport: verdict: Verdict; omega: float; flags: List[str]=field(default_factory=list); reasoning: List[str]=field(default_factory=list)
@dataclass
class HealthReport: omega_performance: float; omega_reliability: float; omega_supply: float; omega_safety: float; omega_economics: float; composite_omega: float=0.0; verdict: HealthVerdict=HealthVerdict.STABLE
@dataclass
class ConceptLayer: name: str; description: str
@dataclass
class FoundationReport: conductor: Optional[ConductorAssessment]=None; noble: Optional[NobleMetalAssessment]=None; screening: Optional[ScreeningReport]=None; health: Optional[HealthReport]=None; concept_layers: List[ConceptLayer]=field(default_factory=list)
