from __future__ import annotations
import re_mag
from re_mag.contracts import ClaimPayload
from re_mag.foundation import run_foundation, screen_claim
def test_version(): assert re_mag.__version__=='0.1.0'
def test_screening(): assert 'supply_denial' in screen_claim(ClaimPayload('',claimed_no_supply_risk=True)).flags
def test_run(): assert run_foundation().health is not None
