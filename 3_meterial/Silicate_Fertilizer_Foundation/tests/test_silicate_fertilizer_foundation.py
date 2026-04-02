from __future__ import annotations
import silicate_fertilizer
from silicate_fertilizer.contracts import ClaimPayload
from silicate_fertilizer.foundation import run_foundation, screen_claim
def test_version(): assert silicate_fertilizer.__version__=='0.1.0'
def test_screening(): assert 'soluble_p_conflation' in screen_claim(ClaimPayload('',claimed_silicate_fungible_with_map=True)).flags
def test_run(): assert run_foundation().health is not None
