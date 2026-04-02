from __future__ import annotations
import tc_pm
from tc_pm.contracts import ClaimPayload
from tc_pm.foundation import run_foundation, screen_claim
def test_version(): assert tc_pm.__version__=='0.1.0'
def test_screening(): assert 'synthetic_abundance_myth' in screen_claim(ClaimPayload('',claimed_natural_bulk_tc_pm=True)).flags
def test_run(): assert run_foundation().health is not None
