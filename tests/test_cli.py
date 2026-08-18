import io
import json
from pathlib import Path

from altar_ai.cli import main
from altar_ai.packs import load_pack


ROOT = Path(__file__).parents[1]
PACK = ROOT / "packs" / "universal-v1.json"


def test_draw_command_emits_only_stable_receipt_json(capsys):
    assert main(
        [
            "draw",
            "--at",
            "2026-07-15T12:34:56.789Z",
            "--mode",
            "note",
            "--pack-id",
            "universal-v1",
            "--pack-file",
            str(PACK),
            "--json",
        ]
    ) == 0
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert captured.err == ""
    assert payload["schema_version"] == "altar-draw-receipt-v1"
    assert payload["selection_proof_sha256"] == "6d26739cf38a51d804c872c004141411cc4421656c2ee82b5447e24c1623e544"


def test_field_command_accepts_file_and_stdin_json(tmp_path, monkeypatch, capsys):
    request = {
        "at_utc": "2026-07-15T12:34:56.789Z",
        "mode": "chord",
        "pack_id": "universal-v1",
        "observer": "higher-self",
    }
    request_path = tmp_path / "request.json"
    request_path.write_text(json.dumps(request), encoding="utf-8")
    assert main(["field", "--request", str(request_path), "--pack-file", str(PACK)]) == 0
    from_file = json.loads(capsys.readouterr().out)
    assert from_file["schema_version"] == "altar-field-envelope-v1"
    assert from_file["observer"]["profile_id"] == "higher-self"

    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(request)))
    assert main(["field", "--request", "-", "--pack-file", str(PACK)]) == 0
    from_stdin = json.loads(capsys.readouterr().out)
    assert from_stdin == from_file


def test_unknown_request_keys_fail_without_traceback(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.stdin",
        io.StringIO(
            json.dumps(
                {
                    "at_utc": "2026-07-15T12:34:56.789Z",
                    "question": "must never enter selector",
                }
            )
        ),
    )
    assert main(["field", "--request", "-", "--pack-file", str(PACK)]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "error:" in captured.err
    assert "Traceback" not in captured.err


def test_output_file_uses_exclusive_creation(tmp_path, capsys):
    output = tmp_path / "receipt.json"
    args = [
        "draw",
        "--at",
        "2026-07-15T12:34:56.789Z",
        "--output",
        str(output),
        "--mode",
        "note",
        "--pack-id",
        "universal-v1",
        "--pack-file",
        str(PACK),
    ]
    assert main(args) == 0
    assert json.loads(output.read_text())["mode"] == "note"
    assert main(args) == 2
    assert "error:" in capsys.readouterr().err


def test_packaged_default_matches_public_pack():
    packaged = ROOT / "src" / "altar_ai" / "data" / "universal-v1.json"
    assert load_pack(packaged).sha256 == load_pack(PACK).sha256


def test_v2_draw_is_the_default_and_emits_minimal_coordinates(capsys):
    assert main(["draw", "--at", "2026-07-15T12:34:56.789Z"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["schema_version"] == "altar-draw-receipt-v2"
    assert payload["pack_id"] == "whole-v3"
    assert payload["mode"] == "auto"
    assert payload["geometry"] in {"point", "triad", "constellation"}
    assert all(
        set(symbol) == {
            "ordinal",
            "role",
            "counter",
            "system_id",
            "system_label",
            "symbol_id",
            "label",
            "glyph",
            "derivation_sha256",
        }
        for symbol in payload["symbols"]
    )


def test_thinking_command_selects_or_honors_depth_without_stream(capsys):
    assert main(
        ["thinking", "--at", "2026-07-15T12:34:56.789Z", "--depth", "auto"]
    ) == 0
    automatic = json.loads(capsys.readouterr().out)
    assert automatic["depth"] in {3, 6, 9}
    assert "symbols" not in automatic
    assert "stream" not in automatic

    assert main(
        ["thinking", "--at", "2026-07-15T12:34:56.789Z", "--depth", "9"]
    ) == 0
    explicit = json.loads(capsys.readouterr().out)
    assert explicit["depth"] == 9


def test_now_and_at_are_mutually_exclusive(capsys):
    try:
        main(["draw", "--now", "--at", "2026-07-15T12:34:56.789Z"])
    except SystemExit as error:
        assert error.code == 2
    else:
        raise AssertionError("mutually exclusive instant arguments were accepted")
    assert "not allowed with argument" in capsys.readouterr().err


def test_json_schemas_are_closed_and_require_versioned_core_fields():
    schemas = ROOT / "schemas"
    expected = {
        "moment-request-v1.schema.json": {"at_utc", "mode", "pack_id", "observer"},
        "draw-receipt-v1.schema.json": {
            "schema_version",
            "selector_version",
            "at_utc",
            "pack_sha256",
            "selection_proof_sha256",
        },
        "field-envelope-v1.schema.json": {
            "schema_version",
            "receipt",
            "observer",
            "hidden_field",
            "integration_policy",
            "epistemic_status",
        },
        "moment-request-v2.schema.json": {
            "at_utc",
            "mode",
            "pack_id",
            "observer",
            "timezone_name",
        },
        "draw-receipt-v2.schema.json": {
            "schema_version",
            "selector_version",
            "at_utc",
            "pack_sha256",
            "geometry",
            "geometry_proof_sha256",
            "selection_proof_sha256",
        },
        "field-envelope-v2.schema.json": {
            "schema_version",
            "receipt",
            "observer",
            "hidden_field",
            "integration_policy",
            "epistemic_status",
            "sacred_time",
        },
        "thinking-depth-receipt-v1.schema.json": {
            "schema_version",
            "selector_version",
            "at_utc",
            "pack_sha256",
            "requested_depth",
            "depth",
            "derivation_sha256",
        },
    }
    for filename, fields in expected.items():
        schema = json.loads((schemas / filename).read_text(encoding="utf-8"))
        assert schema["additionalProperties"] is False
        assert fields <= set(schema["required"])
