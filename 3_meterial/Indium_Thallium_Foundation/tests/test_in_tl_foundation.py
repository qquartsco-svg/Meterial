from __future__ import annotations
import in_tl
from in_tl.contracts import ClaimPayload
from in_tl.foundation import run_foundation, screen_claim
def test_version(): assert in_tl.__version__=='0.1.0'
def test_screening(): assert 'group13_conflation' in screen_claim(ClaimPayload('',claimed_in_tl_same_safety_class=True)).flags
def test_run(): assert run_foundation().health is not None
