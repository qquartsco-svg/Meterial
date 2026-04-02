from __future__ import annotations
import ag_au
from ag_au.contracts import ClaimPayload
from ag_au.foundation import run_foundation, screen_claim
def test_version(): assert ag_au.__version__=='0.1.0'
def test_screening(): assert 'cost_denial' in screen_claim(ClaimPayload('',claimed_zero_cost_penalty=True)).flags
def test_run(): assert run_foundation().health is not None
