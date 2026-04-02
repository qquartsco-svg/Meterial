from __future__ import annotations
import radon
from radon.contracts import ClaimPayload
from radon.foundation import run_foundation, screen_claim
def test_version(): assert radon.__version__=='0.1.0'
def test_screening(): assert 'noble_gas_dose_conflation' in screen_claim(ClaimPayload('',claimed_inert_like_neon_no_dose=True)).flags
def test_run(): assert run_foundation().health is not None
