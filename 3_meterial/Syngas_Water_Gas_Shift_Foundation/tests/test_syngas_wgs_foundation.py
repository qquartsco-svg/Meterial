from __future__ import annotations
import syngas_wgs
from syngas_wgs.contracts import ClaimPayload
from syngas_wgs.foundation import run_foundation, screen_claim
def test_version(): assert syngas_wgs.__version__=='0.1.0'
def test_screening(): assert 'co_toxicity_denial' in screen_claim(ClaimPayload('',claimed_co_benign_like_n2=True)).flags
def test_run(): assert run_foundation().health is not None
