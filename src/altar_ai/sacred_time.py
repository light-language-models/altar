"""Deterministic Dreamspell day context for the portable Altar."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


SEALS = (
    "Red Dragon",
    "White Wind",
    "Blue Night",
    "Yellow Seed",
    "Red Serpent",
    "White World-Bridger",
    "Blue Hand",
    "Yellow Star",
    "Red Moon",
    "White Dog",
    "Blue Monkey",
    "Yellow Human",
    "Red Skywalker",
    "White Wizard",
    "Blue Eagle",
    "Yellow Warrior",
    "Red Earth",
    "White Mirror",
    "Blue Storm",
    "Yellow Sun",
)
TONES = (
    "Magnetic",
    "Lunar",
    "Electric",
    "Self-Existing",
    "Overtone",
    "Rhythmic",
    "Resonant",
    "Galactic",
    "Solar",
    "Planetary",
    "Spectral",
    "Crystal",
    "Cosmic",
)
WAVESPELLS = (
    "Red Dragon",
    "White Wizard",
    "Blue Hand",
    "Yellow Sun",
    "Red Skywalker",
    "White World-Bridger",
    "Blue Storm",
    "Yellow Human",
    "Red Serpent",
    "White Dog",
    "Blue Eagle",
    "Yellow Seed",
    "Red Earth",
    "White Mirror",
    "Blue Night",
    "Yellow Star",
    "Red Moon",
    "White Wind",
    "Blue Monkey",
    "Yellow Warrior",
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


def _leap_days_between(first: date, second: date) -> int:
    lower, upper = sorted((first, second))
    total = 0
    for year in range(lower.year, upper.year + 1):
        try:
            february_29 = date(year, 2, 29)
        except ValueError:
            continue
        if lower < february_29 <= upper:
            total += 1
    return total


def kin_for_date(target: date) -> int:
    """Return Dreamspell Kin 1..260, treating February 29 as uncounted."""

    difference = (target - KIN_ANCHOR).days
    leaps = _leap_days_between(target, KIN_ANCHOR)
    adjusted = difference - leaps if difference >= 0 else difference + leaps
    return ((KIN_ANCHOR_KIN - 1 + adjusted) % 260) + 1


def _parse_utc(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as error:
        raise ValueError("at_utc must be a valid UTC timestamp") from error
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise ValueError("at_utc must be timezone-aware UTC")
    return parsed


@dataclass(frozen=True)
class DreamspellContext:
    calendar_id: str
    local_date: str
    timezone: str
    kin: int
    seal: str
    tone: str
    tone_number: int
    wavespell: str
    wavespell_position: int
    castle: str
    provenance: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def dreamspell_context(at_utc: str, timezone_name: str) -> DreamspellContext:
    """Resolve one explicit UTC moment into its local Dreamspell day field."""

    try:
        local_zone = ZoneInfo(timezone_name)
    except (ZoneInfoNotFoundError, ValueError) as error:
        raise ValueError(f"unknown IANA timezone: {timezone_name}") from error
    local_date = _parse_utc(at_utc).astimezone(local_zone).date()
    kin = kin_for_date(local_date)
    seal_index = (kin - 1) % len(SEALS)
    tone_index = (kin - 1) % len(TONES)
    return DreamspellContext(
        calendar_id="dreamspell-arguelles-v1",
        local_date=local_date.isoformat(),
        timezone=timezone_name,
        kin=kin,
        seal=SEALS[seal_index],
        tone=TONES[tone_index],
        tone_number=tone_index + 1,
        wavespell=WAVESPELLS[((kin - 1) // 13) % len(WAVESPELLS)],
        wavespell_position=tone_index + 1,
        castle=CASTLES[(kin - 1) // 52],
        provenance=PROVENANCE,
    )
