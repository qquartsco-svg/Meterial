from __future__ import annotations

import sodium_chlorine
from sodium_chlorine.contracts import NaClClaimPayload
from sodium_chlorine.foundation import assess_chlor_alkali, assess_salt_system, collect_concept_layers, run_sodium_chlorine_foundation, screen_nacl_claim


def test_version():
    assert sodium_chlorine.__version__ == "0.1.0"


def test_chlor_alkali_outputs():
    p = assess_chlor_alkali()
    assert p.cl2_kg_per_ton_brine > 0 and p.naoh_kg_per_ton_brine > 0


def test_salt_system_risk():
    s = assess_salt_system(35.0)
    assert s.corrosion_risk in ("high", "medium")


def test_screening_flags():
    r = screen_nacl_claim(NaClClaimPayload("", claimed_no_corrosion_in_saltwater=True))
    assert "corrosion_denial" in r.flags


def test_collect_layers():
    assert len(collect_concept_layers()) >= 2


def test_run():
    r = run_sodium_chlorine_foundation()
    assert r.process is not None and r.salt_system is not None and r.health is not None
