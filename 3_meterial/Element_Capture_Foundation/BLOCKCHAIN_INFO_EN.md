# BLOCKCHAIN_INFO

In this repository, “blockchain signature” does **not** mean a consensus ledger, smart contract, or private-key code signing.

It refers to the root [SIGNATURE.sha256](/Users/jazzin/Desktop/00_BRAIN/_staging/Element_Capture_Foundation/SIGNATURE.sha256) file:
a **SHA-256 integrity manifest** for the checked-in source and documentation surface.

What it provides:

- quick tamper checks for release snapshots
- local verification against the repository baseline

What it does not provide:

- private-key signing
- on-chain persistence
- consensus-backed validation

Verify:

```bash
python3 scripts/verify_signature.py
```

Regenerate:

```bash
python3 scripts/generate_signature.py
```
