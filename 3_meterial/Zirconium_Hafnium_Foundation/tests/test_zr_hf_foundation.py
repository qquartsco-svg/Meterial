from __future__ import annotations
import zr_hf
from zr_hf.contracts import ClaimPayload
from zr_hf.foundation import run_foundation, screen_claim
def test_version(): assert zr_hf.__version__=='0.1.0'
def test_screening(): assert 'separation_denial' in screen_claim(ClaimPayload('',claimed_no_separation_complexity=True)).flags
def test_run(): assert run_foundation().health is not None
