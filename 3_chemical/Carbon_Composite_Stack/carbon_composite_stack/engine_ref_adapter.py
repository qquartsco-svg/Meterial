from __future__ import annotations

from typing import Any, Dict

from .contracts import CarbonMaterialCandidate, CompositeProcessConfig, ProductSpec
from .pipeline import run_composite_assessment

ENGINE_REF = "carbon.composite.readiness"


def run_engine_ref_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    m = payload["material"]
    p = payload["process"]
    s = payload["spec"]
    material = CarbonMaterialCandidate(
        name=m["name"],
        density_kg_m3=float(m["density_kg_m3"]),
        tensile_strength_mpa=float(m["tensile_strength_mpa"]),
        youngs_modulus_gpa=float(m["youngs_modulus_gpa"]),
        thermal_conductivity_w_mk=float(m.get("thermal_conductivity_w_mk", 1.0)),
        electrical_conductivity_s_m=float(m.get("electrical_conductivity_s_m", 1.0)),
        fatigue_strength_mpa=float(m["fatigue_strength_mpa"]),
        recycle_content_ratio=float(m.get("recycle_content_ratio", 0.0)),
    )
    process = CompositeProcessConfig(
        cure_temp_c=float(p["cure_temp_c"]),
        cure_pressure_bar=float(p["cure_pressure_bar"]),
        cycle_time_min=float(p["cycle_time_min"]),
        scrap_rate=float(p["scrap_rate"]),
        energy_kwh_per_kg=float(p["energy_kwh_per_kg"]),
    )
    spec = ProductSpec(
        target_specific_strength_kn_m_kg=float(s["target_specific_strength_kn_m_kg"]),
        target_specific_stiffness_mn_m_kg=float(s["target_specific_stiffness_mn_m_kg"]),
        max_mass_kg=float(s["max_mass_kg"]),
        min_fatigue_margin=float(s["min_fatigue_margin"]),
        safety_class=str(s.get("safety_class", "general")),
    )

    readiness, material_report, process_report, circularity_report = run_composite_assessment(material, process, spec)
    return {
        "engine_ref": ENGINE_REF,
        "omega": readiness.omega_total,
        "verdict": readiness.verdict,
        "evidence": readiness.evidence,
        "material": {
            "specific_strength_kn_m_kg": material_report.specific_strength_kn_m_kg,
            "specific_stiffness_mn_m_kg": material_report.specific_stiffness_mn_m_kg,
        },
        "process": {"processability_index": process_report.processability_index},
        "circularity": {"omega_circularity": circularity_report.omega_circularity},
    }

