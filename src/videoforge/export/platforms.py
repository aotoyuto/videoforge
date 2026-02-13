"""Platform-specific export presets for video encoding."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PlatformPreset:
    """Video encoding preset for a specific platform."""

    name: str
    resolution: tuple[int, int]
    fps: int
    codec: str
    bitrate: str
    audio_bitrate: str
    max_duration: int | None  # seconds, None = unlimited
    aspect_ratio: str


# Platform presets
PRESETS: dict[str, PlatformPreset] = {
    "youtube": PlatformPreset(
        name="YouTube",
        resolution=(1920, 1080),
        fps=30,
        codec="libx264",
        bitrate="8M",
        audio_bitrate="192k",
        max_duration=None,
        aspect_ratio="16:9",
    ),
    "youtube_short": PlatformPreset(
        name="YouTube Shorts",
        resolution=(1080, 1920),
        fps=30,
        codec="libx264",
        bitrate="6M",
        audio_bitrate="192k",
        max_duration=60,
        aspect_ratio="9:16",
    ),
    "tiktok": PlatformPreset(
        name="TikTok",
        resolution=(1080, 1920),
        fps=30,
        codec="libx264",
        bitrate="6M",
        audio_bitrate="128k",
        max_duration=180,
        aspect_ratio="9:16",
    ),
    "instagram_reel": PlatformPreset(
        name="Instagram Reels",
        resolution=(1080, 1920),
        fps=30,
        codec="libx264",
        bitrate="6M",
        audio_bitrate="128k",
        max_duration=90,
        aspect_ratio="9:16",
    ),
    "instagram_post": PlatformPreset(
        name="Instagram Post",
        resolution=(1080, 1080),
        fps=30,
        codec="libx264",
        bitrate="5M",
        audio_bitrate="128k",
        max_duration=60,
        aspect_ratio="1:1",
    ),
    "twitter": PlatformPreset(
        name="Twitter/X",
        resolution=(1920, 1080),
        fps=30,
        codec="libx264",
        bitrate="5M",
        audio_bitrate="128k",
        max_duration=140,
        aspect_ratio="16:9",
    ),
}


def get_preset(platform: str) -> PlatformPreset | None:
    """Get a platform preset by name."""
    return PRESETS.get(platform.lower())


def get_ffmpeg_args(preset: PlatformPreset) -> list[str]:
    """Generate FFmpeg encoding arguments from a platform preset."""
    w, h = preset.resolution
    return [
        "-c:v", preset.codec,
        "-b:v", preset.bitrate,
        "-r", str(preset.fps),
        "-vf", f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2",
        "-c:a", "aac",
        "-b:a", preset.audio_bitrate,
        "-movflags", "+faststart",
        "-pix_fmt", "yuv420p",
    ]
