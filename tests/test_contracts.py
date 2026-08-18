import pytest

from altar_ai.contracts import MODE_COUNTS, MomentRequest, Symbol


def test_moment_request_canonicalizes_utc_to_milliseconds():
    request = MomentRequest(at_utc="2026-07-15T12:34:56.789123Z")
    assert request.canonical_at_utc == "2026-07-15T12:34:56.789Z"
    assert request.unix_milliseconds == 1784118896789


@pytest.mark.parametrize(
    "timestamp",
    ["2026-07-15T12:34:56", "2026-07-15T19:34:56+07:00", "not-a-time"],
)
def test_moment_request_rejects_non_utc_or_invalid_time(timestamp):
    with pytest.raises(ValueError, match="UTC"):
        MomentRequest(at_utc=timestamp)


def test_v2_defaults_and_explicit_modalities_are_frozen():
    assert MODE_COUNTS == {"silence": 0, "note": 1, "chord": 3, "field": 5}
    request = MomentRequest(at_utc="2026-07-15T12:00:00Z")
    assert request.mode == "auto"
    assert request.pack_id == "whole-v3"
    assert request.timezone_name == "UTC"


def test_auto_is_v2_only_and_timezone_must_be_valid():
    with pytest.raises(ValueError, match="auto mode"):
        MomentRequest(
            at_utc="2026-07-15T12:00:00Z",
            mode="auto",
            pack_id="universal-v1",
        )
    with pytest.raises(ValueError, match="timezone"):
        MomentRequest(at_utc="2026-07-15T12:00:00Z", timezone_name="Moon/Sea")


def test_observer_and_event_id_are_absent_from_selector_coordinates():
    first = MomentRequest(
        at_utc="2026-07-15T12:00:00Z",
        observer="unlabeled",
        event_id="local-1",
    )
    second = MomentRequest(
        at_utc="2026-07-15T12:00:00Z",
        observer="higher-self",
        event_id="local-2",
    )
    digest = "a" * 64
    assert first.selector_coordinates(digest) == second.selector_coordinates(digest)
    assert "higher-self" not in "|".join(first.selector_coordinates(digest))


def test_symbol_contract_rejects_unstable_ids_and_empty_facets():
    with pytest.raises(ValueError, match="symbol id"):
        Symbol(
            system_id="elements",
            symbol_id="Fire Element!",
            label="Fire",
            glyph="🜂",
            facets=("transformation",),
            tradition="cross-cultural",
        )
    with pytest.raises(ValueError, match="facets"):
        Symbol(
            system_id="elements",
            symbol_id="fire",
            label="Fire",
            glyph="🜂",
            facets=(),
            tradition="cross-cultural",
        )
