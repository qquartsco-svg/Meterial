from __future__ import annotations

import al_ti
from al_ti.contracts import AlTiClaimPayload
from al_ti.foundation import assess_materials, assess_process, run_al_ti_foundation, screen_al_ti_claim


def test_version():
    assert al_ti.__version__ == "0.1.0"


def test_material_strength():
    m = assess_materials()
    assert m.ti_strength_mpa > m.al_strength_mpa


def test_process_energy():
    p = assess_process()
    assert p.ti_energy_kwh_per_kg > p.al_energy_kwh_per_kg


def test_screening():
    s = screen_al_ti_claim(AlTiClaimPayload("", claimed_no_galvanic_corrosion=True))
    assert "galvanic_denial" in s.flags


def test_run():
    r = run_al_ti_foundation()
    assert r.material and r.process and r.health
