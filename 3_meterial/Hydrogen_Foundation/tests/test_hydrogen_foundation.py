"""Comprehensive test suite for Hydrogen_Foundation v0.1.0."""

from __future__ import annotations

import inspect
import math
import pytest

# ── L0 contracts ───────────────────────────────────────────────────────

from hydrogen.contracts import (
    ColorCode,
    ConceptLayer,
    FuelCellAssessment,
    FuelCellType,
    H2Properties,
    HealthVerdict,
    HydrogenClaimPayload,
    HydrogenFoundationReport,
    HydrogenHealthReport,
    HydrogenScreeningReport,
    ProductionAssessment,
    ProductionMethod,
    SafetyAssessment,
    StorageAssessment,
    StorageMethod,
    Verdict,
)

# ── Constants ──────────────────────────────────────────────────────────

from hydrogen.constants import (
    FARADAY_C_PER_MOL,
    H2_BOILING_POINT_K,
    H2_DENSITY_KG_PER_M3_STP,
    H2_HHV_MJ_PER_KG,
    H2_LEL_VOL_PERCENT,
    H2_LHV_MJ_PER_KG,
    H2_LIQUID_DENSITY_KG_PER_M3,
    H2_MOLAR_MASS_G_PER_MOL,
    H2_UEL_VOL_PERCENT,
    R_GAS_J_PER_MOL_K,
    STANDARD_TEMPERATURE_K,
    WATER_ELECTROLYSIS_E0_V,
)


class TestConstants:
    def test_r_gas(self):
        assert 8.31 < R_GAS_J_PER_MOL_K < 8.32

    def test_faraday(self):
        assert 96_000 < FARADAY_C_PER_MOL < 97_000

    def test_h2_molar_mass(self):
        assert 2.0 < H2_MOLAR_MASS_G_PER_MOL < 2.1

    def test_electrolysis_e0(self):
        assert 1.2 < WATER_ELECTROLYSIS_E0_V < 1.3

    def test_lhv_hhv(self):
        assert H2_LHV_MJ_PER_KG < H2_HHV_MJ_PER_KG

    def test_lel_uel(self):
        assert H2_LEL_VOL_PERCENT == 4.0
        assert H2_UEL_VOL_PERCENT == 75.0

    def test_boiling_point(self):
        assert 20.0 < H2_BOILING_POINT_K < 21.0

    def test_liquid_density(self):
        assert 70.0 < H2_LIQUID_DENSITY_KG_PER_M3 < 72.0


# ── L1 properties ─────────────────────────────────────────────────────

from hydrogen.properties import (
    compressibility_factor,
    energy_content_kwh,
    hydrogen_property_card,
    ideal_gas_density_kg_per_m3,
    properties_concept_layers,
    van_der_waals_pressure_pa,
)


class TestProperties:
    def test_property_card(self):
        card = hydrogen_property_card()
        assert isinstance(card, H2Properties)
        assert card.molar_mass_g_per_mol == H2_MOLAR_MASS_G_PER_MOL
        assert card.lhv_mj_per_kg == H2_LHV_MJ_PER_KG

    def test_ideal_gas_density_stp(self):
        rho = ideal_gas_density_kg_per_m3(STANDARD_TEMPERATURE_K, 101_325.0)
        assert abs(rho - H2_DENSITY_KG_PER_M3_STP) < 0.01

    def test_ideal_gas_density_negative_temp(self):
        with pytest.raises(ValueError):
            ideal_gas_density_kg_per_m3(-10.0, 101_325.0)

    def test_vdw_pressure(self):
        vm = R_GAS_J_PER_MOL_K * 298.15 / 101_325.0
        p = van_der_waals_pressure_pa(298.15, vm)
        assert abs(p - 101_325.0) / 101_325.0 < 0.05

    def test_compressibility_near_1_at_low_p(self):
        z = compressibility_factor(298.15, 101_325.0)
        assert abs(z - 1.0) < 0.05

    def test_compressibility_high_pressure(self):
        z = compressibility_factor(298.15, 70e6)
        assert z > 1.0

    def test_energy_content_lhv(self):
        e = energy_content_kwh(1.0, "lhv")
        assert abs(e - 33.33) < 1.0

    def test_energy_content_hhv(self):
        e = energy_content_kwh(1.0, "hhv")
        assert e > energy_content_kwh(1.0, "lhv")

    def test_concept_layers(self):
        layers = properties_concept_layers()
        assert len(layers) >= 2
        assert all(isinstance(l, ConceptLayer) for l in layers)


# ── L2 production ──────────────────────────────────────────────────────

from hydrogen.production import (
    assess_electrolysis,
    assess_smr,
    classify_color,
    electrolysis_cell_voltage,
    electrolysis_efficiency,
    electrolysis_energy_kwh_per_kg_h2,
    electrolysis_h2_rate_mol_per_s,
    production_concept_layers,
    smr_co2_intensity_kg_per_kg_h2,
    smr_equilibrium_constant,
)


class TestProduction:
    def test_cell_voltage_default(self):
        v = electrolysis_cell_voltage()
        assert 1.5 < v < 2.5

    def test_cell_voltage_temperature_effect(self):
        v298 = electrolysis_cell_voltage(temperature_k=298.15)
        v353 = electrolysis_cell_voltage(temperature_k=353.15)
        assert v353 < v298

    def test_h2_rate(self):
        rate = electrolysis_h2_rate_mol_per_s(FARADAY_C_PER_MOL)
        assert abs(rate - 0.5) < 0.01

    def test_electrolysis_efficiency_bounds(self):
        eff = electrolysis_efficiency(1.8, 0.98)
        assert 0.0 < eff < 1.0

    def test_electrolysis_efficiency_zero_voltage(self):
        assert electrolysis_efficiency(0.0) == 0.0

    def test_energy_per_kg(self):
        e = electrolysis_energy_kwh_per_kg_h2(1.8)
        assert 40 < e < 60

    def test_smr_keq_increases_with_temp(self):
        k800 = smr_equilibrium_constant(800.0)
        k1100 = smr_equilibrium_constant(1100.0)
        assert k1100 > k800

    def test_smr_co2_grey(self):
        co2 = smr_co2_intensity_kg_per_kg_h2(with_ccs=False)
        assert co2 == 10.0

    def test_smr_co2_blue(self):
        co2 = smr_co2_intensity_kg_per_kg_h2(with_ccs=True, capture_rate=0.90)
        assert abs(co2 - 1.0) < 0.01

    def test_color_green(self):
        c = classify_color(ProductionMethod.PEM_ELECTROLYSIS, electricity_renewable=True)
        assert c == ColorCode.GREEN

    def test_color_grey(self):
        c = classify_color(ProductionMethod.SMR, ccs_attached=False)
        assert c == ColorCode.GREY

    def test_color_blue(self):
        c = classify_color(ProductionMethod.SMR, ccs_attached=True)
        assert c == ColorCode.BLUE

    def test_assess_electrolysis(self):
        result = assess_electrolysis()
        assert isinstance(result, ProductionAssessment)
        assert result.color_code == ColorCode.GREEN
        assert 0.0 < result.efficiency < 1.0
        assert result.h2_rate_mol_per_s > 0

    def test_assess_smr(self):
        result = assess_smr(temperature_k=1100.0)
        assert isinstance(result, ProductionAssessment)
        assert result.color_code == ColorCode.GREY
        assert result.co2_intensity_kg_per_kg_h2 > 0

    def test_production_concept_layers(self):
        layers = production_concept_layers()
        assert len(layers) >= 3


# ── L3 storage ─────────────────────────────────────────────────────────

from hydrogen.storage import (
    assess_compressed_storage,
    assess_liquid_storage,
    boiloff_percent_per_day,
    boiloff_rate_kg_per_day,
    compressed_gas_density_kg_per_m3,
    compression_energy_kwh_per_kg,
    liquefaction_energy_kwh_per_kg,
    metal_hydride_equilibrium_pressure_mpa,
    storage_concept_layers,
)


class TestStorage:
    def test_compressed_density_700bar(self):
        rho = compressed_gas_density_kg_per_m3(70.0, compressibility_z=1.2)
        assert 20 < rho < 50

    def test_compression_energy_positive(self):
        e = compression_energy_kwh_per_kg(70.0)
        assert e > 0

    def test_compression_energy_zero_if_no_compression(self):
        e = compression_energy_kwh_per_kg(0.1)
        assert e == 0.0

    def test_liquefaction_energy(self):
        e = liquefaction_energy_kwh_per_kg()
        assert 10 < e < 20

    def test_boiloff_rate(self):
        rate = boiloff_rate_kg_per_day(50.0, 50.0)
        assert rate > 0

    def test_boiloff_percent(self):
        pct = boiloff_percent_per_day(50.0, 50.0)
        assert 0.0 < pct < 5.0

    def test_metal_hydride_pressure(self):
        p = metal_hydride_equilibrium_pressure_mpa(350.0)
        assert p > 0

    def test_metal_hydride_increases_with_temp(self):
        p300 = metal_hydride_equilibrium_pressure_mpa(300.0)
        p400 = metal_hydride_equilibrium_pressure_mpa(400.0)
        assert p400 > p300

    def test_assess_compressed(self):
        result = assess_compressed_storage()
        assert isinstance(result, StorageAssessment)
        assert result.boiloff_rate_percent_per_day == 0.0

    def test_assess_liquid(self):
        result = assess_liquid_storage()
        assert isinstance(result, StorageAssessment)
        assert result.boiloff_rate_percent_per_day > 0

    def test_storage_concept_layers(self):
        layers = storage_concept_layers()
        assert len(layers) >= 3


# ── L4 fuel_cell ───────────────────────────────────────────────────────

from hydrogen.fuel_cell import (
    assess_fuel_cell,
    electric_efficiency,
    fuel_cell_concept_layers,
    nernst_ocv,
    power_density_w_per_cm2,
    thermodynamic_efficiency_limit,
    voltage_efficiency,
)


class TestFuelCell:
    def test_nernst_ocv_standard(self):
        e = nernst_ocv(298.15, 1.0, 0.21, 1.0)
        assert 1.1 < e < 1.3

    def test_nernst_higher_p_h2(self):
        e_low = nernst_ocv(298.15, 1.0, 0.21, 1.0)
        e_high = nernst_ocv(298.15, 3.0, 0.21, 1.0)
        assert e_high > e_low

    def test_thermo_limit(self):
        eta = thermodynamic_efficiency_limit(298.15)
        assert 0.80 < eta < 0.86

    def test_voltage_efficiency(self):
        ve = voltage_efficiency(0.65)
        assert 0.3 < ve < 0.6

    def test_electric_efficiency(self):
        ee = electric_efficiency(0.65, 0.95)
        assert 0.0 < ee < 1.0

    def test_power_density(self):
        p = power_density_w_per_cm2(0.65, 1.0)
        assert abs(p - 0.65) < 0.01

    def test_assess_pemfc(self):
        result = assess_fuel_cell(FuelCellType.PEMFC)
        assert isinstance(result, FuelCellAssessment)
        assert result.operating_temperature_k < 400

    def test_assess_sofc(self):
        result = assess_fuel_cell(FuelCellType.SOFC)
        assert result.operating_temperature_k > 900
        assert result.efficiency_total >= result.efficiency_electric

    def test_assess_afc(self):
        result = assess_fuel_cell(FuelCellType.AFC)
        assert isinstance(result, FuelCellAssessment)

    def test_fuel_cell_concept_layers(self):
        layers = fuel_cell_concept_layers()
        assert len(layers) >= 3


# ── L5 safety ──────────────────────────────────────────────────────────

from hydrogen.safety import (
    assess_safety,
    embrittlement_risk_level,
    explosion_overpressure_kpa,
    is_within_flammable_range,
    required_ventilation_m3_per_s,
    safety_concept_layers,
)


class TestSafety:
    def test_flammable_range_inside(self):
        assert is_within_flammable_range(30.0)

    def test_flammable_range_below(self):
        assert not is_within_flammable_range(2.0)

    def test_flammable_range_above(self):
        assert not is_within_flammable_range(80.0)

    def test_ventilation(self):
        q = required_ventilation_m3_per_s(1.0, 1.0)
        assert q > 0

    def test_embrittlement_high(self):
        assert embrittlement_risk_level(1000.0, 50.0) == "high"

    def test_embrittlement_low(self):
        assert embrittlement_risk_level(300.0, 5.0) == "low"

    def test_explosion(self):
        op = explosion_overpressure_kpa(5.0, 50.0)
        assert op > 0

    def test_assess_safety_acceptable(self):
        result = assess_safety(1.0, 0.0, 1.0)
        assert result.risk_level == "acceptable"

    def test_assess_safety_flammable(self):
        result = assess_safety(10.0, 0.5, 0.0)
        assert result.risk_level in ("marginal", "unacceptable")

    def test_safety_concept_layers(self):
        layers = safety_concept_layers()
        assert len(layers) >= 3


# ── L6 screening ───────────────────────────────────────────────────────

from hydrogen.screening import screen_hydrogen_claim, screening_concept_layers


class TestScreening:
    def test_clean_claim(self):
        payload = HydrogenClaimPayload(claim_text="Green H₂ at $3/kg via PEM")
        result = screen_hydrogen_claim(payload)
        assert result.verdict == Verdict.POSITIVE

    def test_over_unity_claim(self):
        payload = HydrogenClaimPayload(
            claim_text="Free energy hydrogen",
            claimed_efficiency=1.5,
        )
        result = screen_hydrogen_claim(payload)
        assert result.verdict == Verdict.NEGATIVE
        assert "thermodynamics_violation" in result.flags

    def test_impossible_cost(self):
        payload = HydrogenClaimPayload(
            claim_text="H₂ at $0.10/kg",
            claimed_cost_usd_per_kg=0.10,
        )
        result = screen_hydrogen_claim(payload)
        assert "impossible_cost" in result.flags
        assert result.verdict in (Verdict.CAUTIOUS, Verdict.NEGATIVE)

    def test_perpetual_flag(self):
        payload = HydrogenClaimPayload(
            claim_text="Self-sustaining H₂ loop",
            tags=["perpetual"],
        )
        result = screen_hydrogen_claim(payload)
        assert "perpetual_hydrogen" in result.flags

    def test_safety_ignored_flag(self):
        payload = HydrogenClaimPayload(
            claim_text="H₂ is perfectly safe",
            tags=["safety_ignored"],
        )
        result = screen_hydrogen_claim(payload)
        assert "safety_handwave" in result.flags

    def test_screening_concept_layers(self):
        layers = screening_concept_layers()
        assert len(layers) >= 1


# ── L7 extension hooks ────────────────────────────────────────────────

from hydrogen.extension_hooks import (
    FUTURE_TAGS,
    SIBLING_BRIDGES,
    extension_hooks_concept_layers,
)


class TestExtensionHooks:
    def test_sibling_bridges_count(self):
        assert len(SIBLING_BRIDGES) >= 9

    def test_future_tags(self):
        assert len(FUTURE_TAGS) >= 10

    def test_vectorspace_bridge(self):
        assert "VectorSpace_102" in SIBLING_BRIDGES

    def test_concept_layers(self):
        layers = extension_hooks_concept_layers()
        assert len(layers) >= 2


# ── Domain: space ──────────────────────────────────────────────────────

from hydrogen.domain_space import (
    isru_water_electrolysis_power_kw,
    lox_lh2_specific_impulse_s,
    space_concept_layers,
)


class TestDomainSpace:
    def test_isp_default(self):
        isp = lox_lh2_specific_impulse_s()
        assert 420 < isp < 470

    def test_isru_power(self):
        p = isru_water_electrolysis_power_kw(1.0)
        assert p > 0

    def test_concept_layers(self):
        layers = space_concept_layers()
        assert len(layers) >= 3


# ── Domain: grid ───────────────────────────────────────────────────────

from hydrogen.domain_grid import (
    grid_concept_layers,
    levelised_cost_of_hydrogen_usd_per_kg,
    round_trip_efficiency_p2g,
)


class TestDomainGrid:
    def test_rte_default(self):
        rte = round_trip_efficiency_p2g()
        assert 0.25 < rte < 0.40

    def test_lcoh_reasonable(self):
        lcoh = levelised_cost_of_hydrogen_usd_per_kg()
        assert 1.0 < lcoh < 20.0

    def test_concept_layers(self):
        layers = grid_concept_layers()
        assert len(layers) >= 2


# ── Domain: transport ──────────────────────────────────────────────────

from hydrogen.domain_transport import (
    fcev_range_km,
    h2_cost_per_100km,
    refuelling_time_min,
    transport_concept_layers,
)


class TestDomainTransport:
    def test_fcev_range(self):
        r = fcev_range_km(5.6, 0.50, 20.0)
        assert 400 < r < 600

    def test_refuelling_time(self):
        t = refuelling_time_min(5.6, 1.8)
        assert 2.0 < t < 5.0

    def test_cost_per_100km(self):
        c = h2_cost_per_100km(10.0, 0.50, 20.0)
        assert c > 0

    def test_concept_layers(self):
        layers = transport_concept_layers()
        assert len(layers) >= 2


# ── Foundation integration ─────────────────────────────────────────────

from hydrogen.foundation import (
    collect_concept_layers,
    compute_health,
    run_hydrogen_foundation,
)


class TestFoundation:
    def test_collect_concept_layers(self):
        layers = collect_concept_layers()
        assert len(layers) >= 15
        assert all(isinstance(l, ConceptLayer) for l in layers)

    def test_compute_health_stable(self):
        h = compute_health(0.65, 0.85, 0.50, True, 5.0)
        assert isinstance(h, HydrogenHealthReport)
        assert h.verdict in (HealthVerdict.HEALTHY, HealthVerdict.STABLE)

    def test_compute_health_critical(self):
        h = compute_health(0.10, 0.10, 0.05, False, 50.0)
        assert h.verdict in (HealthVerdict.FRAGILE, HealthVerdict.CRITICAL)

    def test_compute_health_cold_audit_warning(self):
        h = compute_health(0.99, 0.99, 0.99, True, 0.01, omega_safety_override=0.95)
        assert any("0.90" in w for w in h.warnings)

    def test_run_foundation_basic(self):
        report = run_hydrogen_foundation()
        assert isinstance(report, HydrogenFoundationReport)
        assert report.production is not None
        assert report.storage is not None
        assert report.fuel_cell is not None
        assert report.safety is not None
        assert report.health is not None
        assert len(report.concept_layers) >= 15

    def test_run_foundation_with_claim(self):
        claim = HydrogenClaimPayload(claim_text="H₂ at $2/kg")
        report = run_hydrogen_foundation(claim=claim)
        assert report.screening is not None

    def test_run_foundation_liquid_storage(self):
        report = run_hydrogen_foundation(storage_type="liquid")
        assert report.storage.method == StorageMethod.LIQUID

    def test_run_foundation_sofc(self):
        report = run_hydrogen_foundation(fuel_cell_type=FuelCellType.SOFC)
        assert report.fuel_cell.cell_type == FuelCellType.SOFC


# ── Package integrity ──────────────────────────────────────────────────

import hydrogen


class TestPackageIntegrity:
    def test_version(self):
        assert hydrogen.__version__ == "0.1.0"

    def test_public_api(self):
        names = [
            "run_hydrogen_foundation",
            "collect_concept_layers",
            "compute_health",
            "ProductionMethod",
            "StorageMethod",
            "FuelCellType",
            "Verdict",
            "HealthVerdict",
            "ColorCode",
        ]
        for name in names:
            assert hasattr(hydrogen, name), f"Missing public API: {name}"

    def test_core_modules_exist(self):
        from hydrogen import constants, contracts, properties, production
        from hydrogen import storage, fuel_cell, safety, screening
        from hydrogen import foundation, extension_hooks
        from hydrogen import domain_space, domain_grid, domain_transport

    def test_contracts_has_required_classes(self):
        expected = [
            "ProductionAssessment",
            "StorageAssessment",
            "FuelCellAssessment",
            "SafetyAssessment",
            "HydrogenClaimPayload",
            "HydrogenScreeningReport",
            "HydrogenHealthReport",
            "HydrogenFoundationReport",
            "ConceptLayer",
        ]
        from hydrogen import contracts
        for cls_name in expected:
            assert hasattr(contracts, cls_name), f"Missing contract: {cls_name}"
