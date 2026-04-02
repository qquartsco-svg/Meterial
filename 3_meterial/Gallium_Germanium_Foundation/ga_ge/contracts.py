from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
class Domain(Enum): POWER='power'; RF='rf'; PHOTONICS='photonics'
class Verdict(Enum): POSITIVE='positive'; NEUTRAL='neutral'; CAUTIOUS='cautious'; NEGATIVE='negative'
class HealthVerdict(Enum): HEALTHY='healthy'; STABLE='stable'; FRAGILE='fragile'; CRITICAL='critical'
@dataclass
class DeviceAssessment: material: str; efficiency_gain: str; thermal_limit: str; notes: List[str]=field(default_factory=list)
@dataclass
class SupplyAssessment: ga_risk: str; ge_risk: str; recycling_importance: str; notes: List[str]=field(default_factory=list)
@dataclass
class ClaimPayload: claim_text: str; claimed_unlimited_supply: bool=False; claimed_no_thermal_constraints: bool=False
@dataclass
class ScreeningReport: verdict: Verdict; omega: float; flags: List[str]=field(default_factory=list); reasoning: List[str]=field(default_factory=list)
@dataclass
class HealthReport: omega_device: float; omega_thermal: float; omega_supply: float; omega_recycling: float; omega_economics: float; composite_omega: float=0.0; verdict: HealthVerdict=HealthVerdict.STABLE
@dataclass
class ConceptLayer: name: str; description: str
@dataclass
class FoundationReport: device: Optional[DeviceAssessment]=None; supply: Optional[SupplyAssessment]=None; screening: Optional[ScreeningReport]=None; health: Optional[HealthReport]=None; concept_layers: List[ConceptLayer]=field(default_factory=list)
