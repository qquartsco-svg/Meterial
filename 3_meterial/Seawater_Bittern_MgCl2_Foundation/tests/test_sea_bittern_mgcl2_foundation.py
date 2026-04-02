from __future__ import annotations
import sea_bittern_mgcl2
from sea_bittern_mgcl2.contracts import ClaimPayload
from sea_bittern_mgcl2.foundation import run_foundation, screen_claim


def test_version():
    assert sea_bittern_mgcl2.__version__=='0.1.0'


def test_screening():
    r=screen_claim(ClaimPayload('', claimed_bittern_mg_without_energy=True))
    assert 'bittern_energy_denial' in r.flags


def test_run():
    assert run_foundation().health is not None
