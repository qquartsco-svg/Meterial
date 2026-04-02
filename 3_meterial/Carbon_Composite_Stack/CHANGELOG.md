# Changelog

## 0.1.2

- material: connected `thermal_conductivity_w_mk` and `electrical_conductivity_s_m` to conservative suitability scores
- material: connected `max_mass_kg` and `safety_class` to a density-based lightweight proxy path
- tests: added regression coverage to ensure the newly active public contract fields affect readiness evidence
- docs: updated README/README_EN verification snapshot and clarified the proxy meaning of mass and safety inputs

## 0.1.1

- docs: clarified `observer` vs `pipeline`, expanded processability/circularity notes, and added README test snapshot (`3 passed`)
- integrity: appended blockchain continuity log for the documentation refinement and regenerated SHA-256 signature manifest
- release: synchronized version markers (`VERSION`, `pyproject.toml`, `__init__.py`) to `0.1.1`

## 0.1.0

- initial independent carbon composite design/evaluation stack
- added contracts + material/process/circularity + readiness observer pipeline
- added `engine_ref` adapter: `carbon.composite.readiness`
- added JSON CLI entrypoint and sample payload
- added integrity docs and SHA-256 signature workflow
