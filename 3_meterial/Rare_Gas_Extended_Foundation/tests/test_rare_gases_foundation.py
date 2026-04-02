from __future__ import annotations
import rare_gases
from rare_gases.contracts import ClaimPayload
from rare_gases.foundation import run_foundation, screen_claim
def test_version(): assert rare_gases.__version__=='0.1.0'
def test_screening(): assert 'supply_myth' in screen_claim(ClaimPayload('',claimed_unlimited_supply=True)).flags
def test_run(): assert run_foundation().health is not None
