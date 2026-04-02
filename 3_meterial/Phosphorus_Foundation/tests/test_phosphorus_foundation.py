from __future__ import annotations

import phosphorus
from phosphorus.bioenergetics import assess_atp_cycle
from phosphorus.extraction import assess_phosphate_rock
from phosphorus.foundation import collect_concept_layers, run_phosphorus_foundation
from phosphorus.properties import phosphorus_property_card
from phosphorus.screening import screen_phosphorus_claim
from phosphorus.contracts import PhosphorusClaimPayload


def test_version():
    assert phosphorus.__version__ == "0.1.0"


def test_property_card():
    c = phosphorus_property_card()
    assert c.molar_mass_g_per_mol > 30.0


def test_extraction():
    e = assess_phosphate_rock()
    assert e.ore_grade_p2o5_fraction > 0.1


def test_atp_cycle():
    a = assess_atp_cycle()
    assert a.atp_regeneration_required is True


def test_screening():
    r = screen_phosphorus_claim(PhosphorusClaimPayload("", claimed_atp_without_recycling=True))
    assert "atp_cycle_denial" in r.flags


def test_collect_layers():
    assert len(collect_concept_layers()) >= 5


def test_run():
    r = run_phosphorus_foundation()
    assert r.extraction is not None and r.bioenergetics is not None and r.health is not None
