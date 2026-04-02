from __future__ import annotations
import ce_la
from ce_la.contracts import ClaimPayload
from ce_la.foundation import run_foundation, screen_claim
def test_version(): assert ce_la.__version__=='0.1.0'
def test_screening(): assert 'deactivation_denial' in screen_claim(ClaimPayload('',claimed_no_deactivation=True)).flags
def test_run(): assert run_foundation().health is not None
