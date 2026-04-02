from __future__ import annotations
import beryllium
from beryllium.contracts import ClaimPayload
from beryllium.foundation import run_foundation, screen_claim
def test_version(): assert beryllium.__version__=='0.1.0'
def test_screening(): assert 'respiratory_denial' in screen_claim(ClaimPayload('',claimed_no_respiratory_risk=True)).flags
def test_run(): assert run_foundation().health is not None
