from __future__ import annotations
import nitric_an
from nitric_an.contracts import ClaimPayload
from nitric_an.foundation import run_foundation, screen_claim
def test_version(): assert nitric_an.__version__=='0.1.0'
def test_screening(): assert 'an_hazard_conflation' in screen_claim(ClaimPayload('',claimed_an_inert_like_urea=True)).flags
def test_run(): assert run_foundation().health is not None
