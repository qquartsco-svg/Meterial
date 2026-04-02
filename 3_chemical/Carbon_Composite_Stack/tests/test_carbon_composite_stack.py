from carbon_composite_stack import (
    CarbonMaterialCandidate,
    CompositeProcessConfig,
    ProductSpec,
    run_composite_assessment,
)
from carbon_composite_stack.engine_ref_adapter import ENGINE_REF, run_engine_ref_payload


def _sample():
    material = CarbonMaterialCandidate(
        name="CFRP-A",
        density_kg_m3=1550.0,
        tensile_strength_mpa=1800.0,
        youngs_modulus_gpa=140.0,
        thermal_conductivity_w_mk=8.5,
        electrical_conductivity_s_m=15000.0,
        fatigue_strength_mpa=900.0,
        recycle_content_ratio=0.2,
    )
    process = CompositeProcessConfig(
        cure_temp_c=180.0,
        cure_pressure_bar=6.0,
        cycle_time_min=95.0,
        scrap_rate=0.08,
        energy_kwh_per_kg=9.0,
    )
    spec = ProductSpec(
        target_specific_strength_kn_m_kg=1.0,
        target_specific_stiffness_mn_m_kg=70.0,
        max_mass_kg=120.0,
        min_fatigue_margin=0.45,
        safety_class="aerospace",
    )
    return material, process, spec


def test_pipeline_outputs_valid_ranges() -> None:
    material, process, spec = _sample()
    readiness, mr, pr, cr = run_composite_assessment(material, process, spec)
    assert 0.0 <= readiness.omega_total <= 1.0
    assert readiness.verdict in {"HEALTHY", "STABLE", "FRAGILE", "CRITICAL"}
    assert mr.specific_strength_kn_m_kg > 0
    assert 0.0 <= mr.thermal_suitability_score <= 1.0
    assert 0.0 <= mr.electrical_suitability_score <= 1.0
    assert 0.0 <= mr.mass_budget_proxy_score <= 1.0
    assert pr.processability_index >= 0
    assert cr.omega_circularity >= 0


def test_contract_rejects_non_physical_input() -> None:
    try:
        CarbonMaterialCandidate(
            name="x",
            density_kg_m3=0.0,
            tensile_strength_mpa=100.0,
            youngs_modulus_gpa=10.0,
            thermal_conductivity_w_mk=1.0,
            electrical_conductivity_s_m=1.0,
            fatigue_strength_mpa=50.0,
        )
    except ValueError:
        return
    raise AssertionError("expected ValueError for invalid density")


def test_engine_ref_payload_contract() -> None:
    payload = {
        "material": {
            "name": "CFRP-A",
            "density_kg_m3": 1550.0,
            "tensile_strength_mpa": 1800.0,
            "youngs_modulus_gpa": 140.0,
            "thermal_conductivity_w_mk": 8.5,
            "electrical_conductivity_s_m": 15000.0,
            "fatigue_strength_mpa": 900.0,
            "recycle_content_ratio": 0.2,
        },
        "process": {
            "cure_temp_c": 180.0,
            "cure_pressure_bar": 6.0,
            "cycle_time_min": 95.0,
            "scrap_rate": 0.08,
            "energy_kwh_per_kg": 9.0,
        },
        "spec": {
            "target_specific_strength_kn_m_kg": 1.0,
            "target_specific_stiffness_mn_m_kg": 70.0,
            "max_mass_kg": 120.0,
            "min_fatigue_margin": 0.45,
            "safety_class": "aerospace",
        },
    }
    out = run_engine_ref_payload(payload)
    assert out["engine_ref"] == ENGINE_REF
    assert 0.0 <= out["omega"] <= 1.0
    assert "thermal_suitability_score" in out["evidence"]
    assert "electrical_suitability_score" in out["evidence"]
    assert "mass_budget_proxy_score" in out["evidence"]


def test_safety_class_and_mass_budget_influence_material_score() -> None:
    material, process, _ = _sample()
    strict_spec = ProductSpec(
        target_specific_strength_kn_m_kg=1.0,
        target_specific_stiffness_mn_m_kg=70.0,
        max_mass_kg=20.0,
        min_fatigue_margin=0.45,
        safety_class="aerospace",
    )
    relaxed_spec = ProductSpec(
        target_specific_strength_kn_m_kg=1.0,
        target_specific_stiffness_mn_m_kg=70.0,
        max_mass_kg=240.0,
        min_fatigue_margin=0.45,
        safety_class="marine",
    )

    strict_readiness, strict_material, _, _ = run_composite_assessment(material, process, strict_spec)
    relaxed_readiness, relaxed_material, _, _ = run_composite_assessment(material, process, relaxed_spec)

    assert strict_material.mass_budget_proxy_score < relaxed_material.mass_budget_proxy_score
    assert strict_readiness.omega_total <= relaxed_readiness.omega_total
