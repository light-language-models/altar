import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).parents[1]
README = ROOT / "README.md"


def test_readme_exposes_quick_start_architecture_and_three_integration_routes():
    text = README.read_text(encoding="utf-8").lower()
    assert "quick start" in text
    assert "python -m altar_ai draw" in text
    assert "| layer |" in text and "momentrequest" in text and "fieldenvelope" in text
    assert "install the ai skill" in text
    assert "cli / json" in text
    assert "python api" in text
    assert "mcp" in text and "later adapter" in text


def test_public_docs_separate_verified_mechanism_from_open_claims():
    readme = README.read_text(encoding="utf-8").lower()
    validity = (ROOT / "VALIDITY.md").read_text(encoding="utf-8").lower()
    combined = readme + "\n" + validity
    for concept in ("mechanism", "reproducibility", "correspondence", "metaphysics"):
        assert concept in combined
    assert "| claim | status |" in validity
    assert "pending" in validity
    assert "independent blind" in validity
    assert "correspondence is proven" not in combined
    assert "apache license 2.0" in readme
    assert "license must be selected" not in readme
    assert "private playtest candidate" not in readme


def test_public_security_boundaries_are_explicit():
    text = (ROOT / "SECURITY.md").read_text(encoding="utf-8").lower()
    for boundary in (
        "question",
        "selector",
        "privacy",
        "consent",
        "medical",
        "legal",
        "financial",
        "network",
        "telemetry",
    ):
        assert boundary in text


def test_generic_subprocess_example_emits_valid_receipt_json():
    environment = dict(os.environ)
    source = str(ROOT / "src")
    environment["PYTHONPATH"] = source + os.pathsep + environment.get("PYTHONPATH", "")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "examples" / "generic-subprocess.py"),
            "--at",
            "2026-07-15T12:34:56.789Z",
            "--mode",
            "note",
        ],
        cwd=ROOT,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == "altar-draw-receipt-v1"
    assert payload["selector_inputs"] == [
        "selector_version",
        "pack_sha256",
        "unix_milliseconds",
        "counter",
    ]
    assert payload["symbols"][0]["label"] == "Zhen — Thunder"


def test_public_release_surface_contains_no_private_runtime_references():
    public_files = [
        README,
        ROOT / "VALIDITY.md",
        ROOT / "SECURITY.md",
        ROOT / "examples" / "generic-subprocess.py",
        ROOT / "examples" / "system-prompt.md",
    ]
    public = "\n".join(path.read_text(encoding="utf-8") for path in public_files).lower()
    for forbidden in (
        "lightweaver.db",
        "question_facet_memory",
        "target_row_id",
    ):
        assert forbidden not in public
