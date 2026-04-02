from __future__ import annotations

from dataclasses import replace

from .contracts import (
    CaptureAssessment,
    CaptureEnvironment,
    CaptureHealth,
    IntakeGeometry,
    SeparationStage,
    StorageStage,
)
from .intake import intake_mass_flow_kg_s, species_inflow_kg_s
from .separation import captured_mass_flow_kg_s
from .storage import storage_power_w
from .health import assess_capture_health
from .orbital import orbital_yield_per_pass_kg, drag_penalty_proxy_0_1, orbital_skimming_feasible


class ElementCaptureAdapter:
    def assess(
        self,
        *,
        environment: CaptureEnvironment,
        intake: IntakeGeometry,
        separation: SeparationStage,
        storage: StorageStage,
    ) -> CaptureAssessment:
        mass_in = intake_mass_flow_kg_s(environment, intake)
        species_in = species_inflow_kg_s(environment, intake)
        captured = captured_mass_flow_kg_s(environment, intake, separation)
        net_capture = max(0.0, captured * storage.storage_efficiency_0_1 - storage.boiloff_loss_kg_s)
        total_power_w = separation.process_power_w + storage_power_w(storage)
        energy_intensity = total_power_w / max(net_capture, 1e-12)
        orbital_yield = 0.0
        drag_proxy = 0.0
        orbital_ok = True
        if environment.mode.value == "orbital_skimming":
            orbital_yield = orbital_yield_per_pass_kg(environment, intake, separation)
            drag_proxy = drag_penalty_proxy_0_1(environment, intake)
            orbital_ok = orbital_skimming_feasible(environment, intake, separation)
        health = assess_capture_health(
            environment,
            storage,
            capture_rate_kg_s=net_capture,
            energy_intensity_j_per_kg=energy_intensity,
        )
        capture_possible = (
            net_capture > 0.0
            and storage.stored_mass_kg < storage.capacity_kg
            and health.source_quality_0_1 > 0.05
            and orbital_ok
        )
        return CaptureAssessment(
            environment=environment,
            intake=intake,
            separation=separation,
            storage=storage,
            intake_mass_flow_kg_s=mass_in,
            species_inflow_kg_s=species_in,
            capture_rate_kg_s=captured,
            net_capture_rate_kg_s=net_capture,
            storage_power_w=total_power_w,
            energy_intensity_j_per_kg=energy_intensity,
            capture_possible=capture_possible,
            health=health,
            evidence={
                "mode": environment.mode.value,
                "species": environment.species.value,
                "density_kg_m3": environment.density_kg_m3,
                "species_fraction_0_1": environment.species_fraction_0_1,
                "accessibility_0_1": environment.collection_accessibility_0_1,
                "area_m2": intake.area_m2,
                "recovery_efficiency_0_1": separation.recovery_efficiency_0_1,
            },
            orbital_yield_per_pass_kg=orbital_yield,
            drag_penalty_proxy_0_1=drag_proxy,
        )


def apply_external_health_modifier(
    assessment: CaptureAssessment,
    *,
    machinery_health_0_1: float,
    extra_notes: tuple[str, ...] = (),
    evidence: dict[str, float | str] | None = None,
) -> CaptureAssessment:
    machinery_health = max(0.0, min(1.0, machinery_health_0_1))
    base = assessment.health
    omega = max(
        0.0,
        min(1.0, 0.80 * base.omega_capture + 0.20 * machinery_health),
    )
    notes = tuple(dict.fromkeys([*base.notes, *extra_notes]))
    health = CaptureHealth(
        omega_capture=omega,
        source_quality_0_1=base.source_quality_0_1,
        flux_health_0_1=base.flux_health_0_1,
        storage_health_0_1=base.storage_health_0_1,
        energy_health_0_1=base.energy_health_0_1,
        machinery_health_0_1=machinery_health,
        anomaly_detected=base.anomaly_detected or machinery_health < 0.35 or bool(extra_notes),
        notes=notes,
    )
    merged_evidence = dict(assessment.evidence)
    if evidence:
        merged_evidence.update(evidence)
    return replace(
        assessment,
        health=health,
        capture_possible=assessment.capture_possible and machinery_health >= 0.20,
        evidence=merged_evidence,
    )
