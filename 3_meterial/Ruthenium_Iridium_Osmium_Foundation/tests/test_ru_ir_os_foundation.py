from __future__ import annotations
import ru_ir_os
from ru_ir_os.contracts import ClaimPayload
from ru_ir_os.foundation import run_foundation, screen_claim
def test_version(): assert ru_ir_os.__version__=='0.1.0'
def test_screening(): assert 'os_hazard_conflation' in screen_claim(ClaimPayload('',claimed_osmium_benign_bulk=True)).flags
def test_run(): assert run_foundation().health is not None
