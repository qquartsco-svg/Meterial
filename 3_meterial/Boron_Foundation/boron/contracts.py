from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
class Domain(Enum): GLASS='glass'; COMPOSITE='composite'; DOPING='doping'
class Verdict(Enum): POSITIVE='positive'; NEUTRAL='neutral'; CAUTIOUS='cautious'; NEGATIVE='negative'
class HealthVerdict(Enum): HEALTHY='healthy'; STABLE='stable'; FRAGILE='fragile'; CRITICAL='critical'
@dataclass
class GlassAssessment: boron_fraction: float; thermal_shock_resistance: str; notes: List[str]=field(default_factory=list)
@dataclass
class CompositeAssessment: boron_fiber_fraction: float; brittleness_risk: str; notes: List[str]=field(default_factory=list)
@dataclass
class ClaimPayload: claim_text: str; claimed_no_brittleness_tradeoff: bool=False; claimed_infinite_doping_gain: bool=False
@dataclass
class ScreeningReport: verdict: Verdict; omega: float; flags: List[str]=field(default_factory=list); reasoning: List[str]=field(default_factory=list)
@dataclass
class HealthReport: omega_thermal: float; omega_mechanical: float; omega_process: float; omega_safety: float; omega_economics: float; composite_omega: float=0.0; verdict: HealthVerdict=HealthVerdict.STABLE
@dataclass
class ConceptLayer: name: str; description: str
@dataclass
class FoundationReport: glass: Optional[GlassAssessment]=None; composite: Optional[CompositeAssessment]=None; screening: Optional[ScreeningReport]=None; health: Optional[HealthReport]=None; concept_layers: List[ConceptLayer]=field(default_factory=list)
