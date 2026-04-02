from __future__ import annotations

from element_capture import (
    assess_co2_dac,
    assess_h2_electrolysis,
    assess_he_cryogenic_separation,
)


def test_assess_co2_dac() -> None:
    report = assess_co2_dac(
        density_kg_m3=1.225,
        bulk_velocity_ms=2.0,
        co2_fraction_0_1=420e-6,
    )
    assert report.capture_possible
    assert report.net_capture_rate_kg_s > 0.0


def test_assess_h2_electrolysis() -> None:
    report = assess_h2_electrolysis()
    assert report.capture_possible
    assert report.omega_capture > 0.0


def test_assess_he_cryogenic_separation() -> None:
    report = assess_he_cryogenic_separation(
        density_kg_m3=2.0,
        bulk_velocity_ms=1.0,
        he_fraction_0_1=0.05,
    )
    assert report.capture_possible
    assert report.net_capture_rate_kg_s > 0.0
