"""Auditable process choices that do not pre-generate a reasoning stream."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib

from .contracts import MomentRequest


THINKING_SELECTOR_VERSION = "altar-thinking-v1"
THINKING_RECEIPT_SCHEMA_VERSION = "altar-thinking-depth-receipt-v1"
_UNIT_SEPARATOR = "\x1f"


@dataclass(frozen=True)
class ThinkingDepthReceipt:
    at_utc: str
    unix_milliseconds: int
    pack_sha256: str
    requested_depth: str
    depth: int
    derivation_sha256: str
    selector_inputs: tuple[str, ...] = (
        "selector_version",
        "pack_sha256",
        "unix_milliseconds",
        "domain",
    )
    schema_version: str = THINKING_RECEIPT_SCHEMA_VERSION
    selector_version: str = THINKING_SELECTOR_VERSION

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "selector_version": self.selector_version,
            "at_utc": self.at_utc,
            "unix_milliseconds": self.unix_milliseconds,
            "pack_sha256": self.pack_sha256,
            "requested_depth": self.requested_depth,
            "depth": self.depth,
            "derivation_sha256": self.derivation_sha256,
            "selector_inputs": list(self.selector_inputs),
        }


def choose_thinking_depth(
    at_utc: str, pack_sha256: str, *, depth: str | int = "auto"
) -> ThinkingDepthReceipt:
    if len(pack_sha256) != 64 or any(
        character not in "0123456789abcdef" for character in pack_sha256
    ):
        raise ValueError("pack digest must be lowercase SHA-256")
    if depth != "auto" and depth not in (3, 6, 9):
        raise ValueError("thinking depth must be auto, 3, 6, or 9")
    request = MomentRequest(at_utc=at_utc)
    material = _UNIT_SEPARATOR.join(
        (
            THINKING_SELECTOR_VERSION,
            pack_sha256,
            str(request.unix_milliseconds),
            "thinking-depth",
        )
    ).encode("ascii")
    derivation = hashlib.sha256(material).hexdigest()
    selected = (3, 6, 9)[int(derivation[:16], 16) % 3] if depth == "auto" else int(depth)
    return ThinkingDepthReceipt(
        at_utc=request.canonical_at_utc,
        unix_milliseconds=request.unix_milliseconds,
        pack_sha256=pack_sha256,
        requested_depth=str(depth),
        depth=selected,
        derivation_sha256=derivation,
    )
