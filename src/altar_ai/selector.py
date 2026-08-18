"""Cross-process deterministic selectors for altar-portable-v1 and v2."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib

from .contracts import (
    MODE_COUNTS,
    SELECTOR_VERSION,
    SELECTOR_VERSION_V2,
    MomentRequest,
    SymbolPack,
)


RECEIPT_SCHEMA_VERSION = "altar-draw-receipt-v1"
RECEIPT_SCHEMA_VERSION_V2 = "altar-draw-receipt-v2"
_UNIT_SEPARATOR = b"\x1f"


@dataclass(frozen=True)
class DrawnSymbol:
    ordinal: int
    counter: int
    system_id: str
    system_label: str
    symbol_id: str
    label: str
    glyph: str | None
    facets: tuple[str, ...]
    tradition: str
    caution: str | None
    derivation_sha256: str
    role: str | None = None

    def to_dict(self, *, minimal: bool = False) -> dict[str, object]:
        coordinate = {
            "ordinal": self.ordinal,
            **({"role": self.role} if self.role else {}),
            "counter": self.counter,
            "system_id": self.system_id,
            "system_label": self.system_label,
            "symbol_id": self.symbol_id,
            "label": self.label,
            "glyph": self.glyph,
            "derivation_sha256": self.derivation_sha256,
        }
        if minimal:
            return coordinate
        return {
            **coordinate,
            "facets": list(self.facets),
            "tradition": self.tradition,
            "caution": self.caution,
        }


@dataclass(frozen=True)
class DrawReceipt:
    at_utc: str
    unix_milliseconds: int
    pack_id: str
    pack_sha256: str
    mode: str
    symbols: tuple[DrawnSymbol, ...]
    selection_proof_sha256: str
    schema_version: str = RECEIPT_SCHEMA_VERSION
    selector_version: str = SELECTOR_VERSION
    geometry: str | None = None
    geometry_proof_sha256: str | None = None

    def to_dict(self) -> dict[str, object]:
        if self.selector_version == SELECTOR_VERSION:
            return {
                "schema_version": self.schema_version,
                "selector_version": self.selector_version,
                "at_utc": self.at_utc,
                "unix_milliseconds": self.unix_milliseconds,
                "pack_id": self.pack_id,
                "pack_sha256": self.pack_sha256,
                "mode": self.mode,
                "symbols": [symbol.to_dict() for symbol in self.symbols],
                "selection_proof_sha256": self.selection_proof_sha256,
                "selector_inputs": [
                    "selector_version",
                    "pack_sha256",
                    "unix_milliseconds",
                    "counter",
                ],
            }
        return {
            "schema_version": self.schema_version,
            "selector_version": self.selector_version,
            "at_utc": self.at_utc,
            "unix_milliseconds": self.unix_milliseconds,
            "pack_id": self.pack_id,
            "pack_sha256": self.pack_sha256,
            "mode": self.mode,
            "geometry": self.geometry,
            "geometry_proof_sha256": self.geometry_proof_sha256,
            "symbols": [symbol.to_dict(minimal=True) for symbol in self.symbols],
            "selection_proof_sha256": self.selection_proof_sha256,
            "selector_inputs": [
                "selector_version",
                "pack_sha256",
                "unix_milliseconds",
                "domain",
                "counter",
            ],
        }


def _material_v1(request: MomentRequest, pack: SymbolPack, counter: int) -> bytes:
    return _UNIT_SEPARATOR.join(
        (
            SELECTOR_VERSION.encode("ascii"),
            pack.sha256.encode("ascii"),
            str(request.unix_milliseconds).encode("ascii"),
            str(counter).encode("ascii"),
        )
    )


def _material_v2(
    request: MomentRequest, pack: SymbolPack, domain: str, counter: int = 0
) -> bytes:
    return _UNIT_SEPARATOR.join(
        (
            SELECTOR_VERSION_V2.encode("ascii"),
            pack.sha256.encode("ascii"),
            str(request.unix_milliseconds).encode("ascii"),
            domain.encode("ascii"),
            str(counter).encode("ascii"),
        )
    )


def _geometry_from_percentile(percentile: int) -> tuple[str, int]:
    if not 0 <= percentile <= 99:
        raise ValueError("geometry percentile must be between 0 and 99")
    if percentile < 85:
        return "point", 1
    if percentile < 97:
        return "triad", 3
    return "constellation", 5


def _select_v1(request: MomentRequest, pack: SymbolPack) -> DrawReceipt:
    wanted = MODE_COUNTS[request.mode]
    selected: list[DrawnSymbol] = []
    used_systems: set[str] = set()
    counter = 0
    while len(selected) < wanted:
        digest = hashlib.sha256(_material_v1(request, pack, counter)).digest()
        system = pack.systems[int.from_bytes(digest[:8], "big") % len(pack.systems)]
        symbol = system.symbols[
            int.from_bytes(digest[8:16], "big") % len(system.symbols)
        ]
        if system.system_id not in used_systems:
            selected.append(
                DrawnSymbol(
                    ordinal=len(selected) + 1,
                    counter=counter,
                    system_id=system.system_id,
                    system_label=system.label,
                    symbol_id=symbol.symbol_id,
                    label=symbol.label,
                    glyph=symbol.glyph,
                    facets=symbol.facets,
                    tradition=symbol.tradition,
                    caution=symbol.caution,
                    derivation_sha256=digest.hex(),
                )
            )
            used_systems.add(system.system_id)
        counter += 1
        if counter > 10_000:
            raise RuntimeError("selector could not form a unique-system field")

    proof_parts = [
        SELECTOR_VERSION,
        pack.sha256,
        str(request.unix_milliseconds),
        request.mode,
        *(item.derivation_sha256 for item in selected),
    ]
    selection_proof = hashlib.sha256("\x1f".join(proof_parts).encode("ascii")).hexdigest()
    return DrawReceipt(
        at_utc=request.canonical_at_utc,
        unix_milliseconds=request.unix_milliseconds,
        pack_id=pack.pack_id,
        pack_sha256=pack.sha256,
        mode=request.mode,
        symbols=tuple(selected),
        selection_proof_sha256=selection_proof,
    )


def _select_v2(request: MomentRequest, pack: SymbolPack) -> DrawReceipt:
    geometry_digest = hashlib.sha256(_material_v2(request, pack, "geometry")).digest()
    explicit = {
        "silence": ("open-center", 0),
        "note": ("point", 1),
        "chord": ("triad", 3),
        "field": ("constellation", 5),
    }
    geometry, wanted = (
        _geometry_from_percentile(int.from_bytes(geometry_digest[:8], "big") % 100)
        if request.mode == "auto"
        else explicit[request.mode]
    )
    selected: list[DrawnSymbol] = []
    used_systems: set[str] = set()
    counter = 0
    while len(selected) < wanted:
        digest = hashlib.sha256(_material_v2(request, pack, "symbol", counter)).digest()
        system = pack.systems[int.from_bytes(digest[:8], "big") % len(pack.systems)]
        symbol = system.symbols[
            int.from_bytes(digest[8:16], "big") % len(system.symbols)
        ]
        if system.system_id not in used_systems:
            selected.append(
                DrawnSymbol(
                    ordinal=len(selected) + 1,
                    role="primary" if not selected else "satellite",
                    counter=counter,
                    system_id=system.system_id,
                    system_label=system.label,
                    symbol_id=symbol.symbol_id,
                    label=symbol.label,
                    glyph=symbol.glyph,
                    facets=symbol.facets,
                    tradition=symbol.tradition,
                    caution=symbol.caution,
                    derivation_sha256=digest.hex(),
                )
            )
            used_systems.add(system.system_id)
        counter += 1
        if counter > 10_000:
            raise RuntimeError("selector could not form a unique-system field")

    proof_parts = [
        SELECTOR_VERSION_V2,
        pack.sha256,
        str(request.unix_milliseconds),
        request.mode,
        geometry,
        geometry_digest.hex(),
        *(item.derivation_sha256 for item in selected),
    ]
    return DrawReceipt(
        at_utc=request.canonical_at_utc,
        unix_milliseconds=request.unix_milliseconds,
        pack_id=pack.pack_id,
        pack_sha256=pack.sha256,
        mode=request.mode,
        geometry=geometry,
        geometry_proof_sha256=geometry_digest.hex(),
        symbols=tuple(selected),
        selection_proof_sha256=hashlib.sha256(
            "\x1f".join(proof_parts).encode("ascii")
        ).hexdigest(),
        schema_version=RECEIPT_SCHEMA_VERSION_V2,
        selector_version=SELECTOR_VERSION_V2,
    )


def select(request: MomentRequest, pack: SymbolPack) -> DrawReceipt:
    """Select an ordered field from time and content-addressed pack only."""

    if request.pack_id != pack.pack_id:
        raise ValueError(
            f"request pack {request.pack_id!r} does not match loaded pack {pack.pack_id!r}"
        )
    if pack.pack_id == "universal-v1":
        return _select_v1(request, pack)
    return _select_v2(request, pack)
