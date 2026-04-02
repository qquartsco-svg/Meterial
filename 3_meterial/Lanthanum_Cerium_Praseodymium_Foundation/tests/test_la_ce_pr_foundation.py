from __future__ import annotations
import la_ce_pr
from la_ce_pr.contracts import ClaimPayload
from la_ce_pr.foundation import run_foundation, screen_claim
def test_version(): assert la_ce_pr.__version__=='0.1.0'
def test_screening(): assert 'purity_fantasy' in screen_claim(ClaimPayload('',claimed_one_step_purity=True)).flags
def test_run(): assert run_foundation().health is not None
