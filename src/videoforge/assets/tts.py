"""Text-to-Speech providers for narration generation."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Protocol

import httpx

from ..config import Config

logger = logging.getLogger(__name__)


class TTSProvider(Protocol):
    """Common interface for TTS providers."""

    def synthesize(self, text: str, speaker_id: int = 1, speed: float = 1.0) -> bytes:
        """Synthesize speech from text. Returns WAV audio bytes."""
        ...


class VoicevoxTTS:
    """VOICEVOX local TTS provider.

    Requires VOICEVOX engine running at the configured URL (default: http://localhost:50021).
    """

    def __init__(self, base_url: str = "http://localhost:50021"):
        self.base_url = base_url.rstrip("/")

    def is_available(self) -> bool:
        """Check if VOICEVOX engine is running."""
        try:
            resp = httpx.get(f"{self.base_url}/version", timeout=3)
            return resp.status_code == 200
        except (httpx.ConnectError, httpx.TimeoutException):
            return False

    def get_speakers(self) -> list[dict]:
        """Get available speakers/characters."""
        resp = httpx.get(f"{self.base_url}/speakers", timeout=10)
        resp.raise_for_status()
        return resp.json()

    def synthesize(self, text: str, speaker_id: int = 1, speed: float = 1.0) -> bytes:
        """Synthesize speech using VOICEVOX.

        Args:
            text: Japanese text to synthesize.
            speaker_id: VOICEVOX speaker/character ID.
            speed: Speech speed multiplier.

        Returns:
            WAV audio data as bytes.
        """
        # Step 1: Create audio query
        query_resp = httpx.post(
            f"{self.base_url}/audio_query",
            params={"text": text, "speaker": speaker_id},
            timeout=30,
        )
        query_resp.raise_for_status()
        query = query_resp.json()

        # Adjust speed
        if speed != 1.0:
            query["speedScale"] = speed

        # Step 2: Synthesize audio
        synth_resp = httpx.post(
            f"{self.base_url}/synthesis",
            params={"speaker": speaker_id},
            json=query,
            timeout=60,
        )
        synth_resp.raise_for_status()
        return synth_resp.content

    def synthesize_to_file(
        self,
        text: str,
        output_path: Path,
        speaker_id: int = 1,
        speed: float = 1.0,
    ) -> Path:
        """Synthesize speech and save to a WAV file."""
        audio_data = self.synthesize(text, speaker_id, speed)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(audio_data)
        logger.info("TTS audio saved: %s (%d bytes)", output_path, len(audio_data))
        return output_path


def create_tts_provider(provider_name: str, config: Config) -> TTSProvider | None:
    """Factory function to create a TTS provider instance."""
    if provider_name == "voicevox":
        tts = VoicevoxTTS(config.voicevox_url)
        if tts.is_available():
            return tts
        logger.warning("VOICEVOX not available at %s", config.voicevox_url)
        return None

    logger.warning("TTS provider '%s' not yet implemented.", provider_name)
    return None
