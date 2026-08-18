from datetime import date

from altar_ai.sacred_time import dreamspell_context, kin_for_date


def test_dreamspell_verified_anchors_are_stable():
    assert kin_for_date(date(1994, 6, 24)) == 217
    assert kin_for_date(date(2013, 7, 26)) == 164
    assert kin_for_date(date(2026, 2, 18)) == 71
    assert kin_for_date(date(2026, 7, 12)) == 215


def test_february_29_is_an_uncounted_dreamspell_day():
    assert kin_for_date(date(2028, 2, 29)) == kin_for_date(date(2028, 2, 28))
    assert kin_for_date(date(2028, 3, 1)) == (kin_for_date(date(2028, 2, 28)) % 260) + 1


def test_explicit_timezone_controls_the_local_day_field():
    utc = dreamspell_context("2026-07-12T18:30:00.000Z", "UTC")
    bangkok = dreamspell_context("2026-07-12T18:30:00.000Z", "Asia/Bangkok")
    assert utc.local_date == "2026-07-12"
    assert bangkok.local_date == "2026-07-13"
    assert utc.kin == 215
    assert bangkok.kin == 216


def test_context_names_modern_dreamspell_without_claiming_traditional_maya_lineage():
    context = dreamspell_context("2026-07-12T12:00:00.000Z", "UTC")
    payload = context.to_dict()
    assert payload["calendar_id"] == "dreamspell-arguelles-v1"
    assert payload["kin"] == 215
    assert payload["tone_number"] == 7
    assert payload["seal"] == "Blue Eagle"
    assert payload["wavespell"] == "Red Moon"
    assert payload["wavespell_position"] == 7
    assert "modern dreamspell" in payload["provenance"].lower()
    assert "not the traditional maya calendar" in payload["provenance"].lower()
    assert "is_gap" not in payload
    assert "gap" not in payload
