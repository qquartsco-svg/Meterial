from __future__ import annotations

from .contracts import (
    CarbonCompositeReadinessReport,
    CircularityReport,
    MaterialPerformanceReport,
    ProcessPerformanceReport,
)


def assess_readiness(
    material: MaterialPerformanceReport,
    process: ProcessPerformanceReport,
    circularity: CircularityReport,
) -> CarbonCompositeReadinessReport:
    omega_total = 0.45 * material.omega_material + 0.35 * process.omega_process + 0.20 * circularity.omega_circularity
    if omega_total >= 0.80:
        verdict = "HEALTHY"
    elif omega_total >= 0.60:
        verdict = "STABLE"
    elif omega_total >= 0.40:
        verdict = "FRAGILE"
    else:
        verdict = "CRITICAL"
    return CarbonCompositeReadinessReport(
        omega_material=material.omega_material,
        omega_process=process.omega_process,
        omega_circularity=circularity.omega_circularity,
        omega_total=omega_total,
        verdict=verdict,
        evidence={
            "specific_strength_kn_m_kg": material.specific_strength_kn_m_kg,
            "specific_stiffness_mn_m_kg": material.specific_stiffness_mn_m_kg,
            "fatigue_margin": material.fatigue_margin,
            "thermal_suitability_score": material.thermal_suitability_score,
            "electrical_suitability_score": material.electrical_suitability_score,
            "mass_budget_proxy_score": material.mass_budget_proxy_score,
            "processability_index": process.processability_index,
            "energy_intensity_score": process.energy_intensity_score,
            "recycle_score": circularity.recycle_score,
            "scrap_penalty": circularity.scrap_penalty,
        },
    )
