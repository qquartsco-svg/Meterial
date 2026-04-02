from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class CaptureMode(str, Enum):
    ATMOSPHERIC_CAPTURE = "atmospheric_capture"
    DISSOLVED_EXTRACTION = "dissolved_extraction"
    ELECTROCHEMICAL_EXTRACTION = "electrochemical_extraction"
    CRYOGENIC_SEPARATION = "cryogenic_separation"
    ORBITAL_SKIMMING = "orbital_skimming"


class Species(str, Enum):
    CO2 = "co2"
    H2 = "h2"
    HE = "he"
    HE3 = "he3"
    O2 = "o2"
    N2 = "n2"


@dataclass(frozen=True)
class CaptureEnvironment:
    mode: CaptureMode
    species: Species
    density_kg_m3: float
    bulk_velocity_ms: float
    species_fraction_0_1: float
    collection_accessibility_0_1: float = 1.0
    energetic_cost_index: float = 0.5
    source_density_kg_m3: float | None = None
    pressure_pa: float | None = None
    temperature_k: float | None = None
    gravity_mps2: float | None = None
    residence_time_s: float = 1.0
    platform_mass_kg: float | None = None
    ballistic_coeff_kg_m2: float | None = None

    def __post_init__(self) -> None:
        if self.density_kg_m3 < 0.0:
            raise ValueError("density_kg_m3 must be >= 0")
        if self.bulk_velocity_ms < 0.0:
            raise ValueError("bulk_velocity_ms must be >= 0")
        if not 0.0 <= self.species_fraction_0_1 <= 1.0:
            raise ValueError("species_fraction_0_1 must be within [0,1]")
        if not 0.0 <= self.collection_accessibility_0_1 <= 1.0:
            raise ValueError("collection_accessibility_0_1 must be within [0,1]")
        if self.energetic_cost_index < 0.0:
            raise ValueError("energetic_cost_index must be >= 0")
        if self.residence_time_s <= 0.0:
            raise ValueError("residence_time_s must be > 0")


@dataclass(frozen=True)
class IntakeGeometry:
    area_m2: float
    intake_efficiency_0_1: float = 1.0

    def __post_init__(self) -> None:
        if self.area_m2 < 0.0:
            raise ValueError("area_m2 must be >= 0")
        if not 0.0 <= self.intake_efficiency_0_1 <= 1.0:
            raise ValueError("intake_efficiency_0_1 must be within [0,1]")


@dataclass(frozen=True)
class SeparationStage:
    recovery_efficiency_0_1: float
    selectivity_0_1: float = 1.0
    process_power_w: float = 0.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.recovery_efficiency_0_1 <= 1.0:
            raise ValueError("recovery_efficiency_0_1 must be within [0,1]")
        if not 0.0 <= self.selectivity_0_1 <= 1.0:
            raise ValueError("selectivity_0_1 must be within [0,1]")
        if self.process_power_w < 0.0:
            raise ValueError("process_power_w must be >= 0")


@dataclass(frozen=True)
class StorageStage:
    capacity_kg: float
    stored_mass_kg: float = 0.0
    storage_efficiency_0_1: float = 1.0
    compression_power_w: float = 0.0
    boiloff_loss_kg_s: float = 0.0

    def __post_init__(self) -> None:
        if self.capacity_kg < 0.0:
            raise ValueError("capacity_kg must be >= 0")
        if self.stored_mass_kg < 0.0:
            raise ValueError("stored_mass_kg must be >= 0")
        if self.stored_mass_kg > self.capacity_kg:
            raise ValueError("stored_mass_kg must be <= capacity_kg")
        if not 0.0 <= self.storage_efficiency_0_1 <= 1.0:
            raise ValueError("storage_efficiency_0_1 must be within [0,1]")
        if self.compression_power_w < 0.0:
            raise ValueError("compression_power_w must be >= 0")
        if self.boiloff_loss_kg_s < 0.0:
            raise ValueError("boiloff_loss_kg_s must be >= 0")


@dataclass(frozen=True)
class CaptureHealth:
    omega_capture: float
    source_quality_0_1: float
    flux_health_0_1: float
    storage_health_0_1: float
    energy_health_0_1: float
    anomaly_detected: bool
    machinery_health_0_1: float = 1.0
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class CaptureAssessment:
    environment: CaptureEnvironment
    intake: IntakeGeometry
    separation: SeparationStage
    storage: StorageStage
    intake_mass_flow_kg_s: float
    species_inflow_kg_s: float
    capture_rate_kg_s: float
    net_capture_rate_kg_s: float
    storage_power_w: float
    energy_intensity_j_per_kg: float
    capture_possible: bool
    health: CaptureHealth
    evidence: dict[str, float | str] = field(default_factory=dict)
    orbital_yield_per_pass_kg: float = 0.0
    drag_penalty_proxy_0_1: float = 0.0

    @property
    def omega_capture(self) -> float:
        return self.health.omega_capture
