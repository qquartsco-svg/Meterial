"""Carbon_Composite_Stack 확장 테스트 — §1 재료(8) §2 공정(6) §3 순환성(4) §4 파이프라인(6)"""
from __future__ import annotations
import pytest
from carbon_composite_stack import (
    CarbonMaterialCandidate, CompositeProcessConfig, ProductSpec,
    run_composite_assessment, CarbonCompositeReadinessReport,
    MaterialPerformanceReport, ProcessPerformanceReport, CircularityReport,
)
from carbon_composite_stack.material import assess_material_performance
from carbon_composite_stack.process import assess_process
from carbon_composite_stack.circularity import assess_circularity


@pytest.fixture
def cfrp():
    return CarbonMaterialCandidate("CFRP-T700", 1600, 3500, 230, 5.0, 1e4, 1800, 0.1)

@pytest.fixture
def eco_cfrp():
    return CarbonMaterialCandidate("EcoCFRP", 1550, 3000, 210, 4.0, 8e3, 1500, 0.6)

@pytest.fixture
def proc():
    return CompositeProcessConfig(135.0, 7.0, 90.0, 0.05, 12.0)

@pytest.fixture
def spec():
    return ProductSpec(2.0, 0.14, 50.0, 1.2, safety_class="aerospace")


class TestMaterialAssessment:
    def test_omega_material_range(self, cfrp, spec):
        r = assess_material_performance(cfrp, spec)
        assert 0.0 <= r.omega_material <= 1.0

    def test_high_strength_good_score(self, cfrp, spec):
        r = assess_material_performance(cfrp, spec)
        assert r.omega_material >= 0.5

    def test_weak_material_lower_score(self, spec):
        weak = CarbonMaterialCandidate("Weak", 2000, 500, 50, 2.0, 1e3, 300, 0.0)
        r = assess_material_performance(weak, spec)
        assert r.omega_material <= 0.8

    def test_recycle_content_accepted(self, eco_cfrp, spec):
        r = assess_material_performance(eco_cfrp, spec)
        assert isinstance(r, MaterialPerformanceReport)

    def test_marine_safety_class(self, cfrp):
        s = ProductSpec(2.0, 0.14, 50.0, 1.2, safety_class="marine")
        r = assess_material_performance(cfrp, s)
        assert 0.0 <= r.omega_material <= 1.0

    def test_thermal_suitability_score(self, cfrp, spec):
        r = assess_material_performance(cfrp, spec)
        assert 0.0 <= r.thermal_suitability_score <= 1.0

    def test_negative_density_rejected(self):
        with pytest.raises(ValueError):
            CarbonMaterialCandidate("Bad", -1, 3500, 230, 5.0, 1e4, 1800)

    def test_invalid_recycle_ratio_rejected(self):
        with pytest.raises(ValueError):
            CarbonMaterialCandidate("Bad", 1600, 3500, 230, 5.0, 1e4, 1800, 1.5)


class TestProcessAssessment:
    def test_omega_process_range(self, proc):
        r = assess_process(proc)
        assert 0.0 <= r.omega_process <= 1.0

    def test_high_scrap_penalized(self):
        r = assess_process(CompositeProcessConfig(135.0, 7.0, 90.0, 0.40, 12.0))
        assert r.omega_process < 0.9

    def test_low_scrap_acceptable(self):
        r = assess_process(CompositeProcessConfig(135.0, 7.0, 90.0, 0.01, 10.0))
        assert r.omega_process >= 0.3

    def test_zero_cycle_time_rejected(self):
        with pytest.raises(ValueError):
            CompositeProcessConfig(135.0, 7.0, 0.0, 0.05, 12.0)

    def test_negative_pressure_rejected(self):
        with pytest.raises(ValueError):
            CompositeProcessConfig(135.0, -1.0, 90.0, 0.05, 12.0)

    def test_report_frozen(self, proc):
        r = assess_process(proc)
        with pytest.raises(Exception):
            r.omega_process = 0.0  # type: ignore


class TestCircularity:
    def test_report_type(self, cfrp, proc):
        r = assess_circularity(cfrp, proc)
        assert isinstance(r, CircularityReport)

    def test_omega_circularity_range(self, cfrp, proc):
        r = assess_circularity(cfrp, proc)
        assert 0.0 <= r.omega_circularity <= 1.0

    def test_high_recycle_boosts_score(self, cfrp, eco_cfrp, proc):
        r_eco = assess_circularity(eco_cfrp, proc)
        r_low = assess_circularity(cfrp, proc)
        assert r_eco.omega_circularity >= r_low.omega_circularity

    def test_low_scrap_improves_circularity(self, cfrp):
        good = CompositeProcessConfig(135.0, 7.0, 90.0, 0.02, 10.0)
        bad  = CompositeProcessConfig(135.0, 7.0, 90.0, 0.35, 20.0)
        assert assess_circularity(cfrp, good).omega_circularity >= assess_circularity(cfrp, bad).omega_circularity


class TestPipelineIntegration:
    def test_returns_four_reports(self, cfrp, proc, spec):
        assert len(run_composite_assessment(cfrp, proc, spec)) == 4

    def test_readiness_type(self, cfrp, proc, spec):
        r, *_ = run_composite_assessment(cfrp, proc, spec)
        assert isinstance(r, CarbonCompositeReadinessReport)

    def test_omega_total_range(self, cfrp, proc, spec):
        r, *_ = run_composite_assessment(cfrp, proc, spec)
        assert 0.0 <= r.omega_total <= 1.0

    def test_verdict_valid(self, cfrp, proc, spec):
        r, *_ = run_composite_assessment(cfrp, proc, spec)
        assert r.verdict in ("HEALTHY", "STABLE", "FRAGILE", "CRITICAL")

    def test_eco_material_pipeline(self, eco_cfrp, proc, spec):
        assert len(run_composite_assessment(eco_cfrp, proc, spec)) == 4

    def test_sub_report_omega_fields(self, cfrp, proc, spec):
        _, mat_r, proc_r, circ_r = run_composite_assessment(cfrp, proc, spec)
        assert hasattr(mat_r, "omega_material")
        assert hasattr(proc_r, "omega_process")
        assert hasattr(circ_r, "omega_circularity")
