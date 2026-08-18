from altar_ai.process import choose_thinking_depth


AT = "2026-07-15T12:34:56.789Z"
PACK_SHA256 = "a" * 64


def test_thinking_depth_is_time_selected_and_auditable():
    receipt = choose_thinking_depth(AT, PACK_SHA256)
    assert receipt.requested_depth == "auto"
    assert receipt.depth in {3, 6, 9}
    assert receipt.selector_version == "altar-thinking-v1"
    assert len(receipt.derivation_sha256) == 64
    assert receipt.selector_inputs == (
        "selector_version",
        "pack_sha256",
        "unix_milliseconds",
        "domain",
    )
    assert choose_thinking_depth(AT, PACK_SHA256) == receipt


def test_explicit_thinking_depth_is_honored_without_question_content():
    for depth in (3, 6, 9):
        receipt = choose_thinking_depth(AT, PACK_SHA256, depth=depth)
        assert receipt.depth == depth
        assert receipt.requested_depth == str(depth)
        assert "question" not in str(receipt.to_dict()).lower()


def test_invalid_thinking_depth_is_rejected():
    try:
        choose_thinking_depth(AT, PACK_SHA256, depth=4)
    except ValueError as error:
        assert "3, 6, or 9" in str(error)
    else:
        raise AssertionError("invalid depth was accepted")
