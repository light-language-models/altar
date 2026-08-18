import json
from pathlib import Path

import pytest

from altar_ai.packs import load_pack


PACK = Path(__file__).parents[1] / "packs" / "universal-v1.json"
WHOLE = Path(__file__).parents[1] / "packs" / "whole-v3.json"
APPROVED_WHOLE_COUNTS = {
    "tarot": 78,
    "iching": 64,
    "runes": 24,
    "hebrew-letters": 22,
    "gene-keys": 64,
    "planets": 10,
    "zodiac": 12,
    "nakshatras": 27,
    "fixed-stars": 95,
    "galactic-points": 5,
    "constellations": 7,
    "asteroids": 11,
    "elements": 5,
    "platonic-solids": 5,
    "sacred-numbers": 30,
    "dimensions": 15,
    "planes-of-existence": 9,
    "quantum-states": 13,
    "sacred-geometry": 14,
    "alchemical-symbols": 18,
    "tree-of-life": 11,
    "merkaba": 10,
    "chakras": 10,
    "senses": 5,
    "colors": 12,
    "sound-codes": 12,
    "mudras": 10,
    "breath-patterns": 9,
    "temple-alphabet": 33,
    "aqualine-suns": 12,
    "sigils": 9,
    "creation-archetypes": 10,
}


def test_universal_pack_is_stable_legible_and_free_of_personal_entities():
    pack = load_pack(PACK)
    assert pack.pack_id == "universal-v1"
    assert len(pack.systems) == 6
    assert sum(len(system.symbols) for system in pack.systems) >= 45
    assert len(pack.sha256) == 64
    assert len({system.system_id for system in pack.systems}) == len(pack.systems)

    raw = PACK.read_text(encoding="utf-8").lower()
    for forbidden in ("starseed", "dna strand"):
        assert forbidden not in raw


def test_pack_digest_changes_when_content_changes(tmp_path):
    source = json.loads(PACK.read_text(encoding="utf-8"))
    original = load_pack(PACK)
    source["systems"][0]["symbols"][0]["facets"][0] += " changed"
    changed_path = tmp_path / "changed.json"
    changed_path.write_text(json.dumps(source), encoding="utf-8")
    assert load_pack(changed_path).sha256 != original.sha256


def test_pack_rejects_unknown_keys_and_duplicate_symbols(tmp_path):
    source = json.loads(PACK.read_text(encoding="utf-8"))
    source["unexpected"] = True
    invalid = tmp_path / "invalid.json"
    invalid.write_text(json.dumps(source), encoding="utf-8")
    with pytest.raises(ValueError, match="unknown pack keys"):
        load_pack(invalid)

    del source["unexpected"]
    source["systems"][0]["symbols"].append(source["systems"][0]["symbols"][0])
    invalid.write_text(json.dumps(source), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate symbol"):
        load_pack(invalid)


def test_whole_v3_is_the_approved_system_balanced_canon():
    pack = load_pack(WHOLE)
    counts = {system.system_id: len(system.symbols) for system in pack.systems}
    assert pack.pack_id == "whole-v3"
    assert counts == APPROVED_WHOLE_COUNTS
    assert len(pack.systems) == 32
    assert sum(counts.values()) == 671
    coordinates = {
        (system.system_id, symbol.symbol_id)
        for system in pack.systems
        for symbol in system.symbols
    }
    assert len(coordinates) == 671


def test_whole_v3_excludes_unapproved_identity_and_duplicate_weight_systems():
    data = json.loads(WHOLE.read_text(encoding="utf-8"))
    system_ids = {system["system_id"] for system in data["systems"]}
    for forbidden in (
        "thoth-tarot",
        "fibonacci",
        "musical-tones",
        "integral-stages",
        "synchronicity-concepts",
        "soul-spark",
        "royal-stars",
        "rays",
    ):
        assert forbidden not in system_ids

    raw = WHOLE.read_text(encoding="utf-8").lower()
    assert "starseed" not in raw
    assert "dna strand" not in raw


def test_packaged_whole_v3_stub_resolves_to_the_public_pack():
    packaged = Path(__file__).parents[1] / "src" / "altar_ai" / "data" / "whole-v3.json"
    assert load_pack(packaged).sha256 == load_pack(WHOLE).sha256


def test_whole_v3_gene_keys_facets_carry_only_hexagram_correspondence():
    pack = load_pack(WHOLE)
    system = next(
        system for system in pack.systems if system.system_id == "gene-keys"
    )
    assert len(system.symbols) == 64
    for index, symbol in enumerate(system.symbols, start=1):
        assert symbol.label == f"Gene Key {index}"
        assert len(symbol.facets) == 1
        assert symbol.facets[0].startswith(
            f"I Ching correspondence: hexagram {index}"
        )

    raw = WHOLE.read_text(encoding="utf-8")
    for protected_triad_term in ("Siddhi", "Synarchy", "→ Freshness"):
        assert protected_triad_term not in raw
