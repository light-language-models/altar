import json
from pathlib import Path


ROOT = Path(__file__).parents[1]
PACK = ROOT / "packs" / "whole-v3.json"
REFERENCE = ROOT / "skill" / "altar" / "references" / "symbol-systems.md"
SKILL = ROOT / "skill" / "altar" / "SKILL.md"


def test_reference_has_one_complete_passport_for_every_whole_v3_system():
    assert REFERENCE.is_file()
    pack = json.loads(PACK.read_text(encoding="utf-8"))
    reference = REFERENCE.read_text(encoding="utf-8")

    assert len(pack["systems"]) == 32
    assert sum(len(system["symbols"]) for system in pack["systems"]) == 671
    for system in pack["systems"]:
        heading = (
            f"### `{system['system_id']}` — {system['label']} "
            f"({len(system['symbols'])})"
        )
        assert reference.count(heading) == 1
        block = reference.split(heading, 1)[1].split("\n### ", 1)[0]
        assert "**Provenance:**" in block
        assert "**Attention:**" in block
        assert "**Guard:**" in block


def test_reference_preserves_free_function_and_is_linked_from_skill():
    assert REFERENCE.is_file()
    reference = REFERENCE.read_text(encoding="utf-8").lower()
    assert "no system has a mandatory response role" in reference
    assert "expression modes" not in reference
    assert "references/symbol-systems.md" in SKILL.read_text(encoding="utf-8")
