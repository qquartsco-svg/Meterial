from __future__ import annotations
import boron
from boron.contracts import ClaimPayload
from boron.foundation import run_foundation, screen_claim
def test_version(): assert boron.__version__=='0.1.0'
def test_screening(): assert 'brittleness_denial' in screen_claim(ClaimPayload('',claimed_no_brittleness_tradeoff=True)).flags
def test_run(): assert run_foundation().health is not None
