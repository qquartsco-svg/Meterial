from __future__ import annotations
import sr_ba
from sr_ba.contracts import ClaimPayload
from sr_ba.foundation import run_foundation, screen_claim
def test_version(): assert sr_ba.__version__=='0.1.0'
def test_screening(): assert 'ba_speciation_conflation' in screen_claim(ClaimPayload('',claimed_all_barium_safe_like_contrast_agent=True)).flags
def test_run(): assert run_foundation().health is not None
