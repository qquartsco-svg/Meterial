from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
class Verdict(Enum):
 POSITIVE='positive'; NEUTRAL='neutral'; CAUTIOUS='cautious'; NEGATIVE='negative'
class HealthVerdict(Enum):
 HEALTHY='healthy'; STABLE='stable'; FRAGILE='fragile'; CRITICAL='critical'
@dataclass
class TechAssessment:
 cdte_adjacency: str; cigs_se: str; notes: List[str]=field(default_factory=list)
@dataclass
class SupplyAssessment:
 cu_anode_slime_tail: str; price_volatility: str; notes: List[str]=field(default_factory=list)
@dataclass
class ClaimPayload:
 claim_text: str; claimed_chalcogen_same_hazard_as_sulfur_only: bool=False; claimed_infinite_tellurium: bool=False
@dataclass
class ScreeningReport:
 verdict: Verdict; omega: float; flags: List[str]=field(default_factory=list); reasoning: List[str]=field(default_factory=list)
@dataclass
class HealthReport:
 omega_tech: float; omega_supply: float; omega_safety: float; omega_recycling: float; omega_economics: float
 composite_omega: float=0.0; verdict: HealthVerdict=HealthVerdict.STABLE
@dataclass
class ConceptLayer:
 name: str; description: str
@dataclass
class FoundationReport:
 tech: Optional[TechAssessment]=None; supply: Optional[SupplyAssessment]=None
 screening: Optional[ScreeningReport]=None; health: Optional[HealthReport]=None
 concept_layers: List[ConceptLayer]=field(default_factory=list)
