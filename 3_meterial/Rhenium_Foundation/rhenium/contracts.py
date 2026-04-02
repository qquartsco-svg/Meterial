from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
class Verdict(Enum):
 POSITIVE='positive'; NEUTRAL='neutral'; CAUTIOUS='cautious'; NEGATIVE='negative'
class HealthVerdict(Enum):
 HEALTHY='healthy'; STABLE='stable'; FRAGILE='fragile'; CRITICAL='critical'
@dataclass
class AlloyAssessment:
 single_crystal_ni_role: str; creep_notes: str; notes: List[str]=field(default_factory=list)
@dataclass
class CatalystAssessment:
 reforming_bimetallic: str; regeneration_burden: str; notes: List[str]=field(default_factory=list)
@dataclass
class ClaimPayload:
 claim_text: str; claimed_abundant_rhenium: bool=False; claimed_drop_in_replace_moly: bool=False
@dataclass
class ScreeningReport:
 verdict: Verdict; omega: float; flags: List[str]=field(default_factory=list); reasoning: List[str]=field(default_factory=list)
@dataclass
class HealthReport:
 omega_alloy: float; omega_catalyst: float; omega_supply: float; omega_recycling: float; omega_economics: float
 composite_omega: float=0.0; verdict: HealthVerdict=HealthVerdict.STABLE
@dataclass
class ConceptLayer:
 name: str; description: str
@dataclass
class FoundationReport:
 alloy: Optional[AlloyAssessment]=None; catalyst: Optional[CatalystAssessment]=None
 screening: Optional[ScreeningReport]=None; health: Optional[HealthReport]=None
 concept_layers: List[ConceptLayer]=field(default_factory=list)
