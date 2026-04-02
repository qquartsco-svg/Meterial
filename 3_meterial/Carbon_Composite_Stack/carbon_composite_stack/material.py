from __future__ import annotations

import math

from .contracts import CarbonMaterialCandidate, MaterialPerformanceReport, ProductSpec


_SAFETY_DENSITY_FACTOR = {
    "general": 1.00,
    "aerospace": 0.88,
    "marine": 1.15,
    "automotive": 1.05,
}

_THERMAL_TARGET_W_MK = {
    "general": 3.0,
    "aerospace": 8.0,
    "marine": 5.0,
    "automotive": 4.0,
}

_ELECTRICAL_TARGET_S_M = {
    "general": 1_000.0,
    "aerospace": 10_000.0,
    "marine": 5_000.0,
    "automotive": 2_000.0,
}


def assess_material_performance(
    material: CarbonMaterialCandidate,
    spec: ProductSpec,
) -> MaterialPerformanceReport:
    specific_strength_kn_m_kg = material.tensile_strength_mpa / material.density_kg_m3
    specific_stiffness_mn_m_kg = material.youngs_modulus_gpa * 1000.0 / material.density_kg_m3
    fatigue_margin = material.fatigue_strength_mpa / max(1e-6, material.tensile_strength_mpa)

    strength_score = min(1.0, specific_strength_kn_m_kg / spec.target_specific_strength_kn_m_kg)
    stiffness_score = min(1.0, specific_stiffness_mn_m_kg / spec.target_specific_stiffness_mn_m_kg)
    fatigue_score = min(1.0, fatigue_margin / spec.min_fatigue_margin)
    density_ceiling = (1200.0 + 8.0 * spec.max_mass_kg) * _SAFETY_DENSITY_FACTOR[spec.safety_class]
    mass_budget_proxy_score = max(0.0, min(1.0, density_ceiling / material.density_kg_m3))

    thermal_target = _THERMAL_TARGET_W_MK[spec.safety_class]
    thermal_suitability_score = max(0.0, min(1.0, material.thermal_conductivity_w_mk / thermal_target))

    electrical_target = _ELECTRICAL_TARGET_S_M[spec.safety_class]
    electrical_suitability_score = max(
        0.0,
        min(1.0, math.log10(material.electrical_conductivity_s_m + 1.0) / math.log10(electrical_target + 1.0)),
    )

    omega = max(
        0.0,
        min(
            1.0,
            0.34 * strength_score
            + 0.26 * stiffness_score
            + 0.16 * fatigue_score
            + 0.10 * thermal_suitability_score
            + 0.06 * electrical_suitability_score
            + 0.08 * mass_budget_proxy_score,
        ),
    )

    return MaterialPerformanceReport(
        specific_strength_kn_m_kg=specific_strength_kn_m_kg,
        specific_stiffness_mn_m_kg=specific_stiffness_mn_m_kg,
        fatigue_margin=fatigue_margin,
        thermal_suitability_score=thermal_suitability_score,
        electrical_suitability_score=electrical_suitability_score,
        mass_budget_proxy_score=mass_budget_proxy_score,
        omega_material=omega,
    )
