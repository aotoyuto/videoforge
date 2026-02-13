"""Tests for rendering functions (basic unit tests)."""

from videoforge.render.transitions import XFADE_MAP


def test_xfade_map_has_expected_transitions():
    """XFADE_MAP should map our transition names to FFmpeg xfade names."""
    assert "fade" in XFADE_MAP
    assert "crossfade" in XFADE_MAP
    assert "wipe_left" in XFADE_MAP
    assert "dissolve" in XFADE_MAP


def test_xfade_map_values():
    """FFmpeg xfade names should be valid."""
    assert XFADE_MAP["fade"] == "fade"
    assert XFADE_MAP["wipe_left"] == "wipeleft"
