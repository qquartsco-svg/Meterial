from __future__ import annotations
import sc_y
from sc_y.contracts import ClaimPayload
from sc_y.foundation import run_foundation, screen_claim
def test_version(): assert sc_y.__version__=='0.1.0'
def test_screening(): assert 'supply_myth' in screen_claim(ClaimPayload('',claimed_trivial_supply=True)).flags
def test_run(): assert run_foundation().health is not None
