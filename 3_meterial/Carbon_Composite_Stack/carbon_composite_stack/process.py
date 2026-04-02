from __future__ import annotations

from .contracts import CompositeProcessConfig, ProcessPerformanceReport


def assess_process(config: CompositeProcessConfig) -> ProcessPerformanceReport:
    temp_penalty = 0.0 if 80.0 <= config.cure_temp_c <= 220.0 else 0.15
    pressure_penalty = 0.0 if 1.0 <= config.cure_pressure_bar <= 10.0 else 0.10
    cycle_penalty = min(0.35, max(0.0, (config.cycle_time_min - 120.0) / 400.0))
    scrap_penalty = min(0.45, config.scrap_rate * 0.9)
    processability_index = max(0.0, 1.0 - (temp_penalty + pressure_penalty + cycle_penalty + scrap_penalty))

    energy_intensity_score = max(0.0, min(1.0, 1.0 - (config.energy_kwh_per_kg - 5.0) / 25.0))
    omega = max(0.0, min(1.0, 0.6 * processability_index + 0.4 * energy_intensity_score))
    return ProcessPerformanceReport(
        processability_index=processability_index,
        energy_intensity_score=energy_intensity_score,
        omega_process=omega,
    )

