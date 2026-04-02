from __future__ import annotations
import u_th
from u_th.contracts import ClaimPayload
from u_th.foundation import run_foundation, screen_claim
def test_version(): assert u_th.__version__=='0.1.0'
def test_screening(): assert 'waste_denial' in screen_claim(ClaimPayload('',claimed_no_waste_issue=True)).flags
def test_run(): assert run_foundation().health is not None
