from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "chemical_reaction"


def test_expected_package_files_present() -> None:
    expected = {
        "__init__.py",
        "constants.py",
        "contracts.py",
        "species_and_bonds.py",
        "thermodynamics.py",
        "kinetics.py",
        "equilibrium.py",
        "electrochemistry.py",
        "screening.py",
        "foundation.py",
        "extension_hooks.py",
        "domain_battery.py",
        "domain_life_support.py",
        "domain_materials.py",
    }
    actual = {p.name for p in PACKAGE.iterdir() if p.is_file()}
    assert expected.issubset(actual)


def test_version_files_aligned() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    init_text = (PACKAGE / "__init__.py").read_text(encoding="utf-8")
    assert f'version = "{version}"' in pyproject
    assert f'__version__ = "{version}"' in init_text


def test_readmes_exist() -> None:
    assert (ROOT / "README.md").is_file()
    assert (ROOT / "README_EN.md").is_file()


def test_signature_and_scripts_exist() -> None:
    assert (ROOT / "SIGNATURE.sha256").is_file()
    assert (ROOT / "scripts" / "generate_signature.py").is_file()
    assert (ROOT / "scripts" / "verify_signature.py").is_file()
    assert (ROOT / "scripts" / "verify_hub_snapshot.py").is_file()
    assert (ROOT / "scripts" / "release_check.py").is_file()


def test_blockchain_docs_exist() -> None:
    assert (ROOT / "BLOCKCHAIN_INFO.md").is_file()
    assert (ROOT / "BLOCKCHAIN_INFO_EN.md").is_file()
    assert (ROOT / "PHAM_BLOCKCHAIN_LOG.md").is_file()


def test_3_meterial_hub_exists() -> None:
    hub = ROOT / "3_meterial"
    assert hub.is_dir()
    assert (hub / "README.md").is_file()
    assert (hub / "ELEMENT_REGISTRY.md").is_file()
    assert (hub / "Chemical_Reaction_Foundation").is_dir()
    assert (hub / "Hydrogen_Foundation").is_dir()
