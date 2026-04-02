"""L0 — Data contracts for Hydrogen_Foundation."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


# ── Enums ──────────────────────────────────────────────────────────────

class ProductionMethod(Enum):
    """How H₂ is produced."""
    PEM_ELECTROLYSIS = "pem_electrolysis"
    ALKALINE_ELECTROLYSIS = "alkaline_electrolysis"
    SOEC_ELECTROLYSIS = "soec_electrolysis"
    SMR = "steam_methane_reforming"
    ATR = "autothermal_reforming"
    BIOMASS_GASIFICATION = "biomass_gasification"
    PHOTOELECTROCHEMICAL = "photoelectrochemical"
    THERMOCHEMICAL = "thermochemical"


class StorageMethod(Enum):
    """How H₂ is stored."""
    COMPRESSED_350BAR = "compressed_350bar"
    COMPRESSED_700BAR = "compressed_700bar"
    LIQUID = "liquid_h2"
    METAL_HYDRIDE = "metal_hydride"
    CHEMICAL_CARRIER_AMMONIA = "ammonia"
    CHEMICAL_CARRIER_LOHC = "lohc"
    UNDERGROUND_CAVERN = "underground_cavern"


class FuelCellType(Enum):
    """Fuel cell technology."""
    PEMFC = "pemfc"
    SOFC = "sofc"
    AFC = "afc"
    MCFC = "mcfc"
    PAFC = "pafc"


class Verdict(Enum):
    """ATHENA screening verdict."""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    CAUTIOUS = "cautious"
    NEGATIVE = "negative"


class HealthVerdict(Enum):
    """Composite health verdict."""
    HEALTHY = "healthy"
    STABLE = "stable"
    FRAGILE = "fragile"
    CRITICAL = "critical"


class ColorCode(Enum):
    """Hydrogen 'colour' taxonomy based on production source."""
    GREEN = "green"       # renewable electrolysis
    BLUE = "blue"         # SMR + CCS
    GREY = "grey"         # SMR without CCS
    PINK = "pink"         # nuclear electrolysis
    TURQUOISE = "turquoise"  # methane pyrolysis
    WHITE = "white"       # natural / by-product
    YELLOW = "yellow"     # solar electrolysis (sometimes)


# ── Dataclasses ────────────────────────────────────────────────────────

@dataclass(frozen=True)
class H2Properties:
    """Static physical/chemical properties of molecular hydrogen."""
    molar_mass_g_per_mol: float
    density_kg_per_m3_stp: float
    boiling_point_k: float
    lhv_mj_per_kg: float
    hhv_mj_per_kg: float
    lel_vol_percent: float
    uel_vol_percent: float
    autoignition_k: float


@dataclass
class ProductionAssessment:
    """Output of a hydrogen production pathway evaluation."""
    method: ProductionMethod
    color_code: ColorCode
    h2_rate_mol_per_s: float
    energy_input_kw: float
    efficiency: float                  # 0–1
    co2_intensity_kg_per_kg_h2: float  # direct + indirect
    water_consumption_l_per_kg_h2: float
    notes: List[str] = field(default_factory=list)


@dataclass
class StorageAssessment:
    """Output of a storage method evaluation."""
    method: StorageMethod
    gravimetric_density_wt_percent: float   # kg_H2 / kg_system × 100
    volumetric_density_kg_h2_per_m3: float
    energy_penalty_fraction: float          # energy to store / energy in H₂
    boiloff_rate_percent_per_day: float     # liquid only; 0 for others
    pressure_mpa: float
    temperature_k: float
    round_trip_efficiency: float            # store → retrieve
    notes: List[str] = field(default_factory=list)


@dataclass
class FuelCellAssessment:
    """Output of a fuel cell evaluation."""
    cell_type: FuelCellType
    cell_voltage_v: float
    current_density_a_per_cm2: float
    efficiency_electric: float    # electric power / H₂ energy (LHV)
    efficiency_total: float       # (electric + usable heat) / H₂ energy
    degradation_rate_uv_per_h: float  # µV/h
    power_density_w_per_cm2: float
    operating_temperature_k: float
    notes: List[str] = field(default_factory=list)


@dataclass
class SafetyAssessment:
    """Output of hydrogen safety analysis."""
    h2_concentration_vol_percent: float
    within_flammable_range: bool
    leak_rate_g_per_s: float
    ventilation_adequate: bool
    embrittlement_risk: str          # "low" / "moderate" / "high"
    explosion_overpressure_kpa: float
    risk_level: str                  # "acceptable" / "marginal" / "unacceptable"
    notes: List[str] = field(default_factory=list)


@dataclass
class HydrogenClaimPayload:
    """A claim about hydrogen to be screened."""
    claim_text: str
    claimed_efficiency: Optional[float] = None
    claimed_cost_usd_per_kg: Optional[float] = None
    claimed_energy_density_kwh_per_kg: Optional[float] = None
    production_method: Optional[str] = None
    tags: List[str] = field(default_factory=list)


@dataclass
class HydrogenScreeningReport:
    """Result of ATHENA screening on a hydrogen claim."""
    verdict: Verdict
    omega: float
    flags: List[str] = field(default_factory=list)
    reasoning: List[str] = field(default_factory=list)


@dataclass
class HydrogenHealthReport:
    """5-axis health report for a hydrogen system."""
    omega_production: float
    omega_storage: float
    omega_conversion: float      # fuel cell / combustion
    omega_safety: float
    omega_economics: float
    composite_omega: float = 0.0
    verdict: HealthVerdict = HealthVerdict.STABLE
    warnings: List[str] = field(default_factory=list)


@dataclass
class ConceptLayer:
    """A named conceptual layer with description and key equations."""
    name: str
    description: str
    key_equations: List[str] = field(default_factory=list)


@dataclass
class HydrogenFoundationReport:
    """Unified output of the Hydrogen Foundation pipeline."""
    production: Optional[ProductionAssessment] = None
    storage: Optional[StorageAssessment] = None
    fuel_cell: Optional[FuelCellAssessment] = None
    safety: Optional[SafetyAssessment] = None
    screening: Optional[HydrogenScreeningReport] = None
    health: Optional[HydrogenHealthReport] = None
    concept_layers: List[ConceptLayer] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
