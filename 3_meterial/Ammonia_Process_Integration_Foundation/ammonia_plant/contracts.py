from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
class Verdict(Enum):
 POSITIVE='positive'; NEUTRAL='neutral'; CAUTIOUS='cautious'; NEGATIVE='negative'
class HealthVerdict(Enum):
 HEALTHY='healthy'; STABLE='stable'; FRAGILE='fragile'; CRITICAL='critical'
@dataclass
class ReactorAssessment:
 pressure_temp_class: str; iron_catalyst_notes: str; notes: List[str]=field(default_factory=list)
@dataclass
class HydrogenCouplingAssessment:
 smr_vs_electrolysis_context: str; purge_argon_methane: str; notes: List[str]=field(default_factory=list)
@dataclass
class ClaimPayload:
 claim_text: str; claimed_zero_energy_ammonia: bool=False; claimed_h2_source_irrelevant: bool=False
@dataclass
class ScreeningReport:
 verdict: Verdict; omega: float; flags: List[str]=field(default_factory=list); reasoning: List[str]=field(default_factory=list)
@dataclass
class HealthReport:
 omega_energy: float; omega_h2_coupling: float; omega_catalyst: float; omega_safety: float; omega_economics: float
 composite_omega: float=0.0; verdict: HealthVerdict=HealthVerdict.STABLE
@dataclass
class ConceptLayer:
 name: str; description: str
@dataclass
class FoundationReport:
 reactor: Optional[ReactorAssessment]=None; hydrogen: Optional[HydrogenCouplingAssessment]=None
 screening: Optional[ScreeningReport]=None; health: Optional[HealthReport]=None
 concept_layers: List[ConceptLayer]=field(default_factory=list)
