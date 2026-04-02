from __future__ import annotations
import i_br
from i_br.contracts import ClaimPayload
from i_br.foundation import run_foundation, screen_claim
def test_version(): assert i_br.__version__=='0.1.0'
def test_screening(): assert 'halogen_conflation' in screen_claim(ClaimPayload('',claimed_halogens_interchangeable=True)).flags
def test_run(): assert run_foundation().health is not None
