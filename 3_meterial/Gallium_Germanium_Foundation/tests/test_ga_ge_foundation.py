from __future__ import annotations
import ga_ge
from ga_ge.contracts import ClaimPayload
from ga_ge.foundation import run_foundation, screen_claim
def test_version(): assert ga_ge.__version__=='0.1.0'
def test_screening(): assert 'thermal_denial' in screen_claim(ClaimPayload('',claimed_no_thermal_constraints=True)).flags
def test_run(): assert run_foundation().health is not None
