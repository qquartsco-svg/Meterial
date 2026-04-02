from __future__ import annotations

import iron
from iron.contracts import IronClaimPayload, ProcessMethod
from iron.foundation import assess_corrosion, assess_process, collect_concept_layers, run_iron_foundation, screen_iron_claim


def test_version():
    assert iron.__version__ == "0.1.0"


def test_process_dri_vs_bf():
    bf = assess_process(ProcessMethod.BLAST_FURNACE)
    dr = assess_process(ProcessMethod.DRI_EAF)
    assert dr.co2_intensity_kg_per_ton_steel < bf.co2_intensity_kg_per_ton_steel


def test_corrosion_positive():
    c = assess_corrosion(1.5)
    assert c.corrosion_rate_mm_per_year > 0


def test_screening_corrosion_denial():
    s = screen_iron_claim(IronClaimPayload("", claimed_zero_corrosion=True))
    assert "corrosion_denial" in s.flags


def test_collect_layers():
    assert len(collect_concept_layers()) >= 2


def test_run():
    r = run_iron_foundation()
    assert r.process is not None and r.corrosion is not None and r.health is not None
