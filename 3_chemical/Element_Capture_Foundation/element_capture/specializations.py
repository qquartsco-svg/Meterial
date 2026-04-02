from __future__ import annotations

from .adapter import ElementCaptureAdapter
from .contracts import (
    CaptureEnvironment,
    CaptureMode,
    Species,
    IntakeGeometry,
    SeparationStage,
    StorageStage,
    CaptureAssessment,
)


def assess_co2_dac(
    *,
    density_kg_m3: float,
    bulk_velocity_ms: float,
    co2_fraction_0_1: float,
    area_m2: float = 10.0,
    recovery_efficiency_0_1: float = 0.82,
    process_power_w: float = 1200.0,
) -> CaptureAssessment:
    adapter = ElementCaptureAdapter()
    return adapter.assess(
        environment=CaptureEnvironment(
            mode=CaptureMode.ATMOSPHERIC_CAPTURE,
            species=Species.CO2,
            density_kg_m3=density_kg_m3,
            bulk_velocity_ms=bulk_velocity_ms,
            species_fraction_0_1=co2_fraction_0_1,
            collection_accessibility_0_1=0.95,
            energetic_cost_index=0.45,
        ),
        intake=IntakeGeometry(area_m2=area_m2),
        separation=SeparationStage(
            recovery_efficiency_0_1=recovery_efficiency_0_1,
            process_power_w=process_power_w,
        ),
        storage=StorageStage(
            capacity_kg=50.0,
            stored_mass_kg=5.0,
            storage_efficiency_0_1=0.96,
            compression_power_w=300.0,
        ),
    )


def assess_h2_electrolysis(
    *,
    liquid_density_kg_m3: float = 1000.0,
    pseudo_flow_ms: float = 0.005,
    h2_fraction_0_1: float = 0.111,
    area_m2: float = 10.0,
    recovery_efficiency_0_1: float = 0.85,
    process_power_w: float = 5000.0,
) -> CaptureAssessment:
    adapter = ElementCaptureAdapter()
    return adapter.assess(
        environment=CaptureEnvironment(
            mode=CaptureMode.ELECTROCHEMICAL_EXTRACTION,
            species=Species.H2,
            density_kg_m3=liquid_density_kg_m3,
            bulk_velocity_ms=pseudo_flow_ms,
            species_fraction_0_1=h2_fraction_0_1,
            collection_accessibility_0_1=0.90,
            energetic_cost_index=0.70,
        ),
        intake=IntakeGeometry(area_m2=area_m2),
        separation=SeparationStage(
            recovery_efficiency_0_1=recovery_efficiency_0_1,
            process_power_w=process_power_w,
        ),
        storage=StorageStage(
            capacity_kg=20.0,
            stored_mass_kg=2.0,
            storage_efficiency_0_1=0.98,
            compression_power_w=1000.0,
        ),
    )


def assess_he_cryogenic_separation(
    *,
    density_kg_m3: float,
    bulk_velocity_ms: float,
    he_fraction_0_1: float,
    area_m2: float = 10.0,
    recovery_efficiency_0_1: float = 0.8,
    process_power_w: float = 2000.0,
) -> CaptureAssessment:
    adapter = ElementCaptureAdapter()
    return adapter.assess(
        environment=CaptureEnvironment(
            mode=CaptureMode.CRYOGENIC_SEPARATION,
            species=Species.HE,
            density_kg_m3=density_kg_m3,
            bulk_velocity_ms=bulk_velocity_ms,
            species_fraction_0_1=he_fraction_0_1,
            collection_accessibility_0_1=0.80,
            energetic_cost_index=0.90,
        ),
        intake=IntakeGeometry(area_m2=area_m2),
        separation=SeparationStage(
            recovery_efficiency_0_1=recovery_efficiency_0_1,
            process_power_w=process_power_w,
        ),
        storage=StorageStage(
            capacity_kg=20.0,
            stored_mass_kg=1.0,
            storage_efficiency_0_1=0.97,
            compression_power_w=600.0,
            boiloff_loss_kg_s=1e-6,
        ),
    )
