from __future__ import annotations

import pytest

import nitrogen
from nitrogen.air_separation import assess_cryogenic_separation, nitrogen_yield_from_air_mol_per_mol_air
from nitrogen.contracts import NitrogenClaimPayload, Verdict
from nitrogen.fixation import assess_fixation, haber_equilibrium_nh3_mole_fraction
from nitrogen.foundation import collect_concept_layers, run_nitrogen_foundation
from nitrogen.properties import ideal_gas_density_kg_per_m3, n2_property_card
from nitrogen.screening import screen_nitrogen_claim
from nitrogen.storage import assess_ln2_storage, boiloff_percent_per_day


def test_version():
    assert nitrogen.__version__ == "0.1.0"


def test_n2_card():
    c = n2_property_card()
    assert c.boiling_point_k > 60


def test_ideal_gas():
    rho = ideal_gas_density_kg_per_m3(298.15, 101_325.0)
    assert 1.1 < rho < 1.3


def test_ideal_gas_bad_temp():
    with pytest.raises(ValueError):
        ideal_gas_density_kg_per_m3(0.0, 101_325.0)


def test_air_yield():
    assert 0.77 < nitrogen_yield_from_air_mol_per_mol_air() < 0.79


def test_haber_pressure_increases_nh3():
    low_p = haber_equilibrium_nh3_mole_fraction(700.0, 50.0)
    high_p = haber_equilibrium_nh3_mole_fraction(700.0, 200.0)
    assert high_p >= low_p


def test_assess_fixation():
    f = assess_fixation()
    assert 0.0 <= f.nh3_equilibrium_mole_fraction <= 0.65


def test_boiloff():
    b = boiloff_percent_per_day(10.0, 0.9, 50.0)
    assert b > 0


def test_screening_free_fertilizer():
    r = screen_nitrogen_claim(NitrogenClaimPayload("free", claimed_free_fertilizer=True))
    assert "energy_ignored" in r.flags


def test_screening_air():
    r = screen_nitrogen_claim(NitrogenClaimPayload("pure N2 air", claimed_air_is_pure_n2=True))
    assert "air_composition_error" in r.flags


def test_collect():
    assert len(collect_concept_layers()) >= 7


def test_run():
    r = run_nitrogen_foundation()
    assert r.separation and r.fixation and r.storage
