from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
class Verdict(Enum):
 POSITIVE='positive'; NEUTRAL='neutral'; CAUTIOUS='cautious'; NEGATIVE='negative'
class HealthVerdict(Enum):
 HEALTHY='healthy'; STABLE='stable'; FRAGILE='fragile'; CRITICAL='critical'
@dataclass
class AmericiumAssessment:
 smoke_detector_alpha: str; scale_vs_weapons_grade: str; notes: List[str]=field(default_factory=list)
@dataclass
class CuriumAssessment:
 rtg_heat_legacy: str; production_batch_limits: str; notes: List[str]=field(default_factory=list)
@dataclass
class ClaimPayload:
 claim_text: str; claimed_trivial_handling_no_governance: bool=False; claimed_unlimited_domestic_am_supply: bool=False
@dataclass
class ScreeningReport:
 verdict: Verdict; omega: float; flags: List[str]=field(default_factory=list); reasoning: List[str]=field(default_factory=list)
@dataclass
class HealthReport:
 omega_safety: float; omega_governance: float; omega_supply: float; omega_security: float; omega_economics: float
 composite_omega: float=0.0; verdict: HealthVerdict=HealthVerdict.STABLE
@dataclass
class ConceptLayer:
 name: str; description: str
@dataclass
class FoundationReport:
 americium: Optional[AmericiumAssessment]=None; curium: Optional[CuriumAssessment]=None
 screening: Optional[ScreeningReport]=None; health: Optional[HealthReport]=None
 concept_layers: List[ConceptLayer]=field(default_factory=list)
