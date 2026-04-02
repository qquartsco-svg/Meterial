from __future__ import annotations

import pytest

import oxygen
from oxygen.contracts import OxygenClaimPayload
from oxygen.foundation import collect_concept_layers, run_oxygen_foundation
from oxygen.production import assess_cryogenic_o2, o2_from_electrolysis_mol_per_s
from oxygen.properties import ideal_gas_density_kg_per_m3, o2_property_card
from oxygen.safety import fire_severity_index
from oxygen.screening import screen_oxygen_claim
from oxygen.storage import assess_lox_storage, boiloff_percent_per_day


def test_version():
    assert oxygen.__version__ == "0.1.0"


def test_o2_card():
    c = o2_property_card()
    assert c.boiling_point_k > 80


def test_ideal_gas():
    rho = ideal_gas_density_kg_per_m3(298.15, 101_325.0)
    assert 1.2 < rho < 1.5


def test_ideal_gas_bad():
    with pytest.raises(ValueError):
        ideal_gas_density_kg_per_m3(0.0, 101_325.0)


def test_electrolysis_stoich():
    assert abs(o2_from_electrolysis_mol_per_s(2.0) - 1.0) < 1e-9


def test_cryo_prod():
    p = assess_cryogenic_o2()
    assert p.purity_o2_fraction > 0.99


def test_boiloff():
    assert boiloff_percent_per_day(20.0, 0.9, 100.0) > 0


def test_fire_severity():
    assert fire_severity_index(21.0) < 0.01
    assert fire_severity_index(100.0) > 0.99


def test_screening_pure_o2():
    r = screen_oxygen_claim(OxygenClaimPayload("", claimed_pure_o2_safe=True))
    assert "oxidiser_handwave" in r.flags


def test_collect():
    assert len(collect_concept_layers()) >= 6


def test_run():
    r = run_oxygen_foundation()
    assert r.production and r.storage and r.health
