from __future__ import annotations
import as_sb_bi
from as_sb_bi.contracts import ClaimPayload
from as_sb_bi.foundation import run_foundation, screen_claim
def test_version(): assert as_sb_bi.__version__=='0.1.0'
def test_screening(): assert 'toxicity_conflation' in screen_claim(ClaimPayload('',claimed_group_equally_safe=True)).flags
def test_run(): assert run_foundation().health is not None
