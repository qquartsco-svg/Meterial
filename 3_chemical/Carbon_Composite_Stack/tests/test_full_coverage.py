"""
test_full_coverage.py — Carbon_Composite_Stack 전체 커버리지 확장  (v1.0)

§1  contracts — CarbonMaterialCandidate, CompositeProcessConfig, ProductSpec  (14)
§2  material — assess_material_performance  (14)
§3  process — assess_process  (10)
§4  circularity — assess_circularity  (10)
§5  observer — assess_readiness  (12)
§6  pipeline — run_composite_assessment  (14)
§7  edge cases  (10)

총 84개 테스트
"""
import sys
import os

import pytest

_HERE = os.path.dirname(__file__)
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from carbon_composite_stack.contracts import (
    CarbonMaterialCandidate,
    CompositeProcessConfig,
    ProductSpec,
    MaterialPerformanceReport,
    ProcessPerformanceReport,
    CircularityReport,
    CarbonCompositeReadinessReport,
)
from carbon_composite_stack.material import assess_material_performance
from carbon_composite_stack.process import assess_process
from carbon_composite_stack.circularity import assess_circularity
from carbon_composite_stack.observer import assess_readiness
from carbon_composite_stack.pipeline import run_composite_assessment


# ── 헬퍼 ────────────────────────────────────────────────────────────────────

def make_material(
    name="CFRP_T300",
    density_kg_m3=1560.0,
    tensile_strength_mpa=3500.0,
    youngs_modulus_gpa=230.0,
    thermal_conductivity_w_mk=7.0,
    electrical_conductivity_s_m=5e4,
    fatigue_strength_mpa=1200.0,
    recycle_content_ratio=0.15,
) -> CarbonMaterialCandidate:
    return CarbonMaterialCandidate(
        name=name,
        density_kg_m3=density_kg_m3,
        tensile_strength_mpa=tensile_strength_mpa,
        youngs_modulus_gpa=youngs_modulus_gpa,
        thermal_conductivity_w_mk=thermal_conductivity_w_mk,
        electrical_conductivity_s_m=electrical_conductivity_s_m,
        fatigue_strength_mpa=fatigue_strength_mpa,
        recycle_content_ratio=recycle_content_ratio,
    )


def make_process(
    cure_temp_c=180.0,
    cure_pressure_bar=7.0,
    cycle_time_min=120.0,
    scrap_rate=0.05,
    energy_kwh_per_kg=12.0,
) -> CompositeProcessConfig:
    return CompositeProcessConfig(
        cure_temp_c=cure_temp_c,
        cure_pressure_bar=cure_pressure_bar,
        cycle_time_min=cycle_time_min,
        scrap_rate=scrap_rate,
        energy_kwh_per_kg=energy_kwh_per_kg,
    )


def make_spec(
    target_specific_strength_kn_m_kg=2000.0,
    target_specific_stiffness_mn_m_kg=140.0,
    max_mass_kg=5.0,
    min_fatigue_margin=0.3,
    safety_class="general",
) -> ProductSpec:
    return ProductSpec(
        target_specific_strength_kn_m_kg=target_specific_strength_kn_m_kg,
        target_specific_stiffness_mn_m_kg=target_specific_stiffness_mn_m_kg,
        max_mass_kg=max_mass_kg,
        min_fatigue_margin=min_fatigue_margin,
        safety_class=safety_class,
    )


def full_pipeline():
    return run_composite_assessment(make_material(), make_process(), make_spec())


# ── §1 contracts ─────────────────────────────────────────────────────────────

class TestContracts:
    def test_material_candidate_fields(self):
        m = make_material()
        assert m.name == "CFRP_T300"
        assert m.density_kg_m3 == 1560.0
        assert m.tensile_strength_mpa == 3500.0

    def test_material_default_recycle(self):
        m = CarbonMaterialCandidate(
            name="X", density_kg_m3=1500.0, tensile_strength_mpa=2000.0,
            youngs_modulus_gpa=150.0, thermal_conductivity_w_mk=5.0,
            electrical_conductivity_s_m=1e4, fatigue_strength_mpa=800.0,
        )
        assert m.recycle_content_ratio == 0.0

    def test_process_config_fields(self):
        p = make_process()
        assert p.cure_temp_c == 180.0
        assert p.scrap_rate == 0.05

    def test_spec_safety_class_default(self):
        s = ProductSpec(
            target_specific_strength_kn_m_kg=1000.0,
            target_specific_stiffness_mn_m_kg=100.0,
            max_mass_kg=10.0,
            min_fatigue_margin=0.2,
        )
        assert s.safety_class == "general"

    def test_spec_aerospace(self):
        s = make_spec(safety_class="aerospace")
        assert s.safety_class == "aerospace"

    def test_spec_marine(self):
        s = make_spec(safety_class="marine")
        assert s.safety_class == "marine"

    def test_spec_automotive(self):
        s = make_spec(safety_class="automotive")
        assert s.safety_class == "automotive"

    def test_material_frozen(self):
        m = make_material()
        with pytest.raises((AttributeError, TypeError)):
            m.density_kg_m3 = 9999.0  # type: ignore[misc]

    def test_process_frozen(self):
        p = make_process()
        with pytest.raises((AttributeError, TypeError)):
            p.cure_temp_c = 9999.0  # type: ignore[misc]

    def test_spec_frozen(self):
        s = make_spec()
        with pytest.raises((AttributeError, TypeError)):
            s.max_mass_kg = 9999.0  # type: ignore[misc]

    def test_material_high_performance(self):
        m = make_material(tensile_strength_mpa=7000.0, youngs_modulus_gpa=500.0)
        assert m.tensile_strength_mpa == 7000.0

    def test_process_low_scrap(self):
        p = make_process(scrap_rate=0.01)
        assert p.scrap_rate == 0.01

    def test_spec_tight_mass(self):
        s = make_spec(max_mass_kg=0.5)
        assert s.max_mass_kg == 0.5

    def test_material_zero_recycle(self):
        m = make_material(recycle_content_ratio=0.0)
        assert m.recycle_content_ratio == 0.0


# ── §2 material — assess_material_performance ─────────────────────────────────

class TestMaterialPerformance:
    def test_returns_report(self):
        report = assess_material_performance(make_material(), make_spec())
        assert isinstance(report, MaterialPerformanceReport)

    def test_specific_strength_positive(self):
        report = assess_material_performance(make_material(), make_spec())
        assert report.specific_strength_kn_m_kg > 0.0

    def test_specific_stiffness_positive(self):
        report = assess_material_performance(make_material(), make_spec())
        assert report.specific_stiffness_mn_m_kg > 0.0

    def test_omega_material_in_range(self):
        report = assess_material_performance(make_material(), make_spec())
        assert 0.0 <= report.omega_material <= 1.0

    def test_fatigue_margin_in_range(self):
        report = assess_material_performance(make_material(), make_spec())
        assert report.fatigue_margin >= 0.0

    def test_thermal_suitability_in_range(self):
        report = assess_material_performance(make_material(), make_spec())
        assert 0.0 <= report.thermal_suitability_score <= 1.0

    def test_electrical_suitability_in_range(self):
        report = assess_material_performance(make_material(), make_spec())
        assert 0.0 <= report.electrical_suitability_score <= 1.0

    def test_mass_budget_in_range(self):
        report = assess_material_performance(make_material(), make_spec())
        assert 0.0 <= report.mass_budget_proxy_score <= 1.0

    def test_high_strength_high_specific_strength(self):
        low = make_material(tensile_strength_mpa=200.0)
        high = make_material(tensile_strength_mpa=7000.0)
        r_low = assess_material_performance(low, make_spec())
        r_high = assess_material_performance(high, make_spec())
        assert r_high.specific_strength_kn_m_kg >= r_low.specific_strength_kn_m_kg

    def test_high_density_lower_specific_strength(self):
        light = make_material(density_kg_m3=1000.0)
        heavy = make_material(density_kg_m3=5000.0)
        r_light = assess_material_performance(light, make_spec())
        r_heavy = assess_material_performance(heavy, make_spec())
        assert r_light.specific_strength_kn_m_kg >= r_heavy.specific_strength_kn_m_kg

    def test_all_safety_classes(self):
        for sc in ["general", "aerospace", "marine", "automotive"]:
            spec = make_spec(safety_class=sc)
            report = assess_material_performance(make_material(), spec)
            assert isinstance(report, MaterialPerformanceReport)

    def test_stiffness_scales_with_modulus(self):
        lo = make_material(youngs_modulus_gpa=50.0)
        hi = make_material(youngs_modulus_gpa=500.0)
        r_lo = assess_material_performance(lo, make_spec())
        r_hi = assess_material_performance(hi, make_spec())
        assert r_hi.specific_stiffness_mn_m_kg >= r_lo.specific_stiffness_mn_m_kg

    def test_perfect_material_high_specific_strength(self):
        m = make_material(tensile_strength_mpa=9999.0, youngs_modulus_gpa=999.0,
                          density_kg_m3=500.0, fatigue_strength_mpa=5000.0)
        report = assess_material_performance(m, make_spec())
        assert report.specific_strength_kn_m_kg >= 10.0
        assert 0.0 <= report.omega_material <= 1.0

    def test_weak_material_lower_omega(self):
        m = make_material(tensile_strength_mpa=100.0, youngs_modulus_gpa=10.0)
        report = assess_material_performance(m, make_spec(
            target_specific_strength_kn_m_kg=5000.0))
        assert isinstance(report, MaterialPerformanceReport)


# ── §3 process — assess_process ───────────────────────────────────────────────

class TestProcessAssessment:
    def test_returns_report(self):
        report = assess_process(make_process())
        assert isinstance(report, ProcessPerformanceReport)

    def test_processability_index_in_range(self):
        report = assess_process(make_process())
        assert 0.0 <= report.processability_index <= 1.0

    def test_energy_intensity_score_in_range(self):
        report = assess_process(make_process())
        assert 0.0 <= report.energy_intensity_score <= 1.0

    def test_omega_process_in_range(self):
        report = assess_process(make_process())
        assert 0.0 <= report.omega_process <= 1.0

    def test_low_scrap_better_processability(self):
        r_low = assess_process(make_process(scrap_rate=0.02))
        r_high = assess_process(make_process(scrap_rate=0.40))
        assert r_low.processability_index >= r_high.processability_index

    def test_low_energy_better_score(self):
        r_low = assess_process(make_process(energy_kwh_per_kg=2.0))
        r_high = assess_process(make_process(energy_kwh_per_kg=50.0))
        assert r_low.energy_intensity_score >= r_high.energy_intensity_score

    def test_extreme_scrap_vs_low_scrap(self):
        r_low = assess_process(make_process(scrap_rate=0.01))
        r_high = assess_process(make_process(scrap_rate=0.99))
        assert r_low.processability_index >= r_high.processability_index

    def test_zero_scrap_high_processability(self):
        report = assess_process(make_process(scrap_rate=0.0))
        assert report.processability_index >= 0.8

    def test_high_cure_temp_no_crash(self):
        report = assess_process(make_process(cure_temp_c=400.0))
        assert isinstance(report, ProcessPerformanceReport)

    def test_very_long_cycle_time(self):
        report = assess_process(make_process(cycle_time_min=600.0))
        assert isinstance(report, ProcessPerformanceReport)


# ── §4 circularity — assess_circularity ──────────────────────────────────────

class TestCircularity:
    def test_returns_report(self):
        report = assess_circularity(make_material(), make_process())
        assert isinstance(report, CircularityReport)

    def test_recycle_score_in_range(self):
        report = assess_circularity(make_material(), make_process())
        assert 0.0 <= report.recycle_score <= 1.0

    def test_scrap_penalty_nonnegative(self):
        report = assess_circularity(make_material(), make_process())
        assert report.scrap_penalty >= 0.0

    def test_omega_circularity_in_range(self):
        report = assess_circularity(make_material(), make_process())
        assert 0.0 <= report.omega_circularity <= 1.0

    def test_high_recycle_content_better(self):
        r_low = assess_circularity(make_material(recycle_content_ratio=0.0), make_process())
        r_high = assess_circularity(make_material(recycle_content_ratio=0.8), make_process())
        assert r_high.recycle_score >= r_low.recycle_score

    def test_fully_recycled_material(self):
        m = make_material(recycle_content_ratio=1.0)
        report = assess_circularity(m, make_process())
        assert report.recycle_score >= 0.9

    def test_virgin_material_low_recycle(self):
        m = make_material(recycle_content_ratio=0.0)
        report = assess_circularity(m, make_process())
        assert report.recycle_score <= 0.1

    def test_high_scrap_penalty(self):
        r_lo = assess_circularity(make_material(), make_process(scrap_rate=0.01))
        r_hi = assess_circularity(make_material(), make_process(scrap_rate=0.99))
        assert r_hi.scrap_penalty >= r_lo.scrap_penalty

    def test_circularity_good_vs_bad(self):
        m_good = make_material(recycle_content_ratio=0.9)
        p_good = make_process(scrap_rate=0.01)
        m_bad = make_material(recycle_content_ratio=0.0)
        p_bad = make_process(scrap_rate=0.99)
        r_good = assess_circularity(m_good, p_good)
        r_bad = assess_circularity(m_bad, p_bad)
        assert r_good.omega_circularity >= r_bad.omega_circularity - 0.01

    def test_all_fields_present(self):
        report = assess_circularity(make_material(), make_process())
        for field in ["recycle_score", "scrap_penalty", "omega_circularity"]:
            assert hasattr(report, field), f"missing {field}"


# ── §5 observer — assess_readiness ───────────────────────────────────────────

class TestObserver:
    def _full_reports(self):
        mat_rep = assess_material_performance(make_material(), make_spec())
        proc_rep = assess_process(make_process())
        circ_rep = assess_circularity(make_material(), make_process())
        return mat_rep, proc_rep, circ_rep

    def test_returns_readiness_report(self):
        report = assess_readiness(*self._full_reports())
        assert isinstance(report, CarbonCompositeReadinessReport)

    def test_verdict_valid(self):
        report = assess_readiness(*self._full_reports())
        assert report.verdict in ("HEALTHY", "STABLE", "FRAGILE", "CRITICAL")

    def test_omega_total_in_range(self):
        report = assess_readiness(*self._full_reports())
        assert 0.0 <= report.omega_total <= 1.0

    def test_omega_material_in_range(self):
        report = assess_readiness(*self._full_reports())
        assert 0.0 <= report.omega_material <= 1.0

    def test_omega_process_in_range(self):
        report = assess_readiness(*self._full_reports())
        assert 0.0 <= report.omega_process <= 1.0

    def test_omega_circularity_in_range(self):
        report = assess_readiness(*self._full_reports())
        assert 0.0 <= report.omega_circularity <= 1.0

    def test_evidence_is_dict(self):
        report = assess_readiness(*self._full_reports())
        assert isinstance(report.evidence, dict)

    def test_bad_material_lower_omega(self):
        weak_mat = assess_material_performance(
            make_material(tensile_strength_mpa=50.0),
            make_spec(target_specific_strength_kn_m_kg=5000.0))
        good_mat = assess_material_performance(make_material(), make_spec())
        proc_rep = assess_process(make_process())
        circ_rep = assess_circularity(make_material(), make_process())
        r_weak = assess_readiness(weak_mat, proc_rep, circ_rep)
        r_good = assess_readiness(good_mat, proc_rep, circ_rep)
        assert r_good.omega_material >= r_weak.omega_material - 0.01

    def test_high_scrap_lower_process_omega(self):
        mat_rep = assess_material_performance(make_material(), make_spec())
        proc_bad = assess_process(make_process(scrap_rate=0.90))
        proc_good = assess_process(make_process(scrap_rate=0.01))
        circ_rep = assess_circularity(make_material(), make_process())
        r_bad = assess_readiness(mat_rep, proc_bad, circ_rep)
        r_good = assess_readiness(mat_rep, proc_good, circ_rep)
        assert r_good.omega_process >= r_bad.omega_process - 0.01

    def test_all_fields_present(self):
        report = assess_readiness(*self._full_reports())
        for field in ["omega_material", "omega_process", "omega_circularity",
                      "omega_total", "verdict", "evidence"]:
            assert hasattr(report, field), f"missing {field}"

    def test_nominal_is_not_critical(self):
        report = assess_readiness(*self._full_reports())
        assert report.verdict in ("HEALTHY", "STABLE", "FRAGILE")

    def test_eco_high_circularity(self):
        m = make_material(recycle_content_ratio=1.0)
        mat_rep = assess_material_performance(m, make_spec())
        proc_rep = assess_process(make_process(energy_kwh_per_kg=2.0, scrap_rate=0.01))
        circ_rep = assess_circularity(m, make_process(energy_kwh_per_kg=2.0))
        report = assess_readiness(mat_rep, proc_rep, circ_rep)
        assert report.omega_circularity >= 0.5


# ── §6 pipeline — run_composite_assessment ────────────────────────────────────

class TestPipeline:
    def test_returns_tuple(self):
        result = run_composite_assessment(make_material(), make_process(), make_spec())
        assert isinstance(result, tuple)
        assert len(result) == 4

    def test_readiness_report_first(self):
        readiness, _, _, _ = full_pipeline()
        assert isinstance(readiness, CarbonCompositeReadinessReport)

    def test_material_report_second(self):
        _, mat, _, _ = full_pipeline()
        assert isinstance(mat, MaterialPerformanceReport)

    def test_process_report_third(self):
        _, _, proc, _ = full_pipeline()
        assert isinstance(proc, ProcessPerformanceReport)

    def test_circularity_report_fourth(self):
        _, _, _, circ = full_pipeline()
        assert isinstance(circ, CircularityReport)

    def test_omega_in_range(self):
        readiness, _, _, _ = full_pipeline()
        assert 0.0 <= readiness.omega_total <= 1.0

    def test_verdict_valid(self):
        readiness, _, _, _ = full_pipeline()
        assert readiness.verdict in ("HEALTHY", "STABLE", "FRAGILE", "CRITICAL")

    def test_aerospace_class(self):
        readiness, mat, _, _ = run_composite_assessment(
            make_material(), make_process(), make_spec(safety_class="aerospace"))
        assert isinstance(readiness, CarbonCompositeReadinessReport)

    def test_marine_class(self):
        readiness, _, _, _ = run_composite_assessment(
            make_material(), make_process(), make_spec(safety_class="marine"))
        assert readiness.verdict in ("HEALTHY", "STABLE", "FRAGILE", "CRITICAL")

    def test_automotive_class(self):
        readiness, _, _, _ = run_composite_assessment(
            make_material(), make_process(), make_spec(safety_class="automotive"))
        assert readiness.verdict in ("HEALTHY", "STABLE", "FRAGILE", "CRITICAL")

    def test_consistent_results(self):
        m, p, s = make_material(), make_process(), make_spec()
        r1, _, _, _ = run_composite_assessment(m, p, s)
        r2, _, _, _ = run_composite_assessment(m, p, s)
        assert r1.omega_total == r2.omega_total

    def test_high_recycle_better_circularity(self):
        m_lo = make_material(recycle_content_ratio=0.0)
        m_hi = make_material(recycle_content_ratio=0.9)
        _, _, _, c_lo = run_composite_assessment(m_lo, make_process(), make_spec())
        _, _, _, c_hi = run_composite_assessment(m_hi, make_process(), make_spec())
        assert c_hi.recycle_score >= c_lo.recycle_score

    def test_evidence_populated(self):
        readiness, _, _, _ = full_pipeline()
        assert len(readiness.evidence) > 0

    def test_all_safety_classes_valid(self):
        for sc in ["general", "aerospace", "marine", "automotive"]:
            r, _, _, _ = run_composite_assessment(
                make_material(), make_process(), make_spec(safety_class=sc))
            assert r.verdict in ("HEALTHY", "STABLE", "FRAGILE", "CRITICAL")


# ── §7 edge cases ─────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_minimal_material(self):
        m = make_material(
            tensile_strength_mpa=100.0, youngs_modulus_gpa=10.0,
            fatigue_strength_mpa=50.0, density_kg_m3=2000.0,
        )
        report = assess_material_performance(m, make_spec())
        assert 0.0 <= report.omega_material <= 1.0

    def test_very_high_cure_temp(self):
        p = make_process(cure_temp_c=400.0)
        report = assess_process(p)
        assert isinstance(report, ProcessPerformanceReport)

    def test_very_long_cycle_time(self):
        p = make_process(cycle_time_min=600.0)
        report = assess_process(p)
        assert isinstance(report, ProcessPerformanceReport)

    def test_complete_scrap(self):
        p_bad = make_process(scrap_rate=1.0)
        p_good = make_process(scrap_rate=0.0)
        r_bad = assess_process(p_bad)
        r_good = assess_process(p_good)
        assert r_good.processability_index >= r_bad.processability_index

    def test_zero_energy_process(self):
        p = make_process(energy_kwh_per_kg=0.1)
        report = assess_process(p)
        assert report.energy_intensity_score >= 0.8

    def test_circularity_full_recycle_low_scrap(self):
        m = make_material(recycle_content_ratio=1.0)
        p = make_process(scrap_rate=0.0)
        report = assess_circularity(m, p)
        assert report.omega_circularity >= 0.7

    def test_pipeline_heavy_material(self):
        m = make_material(density_kg_m3=8000.0)
        readiness, _, _, _ = run_composite_assessment(m, make_process(), make_spec())
        assert isinstance(readiness, CarbonCompositeReadinessReport)

    def test_pipeline_tight_mass_constraint(self):
        s = make_spec(max_mass_kg=0.01)
        readiness, _, _, _ = run_composite_assessment(make_material(), make_process(), s)
        assert readiness.verdict in ("HEALTHY", "STABLE", "FRAGILE", "CRITICAL")

    def test_all_safety_classes_omegas_valid(self):
        results = []
        for sc in ["general", "automotive", "marine", "aerospace"]:
            r, _, _, _ = run_composite_assessment(
                make_material(), make_process(), make_spec(safety_class=sc))
            results.append(r.omega_total)
        assert all(0.0 <= v <= 1.0 for v in results)

    def test_high_electrical_conductivity(self):
        m = make_material(electrical_conductivity_s_m=1e7)
        report = assess_material_performance(m, make_spec())
        assert isinstance(report, MaterialPerformanceReport)
