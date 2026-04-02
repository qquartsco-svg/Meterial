from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
class DomainMode(Enum): BATTERY='battery'; AGRI='agriculture'; ENV='environment'
class Verdict(Enum): POSITIVE='positive'; NEUTRAL='neutral'; CAUTIOUS='cautious'; NEGATIVE='negative'
class HealthVerdict(Enum): HEALTHY='healthy'; STABLE='stable'; FRAGILE='fragile'; CRITICAL='critical'
@dataclass
class SulfurProcessAssessment: sulfuric_acid_ton_per_day: float; so2_control_efficiency: float; notes: List[str]=field(default_factory=list)
@dataclass
class SulfurBatteryAssessment: chemistry: str; specific_energy_wh_kg: float; cycle_life: int; polysulfide_risk: str; notes: List[str]=field(default_factory=list)
@dataclass
class SulfurClaimPayload: claim_text: str; claimed_zero_so2_pollution: bool=False; claimed_lis_no_shuttle_effect: bool=False
@dataclass
class SulfurScreeningReport: verdict: Verdict; omega: float; flags: List[str]=field(default_factory=list); reasoning: List[str]=field(default_factory=list)
@dataclass
class SulfurHealthReport: omega_process: float; omega_environment: float; omega_battery: float; omega_safety: float; omega_economics: float; composite_omega: float=0.0; verdict: HealthVerdict=HealthVerdict.STABLE
@dataclass
class ConceptLayer: name: str; description: str
@dataclass
class SulfurFoundationReport: process: Optional[SulfurProcessAssessment]=None; battery: Optional[SulfurBatteryAssessment]=None; screening: Optional[SulfurScreeningReport]=None; health: Optional[SulfurHealthReport]=None; concept_layers: List[ConceptLayer]=field(default_factory=list)
