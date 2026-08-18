"""Immutable contracts for the portable Altar boundary."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import re
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


SELECTOR_VERSION = "altar-portable-v1"
SELECTOR_VERSION_V2 = "altar-portable-v2"
PACK_SCHEMA_VERSION = "altar-symbol-pack-v1"
MODE_COUNTS = {"silence": 0, "note": 1, "chord": 3, "field": 5}
VALID_MODES = frozenset((*MODE_COUNTS, "auto"))
_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _parse_utc(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as error:
        raise ValueError("at_utc must be a valid UTC timestamp") from error
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise ValueError("at_utc must be timezone-aware UTC")
    return parsed.astimezone(timezone.utc)


@dataclass(frozen=True)
class MomentRequest:
    at_utc: str
    mode: str = "auto"
    pack_id: str = "whole-v3"
    observer: str = "unlabeled"
    event_id: str | None = None
    timezone_name: str = "UTC"

    def __post_init__(self) -> None:
        _parse_utc(self.at_utc)
        if self.mode not in VALID_MODES:
            raise ValueError(f"unknown mode: {self.mode}")
        if self.mode == "auto" and self.pack_id != "whole-v3":
            raise ValueError("auto mode requires the whole-v3 selector")
        if not _ID_RE.fullmatch(self.pack_id):
            raise ValueError("pack id must use lowercase hyphen-case")
        if not self.observer.strip() or len(self.observer) > 80:
            raise ValueError("observer must be a short non-empty label")
        if self.event_id is not None and (not self.event_id.strip() or len(self.event_id) > 200):
            raise ValueError("event id must be a short non-empty value")
        try:
            ZoneInfo(self.timezone_name)
        except (ZoneInfoNotFoundError, ValueError) as error:
            raise ValueError("timezone_name must be a valid IANA timezone") from error

    @property
    def instant(self) -> datetime:
        return _parse_utc(self.at_utc)

    @property
    def unix_milliseconds(self) -> int:
        return int(self.instant.timestamp() * 1000)

    @property
    def canonical_at_utc(self) -> str:
        instant = self.instant
        milliseconds = instant.microsecond // 1000
        return instant.strftime("%Y-%m-%dT%H:%M:%S") + f".{milliseconds:03d}Z"

    def selector_coordinates(self, pack_sha256: str) -> tuple[str, str, str]:
        if len(pack_sha256) != 64 or any(
            character not in "0123456789abcdef" for character in pack_sha256
        ):
            raise ValueError("pack digest must be lowercase SHA-256")
        version = SELECTOR_VERSION if self.pack_id == "universal-v1" else SELECTOR_VERSION_V2
        return version, pack_sha256, str(self.unix_milliseconds)


@dataclass(frozen=True)
class Symbol:
    system_id: str
    symbol_id: str
    label: str
    glyph: str | None
    facets: tuple[str, ...]
    tradition: str
    caution: str | None = None

    def __post_init__(self) -> None:
        if not _ID_RE.fullmatch(self.system_id):
            raise ValueError("system id must use lowercase hyphen-case")
        if not _ID_RE.fullmatch(self.symbol_id):
            raise ValueError("symbol id must use lowercase hyphen-case")
        if not self.label.strip() or not self.tradition.strip():
            raise ValueError("symbol label and tradition are required")
        if not self.facets or any(not facet.strip() for facet in self.facets):
            raise ValueError("symbol facets must contain non-empty values")


@dataclass(frozen=True)
class SymbolSystem:
    system_id: str
    label: str
    tradition: str
    symbols: tuple[Symbol, ...]

    def __post_init__(self) -> None:
        if not _ID_RE.fullmatch(self.system_id):
            raise ValueError("system id must use lowercase hyphen-case")
        if not self.label.strip() or not self.tradition.strip() or not self.symbols:
            raise ValueError("symbol system requires label, tradition, and symbols")
        if any(symbol.system_id != self.system_id for symbol in self.symbols):
            raise ValueError("symbol belongs to another system")
        ids = [symbol.symbol_id for symbol in self.symbols]
        if len(ids) != len(set(ids)):
            raise ValueError(f"duplicate symbol in system {self.system_id}")


@dataclass(frozen=True)
class SymbolPack:
    pack_id: str
    title: str
    description: str
    systems: tuple[SymbolSystem, ...]
    sha256: str
    schema_version: str = PACK_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != PACK_SCHEMA_VERSION:
            raise ValueError(f"unknown pack schema: {self.schema_version}")
        if not _ID_RE.fullmatch(self.pack_id):
            raise ValueError("pack id must use lowercase hyphen-case")
        if not self.title.strip() or not self.description.strip() or not self.systems:
            raise ValueError("pack title, description, and systems are required")
        ids = [system.system_id for system in self.systems]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate symbol system")
        if len(self.sha256) != 64:
            raise ValueError("pack digest must be SHA-256")
