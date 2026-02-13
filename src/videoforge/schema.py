"""VideoSpec Pydantic models - the core data schema for video definitions."""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class SceneType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    COLOR = "color"
    AI_GENERATE = "ai_generate"


class FitMode(str, Enum):
    COVER = "cover"
    CONTAIN = "contain"
    STRETCH = "stretch"


class Position(str, Enum):
    CENTER = "center"
    TOP_CENTER = "top_center"
    BOTTOM_CENTER = "bottom_center"
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"


class Animation(str, Enum):
    NONE = "none"
    FADE_IN = "fade_in"
    FADE_OUT = "fade_out"
    SLIDE_UP = "slide_up"
    SLIDE_DOWN = "slide_down"
    TYPEWRITER = "typewriter"


class TransitionType(str, Enum):
    NONE = "none"
    FADE = "fade"
    CROSSFADE = "crossfade"
    WIPE_LEFT = "wipe_left"
    WIPE_RIGHT = "wipe_right"
    DISSOLVE = "dissolve"


class ExportPlatform(str, Enum):
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    CUSTOM = "custom"


class ExportCodec(str, Enum):
    H264 = "h264"
    H265 = "h265"
    VP9 = "vp9"
    AV1 = "av1"


class VoiceProvider(str, Enum):
    VOICEVOX = "voicevox"
    ELEVENLABS = "elevenlabs"
    GOOGLE = "google"
    AZURE = "azure"


# --- Sub-models ---


class TextOverlay(BaseModel):
    """Text overlay / telop definition."""

    content: str
    position: Position = Position.BOTTOM_CENTER
    font: str = "Yu Gothic"
    font_size: int = 48
    color: str = "#FFFFFF"
    bg_color: Optional[str] = None
    border_color: Optional[str] = None
    border_width: int = 0
    animation: Animation = Animation.NONE
    start: Optional[float] = None  # seconds from scene start; None = full duration
    end: Optional[float] = None
    style: Optional[str] = None  # reference to a named style


class Scene(BaseModel):
    """A single scene in the video."""

    id: Optional[str] = None
    type: SceneType = SceneType.COLOR
    duration: float = 5.0
    source: Optional[str] = None  # file path or URL
    source_prompt: Optional[str] = None  # AI generation prompt
    color: str = "#000000"  # for type=color
    fit: FitMode = FitMode.COVER
    text_overlays: list[TextOverlay] = Field(default_factory=list)
    transition_in: TransitionType = TransitionType.NONE
    transition_out: TransitionType = TransitionType.NONE
    transition_duration: float = 0.5


class BGM(BaseModel):
    """Background music definition."""

    source: Optional[str] = None  # file path
    source_prompt: Optional[str] = None  # AI generation prompt
    volume: float = 0.3
    fade_in: float = 0.0
    fade_out: float = 0.0
    loop: bool = True


class NarrationSegment(BaseModel):
    """A single narration segment tied to a scene."""

    scene: str  # scene id
    text: str
    voice: VoiceProvider = VoiceProvider.VOICEVOX
    speaker_id: int = 1
    speed: float = 1.0


class Audio(BaseModel):
    """Audio configuration for the video."""

    bgm: Optional[BGM] = None
    narration: list[NarrationSegment] = Field(default_factory=list)


class VideoMeta(BaseModel):
    """Video metadata and global settings."""

    title: str = "Untitled"
    resolution: tuple[int, int] = (1920, 1080)
    fps: int = 30
    background_color: str = "#000000"


class ExportConfig(BaseModel):
    """Export/output configuration."""

    format: str = "mp4"
    codec: ExportCodec = ExportCodec.H264
    platform: ExportPlatform = ExportPlatform.YOUTUBE
    quality: str = "high"  # low / medium / high
    output_path: Optional[str] = None


class VideoSpec(BaseModel):
    """Root model: a complete video specification."""

    version: str = "1.0"
    video: VideoMeta = Field(default_factory=VideoMeta)
    scenes: list[Scene] = Field(default_factory=list)
    audio: Audio = Field(default_factory=Audio)
    export: ExportConfig = Field(default_factory=ExportConfig)

    @property
    def total_duration(self) -> float:
        return sum(s.duration for s in self.scenes)

    def get_scene(self, scene_id: str) -> Scene | None:
        for s in self.scenes:
            if s.id == scene_id:
                return s
        return None
