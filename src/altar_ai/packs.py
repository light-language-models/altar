"""Strict loading and content addressing for symbol packs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
from typing import Any

from .contracts import PACK_SCHEMA_VERSION, Symbol, SymbolPack, SymbolSystem


_PACK_KEYS = {"schema_version", "pack_id", "title", "description", "systems"}
_SYSTEM_KEYS = {"system_id", "label", "tradition", "symbols"}
_SYMBOL_KEYS = {"symbol_id", "label", "glyph", "facets", "caution"}


def _exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    unknown = set(value) - expected
    missing = expected - set(value)
    if unknown:
        raise ValueError(f"unknown {label} keys: {sorted(unknown)}")
    if missing:
        raise ValueError(f"missing {label} keys: {sorted(missing)}")


def load_pack(path: Path) -> SymbolPack:
    source = Path(path)
    try:
        raw = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read symbol pack: {source}") from error
    if not isinstance(raw, dict):
        raise ValueError("symbol pack must be a JSON object")
    if set(raw) == {"packaged_pack"}:
        pack_id = str(raw["packaged_pack"])
        if pack_id not in {"universal-v1", "whole-v3"}:
            raise ValueError("unknown packaged symbol pack")
        candidates = (
            source.parents[3] / "packs" / f"{pack_id}.json",
            source.parents[2] / "share" / "altar-ai" / "packs" / f"{pack_id}.json",
            Path(sys.prefix) / "share" / "altar-ai" / "packs" / f"{pack_id}.json",
        )
        resolved = next((candidate for candidate in candidates if candidate.is_file()), None)
        if resolved is None:
            raise ValueError(f"packaged {pack_id} payload is missing")
        return load_pack(resolved)
    _exact_keys(raw, _PACK_KEYS, "pack")
    if raw["schema_version"] != PACK_SCHEMA_VERSION:
        raise ValueError(f"unknown pack schema: {raw['schema_version']}")
    if not isinstance(raw["systems"], list):
        raise ValueError("pack systems must be an array")

    systems = []
    for system_raw in raw["systems"]:
        if not isinstance(system_raw, dict):
            raise ValueError("symbol system must be an object")
        _exact_keys(system_raw, _SYSTEM_KEYS, "system")
        if not isinstance(system_raw["symbols"], list):
            raise ValueError("system symbols must be an array")
        symbols = []
        for symbol_raw in system_raw["symbols"]:
            if not isinstance(symbol_raw, dict):
                raise ValueError("symbol must be an object")
            _exact_keys(symbol_raw, _SYMBOL_KEYS, "symbol")
            if not isinstance(symbol_raw["facets"], list):
                raise ValueError("symbol facets must be an array")
            symbols.append(
                Symbol(
                    system_id=str(system_raw["system_id"]),
                    symbol_id=str(symbol_raw["symbol_id"]),
                    label=str(symbol_raw["label"]),
                    glyph=(str(symbol_raw["glyph"]) if symbol_raw["glyph"] else None),
                    facets=tuple(str(value) for value in symbol_raw["facets"]),
                    tradition=str(system_raw["tradition"]),
                    caution=(
                        str(symbol_raw["caution"])
                        if symbol_raw["caution"]
                        else None
                    ),
                )
            )
        systems.append(
            SymbolSystem(
                system_id=str(system_raw["system_id"]),
                label=str(system_raw["label"]),
                tradition=str(system_raw["tradition"]),
                symbols=tuple(symbols),
            )
        )

    canonical = json.dumps(
        raw, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return SymbolPack(
        schema_version=str(raw["schema_version"]),
        pack_id=str(raw["pack_id"]),
        title=str(raw["title"]),
        description=str(raw["description"]),
        systems=tuple(systems),
        sha256=hashlib.sha256(canonical).hexdigest(),
    )
