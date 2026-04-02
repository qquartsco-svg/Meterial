from __future__ import annotations
import photo_cmp
from photo_cmp.contracts import ClaimPayload
from photo_cmp.foundation import run_foundation, screen_claim
def test_version(): assert photo_cmp.__version__=='0.1.0'
def test_screening(): assert 'resist_ehs_denial' in screen_claim(ClaimPayload('',claimed_resist_zero_ehs_tail=True)).flags
def test_run(): assert run_foundation().health is not None
