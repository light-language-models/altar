#!/usr/bin/env python3
"""Install a copied Altar skill into an explicit skill root without overwriting."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil


def install_skill(source: Path, target_root: Path) -> Path:
    source = Path(source).resolve()
    target_root = Path(target_root).expanduser().resolve()
    if not (source / "SKILL.md").is_file():
        raise FileNotFoundError(f"not an Altar skill directory: {source}")
    destination = target_root / "altar"
    target_root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target_root", type=Path, help="explicit destination skill root")
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Altar skill directory (defaults to this bundle)",
    )
    args = parser.parse_args()
    print(install_skill(args.source, args.target_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
