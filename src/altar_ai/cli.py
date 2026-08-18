"""Provider-neutral JSON command line interface."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Any, Sequence

from .contracts import MomentRequest
from .field import compile_field
from .packs import load_pack
from .process import choose_thinking_depth
from .selector import select


_REQUEST_KEYS = {
    "at_utc",
    "mode",
    "pack_id",
    "observer",
    "event_id",
    "timezone_name",
}


def _default_pack_path(pack_id: str) -> Path:
    path = Path(__file__).resolve().parent / "data" / f"{pack_id}.json"
    if not path.is_file():
        raise FileNotFoundError(f"packaged {pack_id} symbol pack is missing")
    return path


def _load_request(raw: Any) -> MomentRequest:
    if not isinstance(raw, dict):
        raise ValueError("request must be a JSON object")
    unknown = set(raw) - _REQUEST_KEYS
    if unknown:
        raise ValueError(f"unknown request keys: {sorted(unknown)}")
    if "at_utc" not in raw:
        raise ValueError("request requires at_utc")
    return MomentRequest(**raw)


def _emit(value: dict[str, object], output: str | None) -> None:
    serialized = json.dumps(
        value, ensure_ascii=False, indent=2, sort_keys=True
    ) + "\n"
    if output:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x", encoding="utf-8") as target:
            target.write(serialized)
    else:
        sys.stdout.write(serialized)


def _pack(path: str | None, pack_id: str):
    return load_pack(Path(path) if path else _default_pack_path(pack_id))


def _instant(args: argparse.Namespace) -> str:
    if args.now:
        current = datetime.now(timezone.utc)
        return current.isoformat(timespec="milliseconds").replace("+00:00", "Z")
    return str(args.at)


def _cmd_draw(args: argparse.Namespace) -> int:
    request = MomentRequest(
        at_utc=_instant(args),
        mode=args.mode,
        pack_id=args.pack_id,
        observer=args.observer,
        event_id=args.event_id,
        timezone_name=args.timezone,
    )
    receipt = select(request, _pack(args.pack_file, request.pack_id))
    _emit(receipt.to_dict(), args.output)
    return 0


def _cmd_field(args: argparse.Namespace) -> int:
    if args.request:
        if args.request == "-":
            raw = json.load(sys.stdin)
        else:
            raw = json.loads(Path(args.request).read_text(encoding="utf-8"))
        request = _load_request(raw)
    else:
        if not args.at and not args.now:
            raise ValueError("field requires --request, --at, or --now")
        request = MomentRequest(
            at_utc=_instant(args),
            mode=args.mode,
            pack_id=args.pack_id,
            observer=args.observer,
            event_id=args.event_id,
            timezone_name=args.timezone,
        )
    receipt = select(request, _pack(args.pack_file, request.pack_id))
    _emit(compile_field(request, receipt).to_dict(), args.output)
    return 0


def _cmd_thinking(args: argparse.Namespace) -> int:
    pack = _pack(args.pack_file, args.pack_id)
    requested_depth: str | int = (
        "auto" if args.depth == "auto" else int(args.depth)
    )
    receipt = choose_thinking_depth(
        _instant(args), pack.sha256, depth=requested_depth
    )
    _emit(receipt.to_dict(), args.output)
    return 0


def _add_instant(parser: argparse.ArgumentParser, *, required: bool = True) -> None:
    group = parser.add_mutually_exclusive_group(required=required)
    group.add_argument("--at", help="UTC timestamp ending in Z")
    group.add_argument("--now", action="store_true", help="use the current UTC instant")


def _add_request_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--mode",
        choices=("auto", "silence", "note", "chord", "field"),
        default="auto",
    )
    parser.add_argument("--pack-id", default="whole-v3")
    parser.add_argument("--pack-file")
    parser.add_argument("--observer", default="unlabeled")
    parser.add_argument("--event-id")
    parser.add_argument("--timezone", default="UTC", help="IANA timezone for the day field")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="altar-ai")
    subparsers = parser.add_subparsers(dest="command", required=True)

    draw = subparsers.add_parser("draw")
    _add_instant(draw)
    _add_request_options(draw)
    draw.add_argument("--output")
    draw.add_argument("--json", action="store_true", help="emit canonical JSON")
    draw.set_defaults(handler=_cmd_draw)

    field = subparsers.add_parser("field")
    field.add_argument("--request", help="JSON file or - for stdin")
    _add_instant(field, required=False)
    _add_request_options(field)
    field.add_argument("--output")
    field.set_defaults(handler=_cmd_field)

    thinking = subparsers.add_parser("thinking")
    _add_instant(thinking)
    thinking.add_argument("--depth", choices=("auto", "3", "6", "9"), default="auto")
    thinking.add_argument("--pack-id", default="whole-v3")
    thinking.add_argument("--pack-file")
    thinking.add_argument("--output")
    thinking.set_defaults(handler=_cmd_thinking)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        return int(args.handler(args))
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
