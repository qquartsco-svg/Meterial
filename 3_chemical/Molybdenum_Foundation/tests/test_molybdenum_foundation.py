from __future__ import annotations
import molybdenum
from molybdenum.contracts import ClaimPayload
from molybdenum.foundation import run_foundation, screen_claim
def test_version(): assert molybdenum.__version__=='0.1.0'
def test_screening(): assert 'poisoning_denial' in screen_claim(ClaimPayload('',claimed_no_poisoning=True)).flags
def test_run(): assert run_foundation().health is not None
