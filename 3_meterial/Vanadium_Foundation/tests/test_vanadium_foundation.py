from __future__ import annotations
import vanadium
from vanadium.contracts import ClaimPayload
from vanadium.foundation import run_foundation, screen_claim
def test_version(): assert vanadium.__version__=='0.1.0'
def test_screening(): assert 'degradation_denial' in screen_claim(ClaimPayload('',claimed_zero_electrolyte_degradation=True)).flags
def test_run(): assert run_foundation().health is not None
