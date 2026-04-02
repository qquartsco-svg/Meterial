from __future__ import annotations
import rb_cs
from rb_cs.contracts import ClaimPayload
from rb_cs.foundation import run_foundation, screen_claim
def test_version(): assert rb_cs.__version__=='0.1.0'
def test_screening(): assert 'alkali_conflation' in screen_claim(ClaimPayload('',claimed_mild_alkali_like_na=True)).flags
def test_run(): assert run_foundation().health is not None
