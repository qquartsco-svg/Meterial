from __future__ import annotations
import rhenium
from rhenium.contracts import ClaimPayload
from rhenium.foundation import run_foundation, screen_claim
def test_version(): assert rhenium.__version__=='0.1.0'
def test_screening(): assert 're_abundance_myth' in screen_claim(ClaimPayload('',claimed_abundant_rhenium=True)).flags
def test_run(): assert run_foundation().health is not None
