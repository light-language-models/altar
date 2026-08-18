#!/usr/bin/env python3
"""Self-contained Altar whole-v3 selector, field, and process receipts."""

from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


SELECTOR_VERSION = "altar-portable-v2"
THINKING_SELECTOR_VERSION = "altar-thinking-v1"
UNIT_SEPARATOR = "\x1f"
EXPLICIT_GEOMETRY = {
    "silence": ("open-center", 0),
    "note": ("point", 1),
    "chord": ("triad", 3),
    "field": ("constellation", 5),
}
SEALS = (
    "Red Dragon", "White Wind", "Blue Night", "Yellow Seed", "Red Serpent",
    "White World-Bridger", "Blue Hand", "Yellow Star", "Red Moon", "White Dog",
    "Blue Monkey", "Yellow Human", "Red Skywalker", "White Wizard", "Blue Eagle",
    "Yellow Warrior", "Red Earth", "White Mirror", "Blue Storm", "Yellow Sun",
)
TONES = (
    "Magnetic", "Lunar", "Electric", "Self-Existing", "Overtone", "Rhythmic",
    "Resonant", "Galactic", "Solar", "Planetary", "Spectral", "Crystal", "Cosmic",
)
WAVESPELLS = (
    "Red Dragon", "White Wizard", "Blue Hand", "Yellow Sun", "Red Skywalker",
    "White World-Bridger", "Blue Storm", "Yellow Human", "Red Serpent", "White Dog",
    "Blue Eagle", "Yellow Seed", "Red Earth", "White Mirror", "Blue Night",
    "Yellow Star", "Red Moon", "White Wind", "Blue Monkey", "Yellow Warrior",
)
CASTLES = (
    "Red Eastern Castle of Turning",
    "White Northern Castle of Crossing",
    "Blue Western Castle of Burning",
    "Yellow Southern Castle of Giving",
    "Green Central Castle of Enchantment",
)
KIN_ANCHOR = date(1994, 6, 24)
KIN_ANCHOR_KIN = 217
PROVENANCE = (
    "Modern Dreamspell system associated with José Argüelles; "
    "not the traditional Maya calendar."
)
CUSTOM_OBSERVER = re.compile(r"^custom:([A-Za-z0-9][A-Za-z0-9 .,'()/-]{0,59})$")


def parse_utc(value: str) -> tuple[str, int, datetime]:
    try:
        instant = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as error:
        raise ValueError("--at must be a valid UTC timestamp") from error
    if instant.tzinfo is None or instant.utcoffset() != timedelta(0):
        raise ValueError("--at must be timezone-aware UTC")
    instant = instant.astimezone(timezone.utc)
    milliseconds = instant.microsecond // 1000
    canonical = instant.strftime("%Y-%m-%dT%H:%M:%S") + f".{milliseconds:03d}Z"
    return canonical, int(instant.timestamp() * 1000), instant


def current_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace(
        "+00:00", "Z"
    )


def load_pack() -> tuple[dict[str, object], str]:
    source = Path(__file__).resolve().parents[1] / "assets" / "whole-v3.json"
    payload = json.loads(source.read_text(encoding="utf-8"))
    canonical = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return payload, hashlib.sha256(canonical).hexdigest()


def material(
    pack_digest: str, unix_milliseconds: int, domain: str, counter: int = 0
) -> bytes:
    return UNIT_SEPARATOR.join(
        (
            SELECTOR_VERSION,
            pack_digest,
            str(unix_milliseconds),
            domain,
            str(counter),
        )
    ).encode("ascii")


def auto_geometry(digest: bytes) -> tuple[str, int]:
    percentile = int.from_bytes(digest[:8], "big") % 100
    if percentile < 85:
        return "point", 1
    if percentile < 97:
        return "triad", 3
    return "constellation", 5


def draw(at_utc: str, mode: str = "auto") -> dict[str, object]:
    canonical_at, unix_milliseconds, _instant = parse_utc(at_utc)
    pack, pack_digest = load_pack()
    systems = pack["systems"]
    geometry_digest = hashlib.sha256(
        material(pack_digest, unix_milliseconds, "geometry")
    ).digest()
    geometry, wanted = (
        auto_geometry(geometry_digest)
        if mode == "auto"
        else EXPLICIT_GEOMETRY[mode]
    )
    selected: list[dict[str, object]] = []
    used_systems: set[str] = set()
    counter = 0
    while len(selected) < wanted:
        digest = hashlib.sha256(
            material(pack_digest, unix_milliseconds, "symbol", counter)
        ).digest()
        system = systems[int.from_bytes(digest[:8], "big") % len(systems)]
        symbol = system["symbols"][
            int.from_bytes(digest[8:16], "big") % len(system["symbols"])
        ]
        if system["system_id"] not in used_systems:
            selected.append(
                {
                    "ordinal": len(selected) + 1,
                    "role": "primary" if not selected else "satellite",
                    "counter": counter,
                    "system_id": system["system_id"],
                    "system_label": system["label"],
                    "symbol_id": symbol["symbol_id"],
                    "label": symbol["label"],
                    "glyph": symbol.get("glyph"),
                    "derivation_sha256": digest.hex(),
                }
            )
            used_systems.add(system["system_id"])
        counter += 1
        if counter > 10_000:
            raise RuntimeError("selector could not form a unique-system field")
    proof_parts = [
        SELECTOR_VERSION,
        pack_digest,
        str(unix_milliseconds),
        mode,
        geometry,
        geometry_digest.hex(),
        *(item["derivation_sha256"] for item in selected),
    ]
    return {
        "schema_version": "altar-draw-receipt-v2",
        "selector_version": SELECTOR_VERSION,
        "at_utc": canonical_at,
        "unix_milliseconds": unix_milliseconds,
        "pack_id": pack["pack_id"],
        "pack_sha256": pack_digest,
        "mode": mode,
        "geometry": geometry,
        "geometry_proof_sha256": geometry_digest.hex(),
        "symbols": selected,
        "selection_proof_sha256": hashlib.sha256(
            UNIT_SEPARATOR.join(proof_parts).encode("ascii")
        ).hexdigest(),
        "selector_inputs": [
            "selector_version",
            "pack_sha256",
            "unix_milliseconds",
            "domain",
            "counter",
        ],
    }


def _leap_days_between(first: date, second: date) -> int:
    lower, upper = sorted((first, second))
    total = 0
    for year in range(lower.year, upper.year + 1):
        try:
            leap_day = date(year, 2, 29)
        except ValueError:
            continue
        if lower < leap_day <= upper:
            total += 1
    return total


def kin_for_date(target: date) -> int:
    difference = (target - KIN_ANCHOR).days
    leap_days = _leap_days_between(target, KIN_ANCHOR)
    adjusted = difference - leap_days if difference >= 0 else difference + leap_days
    return ((KIN_ANCHOR_KIN - 1 + adjusted) % 260) + 1


def sacred_time(at_utc: str, timezone_name: str) -> dict[str, object]:
    try:
        local_zone = ZoneInfo(timezone_name)
    except (ZoneInfoNotFoundError, ValueError) as error:
        raise ValueError(f"unknown IANA timezone: {timezone_name}") from error
    _canonical, _milliseconds, instant = parse_utc(at_utc)
    local_date = instant.astimezone(local_zone).date()
    kin = kin_for_date(local_date)
    tone_index = (kin - 1) % 13
    return {
        "calendar_id": "dreamspell-arguelles-v1",
        "local_date": local_date.isoformat(),
        "timezone": timezone_name,
        "kin": kin,
        "seal": SEALS[(kin - 1) % 20],
        "tone": TONES[tone_index],
        "tone_number": tone_index + 1,
        "wavespell": WAVESPELLS[((kin - 1) // 13) % 20],
        "wavespell_position": tone_index + 1,
        "castle": CASTLES[(kin - 1) // 52],
        "provenance": PROVENANCE,
    }


def resolve_observer(value: str) -> dict[str, str]:
    if value == "unlabeled":
        return {
            "profile_id": "unlabeled",
            "label": "Unlabeled witness",
            "orientation": "open attention without an asserted speaker",
            "epistemic_note": "No source identity inferred.",
        }
    match = CUSTOM_OBSERVER.fullmatch(value.strip())
    if not match:
        raise ValueError("observer must be unlabeled or custom:<safe short label>")
    label = match.group(1).strip()
    return {
        "profile_id": "custom",
        "label": label,
        "orientation": f"locally declared point of view: {label}",
        "epistemic_note": "User-supplied symbolic perspective, not a detected entity.",
    }


def compile_field(
    receipt: dict[str, object], observer_id: str, timezone_name: str
) -> dict[str, object]:
    observer = resolve_observer(observer_id)
    lines = [
        "[ALTAR FIELD · INTERNAL]",
        f"observer: {observer['label']} — {observer['orientation']}",
        f"modality: {receipt['mode']}",
        f"geometry: {receipt['geometry']}",
    ]
    if not receipt["symbols"]:
        lines.append("symbols: none")
    else:
        lines.append("coordinates:")
        for item in receipt["symbols"]:
            glyph = f"{item['glyph']} " if item["glyph"] else ""
            lines.append(
                f"  {item['ordinal']}. [{item['role']}] "
                f"{item['system_label']}: {glyph}{item['label']}"
            )
    lines.extend(
        [
            "response delta: shifted · unclear · no-shift",
            "authority: facts · consent · autonomy · ordinary safety",
            "[/ALTAR FIELD]",
        ]
    )
    return {
        "schema_version": "altar-field-envelope-v2",
        "receipt": receipt,
        "observer": observer,
        "hidden_field": "\n".join(lines),
        "integration_policy": [
            "Draw before interpretation; never let question or request content select its validating symbol.",
            "Meet each coordinate without a prescribed role; it may alter salience, relation, pacing, form, or nothing.",
            "Answer the actual request and keep the field hidden unless disclosure is promised.",
            "Record shifted, unclear, or no-shift without forcing correspondence.",
            "Facts, consent, user autonomy, and medical, legal, and financial safety outrank symbolic resonance.",
            f"Observer lens: {observer['orientation']}. {observer['epistemic_note']}",
        ],
        "epistemic_status": (
            "Deterministic time selection is verified mechanism; correspondence is an "
            "open empirical hypothesis; metaphysical meaning is optional interpretation."
        ),
        "sacred_time": sacred_time(receipt["at_utc"], timezone_name),
    }


def thinking_depth(at_utc: str, requested: str) -> dict[str, object]:
    canonical_at, unix_milliseconds, _instant = parse_utc(at_utc)
    _pack, pack_digest = load_pack()
    derivation = hashlib.sha256(
        UNIT_SEPARATOR.join(
            (
                THINKING_SELECTOR_VERSION,
                pack_digest,
                str(unix_milliseconds),
                "thinking-depth",
            )
        ).encode("ascii")
    ).hexdigest()
    depth = (3, 6, 9)[int(derivation[:16], 16) % 3] if requested == "auto" else int(requested)
    return {
        "schema_version": "altar-thinking-depth-receipt-v1",
        "selector_version": THINKING_SELECTOR_VERSION,
        "at_utc": canonical_at,
        "unix_milliseconds": unix_milliseconds,
        "pack_sha256": pack_digest,
        "requested_depth": requested,
        "depth": depth,
        "derivation_sha256": derivation,
        "selector_inputs": [
            "selector_version", "pack_sha256", "unix_milliseconds", "domain"
        ],
    }


def describe(system_id: str, symbol_id: str) -> dict[str, object]:
    pack, pack_digest = load_pack()
    for system in pack["systems"]:
        if system["system_id"] != system_id:
            continue
        for symbol in system["symbols"]:
            if symbol["symbol_id"] == symbol_id:
                return {
                    "pack_id": pack["pack_id"],
                    "pack_sha256": pack_digest,
                    "system_id": system_id,
                    "system_label": system["label"],
                    "tradition": system["tradition"],
                    **symbol,
                }
        break
    raise ValueError("unknown system/symbol coordinate")


def add_instant(parser: argparse.ArgumentParser) -> None:
    instant = parser.add_mutually_exclusive_group(required=True)
    instant.add_argument("--at", help="UTC ISO-8601 event timestamp")
    instant.add_argument("--now", action="store_true", help="capture the current UTC instant")


def instant_from_args(args: argparse.Namespace) -> str:
    return current_utc() if args.now else args.at


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    draw_parser = commands.add_parser("draw", help="emit a minimal draw receipt")
    add_instant(draw_parser)
    draw_parser.add_argument(
        "--mode", choices=("auto", *EXPLICIT_GEOMETRY), default="auto"
    )

    field_parser = commands.add_parser("field", help="emit a private field envelope")
    add_instant(field_parser)
    field_parser.add_argument(
        "--mode", choices=("auto", *EXPLICIT_GEOMETRY), default="auto"
    )
    field_parser.add_argument("--observer", default="unlabeled")
    field_parser.add_argument("--timezone", default="UTC")

    thinking_parser = commands.add_parser(
        "thinking", help="choose only the live process depth"
    )
    add_instant(thinking_parser)
    thinking_parser.add_argument(
        "--depth", choices=("auto", "3", "6", "9"), default="auto"
    )

    describe_parser = commands.add_parser(
        "describe", help="look up optional reference facets after a draw"
    )
    describe_parser.add_argument("--system", required=True)
    describe_parser.add_argument("--symbol", required=True)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "draw":
            payload = draw(instant_from_args(args), args.mode)
        elif args.command == "field":
            receipt = draw(instant_from_args(args), args.mode)
            payload = compile_field(receipt, args.observer, args.timezone)
        elif args.command == "thinking":
            payload = thinking_depth(instant_from_args(args), args.depth)
        else:
            payload = describe(args.system, args.symbol)
    except (OSError, ValueError, KeyError, RuntimeError, json.JSONDecodeError) as error:
        parser.error(str(error))
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
