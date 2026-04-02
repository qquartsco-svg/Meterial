from __future__ import annotations

import mg_ca
from mg_ca.contracts import MgCaClaimPayload
from mg_ca.foundation import assess_alloy, assess_electrolyte, run_mg_ca_foundation, screen_mg_ca_claim


def test_version():
    assert mg_ca.__version__ == "0.1.0"


def test_electrolyte_normal():
    e = assess_electrolyte()
    assert e.risk_level in ("low", "medium")


def test_alloy():
    a = assess_alloy(0.9,0.1)
    assert a.corrosion_risk in ("low","medium")


def test_screening_flag():
    s = screen_mg_ca_claim(MgCaClaimPayload("", claimed_no_electrolyte_risk=True))
    assert "electrolyte_denial" in s.flags


def test_run():
    r = run_mg_ca_foundation()
    assert r.electrolyte and r.alloy and r.health
