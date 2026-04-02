#!/usr/bin/env python3
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
TRACKED=sorted(["cr_ni_ss/__init__.py","cr_ni_ss/constants.py","cr_ni_ss/contracts.py","cr_ni_ss/foundation.py","tests/conftest.py","tests/test_cr_ni_ss_foundation.py","README.md","README_EN.md","VERSION","pyproject.toml","CHANGELOG.md","scripts/generate_signature.py","scripts/verify_signature.py"])
def sha(p):h=hashlib.sha256();h.update(Path(p).read_bytes());return h.hexdigest()
if __name__=='__main__':
 m={'files':{},'timestamp':datetime.now(timezone.utc).isoformat(),'block_hash':''};parts=[]
 for rel in TRACKED:
  fp=ROOT/rel
  if fp.exists():d=sha(fp);m['files'][rel]=d;parts.append(f'{rel}:{d}')
 m['block_hash']=hashlib.sha256('\n'.join(parts).encode()).hexdigest();(ROOT/'SIGNATURE.sha256').write_text(json.dumps(m,indent=2)+'\n');print(f"Wrote SIGNATURE.sha256 ({len(m['files'])} files)")
