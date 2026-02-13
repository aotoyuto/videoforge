"""Configuration management for VideoForge."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv


@dataclass
class Config:
    """Application configuration loaded from environment variables."""

    # TTS
    voicevox_url: str = "http://localhost:50021"
    elevenlabs_api_key: str = ""
    google_credentials: str = ""

    # Image generation
    stability_api_key: str = ""
    openai_api_key: str = ""

    # Video generation
    runway_api_key: str = ""

    # Music
    suno_api_key: str = ""

    # General
    output_dir: Path = field(default_factory=lambda: Path("./output"))
    default_font: str = "Yu Gothic"
    default_font_path: str = ""

    @classmethod
    def load(cls, env_file: str | Path | None = None) -> Config:
        """Load configuration from .env file and environment variables."""
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()

        return cls(
            voicevox_url=os.getenv("VOICEVOX_URL", "http://localhost:50021"),
            elevenlabs_api_key=os.getenv("ELEVENLABS_API_KEY", ""),
            google_credentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS", ""),
            stability_api_key=os.getenv("STABILITY_API_KEY", ""),
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            runway_api_key=os.getenv("RUNWAY_API_KEY", ""),
            suno_api_key=os.getenv("SUNO_API_KEY", ""),
            output_dir=Path(os.getenv("OUTPUT_DIR", "./output")),
            default_font=os.getenv("DEFAULT_FONT", "Yu Gothic"),
            default_font_path=os.getenv("DEFAULT_FONT_PATH", ""),
        )

    def has_voicevox(self) -> bool:
        return bool(self.voicevox_url)

    def has_stability(self) -> bool:
        return bool(self.stability_api_key)

    def has_openai(self) -> bool:
        return bool(self.openai_api_key)

    def has_elevenlabs(self) -> bool:
        return bool(self.elevenlabs_api_key)
