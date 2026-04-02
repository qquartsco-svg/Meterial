# Changelog

## 0.2.0

- harden repository for public GitHub release
- add detailed Korean and English README documents
- add SHA-256 integrity manifest workflow
- add `BLOCKCHAIN_INFO.md`, `BLOCKCHAIN_INFO_EN.md`, `PHAM_BLOCKCHAIN_LOG.md`
- add release scripts:
  - `scripts/generate_signature.py`
  - `scripts/verify_signature.py`
  - `scripts/cleanup_generated.py`
  - `scripts/release_check.py`
- add example smoke tests in `tests/test_examples.py`
- clarify concept, equations, extensibility, current limits, and self-sufficiency framing

## 0.1.6

- add `CaptureOrbitOperationsReport` and `assess_capture_orbit_operations(...)`
- extend `OrbitalCaptureBridge` with orbit-operations endurance assessment
- add `run_capture_orbit_endurance_demo.py`

## 0.1.5

- add `apply_capture_platform_profile(...)` bridge for real `Satellite_Design_Stack` capture platform profiles
- switch platform comparison demo to `capture_service_bus_profile(...)` from `Satellite_Design_Stack`
- add tests for profile-based service bus integration

## 0.1.4

- add `design_capture_service_bus(...)` engineering what-if helper
- add evidence for `mass_budget_exhausted` and `storage_locked` in satellite constraints
- expand platform comparison demo with baseline vs service-bus view

## 0.1.3

- add crew metabolic profiles for more realistic life-support demand modeling
- add platform class comparison demo for capture-stack fit screening

## 0.1.2

- add `habitat_operations` layer for habitat risk and self-sufficiency prioritization
- add realistic `Satellite_Design` blueprint capture demo
- expand README and self-sufficiency documentation for spacecraft operations

## 0.1.1

- add `Oceanus` dissolved CO2 bridge
- add `Satellite_Design` device constraint bridge
- add `FrequencyCore` machinery health bridge
- add spacecraft self-sufficiency demo and documentation
- add `life_support_bridge` and resource horizon planning
- add `power_governance` and `waste_loop` first-pass operating layers

## 0.1.0

- Initial MVP for environment-aware elemental capture and extraction assessment.
- Added support for:
  - atmospheric CO2 capture
  - electrochemical H2 extraction
  - cryogenic He separation
  - orbital skimming feasibility screening
- Added engineering contracts for source quality, intake, separation, storage, and health.
