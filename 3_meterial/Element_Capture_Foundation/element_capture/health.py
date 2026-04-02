from __future__ import annotations

from .contracts import CaptureEnvironment, StorageStage, CaptureHealth
from .environment import source_quality_index
from .storage import storage_margin_0_1


def assess_capture_health(
    environment: CaptureEnvironment,
    storage: StorageStage,
    *,
    capture_rate_kg_s: float,
    energy_intensity_j_per_kg: float,
    machinery_health_0_1: float = 1.0,
) -> CaptureHealth:
    source_q = source_quality_index(environment)
    flux_health = max(0.0, min(1.0, capture_rate_kg_s / 0.01))
    storage_health = storage_margin_0_1(storage)
    energy_health = 1.0 / (1.0 + max(0.0, energy_intensity_j_per_kg) / 1_000_000.0)
    machinery_health = max(0.0, min(1.0, machinery_health_0_1))
    omega = max(
        0.0,
        min(
            1.0,
            0.24 * source_q
            + 0.24 * flux_health
            + 0.16 * storage_health
            + 0.16 * energy_health
            + 0.20 * machinery_health,
        ),
    )

    notes: list[str] = []
    if capture_rate_kg_s <= 0.0:
        notes.append("capture_rate_zero")
    if source_q < 0.35:
        notes.append("source_quality_low")
    if storage_health < 0.20:
        notes.append("storage_margin_low")
    if energy_health < 0.35:
        notes.append("energy_intensity_high")
    if machinery_health < 0.35:
        notes.append("machinery_health_low")

    return CaptureHealth(
        omega_capture=omega,
        source_quality_0_1=source_q,
        flux_health_0_1=flux_health,
        storage_health_0_1=storage_health,
        energy_health_0_1=energy_health,
        machinery_health_0_1=machinery_health,
        anomaly_detected=bool(notes),
        notes=tuple(notes),
    )
