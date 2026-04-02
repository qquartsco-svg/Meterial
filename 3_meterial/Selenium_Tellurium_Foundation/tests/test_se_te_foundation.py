from __future__ import annotations
import se_te
from se_te.contracts import ClaimPayload
from se_te.foundation import run_foundation, screen_claim
def test_version(): assert se_te.__version__=='0.1.0'
def test_screening(): assert 'te_abundance_myth' in screen_claim(ClaimPayload('',claimed_infinite_tellurium=True)).flags
def test_run(): assert run_foundation().health is not None
