from __future__ import annotations
import urea_co2
from urea_co2.contracts import ClaimPayload
from urea_co2.foundation import run_foundation, screen_claim
def test_version(): assert urea_co2.__version__=='0.1.0'
def test_screening(): assert 'co2_purity_myth' in screen_claim(ClaimPayload('',claimed_free_pure_co2_anywhere=True)).flags
def test_run(): assert run_foundation().health is not None
