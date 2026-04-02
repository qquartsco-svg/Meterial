from __future__ import annotations
import fluorine
from fluorine.contracts import ClaimPayload
from fluorine.foundation import run_foundation, screen_claim
def test_version(): assert fluorine.__version__=='0.1.0'
def test_screening(): assert 'hf_denial' in screen_claim(ClaimPayload('',claimed_no_hf_risk=True)).flags
def test_run(): assert run_foundation().health is not None
