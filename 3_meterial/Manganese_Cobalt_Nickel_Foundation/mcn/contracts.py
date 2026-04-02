from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
class Chemistry(Enum): NMC111='nmc111'; NMC622='nmc622'; NMC811='nmc811'; LNO='lno'
class Verdict(Enum): POSITIVE='positive'; NEUTRAL='neutral'; CAUTIOUS='cautious'; NEGATIVE='negative'
class HealthVerdict(Enum): HEALTHY='healthy'; STABLE='stable'; FRAGILE='fragile'; CRITICAL='critical'
@dataclass
class CathodeAssessment: chemistry: Chemistry; specific_energy_wh_kg: float; cycle_life_80pct: int; thermal_risk: str; cobalt_dependency: str; notes: List[str]=field(default_factory=list)
@dataclass
class SupplyAssessment: mn_risk: str; co_risk: str; ni_risk: str; recycling_importance: str; notes: List[str]=field(default_factory=list)
@dataclass
class MCNClaimPayload: claim_text: str; claimed_no_supply_risk: bool=False; claimed_high_ni_no_safety_tradeoff: bool=False
@dataclass
class MCNScreeningReport: verdict: Verdict; omega: float; flags: List[str]=field(default_factory=list); reasoning: List[str]=field(default_factory=list)
@dataclass
class MCNHealthReport: omega_energy: float; omega_life: float; omega_safety: float; omega_supply: float; omega_economics: float; composite_omega: float=0.0; verdict: HealthVerdict=HealthVerdict.STABLE
@dataclass
class ConceptLayer: name: str; description: str
@dataclass
class MCNFoundationReport: cathode: Optional[CathodeAssessment]=None; supply: Optional[SupplyAssessment]=None; screening: Optional[MCNScreeningReport]=None; health: Optional[MCNHealthReport]=None; concept_layers: List[ConceptLayer]=field(default_factory=list)
