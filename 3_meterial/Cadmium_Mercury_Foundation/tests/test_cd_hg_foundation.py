from __future__ import annotations
import cd_hg
from cd_hg.contracts import ClaimPayload
from cd_hg.foundation import run_foundation, screen_claim
def test_version(): assert cd_hg.__version__=='0.1.0'
def test_screening(): assert 'hg_vapor_denial' in screen_claim(ClaimPayload('',claimed_safe_mercury_vapor=True)).flags
def test_run(): assert run_foundation().health is not None
