from __future__ import annotations

from element_capture import (
    CaptureMode,
    Species,
    CaptureEnvironment,
    IntakeGeometry,
    SeparationStage,
    StorageStage,
    ElementCaptureAdapter,
    source_loading_kg_m3,
    source_quality_index,
    intake_mass_flow_kg_s,
    species_inflow_kg_s,
    captured_mass_flow_kg_s,
    storage_margin_0_1,
    co2_capture_environment_from_terracore,
    h2_extraction_environment_from_terracore,
    EurusCaptureBridge,
    OrbitalCaptureBridge,
    OceanusCaptureBridge,
    constrain_capture_stack,
    design_capture_service_bus,
    apply_capture_platform_profile,
    apply_satellite_constraints,
    CaptureFrequencyBridge,
    apply_frequency_health_to_capture,
    crew_metabolic_profile,
    snapshot_from_terracore,
    demand_profile_from_snapshot,
    ResourceDemandProfile,
    plan_resource_horizon,
    PowerBudget,
    govern_capture_power,
    assess_waste_loop,
    apply_satellite_thermal_constraints,
    assess_terracore_regeneration,
    assess_habitat_operations,
)


def test_source_loading_positive() -> None:
    env = CaptureEnvironment(
        mode=CaptureMode.ATMOSPHERIC_CAPTURE,
        species=Species.CO2,
        density_kg_m3=1.2,
        bulk_velocity_ms=1.0,
        species_fraction_0_1=0.1,
    )
    assert abs(source_loading_kg_m3(env) - 0.12) < 1e-9


def test_source_quality_bounds() -> None:
    env = CaptureEnvironment(
        mode=CaptureMode.CRYOGENIC_SEPARATION,
        species=Species.HE,
        density_kg_m3=2.0,
        bulk_velocity_ms=1.0,
        species_fraction_0_1=0.05,
        collection_accessibility_0_1=0.8,
        energetic_cost_index=0.9,
    )
    score = source_quality_index(env)
    assert 0.0 <= score <= 1.0


def test_intake_mass_flow_formula() -> None:
    env = CaptureEnvironment(
        mode=CaptureMode.ATMOSPHERIC_CAPTURE,
        species=Species.CO2,
        density_kg_m3=1.0,
        bulk_velocity_ms=3.0,
        species_fraction_0_1=0.5,
    )
    intake = IntakeGeometry(area_m2=2.0, intake_efficiency_0_1=0.5)
    assert abs(intake_mass_flow_kg_s(env, intake) - 3.0) < 1e-9


def test_species_inflow_applies_fraction() -> None:
    env = CaptureEnvironment(
        mode=CaptureMode.ATMOSPHERIC_CAPTURE,
        species=Species.CO2,
        density_kg_m3=1.0,
        bulk_velocity_ms=4.0,
        species_fraction_0_1=0.25,
    )
    intake = IntakeGeometry(area_m2=2.0)
    assert abs(species_inflow_kg_s(env, intake) - 2.0) < 1e-9


def test_capture_rate_applies_efficiency_and_accessibility() -> None:
    env = CaptureEnvironment(
        mode=CaptureMode.ATMOSPHERIC_CAPTURE,
        species=Species.CO2,
        density_kg_m3=1.0,
        bulk_velocity_ms=4.0,
        species_fraction_0_1=0.25,
        collection_accessibility_0_1=0.5,
    )
    intake = IntakeGeometry(area_m2=2.0)
    sep = SeparationStage(recovery_efficiency_0_1=0.5, selectivity_0_1=0.8)
    assert abs(captured_mass_flow_kg_s(env, intake, sep) - 0.4) < 1e-9


def test_storage_margin() -> None:
    storage = StorageStage(capacity_kg=100.0, stored_mass_kg=25.0)
    assert abs(storage_margin_0_1(storage) - 0.75) < 1e-9


def test_adapter_returns_positive_h2_extraction() -> None:
    adapter = ElementCaptureAdapter()
    report = adapter.assess(
        environment=CaptureEnvironment(
            mode=CaptureMode.ELECTROCHEMICAL_EXTRACTION,
            species=Species.H2,
            density_kg_m3=1000.0,
            bulk_velocity_ms=0.01,
            species_fraction_0_1=0.111,
            collection_accessibility_0_1=0.95,
            energetic_cost_index=0.7,
        ),
        intake=IntakeGeometry(area_m2=1.0),
        separation=SeparationStage(recovery_efficiency_0_1=0.85, process_power_w=5000.0),
        storage=StorageStage(capacity_kg=20.0, stored_mass_kg=2.0, storage_efficiency_0_1=0.98),
    )
    assert report.net_capture_rate_kg_s > 0.0
    assert report.capture_possible
    assert 0.0 <= report.omega_capture <= 1.0


def test_adapter_flags_low_source_quality_for_orbital_skimming() -> None:
    adapter = ElementCaptureAdapter()
    report = adapter.assess(
        environment=CaptureEnvironment(
            mode=CaptureMode.ORBITAL_SKIMMING,
            species=Species.HE,
            density_kg_m3=1e-10,
            bulk_velocity_ms=7600.0,
            species_fraction_0_1=1e-6,
            collection_accessibility_0_1=0.1,
            energetic_cost_index=5.0,
        ),
        intake=IntakeGeometry(area_m2=5.0),
        separation=SeparationStage(recovery_efficiency_0_1=0.4, process_power_w=1000.0),
        storage=StorageStage(capacity_kg=5.0, stored_mass_kg=0.0),
    )
    assert report.health.source_quality_0_1 < 0.35
    assert "source_quality_low" in report.health.notes
    assert report.orbital_yield_per_pass_kg >= 0.0
    assert 0.0 <= report.drag_penalty_proxy_0_1 <= 1.0
    assert not report.capture_possible


def test_capture_impossible_when_storage_full() -> None:
    adapter = ElementCaptureAdapter()
    report = adapter.assess(
        environment=CaptureEnvironment(
            mode=CaptureMode.CRYOGENIC_SEPARATION,
            species=Species.HE,
            density_kg_m3=2.0,
            bulk_velocity_ms=1.0,
            species_fraction_0_1=0.05,
        ),
        intake=IntakeGeometry(area_m2=10.0),
        separation=SeparationStage(recovery_efficiency_0_1=0.8),
        storage=StorageStage(capacity_kg=5.0, stored_mass_kg=5.0),
    )
    assert not report.capture_possible


def test_environment_validation_rejects_bad_fraction() -> None:
    try:
        CaptureEnvironment(
            mode=CaptureMode.ATMOSPHERIC_CAPTURE,
            species=Species.CO2,
            density_kg_m3=1.0,
            bulk_velocity_ms=1.0,
            species_fraction_0_1=1.2,
        )
    except ValueError:
        return
    assert False, "Expected ValueError"


def test_terracore_co2_bridge() -> None:
    env = co2_capture_environment_from_terracore(
        {"total_pressure_pa": 100000.0, "co2_partial_pa": 50.0, "temperature_k": 300.0}
    )
    assert env.mode is CaptureMode.ATMOSPHERIC_CAPTURE
    assert env.species is Species.CO2
    assert env.species_fraction_0_1 > 0.0


def test_terracore_h2_bridge() -> None:
    env = h2_extraction_environment_from_terracore(
        {"electrolysis_rate_mol_s": 100.0, "h2_produced_mol_s": 50.0, "power_consumed_mw": 1.0}
    )
    assert env.mode is CaptureMode.ELECTROCHEMICAL_EXTRACTION
    assert env.species is Species.H2
    assert env.species_fraction_0_1 > 0.0


def test_eurus_capture_bridge() -> None:
    bridge = EurusCaptureBridge()
    env = bridge.atmosphere_capture_environment(altitude_m=1000.0)
    assert env.mode is CaptureMode.ATMOSPHERIC_CAPTURE
    assert env.pressure_pa is not None
    assert env.temperature_k is not None
    assert env.density_kg_m3 > 0.0


def test_orbital_capture_bridge() -> None:
    bridge = OrbitalCaptureBridge()
    env = bridge.orbital_skimming_environment(
        altitude_m=180000.0,
        velocity_ms=7800.0,
        residence_time_s=120.0,
        platform_mass_kg=1000.0,
    )
    assert env.mode is CaptureMode.ORBITAL_SKIMMING
    assert env.bulk_velocity_ms == 7800.0
    assert env.residence_time_s == 120.0
    assert env.density_kg_m3 >= 0.0


def test_oceanus_dissolved_bridge() -> None:
    bridge = OceanusCaptureBridge()
    env = bridge.dissolved_co2_environment(
        {
            "rho_kg_m3": 1028.0,
            "u_ms": 0.4,
            "v_ms": 0.3,
            "S_psu": 36.0,
            "T_k": 286.0,
            "p_bottom_pa": 2.0e6,
            "water_column_m": 120.0,
        }
    )
    assert env.mode is CaptureMode.DISSOLVED_EXTRACTION
    assert env.species is Species.CO2
    assert env.species_fraction_0_1 > 0.0


def test_satellite_constraints_reduce_capture_when_budget_small() -> None:
    class Eps:
        solar_panel_area_m2 = 1.0
        generated_power_w = 150.0

    class Mission:
        power_req_w = 140.0

    class Structure:
        total_mass_kg = 50.0
        mass_margin_ratio = 0.02

    class Blueprint:
        eps = Eps()
        mission = Mission()
        structure = Structure()

    intake = IntakeGeometry(area_m2=10.0)
    separation = SeparationStage(recovery_efficiency_0_1=0.8, process_power_w=500.0)
    storage = StorageStage(capacity_kg=20.0, stored_mass_kg=2.0, compression_power_w=100.0)
    constrained_intake, constrained_separation, constrained_storage, evidence = constrain_capture_stack(
        Blueprint(),
        intake=intake,
        separation=separation,
        storage=storage,
    )
    assessment = ElementCaptureAdapter().assess(
        environment=CaptureEnvironment(
            mode=CaptureMode.ATMOSPHERIC_CAPTURE,
            species=Species.CO2,
            density_kg_m3=1.225,
            bulk_velocity_ms=2.0,
            species_fraction_0_1=420e-6,
        ),
        intake=constrained_intake,
        separation=constrained_separation,
        storage=constrained_storage,
    )
    constrained = apply_satellite_constraints(assessment, constraint_evidence=evidence)
    assert constrained.evidence["platform_power_surplus_w"] == 10.0
    assert constrained.evidence["platform_mass_budget_exhausted"] == "false"
    assert constrained.intake.area_m2 < intake.area_m2
    assert not constrained.capture_possible


def test_satellite_constraints_flag_locked_storage_when_mass_budget_empty() -> None:
    class Eps:
        solar_panel_area_m2 = 1.0
        generated_power_w = 250.0

    class Mission:
        power_req_w = 100.0

    class Structure:
        total_mass_kg = 50.0
        mass_margin_ratio = -0.01

    class Blueprint:
        eps = Eps()
        mission = Mission()
        structure = Structure()

    _, _, constrained_storage, evidence = constrain_capture_stack(
        Blueprint(),
        intake=IntakeGeometry(area_m2=1.0),
        separation=SeparationStage(recovery_efficiency_0_1=0.8, process_power_w=20.0),
        storage=StorageStage(capacity_kg=5.0, stored_mass_kg=0.4, compression_power_w=10.0),
    )
    assert evidence["platform_mass_budget_exhausted"] == "true"
    assert evidence["platform_storage_locked"] == "true"
    assert constrained_storage.capacity_kg == 0.4


def test_capture_service_bus_can_unlock_storage_budget() -> None:
    class Blueprint:
        pass

    intake, separation, storage, evidence = design_capture_service_bus(
        Blueprint(),
        intake=IntakeGeometry(area_m2=1.2),
        separation=SeparationStage(recovery_efficiency_0_1=0.82, process_power_w=90.0),
        storage=StorageStage(capacity_kg=4.0, stored_mass_kg=0.3, compression_power_w=18.0),
        dedicated_power_w=400.0,
        collector_area_m2=2.5,
        payload_mass_allowance_kg=12.0,
        thermal_storage_scale_0_1=0.7,
    )
    assessment = ElementCaptureAdapter().assess(
        environment=CaptureEnvironment(
            mode=CaptureMode.ATMOSPHERIC_CAPTURE,
            species=Species.CO2,
            density_kg_m3=1.225,
            bulk_velocity_ms=1.5,
            species_fraction_0_1=600e-6,
            collection_accessibility_0_1=0.9,
            energetic_cost_index=0.5,
        ),
        intake=intake,
        separation=separation,
        storage=storage,
    )
    constrained = apply_satellite_constraints(assessment, constraint_evidence=evidence)
    assert evidence["service_bus_mode"] == "capture_optimized"
    assert evidence["platform_storage_locked"] == "false"
    assert constrained.capture_possible is True


def test_apply_capture_platform_profile_respects_profile_contract() -> None:
    class Profile:
        mode = "capture_service_bus"
        satellite_class = "smallsat"
        dedicated_power_w = 300.0
        collector_area_m2 = 2.0
        payload_mass_allowance_kg = 10.0
        thermal_storage_scale_0_1 = 0.6
        recommendation = "allocate dedicated recovery bay"

    intake, separation, storage, evidence = apply_capture_platform_profile(
        Profile(),
        intake=IntakeGeometry(area_m2=1.5),
        separation=SeparationStage(recovery_efficiency_0_1=0.8, process_power_w=90.0),
        storage=StorageStage(capacity_kg=4.0, stored_mass_kg=0.3, compression_power_w=18.0),
    )
    assert evidence["service_bus_mode"] == "capture_service_bus"
    assert evidence["service_bus_satellite_class"] == "smallsat"
    assert evidence["service_bus_recommendation"] == "allocate dedicated recovery bay"
    assert intake.area_m2 > 0.0
    assert storage.capacity_kg > 0.3


def test_orbital_capture_operations_report_positive_for_viable_vleo_case() -> None:
    bridge = OrbitalCaptureBridge()
    env = bridge.orbital_skimming_environment(
        altitude_m=180_000.0,
        velocity_ms=7_800.0,
        species=Species.O2,
        species_fraction_0_1=0.2,
        collection_accessibility_0_1=0.6,
        energetic_cost_index=2.0,
        residence_time_s=120.0,
        platform_mass_kg=500.0,
    )
    assessment = ElementCaptureAdapter().assess(
        environment=env,
        intake=IntakeGeometry(area_m2=1.5),
        separation=SeparationStage(recovery_efficiency_0_1=0.82, process_power_w=90.0),
        storage=StorageStage(capacity_kg=4.0, stored_mass_kg=0.3, compression_power_w=18.0),
    )
    ops = bridge.assess_capture_operations(
        assessment=assessment,
        altitude_m=180_000.0,
        inclination_deg=51.6,
        delta_v_remaining_ms=180.0,
        mass_kg=500.0,
        area_m2=1.5,
    )
    assert ops.orbits_per_day > 0.0
    assert ops.daily_capture_kg > 0.0
    assert 0.0 <= ops.endurance_score_0_1 <= 1.0


def test_frequency_health_bridge_modifies_capture_health() -> None:
    assessment = ElementCaptureAdapter().assess(
        environment=CaptureEnvironment(
            mode=CaptureMode.ATMOSPHERIC_CAPTURE,
            species=Species.CO2,
            density_kg_m3=1.225,
            bulk_velocity_ms=2.0,
            species_fraction_0_1=420e-6,
        ),
        intake=IntakeGeometry(area_m2=10.0),
        separation=SeparationStage(recovery_efficiency_0_1=0.85, process_power_w=100.0),
        storage=StorageStage(capacity_kg=10.0, stored_mass_kg=1.0),
    )

    class Signal:
        def __init__(self, pump_rpm: float, membrane_dp: float, compressor_vibration: float) -> None:
            self.pump_rpm = pump_rpm
            self.membrane_dp = membrane_dp
            self.compressor_vibration = compressor_vibration

    bridge = CaptureFrequencyBridge(sample_rate_hz=100.0)
    for i in range(64):
        bridge.push(Signal(3000.0, 1.0, 0.02 if i % 2 == 0 else -0.02))
    freq_health = bridge.health("compressor_vibration")
    updated = apply_frequency_health_to_capture(assessment, machinery_health=freq_health)
    assert freq_health is not None
    assert "machinery_omega_freq" in updated.evidence
    assert updated.health.machinery_health_0_1 == updated.evidence["machinery_omega_freq"]


def test_life_support_snapshot_and_demand_profile() -> None:
    snap = snapshot_from_terracore(
        atmosphere={"co2_ppm": 1500.0, "o2_fraction": 0.209},
        hydrosphere={"water_margin": 0.8, "h2_produced_mol_s": 0.02, "o2_from_water_mol_s": 0.01},
        crew_count=4,
    )
    demand = demand_profile_from_snapshot(snap)
    assert snap.crew_count == 4
    assert demand.co2_scrub_demand_kg_day > 0.0
    assert demand.o2_support_demand_kg_day > 0.0
    assert demand.water_recovery_demand_kg_day > 0.0


def test_life_support_snapshot_respects_metabolic_profile() -> None:
    profile = crew_metabolic_profile("eva_recovery")
    snap = snapshot_from_terracore(
        atmosphere={"co2_ppm": 2200.0, "o2_fraction": 0.205},
        hydrosphere={"water_margin": 0.6, "h2_produced_mol_s": 0.01, "o2_from_water_mol_s": 0.01},
        crew_count=4,
        metabolic_profile=profile,
    )
    nominal = snapshot_from_terracore(
        atmosphere={"co2_ppm": 2200.0, "o2_fraction": 0.205},
        hydrosphere={"water_margin": 0.6, "h2_produced_mol_s": 0.01, "o2_from_water_mol_s": 0.01},
        crew_count=4,
    )
    assert snap.crew_co2_output_mol_s > nominal.crew_co2_output_mol_s
    assert snap.crew_water_consumption_mol_s > nominal.crew_water_consumption_mol_s


def test_resource_planning_horizon() -> None:
    assessment = ElementCaptureAdapter().assess(
        environment=CaptureEnvironment(
            mode=CaptureMode.ATMOSPHERIC_CAPTURE,
            species=Species.CO2,
            density_kg_m3=1.225,
            bulk_velocity_ms=2.5,
            species_fraction_0_1=0.002,
        ),
        intake=IntakeGeometry(area_m2=6.0),
        separation=SeparationStage(recovery_efficiency_0_1=0.85, process_power_w=200.0),
        storage=StorageStage(capacity_kg=20.0, stored_mass_kg=3.0, storage_efficiency_0_1=0.98),
    )
    plan = plan_resource_horizon(
        assessment,
        ResourceDemandProfile(
            species="co2",
            daily_demand_kg=1.0,
            current_inventory_kg=4.0,
            target_buffer_days=3.0,
        ),
    )
    assert plan.daily_capture_kg > 0.0
    assert plan.inventory_horizon_days > 0.0
    assert isinstance(plan.recommendation, str)


def test_power_governance_derates_capture() -> None:
    assessment = ElementCaptureAdapter().assess(
        environment=CaptureEnvironment(
            mode=CaptureMode.ATMOSPHERIC_CAPTURE,
            species=Species.CO2,
            density_kg_m3=1.225,
            bulk_velocity_ms=2.0,
            species_fraction_0_1=0.001,
        ),
        intake=IntakeGeometry(area_m2=4.0),
        separation=SeparationStage(recovery_efficiency_0_1=0.8, process_power_w=1000.0),
        storage=StorageStage(capacity_kg=10.0, stored_mass_kg=1.0, compression_power_w=200.0),
    )
    report = govern_capture_power(
        assessment,
        PowerBudget(
            generation_w=1500.0,
            habitat_load_w=900.0,
            propulsion_reserve_w=300.0,
            research_load_w=100.0,
        ),
    )
    assert report.available_for_capture_w == 200.0
    assert report.capture_power_scale_0_1 < 1.0
    assert report.capture_allowed is False


def test_waste_loop_reports_byproduct() -> None:
    assessment = ElementCaptureAdapter().assess(
        environment=CaptureEnvironment(
            mode=CaptureMode.ELECTROCHEMICAL_EXTRACTION,
            species=Species.H2,
            density_kg_m3=1000.0,
            bulk_velocity_ms=0.01,
            species_fraction_0_1=0.111,
        ),
        intake=IntakeGeometry(area_m2=2.0),
        separation=SeparationStage(recovery_efficiency_0_1=0.85, process_power_w=100.0),
        storage=StorageStage(capacity_kg=20.0, stored_mass_kg=1.0),
    )
    report = assess_waste_loop(assessment)
    assert report.byproduct_species == "o2"
    assert report.byproduct_kg_day > report.recovered_kg_day


def test_satellite_thermal_constraints_scale_storage() -> None:
    class Thermal:
        heater_power_w = 20.0
        radiator_area_m2 = 0.5
        is_thermally_viable = True
        thermal_margin_hot_c = 10.0
        thermal_margin_cold_c = -10.0

    class Blueprint:
        thermal = Thermal()

    storage = StorageStage(capacity_kg=20.0, stored_mass_kg=2.0, compression_power_w=100.0)
    adjusted, evidence = apply_satellite_thermal_constraints(Blueprint(), storage=storage)
    assert adjusted.capacity_kg < storage.capacity_kg
    assert adjusted.compression_power_w > storage.compression_power_w
    assert "thermal_storage_scale_0_1" in evidence


def test_terracore_regeneration_report_positive() -> None:
    report = assess_terracore_regeneration(
        atmosphere={"co2_ppm": 1800.0, "o2_fraction": 0.208},
        hydrosphere={"water_margin": 0.72, "h2_produced_mol_s": 0.015, "o2_from_water_mol_s": 0.0075},
        biosphere={"co2_uptake_mol_s": 0.01},
    )
    assert report.recoverable_water_kg_day > 0.0
    assert report.recoverable_o2_kg_day > 0.0
    assert 0.0 <= report.closure_gain_0_1 <= 1.0


def test_habitat_operations_prioritizes_actions() -> None:
    snap = snapshot_from_terracore(
        atmosphere={"co2_ppm": 2400.0, "o2_fraction": 0.185},
        hydrosphere={"water_margin": 0.3, "h2_produced_mol_s": 0.01, "o2_from_water_mol_s": 0.005},
        crew_count=6,
    )
    demand = demand_profile_from_snapshot(snap)
    assessment = ElementCaptureAdapter().assess(
        environment=CaptureEnvironment(
            mode=CaptureMode.ATMOSPHERIC_CAPTURE,
            species=Species.CO2,
            density_kg_m3=1.225,
            bulk_velocity_ms=1.5,
            species_fraction_0_1=0.001,
        ),
        intake=IntakeGeometry(area_m2=2.0),
        separation=SeparationStage(recovery_efficiency_0_1=0.7, process_power_w=200.0),
        storage=StorageStage(capacity_kg=5.0, stored_mass_kg=1.0),
    )
    plan = plan_resource_horizon(
        assessment,
        ResourceDemandProfile(species="co2", daily_demand_kg=demand.co2_scrub_demand_kg_day, current_inventory_kg=1.0),
    )
    power = govern_capture_power(
        assessment,
        PowerBudget(generation_w=900.0, habitat_load_w=700.0, propulsion_reserve_w=150.0, research_load_w=80.0),
    )
    regen = assess_terracore_regeneration(
        atmosphere={"co2_ppm": 2400.0, "o2_fraction": 0.185},
        hydrosphere={"water_margin": 0.3, "h2_produced_mol_s": 0.01, "o2_from_water_mol_s": 0.005},
        biosphere={"co2_uptake_mol_s": 0.001},
    )
    ops = assess_habitat_operations(
        life_support=snap,
        demand=demand,
        co2_plan=plan,
        power=power,
        regeneration=regen,
    )
    assert ops.priority in {"stabilize", "survival", "optimize"}
    assert len(ops.actions) > 0
