from __future__ import annotations

import silicon
from silicon.contracts import DomainMode, SiliconClaimPayload
from silicon.device import assess_logic_device, assess_pv_device
from silicon.foundation import collect_concept_layers, run_silicon_foundation
from silicon.properties import silicon_property_card
from silicon.refining import assess_siemens_refining
from silicon.screening import screen_silicon_claim


def test_version():
    assert silicon.__version__ == "0.1.0"


def test_property_card():
    c = silicon_property_card()
    assert c.bandgap_ev_300k > 1.0


def test_refining():
    r = assess_siemens_refining()
    assert r.purity_six_nines_fraction > 0.99


def test_devices():
    pv = assess_pv_device()
    lg = assess_logic_device()
    assert pv.efficiency_fraction < lg.efficiency_fraction


def test_screening():
    s = screen_silicon_claim(SiliconClaimPayload("", claimed_zero_defects=True))
    assert "defect_free_myth" in s.flags


def test_collect_layers():
    assert len(collect_concept_layers()) >= 5


def test_run():
    r = run_silicon_foundation(domain=DomainMode.PHOTOVOLTAIC)
    assert r.refining is not None and r.device is not None and r.health is not None
