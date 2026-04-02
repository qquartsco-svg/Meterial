from __future__ import annotations
import sn_pb
from sn_pb.contracts import ClaimPayload
from sn_pb.foundation import run_foundation, screen_claim
def test_version(): assert sn_pb.__version__=='0.1.0'
def test_screening(): assert 'whisker_denial' in screen_claim(ClaimPayload('',claimed_no_whisker_issue=True)).flags
def test_run(): assert run_foundation().health is not None
