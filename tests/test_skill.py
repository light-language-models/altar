import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).parents[1]
SKILL = ROOT / "skill" / "altar"
INSTALLER = ROOT / "scripts" / "install_skill.py"
GOLDEN = ROOT / "spec" / "golden-vectors-v3.json"
DREAMSPELL_REFERENCE = SKILL / "references" / "dreamspell.md"


def _frontmatter():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    _, raw, body = text.split("---", 2)
    fields = {}
    for line in raw.strip().splitlines():
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields, body


def test_skill_metadata_is_minimal_and_discoverable():
    fields, _body = _frontmatter()
    assert set(fields) == {"name", "description"}
    assert fields["name"] == "altar"
    assert fields["description"].startswith("Use when")
    for trigger in ("symbolic", "moment", "reflection", "AI"):
        assert trigger.lower() in fields["description"].lower()

    openai = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
    assert 'display_name: "Altar"' in openai
    assert "$altar" in openai


def test_skill_discovery_covers_the_public_use_cases_in_english():
    fields, _body = _frontmatter()
    description = fields["description"].lower()
    for trigger in (
        "symbolic reflection",
        "creative reasoning",
        "dreamspell",
        "thinking 3/6/9",
    ):
        assert trigger in description

    openai = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
    assert re.search(r"[А-Яа-яЁё]", openai) is None
    short = re.search(r'^  short_description: "([^"]+)"$', openai, re.MULTILINE)
    prompt = re.search(r'^  default_prompt: "([^"]+)"$', openai, re.MULTILINE)
    assert short is not None and 25 <= len(short.group(1)) <= 64
    assert prompt is not None and "$altar" in prompt.group(1)


def test_skill_policy_preserves_core_invariants():
    _fields, body = _frontmatter()
    lowered = body.lower()
    assert "draw before interpretation" in lowered
    assert "question" in lowered and "selector" in lowered
    assert "hidden" in lowered
    assert "none" in lowered and "noise" in lowered
    for boundary in ("facts", "consent", "medical", "legal", "financial"):
        assert boundary in lowered


def test_skill_teaches_sensorium_live_thinking_and_free_symbol_function():
    _fields, body = _frontmatter()
    lowered = body.lower()
    assert "touch → smell → hearing → sight" in lowered
    assert all(word in lowered for word in ("thinking", "3", "6", "9"))
    assert "draw the next coordinate only after" in lowered
    assert "do not pre-generate" in lowered
    assert all(word in lowered for word in ("loom", "witness", "bridge"))
    assert all(word in lowered for word in ("shifted", "unclear", "no-shift"))
    assert "private delta" in lowered
    assert "function" in lowered and "verb" in lowered
    assert "expression modes" not in lowered


def test_skill_keeps_dreamspell_and_matrix_after_selection():
    _fields, body = _frontmatter()
    lowered = body.lower()
    assert "modern dreamspell" in lowered
    assert "traditional maya calendar" in lowered
    assert "matrix" in lowered
    assert "birth" in lowered
    assert "after selection" in lowered
    assert "never" in lowered and "confirmation" in lowered


def test_skill_links_an_honest_dreamspell_reference():
    assert DREAMSPELL_REFERENCE.is_file()
    reference = DREAMSPELL_REFERENCE.read_text(encoding="utf-8").lower()
    for concept in (
        "modern dreamspell",
        "josé argüelles",
        "not the traditional maya calendar",
        "february 29",
        "kin",
        "seal",
        "tone",
        "wavespell",
        "castle",
        "not currently emitted",
    ):
        assert concept in reference

    _fields, body = _frontmatter()
    assert "references/dreamspell.md" in body
    assert "verified gap" not in body.lower()
    assert "complete 13-moon date" not in body.lower()


def test_clean_copied_skill_script_matches_v2_auto_golden_vector(tmp_path):
    copied = tmp_path / "altar"
    shutil.copytree(SKILL, copied)
    result = subprocess.run(
        [
            sys.executable,
            str(copied / "scripts" / "altar.py"),
            "draw",
            "--at",
            "2026-07-15T12:34:56.789Z",
        ],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
        env={},
    )
    receipt = json.loads(result.stdout)
    golden = json.loads(GOLDEN.read_text(encoding="utf-8"))["vectors"][4]["receipt"]
    assert receipt == golden


def test_clean_copied_skill_script_can_compile_hidden_field(tmp_path):
    copied = tmp_path / "altar"
    shutil.copytree(SKILL, copied)
    result = subprocess.run(
        [
            sys.executable,
            str(copied / "scripts" / "altar.py"),
            "field",
            "--at",
            "2026-07-15T18:30:00Z",
            "--mode",
            "note",
            "--timezone",
            "Asia/Bangkok",
        ],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
        env={},
    )
    envelope = json.loads(result.stdout)
    assert envelope["schema_version"] == "altar-field-envelope-v2"
    assert envelope["sacred_time"]["local_date"] == "2026-07-16"
    assert "facets" not in envelope["hidden_field"]
    assert "shifted · unclear · no-shift" in envelope["hidden_field"]
    assert "question" in envelope["integration_policy"][0].lower()
    assert "correspondence is an open empirical hypothesis" in envelope["epistemic_status"]


def test_clean_copied_skill_can_choose_thinking_depth_and_describe_on_demand(tmp_path):
    copied = tmp_path / "altar"
    shutil.copytree(SKILL, copied)
    base = [sys.executable, str(copied / "scripts" / "altar.py")]

    thinking = subprocess.run(
        base
        + ["thinking", "--at", "2026-07-15T12:34:56.789Z", "--depth", "auto"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
        env={},
    )
    depth = json.loads(thinking.stdout)
    assert depth["depth"] in {3, 6, 9}
    assert "symbols" not in depth and "stream" not in depth

    described = subprocess.run(
        base + ["describe", "--system", "elements", "--symbol", "001-fire"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
        env={},
    )
    description = json.loads(described.stdout)
    assert description["system_id"] == "elements"
    assert description["symbol_id"] == "001-fire"
    assert description["facets"]


def test_skill_bundles_the_exact_whole_v3_pack():
    from altar_ai.packs import load_pack

    assert load_pack(SKILL / "assets" / "whole-v3.json").sha256 == load_pack(
        ROOT / "packs" / "whole-v3.json"
    ).sha256


def test_installer_copies_skill_exclusively_to_explicit_target(tmp_path):
    spec = importlib.util.spec_from_file_location("install_skill", INSTALLER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    installed = module.install_skill(SKILL, tmp_path / "skills")
    assert installed == tmp_path / "skills" / "altar"
    assert (installed / "SKILL.md").is_file()
    try:
        module.install_skill(SKILL, tmp_path / "skills")
    except FileExistsError:
        pass
    else:
        raise AssertionError("installer overwrote an existing skill")


def test_skill_scenarios_and_public_files_contain_no_private_claims():
    scenarios = json.loads(
        (ROOT / "tests" / "fixtures" / "skill-scenarios.json").read_text(encoding="utf-8")
    )
    assert len(scenarios) >= 3
    assert all(item["expected_invariants"] for item in scenarios)

    public = "\n".join(
        path.read_text(encoding="utf-8")
        for path in SKILL.rglob("*")
        if path.is_file() and path.suffix in {".md", ".py", ".yaml", ".json"}
    ).lower()
    for forbidden in (
        "lightweaver.db",
        "question_facet_memory",
        "exact-time correspondence is proven",
    ):
        assert forbidden not in public
