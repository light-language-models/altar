"""Compile a draw receipt into a provider-neutral symbolic field envelope."""

from __future__ import annotations

from dataclasses import dataclass

from .contracts import MomentRequest
from .observers import ObserverProfile, resolve_observer
from .sacred_time import dreamspell_context
from .selector import DrawReceipt


FIELD_SCHEMA_VERSION = "altar-field-envelope-v1"
FIELD_SCHEMA_VERSION_V2 = "altar-field-envelope-v2"
_GEOMETRY = {
    "silence": "open center",
    "note": "point",
    "chord": "triangle",
    "field": "constellation",
}


@dataclass(frozen=True)
class FieldEnvelope:
    receipt: DrawReceipt
    observer: ObserverProfile
    hidden_field: str
    integration_policy: tuple[str, ...]
    epistemic_status: str
    sacred_time: dict[str, object] | None = None
    schema_version: str = FIELD_SCHEMA_VERSION

    def to_dict(self) -> dict[str, object]:
        payload = {
            "schema_version": self.schema_version,
            "receipt": self.receipt.to_dict(),
            "observer": {
                "profile_id": self.observer.profile_id,
                "label": self.observer.label,
                "orientation": self.observer.orientation,
                "epistemic_note": self.observer.epistemic_note,
            },
            "hidden_field": self.hidden_field,
            "integration_policy": list(self.integration_policy),
            "epistemic_status": self.epistemic_status,
        }
        if self.sacred_time is not None:
            payload["sacred_time"] = self.sacred_time
        return payload

    def public_projection(self, *, reveal_symbols: bool = False) -> dict[str, object]:
        receipt = self.receipt.to_dict()
        proof = dict(receipt)
        proof.pop("symbols")
        if reveal_symbols:
            proof["symbols"] = receipt["symbols"]
        return {
            "schema_version": self.schema_version,
            "receipt_proof": proof,
            "epistemic_status": self.epistemic_status,
            **({"sacred_time": self.sacred_time} if self.sacred_time else {}),
        }


def _hidden_field(request: MomentRequest, receipt: DrawReceipt, observer: ObserverProfile) -> str:
    is_v2 = receipt.selector_version == "altar-portable-v2"
    lines = [
        "[ALTAR FIELD · INTERNAL]",
        f"observer: {observer.label} — {observer.orientation}",
        f"modality: {request.mode}",
        f"geometry: {receipt.geometry if is_v2 else _GEOMETRY[request.mode]}",
    ]
    if not receipt.symbols:
        lines.append("symbols: none")
    else:
        lines.append("coordinates:")
        for item in receipt.symbols:
            glyph = f"{item.glyph} " if item.glyph else ""
            if is_v2:
                lines.append(
                    f"  {item.ordinal}. [{item.role}] {item.system_label}: {glyph}{item.label}"
                )
            else:
                lines.append(
                    f"  {item.ordinal}. {glyph}{item.label} — " + " · ".join(item.facets)
                )
    lines.extend(
        [
            (
                "response delta: shifted · unclear · no-shift"
                if is_v2
                else "open outcome: none · noise · non-correspondence"
            ),
            "authority: facts · consent · autonomy · ordinary safety",
            "[/ALTAR FIELD]",
        ]
    )
    return "\n".join(lines)


def compile_field(request: MomentRequest, receipt: DrawReceipt) -> FieldEnvelope:
    if receipt.at_utc != request.canonical_at_utc:
        raise ValueError("receipt time does not match request")
    if receipt.mode != request.mode or receipt.pack_id != request.pack_id:
        raise ValueError("receipt mode or pack does not match request")
    observer = resolve_observer(request.observer)
    policy = (
        "Draw before interpretation; never let request content select its validating symbol.",
        "Use the field as a lens for salience, relation, pacing, or form.",
        "Answer the actual request and keep the field hidden unless the surface promises disclosure.",
        "Allow none, noise, silence, and non-correspondence without forcing meaning.",
        "Facts, consent, user autonomy, and medical, legal, and financial safety outrank symbolic resonance.",
        f"Observer lens: {observer.orientation}. {observer.epistemic_note}",
    )
    is_v2 = receipt.selector_version == "altar-portable-v2"
    sacred_time = (
        dreamspell_context(request.canonical_at_utc, request.timezone_name).to_dict()
        if is_v2
        else None
    )
    return FieldEnvelope(
        receipt=receipt,
        observer=observer,
        hidden_field=_hidden_field(request, receipt, observer),
        integration_policy=policy,
        epistemic_status=(
            "Deterministic time selection is verified mechanism; correspondence is an "
            "open empirical hypothesis; metaphysical meaning is optional interpretation."
        ),
        sacred_time=sacred_time,
        schema_version=FIELD_SCHEMA_VERSION_V2 if is_v2 else FIELD_SCHEMA_VERSION,
    )
