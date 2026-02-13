"""AI music generation providers. (Phase 2 - placeholder)"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Protocol

logger = logging.getLogger(__name__)


class MusicProvider(Protocol):
    """Common interface for music generation providers."""

    def generate(self, prompt: str, duration: float) -> Path:
        """Generate music from a text prompt. Returns path to audio file."""
        ...


class MusicGenProvider:
    """Meta MusicGen local music generation. (Phase 2)"""

    def generate(self, prompt: str, duration: float = 30.0) -> Path:
        raise NotImplementedError("MusicGen integration coming in Phase 2")
