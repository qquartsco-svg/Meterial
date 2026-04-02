from __future__ import annotations
import co_mn_spinel
from co_mn_spinel.contracts import ClaimPayload
from co_mn_spinel.foundation import run_foundation, screen_claim
def test_version(): assert co_mn_spinel.__version__=='0.1.0'
def test_screening(): assert 'supply_denial' in screen_claim(ClaimPayload('',claimed_no_supply_risk=True)).flags
def test_run(): assert run_foundation().health is not None
