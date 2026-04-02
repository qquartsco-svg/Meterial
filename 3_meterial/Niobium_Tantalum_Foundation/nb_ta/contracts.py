from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
class Verdict(Enum): POSITIVE='positive'; NEUTRAL='neutral'; CAUTIOUS='cautious'; NEGATIVE='negative'
class HealthVerdict(Enum): HEALTHY='healthy'; STABLE='stable'; FRAGILE='fragile'; CRITICAL='critical'
@dataclass
class AlloyAssessment: nb_fraction: float; ta_fraction: float; high_temp_benefit: str; notes: List[str]=field(default_factory=list)
@dataclass
class CapacitorAssessment: volumetric_efficiency: str; failure_risk: str; notes: List[str]=field(default_factory=list)
@dataclass
class ClaimPayload: claim_text: str; claimed_no_supply_risk: bool=False; claimed_no_failure_modes: bool=False
@dataclass
class ScreeningReport: verdict: Verdict; omega: float; flags: List[str]=field(default_factory=list); reasoning: List[str]=field(default_factory=list)
@dataclass
class HealthReport: omega_alloy: float; omega_capacitor: float; omega_supply: float; omega_safety: float; omega_economics: float; composite_omega: float=0.0; verdict: HealthVerdict=HealthVerdict.STABLE
@dataclass
class ConceptLayer: name: str; description: str
@dataclass
class FoundationReport: alloy: Optional[AlloyAssessment]=None; capacitor: Optional[CapacitorAssessment]=None; screening: Optional[ScreeningReport]=None; health: Optional[HealthReport]=None; concept_layers: List[ConceptLayer]=field(default_factory=list)
