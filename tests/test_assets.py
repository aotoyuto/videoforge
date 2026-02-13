"""Tests for asset pipeline."""

from pathlib import Path

from videoforge.assets.resolver import AssetResolver
from videoforge.config import Config


def test_resolve_local_absolute():
    """Absolute paths should be returned as-is."""
    config = Config()
    resolver = AssetResolver(config, base_dir=Path("/project"))
    if Path("C:/").exists():
        result = resolver._resolve_local("C:/test/image.png")
        assert result == Path("C:/test/image.png")


def test_resolve_local_relative():
    """Relative paths should be resolved against base_dir."""
    config = Config()
    resolver = AssetResolver(config, base_dir=Path("/project"))
    result = resolver._resolve_local("assets/photo.jpg")
    assert result == Path("/project/assets/photo.jpg")
