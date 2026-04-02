# BLOCKCHAIN_INFO

This repository, `Meterial`, uses `SIGNATURE.sha256` as a lightweight integrity manifest.

Purpose:

- track the integrity of README, code, tests, and design docs
- detect post-release drift
- compare local copies against the published reference state

This is a **repository-level SHA-256 integrity layer**.
It is not presented as a full public-chain smart-contract system.
It should be read as a blockchain-style chained integrity record for the repository.

Core files:

- `SIGNATURE.sha256`
- `scripts/generate_signature.py`
- `scripts/verify_signature.py`
- `scripts/release_check.py`

Recommended flow:

1. run tests
2. clean caches/generated files
3. regenerate signature
4. verify signature
5. run release check

This document is not a claim of absolute truth. It is an integrity guide for the current repository state.
