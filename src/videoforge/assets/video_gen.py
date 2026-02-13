"""AI video generation providers. (Phase 3 - placeholder)"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Protocol

logger = logging.getLogger(__name__)


class VideoProvider(Protocol):
    """Common interface for video generation providers."""

    def generate(self, prompt: str, duration: float, width: int, height: int) -> Path:
        """Generate a video clip from a text prompt."""
        ...


class RunwayProvider:
    """Runway Gen-4 video generation. (Phase 3)"""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate(
        self, prompt: str, duration: float = 5.0, width: int = 1920, height: int = 1080
    ) -> Path:
        raise NotImplementedError("Runway integration coming in Phase 3")
