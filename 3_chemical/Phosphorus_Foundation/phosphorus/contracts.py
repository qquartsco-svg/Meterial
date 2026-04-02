from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class ExtractionMethod(Enum):
    PHOSPHATE_ROCK_MINING = "phosphate_rock_mining"
    WET_PROCESS_PHOSPHORIC_ACID = "wet_process_phosphoric_acid"
    THERMAL_PROCESS = "thermal_process"


class DomainMode(Enum):
    AGRICULTURE = "agriculture"
    BIOENERGETICS = "bioenergetics"
    MATERIALS = "materials"


class Verdict(Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    CAUTIOUS = "cautious"
    NEGATIVE = "negative"


class HealthVerdict(Enum):
    HEALTHY = "healthy"
    STABLE = "stable"
    FRAGILE = "fragile"
    CRITICAL = "critical"


@dataclass(frozen=True)
class PProperties:
    molar_mass_g_per_mol: float
    density_g_per_cm3_white: float
    melting_point_k_white: float


@dataclass
class ExtractionAssessment:
    method: ExtractionMethod
    ore_grade_p2o5_fraction: float
    co2_intensity_kg_per_kg_p2o5: float
    contaminants_risk: str
    notes: List[str] = field(default_factory=list)


@dataclass
class BioenergeticsAssessment:
    atp_turnover_mol_per_day_human: float
    atp_regeneration_required: bool
    notes: List[str] = field(default_factory=list)


@dataclass
class PhosphorusClaimPayload:
    claim_text: str
    claimed_infinite_phosphate: bool = False
    claimed_atp_without_recycling: bool = False
    tags: List[str] = field(default_factory=list)


@dataclass
class PhosphorusScreeningReport:
    verdict: Verdict
    omega: float
    flags: List[str] = field(default_factory=list)
    reasoning: List[str] = field(default_factory=list)


@dataclass
class PhosphorusHealthReport:
    omega_extraction: float
    omega_bio_cycle: float
    omega_pollution_control: float
    omega_recycling: float
    omega_economics: float
    composite_omega: float = 0.0
    verdict: HealthVerdict = HealthVerdict.STABLE
    warnings: List[str] = field(default_factory=list)


@dataclass
class ConceptLayer:
    name: str
    description: str
    key_equations: List[str] = field(default_factory=list)


@dataclass
class PhosphorusFoundationReport:
    extraction: Optional[ExtractionAssessment] = None
    bioenergetics: Optional[BioenergeticsAssessment] = None
    screening: Optional[PhosphorusScreeningReport] = None
    health: Optional[PhosphorusHealthReport] = None
    concept_layers: List[ConceptLayer] = field(default_factory=list)
