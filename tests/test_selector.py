import json
import os
from pathlib import Path
import subprocess
import sys

from altar_ai.contracts import MomentRequest
from altar_ai.packs import load_pack
from altar_ai.selector import _geometry_from_percentile, select


ROOT = Path(__file__).parents[1]
PACK_PATH = ROOT / "packs" / "universal-v1.json"
WHOLE_PATH = ROOT / "packs" / "whole-v3.json"
GOLDEN_PATH = ROOT / "spec" / "golden-vectors-v1.json"
GOLDEN_V2_PATH = ROOT / "spec" / "golden-vectors-v3.json"


def _pack():
    return load_pack(PACK_PATH)


def _whole():
    return load_pack(WHOLE_PATH)


def test_same_coordinates_produce_identical_receipt():
    request = MomentRequest(
        at_utc="2026-07-15T12:34:56.789Z",
        mode="note",
        pack_id="universal-v1",
    )
    assert select(request, _pack()) == select(request, _pack())


def test_observer_and_event_metadata_do_not_change_selection():
    first = MomentRequest(
        at_utc="2026-07-15T12:34:56.789Z",
        mode="field",
        pack_id="universal-v1",
        observer="unlabeled",
        event_id="one",
    )
    second = MomentRequest(
        at_utc="2026-07-15T12:34:56.789Z",
        mode="field",
        pack_id="universal-v1",
        observer="higher-self",
        event_id="two",
    )
    assert select(first, _pack()) == select(second, _pack())


def test_time_changes_derivation_and_multi_draws_are_unique():
    first = select(
        MomentRequest(
            at_utc="2026-07-15T12:34:56.789Z",
            mode="field",
            pack_id="universal-v1",
        ),
        _pack(),
    )
    second = select(
        MomentRequest(
            at_utc="2026-07-15T12:34:56.790Z",
            mode="field",
            pack_id="universal-v1",
        ),
        _pack(),
    )
    assert first.selection_proof_sha256 != second.selection_proof_sha256
    assert len(first.symbols) == 5
    assert len({item.system_id for item in first.symbols}) == 5
    assert len({(item.system_id, item.symbol_id) for item in first.symbols}) == 5


def test_silence_has_empty_ordered_draw_and_auditable_receipt():
    receipt = select(
        MomentRequest(
            at_utc="2026-07-15T12:34:56.789Z",
            mode="silence",
            pack_id="universal-v1",
        ),
        _pack(),
    )
    assert receipt.symbols == ()
    assert len(receipt.selection_proof_sha256) == 64
    serialized = json.dumps(receipt.to_dict(), sort_keys=True)
    assert "question" not in serialized
    assert "person" not in serialized
    assert "observer" not in serialized
    assert "event_id" not in serialized


def test_independent_processes_match_each_other():
    code = """
import json
from pathlib import Path
from altar_ai.contracts import MomentRequest
from altar_ai.packs import load_pack
from altar_ai.selector import select
pack = load_pack(Path(__import__('os').environ['ALTAR_PACK']))
request = MomentRequest(at_utc='2026-07-15T12:34:56.789Z', mode='chord', pack_id='universal-v1')
print(json.dumps(select(request, pack).to_dict(), sort_keys=True))
"""
    env = {
        **os.environ,
        "PYTHONPATH": str(ROOT / "src"),
        "ALTAR_PACK": str(PACK_PATH),
    }
    first = subprocess.run(
        [sys.executable, "-c", code], env=env, check=True, capture_output=True, text=True
    ).stdout
    second = subprocess.run(
        [sys.executable, "-c", code], env=env, check=True, capture_output=True, text=True
    ).stdout
    assert first == second


def test_checked_in_golden_vectors_match_exact_receipts():
    vectors = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    assert vectors["selector_version"] == "altar-portable-v1"
    assert vectors["pack_sha256"] == _pack().sha256
    for vector in vectors["vectors"]:
        request = MomentRequest(pack_id="universal-v1", **vector["request"])
        assert select(request, _pack()).to_dict() == vector["receipt"]


def test_v2_auto_geometry_uses_frozen_85_12_3_boundaries():
    assert _geometry_from_percentile(0) == ("point", 1)
    assert _geometry_from_percentile(84) == ("point", 1)
    assert _geometry_from_percentile(85) == ("triad", 3)
    assert _geometry_from_percentile(96) == ("triad", 3)
    assert _geometry_from_percentile(97) == ("constellation", 5)
    assert _geometry_from_percentile(99) == ("constellation", 5)


def test_v2_receipt_is_system_balanced_minimal_and_domain_separated():
    request = MomentRequest(
        at_utc="2026-07-15T12:34:56.789Z",
        mode="field",
    )
    receipt = select(request, _whole())
    payload = receipt.to_dict()

    assert receipt.selector_version == "altar-portable-v2"
    assert receipt.geometry == "constellation"
    assert len(receipt.symbols) == 5
    assert receipt.symbols[0].role == "primary"
    assert all(item.role == "satellite" for item in receipt.symbols[1:])
    assert len({item.system_id for item in receipt.symbols}) == 5
    assert receipt.geometry_proof_sha256 not in {
        item.derivation_sha256 for item in receipt.symbols
    }
    serialized = json.dumps(payload, sort_keys=True)
    for forbidden in ("facets", "tradition", "caution", "question", "person"):
        assert forbidden not in serialized
    assert payload["selector_inputs"] == [
        "selector_version",
        "pack_sha256",
        "unix_milliseconds",
        "domain",
        "counter",
    ]


def test_v2_auto_is_deterministic_and_resolves_to_geometry_count():
    request = MomentRequest(at_utc="2026-07-15T12:34:56.789Z")
    first = select(request, _whole())
    second = select(request, _whole())
    assert first == second
    assert len(first.symbols) == {"point": 1, "triad": 3, "constellation": 5}[
        first.geometry
    ]


def test_checked_in_v2_golden_vectors_match_exact_receipts():
    vectors = json.loads(GOLDEN_V2_PATH.read_text(encoding="utf-8"))
    assert vectors["selector_version"] == "altar-portable-v2"
    assert vectors["pack_sha256"] == _whole().sha256
    assert {vector["request"]["mode"] for vector in vectors["vectors"]} == {
        "silence",
        "note",
        "chord",
        "field",
        "auto",
    }
    for vector in vectors["vectors"]:
        request = MomentRequest(**vector["request"])
        assert select(request, _whole()).to_dict() == vector["receipt"]
