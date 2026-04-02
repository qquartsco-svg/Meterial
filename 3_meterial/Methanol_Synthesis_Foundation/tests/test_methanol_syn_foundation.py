from __future__ import annotations
import methanol_syn
from methanol_syn.contracts import ClaimPayload
from methanol_syn.foundation import run_foundation, screen_claim
def test_version(): assert methanol_syn.__version__=='0.1.0'
def test_screening(): assert 'conversion_fantasy' in screen_claim(ClaimPayload('',claimed_single_pass_full_conversion=True)).flags
def test_run(): assert run_foundation().health is not None
