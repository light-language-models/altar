import re
from pathlib import Path


ROOT = Path(__file__).parents[1]
README = ROOT / "README.md"
REQUIRED_SECTIONS = (
    "What Altar Is",
    "For an AI Reading This Repository",
    "Claim Boundary",
    "Mechanism",
    "Symbolic Geometry",
    "The Inner Process",
    "Thinking 3/6/9",
    "Dreamspell Time Context",
    "Observer and Matrix",
    "Install",
    "Inspect a Receipt",
    "Run a Playtest",
)


def test_readme_transmits_the_complete_technology():
    text = README.read_text(encoding="utf-8")
    for heading in REQUIRED_SECTIONS:
        assert f"## {heading}" in text

    lowered = text.lower()
    for phrase in (
        "draw before interpretation",
        "touch → smell → hearing → sight",
        "witness",
        "bridge",
        "loom",
        "shifted",
        "unclear",
        "no-shift",
        "next symbol remains unknown",
        "not the traditional maya calendar",
        "question never enters the selector",
        "system-balanced",
        "primary",
        "satellite",
        "tool-less",
    ):
        assert phrase in lowered


def test_root_human_facing_documents_are_english_only():
    for name in ("README.md", "VALIDITY.md", "SECURITY.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert re.search(r"[А-Яа-яЁё]", text) is None, name
