from __future__ import annotations
import organic_microbial_fert
from organic_microbial_fert.contracts import ClaimPayload
from organic_microbial_fert.foundation import run_foundation, screen_claim
def test_version(): assert organic_microbial_fert.__version__=='0.1.0'
def test_screening(): assert 'organic_safety_denial' in screen_claim(ClaimPayload('',claimed_organic_always_safe=True)).flags
def test_run(): assert run_foundation().health is not None
