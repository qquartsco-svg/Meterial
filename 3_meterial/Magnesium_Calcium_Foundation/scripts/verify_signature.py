#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent

def sha(p): h=hashlib.sha256(); h.update(Path(p).read_bytes()); return h.hexdigest()
sp=ROOT/"SIGNATURE.sha256"
if not sp.exists(): sys.exit(1)
m=json.loads(sp.read_text()); fail=0
for rel,exp in m.get("files",{}).items():
 fp=ROOT/rel
 if (not fp.exists()) or (sha(fp)!=exp): fail+=1
sys.exit(1 if fail else 0)
