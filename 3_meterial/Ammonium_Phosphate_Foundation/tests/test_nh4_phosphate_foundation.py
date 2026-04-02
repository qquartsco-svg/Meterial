from __future__ import annotations
import nh4_phosphate
from nh4_phosphate.contracts import ClaimPayload
from nh4_phosphate.foundation import run_foundation, screen_claim
def test_version(): assert nh4_phosphate.__version__=='0.1.0'
def test_screening(): assert 'np_ratio_conflation' in screen_claim(ClaimPayload('',claimed_map_dap_fungible_no_agronomy=True)).flags
def test_run(): assert run_foundation().health is not None
