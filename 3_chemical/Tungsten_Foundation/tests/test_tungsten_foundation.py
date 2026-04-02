from __future__ import annotations
import tungsten
from tungsten.contracts import ClaimPayload
from tungsten.foundation import run_foundation, screen_claim
def test_version(): assert tungsten.__version__=='0.1.0'
def test_screening(): assert 'oxidation_denial' in screen_claim(ClaimPayload('',claimed_no_oxidation=True)).flags
def test_run(): assert run_foundation().health is not None
