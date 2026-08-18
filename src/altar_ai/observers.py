"""Optional observer lenses applied after selection."""

from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class ObserverProfile:
    profile_id: str
    label: str
    orientation: str
    epistemic_note: str


_BUILT_INS = {
    "unlabeled": ObserverProfile(
        profile_id="unlabeled",
        label="Unlabeled witness",
        orientation="open attention without an asserted speaker",
        epistemic_note="No source identity inferred.",
    ),
    "higher-self": ObserverProfile(
        profile_id="higher-self",
        label="Higher Self",
        orientation="the wider continuity and long horizon of the self",
        epistemic_note="Opt-in symbolic perspective, not a detected entity.",
    ),
    "earth": ObserverProfile(
        profile_id="earth",
        label="Earth",
        orientation="embodiment, ecology, limits, and mutual dependence",
        epistemic_note="Opt-in symbolic perspective, not a factual attribution.",
    ),
    "ancestors": ObserverProfile(
        profile_id="ancestors",
        label="Ancestors",
        orientation="inheritance, continuity, debt, and received support",
        epistemic_note="Opt-in symbolic perspective, not verified contact.",
    ),
}
_CUSTOM_RE = re.compile(r"^custom:([A-Za-z0-9][A-Za-z0-9 .,'()/-]{0,59})$")


def resolve_observer(value: str) -> ObserverProfile:
    normalized = value.strip().lower()
    if normalized in _BUILT_INS:
        return _BUILT_INS[normalized]
    match = _CUSTOM_RE.fullmatch(value.strip())
    if not match:
        raise ValueError(
            "observer must be a built-in id or custom: followed by a safe short label"
        )
    label = match.group(1).strip()
    return ObserverProfile(
        profile_id="custom",
        label=label,
        orientation=f"locally declared point of view: {label}",
        epistemic_note="User-supplied symbolic perspective, not a detected entity.",
    )
