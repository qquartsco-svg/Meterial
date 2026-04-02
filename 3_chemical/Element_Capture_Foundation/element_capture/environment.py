from __future__ import annotations

from .contracts import CaptureEnvironment


def source_loading_kg_m3(environment: CaptureEnvironment) -> float:
    return environment.density_kg_m3 * environment.species_fraction_0_1


def source_quality_index(environment: CaptureEnvironment) -> float:
    loading = source_loading_kg_m3(environment)
    loading_score = min(1.0, loading / 0.05)
    accessibility_score = environment.collection_accessibility_0_1
    energy_penalty = 1.0 / (1.0 + environment.energetic_cost_index)
    return max(0.0, min(1.0, 0.45 * loading_score + 0.35 * accessibility_score + 0.20 * energy_penalty))
