from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
class Verdict(Enum):
 POSITIVE='positive'; NEUTRAL='neutral'; CAUTIOUS='cautious'; NEGATIVE='negative'
class HealthVerdict(Enum):
 HEALTHY='healthy'; STABLE='stable'; FRAGILE='fragile'; CRITICAL='critical'
@dataclass
class StoichiometryAssessment:
 map_vs_dap_np_ratio: str; acid_base_soil_cartoon: str; notes: List[str]=field(default_factory=list)
@dataclass
class HandlingAssessment:
 hygroscopic_caking: str; storage_discipline: str; notes: List[str]=field(default_factory=list)
@dataclass
class ClaimPayload:
 claim_text: str; claimed_map_dap_fungible_no_agronomy: bool=False; claimed_no_caking_or_moisture_risk: bool=False
@dataclass
class ScreeningReport:
 verdict: Verdict; omega: float; flags: List[str]=field(default_factory=list); reasoning: List[str]=field(default_factory=list)
@dataclass
class HealthReport:
 omega_agronomy_fit: float; omega_handling: float; omega_supply: float; omega_env: float; omega_economics: float
 composite_omega: float=0.0; verdict: HealthVerdict=HealthVerdict.STABLE
@dataclass
class ConceptLayer:
 name: str; description: str
@dataclass
class FoundationReport:
 stoich: Optional[StoichiometryAssessment]=None; handling: Optional[HandlingAssessment]=None
 screening: Optional[ScreeningReport]=None; health: Optional[HealthReport]=None
 concept_layers: List[ConceptLayer]=field(default_factory=list)
