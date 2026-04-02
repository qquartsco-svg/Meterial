from __future__ import annotations
import am_cm
from am_cm.contracts import ClaimPayload
from am_cm.foundation import run_foundation, screen_claim
def test_version(): assert am_cm.__version__=='0.1.0'
def test_screening(): assert 'governance_denial' in screen_claim(ClaimPayload('',claimed_trivial_handling_no_governance=True)).flags
def test_run(): assert run_foundation().health is not None
