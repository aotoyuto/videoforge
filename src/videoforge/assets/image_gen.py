"""AI image generation providers. (Phase 2 - placeholder)"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Protocol

logger = logging.getLogger(__name__)


class ImageProvider(Protocol):
    """Common interface for image generation providers."""

    def generate(self, prompt: str, width: int, height: int) -> Path:
        """Generate an image from a text prompt. Returns path to saved image."""
        ...


class StabilityProvider:
    """Stability AI image generation. (Phase 2)"""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate(self, prompt: str, width: int = 1920, height: int = 1080) -> Path:
        raise NotImplementedError("Stability AI integration coming in Phase 2")


class DallEProvider:
    """OpenAI DALL-E image generation. (Phase 2)"""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate(self, prompt: str, width: int = 1920, height: int = 1080) -> Path:
        raise NotImplementedError("DALL-E integration coming in Phase 2")
