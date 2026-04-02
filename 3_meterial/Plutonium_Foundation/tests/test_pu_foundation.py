from __future__ import annotations
import pu
from pu.contracts import ClaimPayload
from pu.foundation import run_foundation, screen_claim
def test_version(): assert pu.__version__=='0.1.0'
def test_screening(): assert 'criticality_denial' in screen_claim(ClaimPayload('',claimed_no_criticality_engineering=True)).flags
def test_run(): assert run_foundation().health is not None
