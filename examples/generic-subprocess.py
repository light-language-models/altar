#!/usr/bin/env python3
"""Call Altar through its stable JSON stdout boundary from any Python host."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--at", required=True, help="captured UTC event timestamp")
    parser.add_argument(
        "--mode", choices=("silence", "note", "chord", "field"), default="note"
    )
    args = parser.parse_args()
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "altar_ai",
            "draw",
            "--at",
            args.at,
            "--mode",
            args.mode,
            "--pack-id",
            "universal-v1",
            "--json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    json.dump(payload, sys.stdout, ensure_ascii=False, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
