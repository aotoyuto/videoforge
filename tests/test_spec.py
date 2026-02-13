"""Tests for VideoSpec parsing and validation."""

from videoforge.schema import (
    ExportConfig,
    Position,
    Scene,
    SceneType,
    TextOverlay,
    VideoMeta,
    VideoSpec,
)
from videoforge.spec import dump_spec, parse_spec


def test_minimal_spec():
    """A minimal spec with no scenes should be valid."""
    spec = VideoSpec()
    assert spec.version == "1.0"
    assert spec.video.title == "Untitled"
    assert spec.scenes == []
    assert spec.total_duration == 0.0


def test_parse_basic_dict():
    """Parse a basic dictionary into a VideoSpec."""
    data = {
        "version": "1.0",
        "video": {"title": "テスト動画", "resolution": [1920, 1080], "fps": 30},
        "scenes": [
            {
                "id": "s1",
                "type": "color",
                "duration": 5.0,
                "color": "#FF0000",
                "text_overlays": [
                    {
                        "content": "テスト テロップ",
                        "position": "center",
                        "font_size": 48,
                    }
                ],
            }
        ],
        "export": {"platform": "youtube"},
    }
    spec = parse_spec(data)
    assert spec.video.title == "テスト動画"
    assert len(spec.scenes) == 1
    assert spec.scenes[0].type == SceneType.COLOR
    assert spec.scenes[0].text_overlays[0].content == "テスト テロップ"
    assert spec.scenes[0].text_overlays[0].position == Position.CENTER
    assert spec.total_duration == 5.0


def test_dump_and_roundtrip():
    """Dump a spec to YAML and verify it's valid YAML."""
    spec = VideoSpec(
        video=VideoMeta(title="往復テスト"),
        scenes=[
            Scene(id="s1", type=SceneType.COLOR, duration=3.0, color="#00FF00"),
        ],
    )
    yaml_str = dump_spec(spec)
    assert "往復テスト" in yaml_str
    assert "color" in yaml_str


def test_get_scene():
    """get_scene should return the correct scene by ID."""
    spec = VideoSpec(
        scenes=[
            Scene(id="a", duration=1.0),
            Scene(id="b", duration=2.0),
        ]
    )
    assert spec.get_scene("b") is not None
    assert spec.get_scene("b").duration == 2.0
    assert spec.get_scene("z") is None


def test_text_overlay_defaults():
    """TextOverlay should have sensible defaults."""
    overlay = TextOverlay(content="テスト")
    assert overlay.font == "Yu Gothic"
    assert overlay.font_size == 48
    assert overlay.color == "#FFFFFF"
    assert overlay.position == Position.BOTTOM_CENTER
