from __future__ import annotations

import pytest

import helium
from helium.constants import HE_BOILING_POINT_K, HE_DENSITY_KG_PER_M3_STP
from helium.contracts import HeliumClaimPayload, Verdict
from helium.foundation import collect_concept_layers, compute_health, run_helium_foundation
from helium.properties import helium_property_card, ideal_gas_density_kg_per_m3
from helium.sourcing import assess_natural_gas_sourcing, stripping_recovery_fraction
from helium.storage import assess_liquid_storage, boiloff_percent_per_day, compression_energy_kwh_per_kg
from helium.screening import screen_helium_claim
from helium.domain_space import balloon_lift_n_per_m3


def test_version():
    assert helium.__version__ == "0.1.0"


def test_property_card():
    c = helium_property_card()
    assert c.boiling_point_k == HE_BOILING_POINT_K


def test_ideal_gas_density_stp():
    rho = ideal_gas_density_kg_per_m3(298.15, 101_325.0)
    assert abs(rho - HE_DENSITY_KG_PER_M3_STP) < 0.02


def test_ideal_gas_negative_temp():
    with pytest.raises(ValueError):
        ideal_gas_density_kg_per_m3(-1.0, 101_325.0)


def test_stripping_recovery():
    r = stripping_recovery_fraction(0.01)
    assert 0.0 < r <= 1.0


def test_assess_sourcing():
    a = assess_natural_gas_sourcing()
    assert a.method.value == "natural_gas_stripping"


def test_storage_boiloff():
    b = boiloff_percent_per_day(50.0, 0.9, 10.0)
    assert b > 0


def test_compression_energy():
    e = compression_energy_kwh_per_kg(20.0)
    assert e > 0


def test_assess_liquid_storage():
    s = assess_liquid_storage()
    assert s.boiloff_percent_per_day >= 0


def test_screening_clean():
    r = screen_helium_claim(HeliumClaimPayload(claim_text="He from natural gas"))
    assert r.verdict in (Verdict.POSITIVE, Verdict.NEUTRAL)


def test_screening_abundance_myth():
    r = screen_helium_claim(
        HeliumClaimPayload(claim_text="infinite He", claimed_abundance_unlimited=True)
    )
    assert "abundance_myth" in r.flags


def test_balloon_lift():
    lift = balloon_lift_n_per_m3()
    assert lift > 0


def test_collect_layers():
    assert len(collect_concept_layers()) >= 6


def test_compute_health():
    h = compute_health(0.5, 0.85, 0.7, True, 5.0)
    assert h.composite_omega > 0


def test_run_foundation():
    r = run_helium_foundation()
    assert r.sourcing is not None and r.health is not None


def test_run_with_claim():
    r = run_helium_foundation(HeliumClaimPayload(claim_text="test"))
    assert r.screening is not None
