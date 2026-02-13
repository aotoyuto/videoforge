"""Asset resolver - determines how to obtain each asset (local file, URL, AI generation)."""

from __future__ import annotations

import logging
from pathlib import Path

from ..config import Config

logger = logging.getLogger(__name__)


class AssetResolver:
    """Resolves asset references to actual file paths.

    Handles local files, URLs (future), and AI generation (future).
    """

    def __init__(self, config: Config, base_dir: Path | None = None):
        self.config = config
        self.base_dir = base_dir or Path(".")

    def resolve_image(self, source: str | None, prompt: str | None = None) -> Path | None:
        """Resolve an image source to a local file path."""
        if source:
            return self._resolve_local(source)
        if prompt:
            return self._generate_image(prompt)
        return None

    def resolve_audio(self, source: str | None, prompt: str | None = None) -> Path | None:
        """Resolve an audio source to a local file path."""
        if source:
            return self._resolve_local(source)
        if prompt:
            return self._generate_music(prompt)
        return None

    def resolve_video(self, source: str | None, prompt: str | None = None) -> Path | None:
        """Resolve a video source to a local file path."""
        if source:
            return self._resolve_local(source)
        if prompt:
            return self._generate_video(prompt)
        return None

    def _resolve_local(self, source: str) -> Path:
        """Resolve a local file path."""
        p = Path(source)
        if p.is_absolute():
            return p
        return self.base_dir / p

    def _generate_image(self, prompt: str) -> Path | None:
        """Generate an image using AI. Placeholder for Phase 2."""
        logger.warning("AI image generation not yet implemented. Prompt: %s", prompt)
        return None

    def _generate_music(self, prompt: str) -> Path | None:
        """Generate music using AI. Placeholder for Phase 2."""
        logger.warning("AI music generation not yet implemented. Prompt: %s", prompt)
        return None

    def _generate_video(self, prompt: str) -> Path | None:
        """Generate video using AI. Placeholder for Phase 3."""
        logger.warning("AI video generation not yet implemented. Prompt: %s", prompt)
        return None
